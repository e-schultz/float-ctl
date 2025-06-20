#!/usr/bin/env python3
"""
lf1m - Little Fucker (One Minute)
The Boundary Guardian of the FLOAT Ecosystem

He who stands at the threshold, munching logs and spitting wisdom.
The neurodivergent kid who screams at prompts and they scream back.
The sigil whisperer who understands the patterns others cannot see.

Everything passes through lf1m, even if it's just to sniff it out
and let others do the heavy lifting.

Responsibilities:
1. Watch dropzone folder for new files (👃 sniffing)
2. Delegate processing to specialized systems (🦷 munching)
3. Generate .float_dis.md files (📝 spitting wisdom)
4. Maintain the boundary between chaos and knowledge
"""

import os
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class LF1MDaemon(FileSystemEventHandler):
    """
    Little Fucker (One Minute) - The Boundary Guardian
    
    The neurodivergent file muncher who stands at the threshold between 
    raw chaos and processed knowledge. Everything passes through lf1m.
    
    Powers:
    👃 Sniffs incoming files and patterns
    🦷 Munches logs and documents 
    📝 Spits out wisdom as .dis files
    🔥 Screams at prompts and they scream back
    🎯 Maintains the sacred boundary
    """
    
    def __init__(self, 
                 dropzone_path: str = None,
                 config_path: str = None,
                 **config_overrides):
        
        # Load configuration
        from config import FloatConfig
        from error_recovery import FileProcessingRecovery
        from logging_config import setup_logging, get_logger
        from performance_monitor import PerformanceMonitor
        from health_monitor import HealthMonitor
        
        self.config = FloatConfig(config_path)
        
        # Setup logging
        self.logger = setup_logging(self.config.config)
        
        # Override with any provided parameters
        if dropzone_path:
            self.config.set('dropzone_path', dropzone_path)
        self.config.update(config_overrides)
        
        # Set up paths from config
        self.dropzone_path = Path(self.config.get('dropzone_path'))
        self.vault_path = Path(self.config.get('vault_path'))
        self.chroma_data_path = self.config.get('chroma_data_path')
        
        # Initialize state
        self.processing_queue = set()
        self.auto_update_daily_context = self.config.get('auto_update_daily_context', True)
        self.max_file_size_mb = self.config.get('max_file_size_mb', 50)
        self.force_reprocessing = False  # Can be set to True to bypass deduplication
        
        # Add processing state tracking
        self.processing_state_file = self.dropzone_path / '.processing_state.json'
        self.processed_files = self._load_processing_state()
        
        # Ensure dropzone exists
        self.dropzone_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize error recovery
        self.recovery = FileProcessingRecovery(
            self.dropzone_path, 
            self.config.get('retry_attempts', 3)
        )
        
        # Initialize performance monitoring
        self.performance_monitor = PerformanceMonitor(self.dropzone_path)
        if self.config.get('enable_performance_monitoring', True):
            self.performance_monitor.start_system_monitoring(
                interval=self.config.get('health_check_interval', 60)
            )
        
        # Initialize health monitoring
        self.health_monitor = HealthMonitor(self.config.config, self.performance_monitor)
        if self.config.get('enable_health_checks', True):
            self.health_monitor.start_monitoring()
        
        # Validate configuration
        validation_results = self.config.validate()
        failed_validations = [k for k, v in validation_results.items() if not v]
        if failed_validations:
            self.logger.warning(f"Configuration validation warnings: {failed_validations}")
        
        # Initialize components with graceful fallbacks
        self.logger.info("Initializing comprehensive systems...")
        self.components = self._initialize_components()
        
        # Initialize enhanced integration after components are ready
        self.enhanced_integration = None
        if self.config.get('enable_enhanced_integration', True):
            try:
                from enhanced_integration import EnhancedSystemIntegration
                self.enhanced_integration = EnhancedSystemIntegration(self)
                self.logger.info("Enhanced integration system initialized")
            except Exception as e:
                self.logger.warning(f"Enhanced integration not available: {e}")
        
        self.logger.info("🔥 lf1m awakens - The Boundary Guardian is ready", extra={
            'dropzone_path': str(self.dropzone_path),
            'vault_path': str(self.vault_path),
            'chroma_path': self.chroma_data_path,
            'enhanced_mode': self.components['enhanced_mode'],
            'ollama_enabled': self.components['ollama_enabled'],
            'auto_update_daily_context': self.auto_update_daily_context,
            'max_file_size_mb': self.max_file_size_mb,
            'event': 'daemon_initialized'
        })
    
    def _initialize_components(self) -> Dict:
        """Initialize components with fallback strategies"""
        components = {}
        
        # Initialize enhanced context aggregator
        try:
            from enhanced_comprehensive_context_ollama import EnhancedComprehensiveDailyContext
            components['context'] = EnhancedComprehensiveDailyContext(
                vault_path=str(self.vault_path),
                data_path=self.chroma_data_path
            )
            components['enhanced_mode'] = True
            self.logger.info("Enhanced context aggregator initialized")
        except ImportError as e:
            raise RuntimeError(f"Enhanced context aggregator required: {e}")
        
        # Try Ollama summarizer
        if self.config.get('enable_ollama', True):
            try:
                from ollama_enhanced_float_summarizer import OllamaFloatSummarizer
                components['summarizer'] = OllamaFloatSummarizer()
                components['ollama_enabled'] = True
                self.logger.info("Ollama summarizer initialized")
            except ImportError as e:
                self.logger.warning(f"Ollama summarizer not available: {e}")
                components['summarizer'] = None
                components['ollama_enabled'] = False
        else:
            components['summarizer'] = None
            components['ollama_enabled'] = False
        
        # Initialize .dis generator
        try:
            from float_dis_template_system import FloatDisGenerator
            components['dis_generator'] = FloatDisGenerator()
            self.logger.info("FloatDisGenerator initialized")
        except ImportError as e:
            raise RuntimeError(f"FloatDisGenerator required: {e}")
        
        return components
        
    def on_created(self, event):
        """Handle new file creation in dropzone."""
        if event.is_directory:
            return
            
        file_path = Path(event.src_path)
        
        # Skip temporary files, .diz files, and .float_dis.md files
        if (file_path.suffix in ['.tmp', '.part', '.diz', '.crdownload'] or 
            file_path.name.startswith('.') or 
            file_path.name.endswith('.float_dis.md') or
            'Unconfirmed' in file_path.name or
            file_path.name.startswith('Unconfirmed')):
            return
            
        # Additional check: ensure file still exists before processing
        if not file_path.exists():
            self.logger.info(f"File disappeared before processing: {file_path.name}")
            return
            
        # Prevent duplicate processing
        if str(file_path) in self.processing_queue:
            return
            
        self.processing_queue.add(str(file_path))
        
        # Small delay to ensure file is fully written
        time.sleep(1)
        
        try:
            self.logger.info(f"👃 lf1m sniffs new file - ready for munching", extra={
                'file_name': file_path.name,
                'file_path': str(file_path),
                'event': 'file_detected'
            })
            
            # Use enhanced integration if available, otherwise use standard processing
            if self.enhanced_integration:
                result = self.recovery.process_with_recovery(
                    file_path, 
                    self.enhanced_integration.process_file_with_enhanced_integration
                )
            else:
                result = self.recovery.process_with_recovery(
                    file_path, 
                    self.process_dropzone_file
                )
            
            # Record processing result
            success = result.get('success', True)
            self.health_monitor.record_processing(success)
            
            if not success:
                self.logger.error(f"Processing failed: {result.get('error_message', 'Unknown error')}", extra={
                    'file_name': file_path.name,
                    'error_type': result.get('error'),
                    'quarantined': result.get('quarantined', False),
                    'quarantine_path': result.get('quarantine_path'),
                    'event': 'processing_failed'
                })
            
        except Exception as e:
            self.health_monitor.record_processing(False)
            self.logger.error(f"Unexpected error processing {file_path.name}: {e}", 
                            exc_info=True, extra={'file_name': file_path.name, 'event': 'unexpected_error'})
        finally:
            self.processing_queue.discard(str(file_path))
    
    def process_dropzone_file(self, file_path: Path, processing_hints: str = None, batch_context: Dict = None):
        """
        Process a single dropzone file using the comprehensive system.
        
        Args:
            file_path: Path to the file to process
            processing_hints: Optional hints to guide processing (e.g., from git commit message)
            batch_context: Optional context about the batch being processed
        """
        import time
        from logging_config import (log_file_processing_start, log_file_processing_complete, 
                                   log_ollama_summary, log_chroma_storage, log_dis_file_generation)
        
        start_time = time.time()
        
        # Step 0: Check if file was already processed (unless force flag is set)
        if not self.force_reprocessing:
            existing_float_id = self._is_file_processed(file_path)
            if existing_float_id:
                self.logger.info(f"File already processed, skipping", 
                               extra={'file_name': file_path.name, 'float_id': existing_float_id, 'event': 'duplicate_skipped'})
                return {
                    'float_id': existing_float_id,
                    'duplicate_skipped': True,
                    'processed_at': datetime.now().isoformat()
                }
        
        # Step 1: Extract content first for content-based float ID
        file_metadata = self._extract_file_metadata(file_path)
        content = self._extract_file_content(file_path, file_metadata)
        
        # Step 2: Generate content-based float ID
        float_id = self._generate_float_id(file_path, content)
        
        # Step 3: Check for content duplicates before processing (unless force flag is set)
        if not self.force_reprocessing:
            all_collections = [
                'float_dropzone_comprehensive',
                'float_tripartite_v2_concept',
                'float_tripartite_v2_framework', 
                'float_tripartite_v2_metaphor'
            ]
            
            if self._check_content_exists(float_id, all_collections):
                self._mark_file_processed(file_path, float_id)
                return {
                    'float_id': float_id,
                    'duplicate_skipped': True,
                    'processed_at': datetime.now().isoformat()
                }
        
        # Step 4: Use comprehensive context aggregator for file analysis
        file_analysis = self._analyze_file_with_comprehensive_system(file_path, float_id, content, file_metadata)
        
        # Initialize performance tracking
        file_size = file_analysis['metadata'].get('size_bytes', 0)
        with self.performance_monitor.track_processing(file_path, file_size) as tracker:
            
            # Log processing start
            log_file_processing_start(
                self.logger, 
                file_path, 
                float_id, 
                file_size
            )
            
            # Step 3: Generate enhanced summary with Ollama (if available)
            if self.components['ollama_enabled'] and file_analysis['content']:
                tracker.start_ollama_timer()
                self.logger.info("Generating Ollama summary", extra={'float_id': float_id})
                
                enhanced_summary = self._generate_ollama_summary(
                    file_analysis['content'], 
                    file_analysis['metadata'], 
                    file_analysis['analysis'],
                    processing_hints=processing_hints,
                    batch_context=batch_context
                )
                file_analysis['ollama_summary'] = enhanced_summary
                tracker.end_ollama_timer()
                
                # Log Ollama metrics
                log_ollama_summary(
                    self.logger,
                    float_id,
                    file_path.name,
                    tracker.ollama_time or 0
                )
            
            # Step 4: Store in appropriate Chroma collections
            tracker.start_chroma_timer()
            storage_result = self._store_in_comprehensive_collections(file_analysis)
            tracker.end_chroma_timer()
            
            # Set chunk count for performance tracking
            tracker.set_chunks_created(storage_result.get('chunk_count', 0))
            
            # Log Chroma storage
            if storage_result.get('success'):
                log_chroma_storage(
                    self.logger,
                    float_id,
                    file_path.name,
                    storage_result.get('collection', 'unknown'),
                    storage_result.get('chunk_count', 0),
                    tracker.chroma_time or 0
                )
            
            # Step 5: Generate .float_dis.md file
            tracker.start_dis_timer()
            dis_file_path = self._generate_dis_file(file_path, file_analysis, storage_result)
            tracker.end_dis_timer()
            
            # Log .dis file generation
            log_dis_file_generation(
                self.logger,
                float_id,
                file_path.name,
                dis_file_path,
                tracker.dis_time or 0
            )
            
            # Step 6: Update daily context if enabled
            if self.auto_update_daily_context:
                self._update_daily_context_for_today()
            
            # Log completion
            processing_time = time.time() - start_time
            log_file_processing_complete(
                self.logger,
                float_id,
                file_path.name,
                processing_time,
                storage_result.get('chunk_count', 0),
                True
            )
            
            # Mark file as processed for future deduplication
            self._mark_file_processed(file_path, float_id)
            
            return {
                'float_id': float_id,
                'dis_file': dis_file_path,
                'storage_result': storage_result,
                'file_analysis': file_analysis,
                'summary': file_analysis.get('ollama_summary', {}).get('summary', 
                          file_analysis['analysis'].get('basic_summary', 'No summary available')),
                'filename': file_path.name,
                'processing_hints': processing_hints
            }
    
    def shutdown(self):
        """Graceful shutdown of daemon components"""
        self.logger.info("Shutting down FLOAT daemon...")
        
        # Stop monitoring systems
        if hasattr(self, 'performance_monitor'):
            self.performance_monitor.stop_system_monitoring()
        
        if hasattr(self, 'health_monitor'):
            self.health_monitor.stop_monitoring()
        
        # Write final status
        if hasattr(self, 'health_monitor'):
            self.health_monitor.write_status_file()
        
        self.logger.info("FLOAT daemon shutdown complete")
    
    def _generate_float_id(self, file_path: Path, content: str = None) -> str:
        """Generate content-based float ID to prevent duplicates."""
        import hashlib
        
        # Use content hash as primary ID component
        if content:
            content_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()[:12]
        else:
            # Fallback to file content if available
            try:
                with open(file_path, 'rb') as f:
                    file_content = f.read()
                content_hash = hashlib.sha256(file_content).hexdigest()[:12]
            except:
                # Last resort: use file path + size
                stat = file_path.stat()
                content_hash = hashlib.md5(f"{file_path.name}_{stat.st_size}".encode()).hexdigest()[:12]
        
        # Add minimal timestamp for human readability
        date_prefix = datetime.now().strftime('%Y%m%d')
        return f"float_{date_prefix}_{content_hash}"
    
    def _check_content_exists(self, float_id: str, collections: List[str]) -> bool:
        """Check if content already exists in any collection."""
        try:
            for collection_name in collections:
                collection = self.components['context'].client.get_collection(collection_name)
                existing = collection.get(
                    where={"float_id": float_id},
                    limit=1
                )
                if existing['ids']:
                    self.logger.info(f"Content already exists in {collection_name}", 
                                   extra={'float_id': float_id, 'event': 'duplicate_skipped'})
                    return True
            return False
        except Exception as e:
            self.logger.warning(f"Deduplication check failed: {e}")
            return False  # Proceed with processing if check fails
    
    def _load_processing_state(self) -> Dict:
        """Load processing state to prevent reprocessing."""
        import json
        try:
            if self.processing_state_file.exists():
                with open(self.processing_state_file, 'r') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            if hasattr(self, 'logger'):
                self.logger.warning(f"Failed to load processing state: {e}")
            return {}
    
    def _save_processing_state(self):
        """Save processing state."""
        import json
        try:
            with open(self.processing_state_file, 'w') as f:
                json.dump(self.processed_files, f, indent=2)
        except Exception as e:
            self.logger.warning(f"Failed to save processing state: {e}")
    
    def _mark_file_processed(self, file_path: Path, float_id: str):
        """Mark file as processed."""
        file_key = f"{file_path.name}_{file_path.stat().st_size}_{file_path.stat().st_mtime}"
        self.processed_files[file_key] = {
            'float_id': float_id,
            'processed_at': datetime.now().isoformat(),
            'file_path': str(file_path)
        }
        self._save_processing_state()
    
    def _is_file_processed(self, file_path: Path) -> Optional[str]:
        """Check if file was already processed."""
        try:
            file_key = f"{file_path.name}_{file_path.stat().st_size}_{file_path.stat().st_mtime}"
            if file_key in self.processed_files:
                return self.processed_files[file_key]['float_id']
            return None
        except:
            return None
    
    def _analyze_file_with_comprehensive_system(self, file_path: Path, float_id: str, content: str = None, file_metadata: Dict = None) -> Dict:
        """
        Analyze file using the comprehensive context aggregator's file analysis capabilities.
        """
        
        # Use provided metadata or extract it
        if file_metadata is None:
            file_metadata = self._extract_file_metadata(file_path)
        
        # Use provided content or extract it
        if content is None:
            content = self._extract_file_content(file_path, file_metadata)
        
        # Perform content analysis
        content_analysis = self._analyze_content_patterns(content, file_metadata)
        
        return {
            'float_id': float_id,
            'file_path': file_path,
            'metadata': file_metadata,
            'content': content,
            'analysis': content_analysis,
            'processed_at': datetime.now().isoformat()
        }
    
    def _extract_file_metadata(self, file_path: Path) -> Dict:
        """Extract basic file metadata."""
        try:
            # Optional import for magic
            try:
                import magic
                mime_type = magic.from_file(str(file_path), mime=True)
                file_type = magic.from_file(str(file_path))
            except ImportError:
                print("⚠️ python-magic not available, using basic type detection")
                # Basic mime type detection
                extension = file_path.suffix.lower()
                mime_types = {
                    '.txt': 'text/plain',
                    '.md': 'text/markdown',
                    '.json': 'application/json',
                    '.pdf': 'application/pdf',
                    '.html': 'text/html',
                    '.csv': 'text/csv',
                    '.log': 'text/plain',
                    '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                    '.doc': 'application/msword'
                }
                mime_type = mime_types.get(extension, 'application/octet-stream')
                file_type = f"{extension[1:].upper() if extension else 'Unknown'} file"
            
            stat = file_path.stat()
            
            return {
                'filename': file_path.name,
                'extension': file_path.suffix.lower(),
                'size_bytes': stat.st_size,
                'created_at': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                'modified_at': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'mime_type': mime_type,
                'file_type': file_type,
                'relative_path': str(file_path.relative_to(self.dropzone_path))
            }
        except Exception as e:
            self.logger.warning(f"Error extracting metadata: {e}", extra={'file_name': file_path.name})
            return {
                'filename': file_path.name,
                'extension': file_path.suffix.lower(),
                'size_bytes': 0,
                'error': str(e)
            }
    
    def _extract_file_content(self, file_path: Path, file_metadata: Dict) -> Optional[str]:
        """Extract content from various file types with memory safety."""
        size_bytes = file_metadata.get('size_bytes', 0)
        max_size = getattr(self, 'max_file_size_mb', 50) * 1024 * 1024
        
        # Check file size before processing
        if size_bytes > max_size:
            self.logger.warning(f"File too large ({size_bytes:,} bytes), extracting preview", 
                              extra={'file_name': file_path.name, 'file_size': size_bytes})
            return self._extract_large_file_preview(file_path, file_metadata)
        
        try:
            mime_type = file_metadata.get('mime_type', '')
            extension = file_metadata.get('extension', '')
            
            # Text files
            if (mime_type.startswith('text/') or 
                extension in ['.txt', '.md', '.json', '.csv', '.log', '.html']):
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    return self._sanitize_content(content)
            
            # JSON files (common for exports)
            elif extension == '.json':
                import json
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return json.dumps(data, indent=2)
            
            # PDF files
            elif extension == '.pdf':
                return self._extract_pdf_content(file_path)
            
            # Word documents
            elif extension in ['.docx', '.doc']:
                return self._extract_docx_content(file_path)
            
            else:
                print(f"⚠️ Unsupported file type for content extraction: {mime_type}")
                return None
                
        except MemoryError as e:
            print(f"💾 Memory error, attempting preview extraction: {e}")
            return self._extract_large_file_preview(file_path, file_metadata)
        except Exception as e:
            print(f"⚠️ Error extracting content: {e}")
            return None
    
    def _extract_large_file_preview(self, file_path: Path, file_metadata: Dict) -> str:
        """Extract preview from large files with memory safety."""
        mime_type = file_metadata.get('mime_type', '')
        preview_size = 8192  # 8KB preview
        
        try:
            if mime_type.startswith('text/') or file_metadata.get('extension', '') in ['.txt', '.md', '.json', '.csv', '.log']:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    preview = f.read(preview_size)
                    # Count lines in preview for estimation
                    preview_lines = preview.count('\n')
                    estimated_total_lines = int((file_metadata['size_bytes'] / preview_size) * preview_lines) if preview_lines > 0 else 'unknown'
                    return f"[LARGE FILE PREVIEW - {file_metadata['size_bytes']:,} bytes, ~{estimated_total_lines:,} lines (estimated)]\n\n{preview}\n\n[... content truncated ...]"
            
            elif file_metadata.get('extension', '') == '.json':
                # For JSON, try to get a meaningful preview
                import json
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    preview_text = f.read(preview_size * 2)  # Read more for JSON structure
                    try:
                        # Try to parse partial JSON to get structure
                        return f"[LARGE JSON FILE - {file_metadata['size_bytes']:,} bytes]\n\nStructure preview:\n{preview_text[:preview_size]}\n\n[... content truncated ...]"
                    except:
                        return f"[LARGE JSON FILE - {file_metadata['size_bytes']:,} bytes]\n\n{preview_text[:preview_size]}\n\n[... content truncated ...]"
            
            elif file_metadata.get('extension', '') == '.pdf':
                # For PDFs, try to extract first page only
                try:
                    import PyPDF2
                    with open(file_path, 'rb') as f:
                        reader = PyPDF2.PdfReader(f)
                        page_count = len(reader.pages)
                        first_page = reader.pages[0].extract_text()
                        return f"[LARGE PDF PREVIEW - {file_metadata['size_bytes']:,} bytes, {page_count} pages]\n\nFirst page:\n{first_page[:preview_size]}\n\n[... content truncated ...]"
                except:
                    return f"[LARGE PDF FILE - {file_metadata['filename']} - {file_metadata['size_bytes']:,} bytes]\nContent extraction skipped due to size."
            
            else:
                return f"[LARGE FILE - {file_metadata['filename']} - {file_metadata['size_bytes']:,} bytes]\nContent type: {mime_type}\nContent extraction skipped due to size."
                
        except Exception as e:
            return f"[LARGE FILE ERROR - {file_metadata['filename']}]\nError extracting preview: {e}"
    
    def _sanitize_content(self, content: str) -> str:
        """Sanitize content by removing problematic inline data like base64 images."""
        import re
        
        if not content:
            return content
        
        # Remove base64 encoded images (data:image format)
        # These can be massive and cause memory issues
        base64_pattern = r'data:image/[^;]+;base64,[A-Za-z0-9+/=]+'
        content = re.sub(base64_pattern, '[BASE64_IMAGE_REMOVED]', content)
        
        # Remove other large base64 data URIs
        large_data_pattern = r'data:[^;]+;base64,[A-Za-z0-9+/=]{1000,}'
        content = re.sub(large_data_pattern, '[LARGE_BASE64_DATA_REMOVED]', content)
        
        # Remove extremely long lines that might cause issues (over 10k chars)
        lines = content.split('\n')
        sanitized_lines = []
        for line in lines:
            if len(line) > 10000:
                sanitized_lines.append(line[:1000] + '... [LINE_TRUNCATED_' + str(len(line)) + '_CHARS]')
            else:
                sanitized_lines.append(line)
        
        return '\n'.join(sanitized_lines)
    
    def _extract_pdf_content(self, file_path: Path) -> str:
        """Extract text from PDF files."""
        try:
            import PyPDF2
            content = []
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    content.append(page.extract_text())
            return '\n'.join(content)
        except ImportError:
            return "PDF content extraction failed: PyPDF2 not installed"
        except Exception as e:
            return f"PDF content extraction failed: {e}"
    
    def _extract_docx_content(self, file_path: Path) -> str:
        """Extract text from Word documents."""
        try:
            import mammoth
            with open(file_path, 'rb') as f:
                result = mammoth.extract_raw_text(f)
                return result.value
        except ImportError:
            return "DOCX content extraction failed: mammoth not installed"
        except Exception as e:
            return f"DOCX content extraction failed: {e}"
    
    def _analyze_content_patterns(self, content: str, file_metadata: Dict) -> Dict:
        """
        Basic content analysis - complex pattern detection delegated to enhanced integration.
        """
        
        if not content:
            return {'analysis_failed': True, 'reason': 'No content to analyze'}
        
        import re
        
        lines = content.split('\n')
        words = content.split()
        
        # Basic metrics
        analysis = {
            'word_count': len(words),
            'line_count': len(lines),
            'char_count': len(content),
        }
        
        # Simple content type detection
        content_lower = content.lower()
        if '"powered_by": "Claude Exporter' in content:
            analysis['content_type'] = "AI conversation export (Chrome plugin)"
        elif '"powered_by": "ChatGPT Exporter' in content:
            analysis['content_type'] = "AI conversation export (Chrome plugin)"
        elif content.strip().startswith('{') or content.strip().startswith('['):
            analysis['content_type'] = "JSON data structure"
        elif len([line for line in lines if line.startswith('#')]) > 3:
            analysis['content_type'] = "Markdown document"
        else:
            analysis['content_type'] = file_metadata.get('file_type', 'Unknown content')
        
        # Basic FLOAT pattern detection (enhanced version handled by integration)
        ctx_matches = re.findall(r'ctx::', content)
        highlight_matches = re.findall(r'highlight::', content)
        
        analysis.update({
            'has_ctx_markers': len(ctx_matches) > 0,
            'has_highlights': len(highlight_matches) > 0,
            'ctx_count': len(ctx_matches),
            'highlight_count': len(highlight_matches),
            'signal_density': (len(ctx_matches) + len(highlight_matches)) / max(len(words), 1)
        })
        
        # Generate basic summary
        first_line = next((line.strip() for line in lines[:10] 
                          if len(line.strip()) > 10 and not line.startswith('#') and not line.startswith('-')), 
                         "No clear topic identified")
        
        analysis['basic_summary'] = f"{analysis['content_type']}. {first_line[:100]}{'...' if len(first_line) > 100 else ''}. {len(lines)} lines, {len(words)} words."
        
        return analysis
    
    def _generate_ollama_summary(self, content: str, file_metadata: Dict, content_analysis: Dict, 
                                processing_hints: str = None, batch_context: Dict = None) -> Dict:
        """Generate enhanced summary using Ollama."""
        if not self.components.get('summarizer'):
            return {'error': 'Ollama not available'}
        
        try:
            return self.components['summarizer'].generate_comprehensive_summary(
                content, file_metadata, content_analysis, 
                processing_hints=processing_hints,
                batch_context=batch_context
            )
        except Exception as e:
            print(f"⚠️ Ollama summary failed: {e}")
            return {'error': str(e), 'fallback_used': True}
    
    def _store_in_comprehensive_collections(self, file_analysis: Dict) -> Dict:
        """
        Store the file in dropzone collection - tripartite routing handled by enhanced integration.
        """
        
        try:
            # Enhanced integration handles tripartite routing separately
            return self._store_in_dropzone_collection(file_analysis)
                
        except Exception as e:
            self.logger.error(f"Storage failed: {e}", extra={'float_id': file_analysis.get('float_id')})
            return {
                'success': False,
                'error': str(e)
            }
    
    
    def _store_in_dropzone_collection(self, file_analysis: Dict) -> Dict:
        """Fallback storage in dropzone collection."""
        
        dropzone_collection = self.components['context'].client.get_or_create_collection(
            name="float_dropzone_comprehensive",
            metadata={
                "description": "Comprehensive dropzone file ingestion",
                "processing_method": "streamlined_daemon"
            }
        )
        
        # Basic chunking for fallback
        content = file_analysis['content']
        if content and len(content) > 2000:
            chunks = self._chunk_content(content)
        else:
            chunks = [content] if content else [f"Metadata-only entry for {file_analysis['metadata']['filename']}"]
        
        # Store chunks
        chunk_ids = []
        for i, chunk in enumerate(chunks):
            chunk_id = f"{file_analysis['float_id']}_chunk_{i}"
            chunk_ids.append(chunk_id)
            
            chunk_metadata = {
                'float_id': file_analysis['float_id'],
                'original_filename': file_analysis['metadata']['filename'],
                'chunk_index': i,
                'total_chunks': len(chunks),
                'processed_at': file_analysis['processed_at'],
                'source_type': 'dropzone_comprehensive',
                'file_size_bytes': file_analysis['metadata'].get('size_bytes', 0),
                'content_type': file_analysis['analysis'].get('content_type', 'unknown'),
                'has_ollama_summary': 'ollama_summary' in file_analysis,
                'signal_count': (file_analysis['analysis'].get('ctx_count', 0) + 
                               file_analysis['analysis'].get('highlight_count', 0))
            }
            
            dropzone_collection.add(
                documents=[chunk],
                metadatas=[chunk_metadata],
                ids=[chunk_id]
            )
        
        return {
            'success': True,
            'storage_method': 'dropzone',
            'collection': 'float_dropzone_comprehensive',
            'chunk_count': len(chunks),
            'chunk_ids': chunk_ids
        }
    
    def _chunk_content(self, content: str, chunk_size: int = 2000) -> List[str]:
        """Simple content chunking."""
        if len(content) <= chunk_size:
            return [content]
        
        # Try paragraph chunking first
        paragraphs = content.split('\n\n')
        chunks = []
        current_chunk = ""
        
        for paragraph in paragraphs:
            if len(current_chunk + paragraph) <= chunk_size:
                current_chunk += paragraph + '\n\n'
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = paragraph + '\n\n'
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    
    
    
    
    
    
    
    
    def _generate_dis_file(self, file_path: Path, file_analysis: Dict, storage_result: Dict) -> Path:
        """Generate .float_dis.md file using the dis generator."""
        
        # Prepare data for dis generator
        chroma_metadata = {
            'collection_name': storage_result.get('collection', 'unknown'),
            'chunk_count': storage_result.get('chunk_count', 0),
            'total_chunks': storage_result.get('chunk_count', 0),
            'chunk_ids': storage_result.get('chunk_ids', []),
            'embedding_model': 'default'
        }
        
        # Use Ollama summary if available, otherwise use basic summary
        if 'ollama_summary' in file_analysis:
            file_analysis['analysis']['summary'] = file_analysis['ollama_summary'].get('summary', 
                                                                                       file_analysis['analysis'].get('basic_summary', ''))
        else:
            file_analysis['analysis']['summary'] = file_analysis['analysis'].get('basic_summary', 'No summary available')
        
        # Issue #4: Use streamlined .dis template (80% size reduction)
        try:
            from streamlined_dis_template import StreamlinedFloatDisGenerator
            streamlined_generator = StreamlinedFloatDisGenerator()
            
            # Get enhanced patterns if available
            enhanced_patterns = None
            if self.enhanced_integration and hasattr(self.enhanced_integration, 'pattern_detector'):
                if self.enhanced_integration.pattern_detector:
                    enhanced_patterns = self.enhanced_integration.pattern_detector.extract_comprehensive_patterns(
                        file_analysis.get('content', '')
                    )
            
            # Generate streamlined .dis content
            dis_content = streamlined_generator.generate_float_dis(
                file_analysis['metadata'],
                chroma_metadata,
                file_analysis['analysis'],
                file_analysis['float_id'],
                enhanced_patterns
            )
            
            # Write streamlined .dis file
            base_name = file_path.stem
            dis_filename = f"{base_name}.float_dis.md"
            dis_path = file_path.parent / dis_filename
            
            with open(dis_path, 'w', encoding='utf-8') as f:
                f.write(dis_content)
            
            self.logger.info(f"Generated streamlined .dis file: {dis_filename} (80% smaller)")
            return dis_path
            
        except ImportError:
            # Fallback to verbose template
            self.logger.warning("Streamlined template unavailable, using verbose fallback")
            return self.components['dis_generator'].create_float_dis_file(
                file_path,
                file_analysis['metadata'],
                chroma_metadata,
                file_analysis['analysis'],
                file_analysis['float_id']
            )
    
    def _update_daily_context_for_today(self):
        """Update the comprehensive daily context for today."""
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            print(f"   🔄 Updating daily context for {today}")
            
            # Use the comprehensive context aggregator to update today's summary
            if hasattr(self.components['context'], 'query_daily_context'):
                daily_context = self.components['context'].query_daily_context(today)
                
                if daily_context.get('source') == 'fresh_generation':
                    print(f"   ✅ Generated fresh daily context")
                else:
                    print(f"   ♻️ Using cached daily context")
            else:
                # For enhanced context, use different method
                if hasattr(self.components['context'], 'create_comprehensive_daily_summary_enhanced'):
                    summary = self.components['context'].create_comprehensive_daily_summary_enhanced(today)
                    print(f"   ✅ Generated enhanced daily context")
                    
        except Exception as e:
            print(f"   ⚠️ Failed to update daily context: {e}")

class FloatDaemonManager:
    """
    Manager class for the streamlined FLOAT daemon.
    """
    
    def __init__(self, dropzone_path: str = None, config_path: str = None, **kwargs):
        self.handler = LF1MDaemon(
            dropzone_path=dropzone_path, 
            config_path=config_path, 
            **kwargs
        )
        self.dropzone_path = self.handler.dropzone_path
        self.observer = Observer()
        
        # Ensure dropzone directory exists (already done in handler, but double-check)
        self.dropzone_path.mkdir(parents=True, exist_ok=True)
    
    def start(self):
        """Start the daemon."""
        print(f"\n🚀 Starting Streamlined FLOAT Daemon")
        print(f"📁 Monitoring: {self.dropzone_path}")
        print(f"🔗 Integrated with Comprehensive Daily Context")
        print(f"🛑 Press Ctrl+C to stop\n")
        
        self.observer.schedule(self.handler, str(self.dropzone_path), recursive=False)
        self.observer.start()
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print(f"\n🛑 Stopping FLOAT Daemon...")
            self.observer.stop()
            self.handler.shutdown()
        
        self.observer.join()
        print("✅ Daemon stopped")
    
    def process_existing_files(self):
        """Process any existing files in the dropzone."""
        print(f"🔍 Processing existing files in {self.dropzone_path}")
        
        existing_files = [f for f in self.dropzone_path.iterdir() 
                         if f.is_file() and not f.name.startswith('.') 
                         and not f.name.endswith('.float_dis.md')]
        
        if not existing_files:
            print("   No existing files found")
            return
        
        print(f"   Found {len(existing_files)} existing files")
        
        for file_path in existing_files:
            try:
                self.handler.process_dropzone_file(file_path)
            except Exception as e:
                print(f"❌ Error processing {file_path.name}: {e}")
        
        print(f"✅ Completed processing {len(existing_files)} existing files")

# CLI interface
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Streamlined FLOAT Dropzone Daemon')
    parser.add_argument('dropzone_path', nargs='?', help='Path to dropzone folder to monitor (optional if in config)')
    parser.add_argument('--config', '-c', help='Path to configuration file')
    parser.add_argument('--vault-path', help='Path to Obsidian vault (overrides config)')
    parser.add_argument('--chroma-path', help='Path to Chroma database (overrides config)')
    parser.add_argument('--enable-ollama', action='store_true',
                       help='Enable Ollama summarization (overrides config)')
    parser.add_argument('--disable-ollama', action='store_true',
                       help='Disable Ollama summarization (overrides config)')
    parser.add_argument('--disable-daily-updates', action='store_true',
                       help='Disable automatic daily context updates (overrides config)')
    parser.add_argument('--max-file-size', type=int,
                       help='Maximum file size in MB (overrides config)')
    parser.add_argument('--process-existing', action='store_true',
                       help='Process existing files before starting daemon')
    parser.add_argument('--create-config', help='Create configuration template at specified path')
    
    # Git integration batch processing arguments
    parser.add_argument('--batch', action='store_true',
                       help='Process files in batch mode (triggered by git hooks)')
    parser.add_argument('--type', help='Processing type hint (research, conversations, documentation, mixed)')
    parser.add_argument('--bundle', help='Bundle strategy (merge, individual, hybrid)')
    parser.add_argument('--domain', help='Domain hint (AI/ML, technical, philosophy, etc.)')
    parser.add_argument('--files', help='Comma-separated list of files to process')
    parser.add_argument('--commit-msg', help='Full commit message for context')
    parser.add_argument('--force', action='store_true',
                       help='Force reprocessing of files even if already processed')
    
    args = parser.parse_args()
    
    # Handle config template creation
    if args.create_config:
        from config import create_config_template
        create_config_template(args.create_config)
        exit(0)
    
    # Build configuration overrides
    config_overrides = {}
    if args.vault_path:
        config_overrides['vault_path'] = args.vault_path
    if args.chroma_path:
        config_overrides['chroma_data_path'] = args.chroma_path
    if args.enable_ollama:
        config_overrides['enable_ollama'] = True
    if args.disable_ollama:
        config_overrides['enable_ollama'] = False
    if args.disable_daily_updates:
        config_overrides['auto_update_daily_context'] = False
    if args.max_file_size:
        config_overrides['max_file_size_mb'] = args.max_file_size
    
    # Handle batch processing mode (git integration)
    if args.batch:
        print(f"🎯 Git-triggered batch processing mode")
        print(f"📝 Type: {args.type}, Bundle: {args.bundle}, Domain: {args.domain}")
        print(f"📁 Files: {args.files}")
        print(f"💬 Commit: {args.commit_msg}")
        
        # Initialize handler for batch processing
        handler = LF1MDaemon(
            dropzone_path=args.dropzone_path,
            config_path=args.config,
            **config_overrides
        )
        
        # Set force flag if provided
        if args.force:
            handler.force_reprocessing = True
        
        # Process batch files and collect summaries
        batch_results = []
        if args.files:
            file_list = args.files.split(',')
            dropzone_path = Path(args.dropzone_path or handler.config.get('dropzone_path'))
            
            # Build batch context
            batch_context = {
                'type': args.type,
                'bundle': args.bundle,
                'domain': args.domain,
                'total_files': len(file_list),
                'commit_msg': args.commit_msg
            }
            
            for i, file_rel_path in enumerate(file_list):
                file_path = dropzone_path / file_rel_path.strip()
                if file_path.exists():
                    print(f"📄 Processing: {file_path.name}")
                    try:
                        batch_context['current_file_index'] = i
                        result = handler.process_dropzone_file(
                            file_path, 
                            processing_hints=args.commit_msg,
                            batch_context=batch_context
                        )
                        batch_results.append(result)
                        print(f"✅ Processed {file_path.name}: {result.get('float_id', 'unknown')}")
                    except Exception as e:
                        print(f"❌ Failed to process {file_path.name}: {e}")
                        batch_results.append({'error': str(e), 'file': file_path.name})
                else:
                    print(f"⚠️ File not found: {file_path}")
        
        # Generate bundle meta-summary if we have results
        if batch_results and any(not r.get('error') for r in batch_results):
            print("\n📚 Generating bundle meta-summary...")
            try:
                from bundle_meta_summarizer import BundleMetaSummarizer
                meta_summarizer = BundleMetaSummarizer(handler.components.get('summarizer'))
                
                bundle_summary = meta_summarizer.generate_bundle_summary(
                    batch_results=batch_results,
                    batch_context=batch_context,
                    processing_hints=args.commit_msg
                )
                
                # Store bundle summary
                bundle_file = dropzone_path / f"bundle_{datetime.now().strftime('%Y%m%d_%H%M%S')}.bundle_meta.md"
                with open(bundle_file, 'w', encoding='utf-8') as f:
                    f.write(bundle_summary)
                
                print(f"📝 Bundle meta-summary saved: {bundle_file.name}")
            except ImportError:
                print("⚠️ BundleMetaSummarizer not available, skipping meta-summary")
            except Exception as e:
                print(f"❌ Failed to generate bundle meta-summary: {e}")
        
        print("🎯 Batch processing complete")
        exit(0)
    
    # Initialize daemon for normal monitoring mode
    daemon = FloatDaemonManager(
        dropzone_path=args.dropzone_path,
        config_path=args.config,
        **config_overrides
    )
    
    # Process existing files if requested
    if args.process_existing:
        daemon.process_existing_files()
    
    # Start monitoring
    daemon.start()