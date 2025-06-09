"""
Streamlined FLOAT Daemon Architecture
Simple file watcher that delegates to Comprehensive Daily Context Aggregator
Clean separation: daemon watches, aggregator processes, summarizer enhances
"""

import os
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class StreamlinedFloatDaemon(FileSystemEventHandler):
    """
    Simplified daemon that delegates all processing to existing comprehensive systems.
    
    Responsibilities:
    1. Watch dropzone folder for new files
    2. Delegate processing to ComprehensiveDailyContext
    3. Trigger daily summary updates when files are added
    4. Generate .float_dis.md files via the dis generator
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
        
        self.logger.info("FLOAT Daemon initialized", extra={
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
        
        # Try enhanced context aggregator first
        try:
            from enhanced_comprehensive_context_ollama import EnhancedComprehensiveDailyContext
            components['context'] = EnhancedComprehensiveDailyContext(
                vault_path=str(self.vault_path),
                data_path=self.chroma_data_path
            )
            components['enhanced_mode'] = True
            self.logger.info("Enhanced context aggregator initialized")
        except ImportError as e:
            self.logger.warning(f"Enhanced context not available: {e}")
            try:
                from comprehensive_daily_context import ComprehensiveDailyContext
                components['context'] = ComprehensiveDailyContext(
                    vault_path=str(self.vault_path),
                    data_path=self.chroma_data_path
                )
                components['enhanced_mode'] = False
                self.logger.info("Basic context aggregator initialized")
            except ImportError as e:
                raise RuntimeError(f"No context aggregator available: {e}")
        
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
        
        # Try .dis generator
        try:
            from float_dis_template_system import FloatDisGenerator
            components['dis_generator'] = FloatDisGenerator()
            self.logger.info("FloatDisGenerator initialized")
        except ImportError:
            try:
                from float_dis_generator import FloatDisGenerator
                components['dis_generator'] = FloatDisGenerator()
                self.logger.info("FloatDisGenerator initialized (alternate import)")
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
            self.logger.info(f"New dropzone file detected", extra={
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
    
    def process_dropzone_file(self, file_path: Path):
        """
        Process a single dropzone file using the comprehensive system.
        """
        import time
        from logging_config import (log_file_processing_start, log_file_processing_complete, 
                                   log_ollama_summary, log_chroma_storage, log_dis_file_generation)
        
        start_time = time.time()
        
        # Step 1: Generate float ID for tracking
        float_id = self._generate_float_id(file_path)
        
        # Step 2: Use comprehensive context aggregator for file analysis
        file_analysis = self._analyze_file_with_comprehensive_system(file_path, float_id)
        
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
                    file_analysis['analysis']
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
            
            return {
                'float_id': float_id,
                'dis_file': dis_file_path,
                'storage_result': storage_result,
                'file_analysis': file_analysis
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
    
    def _generate_float_id(self, file_path: Path) -> str:
        """Generate unique float ID for the file."""
        import hashlib
        
        # Use file path + timestamp for uniqueness
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        file_hash = hashlib.md5(str(file_path).encode()).hexdigest()[:8]
        
        return f"float_{timestamp}_{file_hash}"
    
    def _analyze_file_with_comprehensive_system(self, file_path: Path, float_id: str) -> Dict:
        """
        Analyze file using the comprehensive context aggregator's file analysis capabilities.
        """
        
        # Detect file type and extract metadata
        file_metadata = self._extract_file_metadata(file_path)
        
        # Extract content using the context aggregator's methods
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
                    return f.read()
            
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
        Analyze content for FLOAT patterns and other characteristics.
        Reuses the comprehensive context aggregator's analysis methods.
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
        
        # Content type detection
        content_lower = content.lower()
        if '"powered_by": "Claude Exporter' in content:
            analysis['content_type'] = "AI conversation export (Chrome plugin)"
        elif '"powered_by": "ChatGPT Exporter' in content:
            analysis['content_type'] = "AI conversation export (Chrome plugin)"
        elif 'conversation' in content_lower or 'chat' in content_lower:
            analysis['content_type'] = "Conversation/Chat export"
        elif content.strip().startswith('{') or content.strip().startswith('['):
            analysis['content_type'] = "JSON data structure"
        elif 'claude.ai' in content or 'chatgpt.com' in content:
            analysis['content_type'] = "AI conversation export"
        elif len([line for line in lines if line.startswith('#')]) > 3:
            analysis['content_type'] = "Markdown document"
        else:
            analysis['content_type'] = file_metadata.get('file_type', 'Unknown content')
        
        # FLOAT pattern detection
        ctx_matches = re.findall(r'ctx::', content)
        highlight_matches = re.findall(r'highlight::', content)
        dispatch_matches = re.findall(r'float\.dispatch', content)
        conversation_links = re.findall(r'https://(?:claude\.ai|chatgpt\.com)', content)
        
        analysis.update({
            'has_ctx_markers': len(ctx_matches) > 0,
            'has_highlights': len(highlight_matches) > 0,
            'has_float_dispatch': len(dispatch_matches) > 0,
            'has_conversation_links': len(conversation_links) > 0,
            'ctx_count': len(ctx_matches),
            'highlight_count': len(highlight_matches),
            'signal_density': (len(ctx_matches) + len(highlight_matches) + len(dispatch_matches)) / max(len(words), 1)
        })
        
        # Generate basic summary
        topic = "No clear topic identified"
        for line in lines[:10]:
            line = line.strip()
            if len(line) > 10 and not line.startswith('#') and not line.startswith('-'):
                topic = line[:100] + "..." if len(line) > 100 else line
                break
        
        analysis['basic_summary'] = f"{analysis['content_type']}. {topic}. {len(lines)} lines, {len(words)} words."
        
        return analysis
    
    def _generate_ollama_summary(self, content: str, file_metadata: Dict, content_analysis: Dict) -> Dict:
        """Generate enhanced summary using Ollama."""
        if not self.components.get('summarizer'):
            return {'error': 'Ollama not available'}
        
        try:
            return self.components['summarizer'].generate_comprehensive_summary(
                content, file_metadata, content_analysis
            )
        except Exception as e:
            print(f"⚠️ Ollama summary failed: {e}")
            return {'error': str(e), 'fallback_used': True}
    
    def _store_in_comprehensive_collections(self, file_analysis: Dict) -> Dict:
        """
        Store the file in appropriate Chroma collections.
        Delegates to the comprehensive context aggregator's storage methods.
        """
        
        # For now, store in a dedicated dropzone collection
        # In the future, this could intelligently route to tripartite collections
        
        try:
            dropzone_collection = self.components['context'].client.get_or_create_collection(
                name="float_dropzone_comprehensive",
                metadata={
                    "description": "Comprehensive dropzone file ingestion",
                    "processing_method": "streamlined_daemon"
                }
            )
            
            # Chunk content if needed
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
                'collection': 'float_dropzone_comprehensive',
                'chunk_count': len(chunks),
                'chunk_ids': chunk_ids
            }
            
        except Exception as e:
            print(f"⚠️ Storage failed: {e}")
            return {
                'success': False,
                'error': str(e)
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
        self.handler = StreamlinedFloatDaemon(
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
    
    # Initialize daemon
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