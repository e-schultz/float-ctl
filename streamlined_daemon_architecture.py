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

# Import the comprehensive systems
from comprehensive_daily_context import ComprehensiveDailyContext
from ollama_enhanced_float_summarizer import OllamaFloatSummarizer
from float_dis_generator import FloatDisGenerator

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
                 dropzone_path: str,
                 vault_path: str = "/Users/evan/vault",
                 chroma_data_path: str = "/Users/evan/github/chroma-data",
                 enable_ollama: bool = True,
                 auto_update_daily_context: bool = True):
        
        self.dropzone_path = Path(dropzone_path)
        self.vault_path = Path(vault_path)
        self.processing_queue = set()
        self.auto_update_daily_context = auto_update_daily_context
        
        # Initialize the comprehensive systems
        print("🔧 Initializing comprehensive systems...")
        
        # Main processing engine
        self.context_aggregator = ComprehensiveDailyContext(
            vault_path=str(vault_path),
            data_path=chroma_data_path
        )
        
        # Ollama summarizer (optional)
        if enable_ollama:
            try:
                self.summarizer = OllamaFloatSummarizer()
                self.ollama_enabled = True
                print("✅ Ollama summarizer initialized")
            except Exception as e:
                print(f"⚠️ Ollama not available: {e}")
                self.summarizer = None
                self.ollama_enabled = False
        else:
            self.summarizer = None
            self.ollama_enabled = False
        
        # .dis file generator
        self.dis_generator = FloatDisGenerator()
        
        print(f"🤖 FLOAT Daemon initialized")
        print(f"📁 Watching: {self.dropzone_path}")
        print(f"🏠 Vault: {self.vault_path}")
        print(f"🧠 Ollama: {'Enabled' if self.ollama_enabled else 'Disabled'}")
        print(f"🔄 Auto-update daily context: {auto_update_daily_context}")
        
    def on_created(self, event):
        """Handle new file creation in dropzone."""
        if event.is_directory:
            return
            
        file_path = Path(event.src_path)
        
        # Skip temporary files, .diz files, and .float_dis.md files
        if (file_path.suffix in ['.tmp', '.part', '.diz'] or 
            file_path.name.startswith('.') or 
            file_path.name.endswith('.float_dis.md')):
            return
            
        # Prevent duplicate processing
        if str(file_path) in self.processing_queue:
            return
            
        self.processing_queue.add(str(file_path))
        
        # Small delay to ensure file is fully written
        time.sleep(1)
        
        try:
            print(f"\n🔍 New dropzone file: {file_path.name}")
            self.process_dropzone_file(file_path)
        except Exception as e:
            print(f"❌ Error processing {file_path.name}: {e}")
        finally:
            self.processing_queue.discard(str(file_path))
    
    def process_dropzone_file(self, file_path: Path):
        """
        Process a single dropzone file using the comprehensive system.
        """
        
        print(f"🔄 Processing: {file_path.name}")
        
        # Step 1: Generate float ID for tracking
        float_id = self._generate_float_id(file_path)
        print(f"   Float ID: {float_id}")
        
        # Step 2: Use comprehensive context aggregator for file analysis
        file_analysis = self._analyze_file_with_comprehensive_system(file_path, float_id)
        
        # Step 3: Generate enhanced summary with Ollama (if available)
        if self.ollama_enabled and file_analysis['content']:
            print(f"   🤖 Generating Ollama summary...")
            enhanced_summary = self._generate_ollama_summary(
                file_analysis['content'], 
                file_analysis['metadata'], 
                file_analysis['analysis']
            )
            file_analysis['ollama_summary'] = enhanced_summary
        
        # Step 4: Store in appropriate Chroma collections
        storage_result = self._store_in_comprehensive_collections(file_analysis)
        
        # Step 5: Generate .float_dis.md file
        dis_file_path = self._generate_dis_file(file_path, file_analysis, storage_result)
        
        # Step 6: Update daily context if enabled
        if self.auto_update_daily_context:
            self._update_daily_context_for_today()
        
        print(f"✅ Completed: {file_path.name} → {float_id}")
        print(f"   📄 Generated: {dis_file_path.name}")
        
        return {
            'float_id': float_id,
            'dis_file': dis_file_path,
            'storage_result': storage_result,
            'file_analysis': file_analysis
        }
    
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
            import magic
            
            stat = file_path.stat()
            mime_type = magic.from_file(str(file_path), mime=True)
            file_type = magic.from_file(str(file_path))
            
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
            print(f"⚠️ Error extracting metadata: {e}")
            return {
                'filename': file_path.name,
                'extension': file_path.suffix.lower(),
                'size_bytes': 0,
                'error': str(e)
            }
    
    def _extract_file_content(self, file_path: Path, file_metadata: Dict) -> Optional[str]:
        """Extract content from various file types."""
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
                
        except Exception as e:
            print(f"⚠️ Error extracting content: {e}")
            return None
    
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
        except Exception as e:
            return f"PDF content extraction failed: {e}"
    
    def _extract_docx_content(self, file_path: Path) -> str:
        """Extract text from Word documents."""
        try:
            import mammoth
            with open(file_path, 'rb') as f:
                result = mammoth.extract_raw_text(f)
                return result.value
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
        if 'conversation' in content_lower or 'chat' in content_lower:
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
        if not self.summarizer:
            return {'error': 'Ollama not available'}
        
        try:
            return self.summarizer.generate_comprehensive_summary(
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
            dropzone_collection = self.context_aggregator.client.get_or_create_collection(
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
        
        return self.dis_generator.create_float_dis_file(
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
            daily_context = self.context_aggregator.query_daily_context(today)
            
            if daily_context['source'] == 'fresh_generation':
                print(f"   ✅ Generated fresh daily context")
            else:
                print(f"   ♻️ Using cached daily context")
                
        except Exception as e:
            print(f"   ⚠️ Failed to update daily context: {e}")

class FloatDaemonManager:
    """
    Manager class for the streamlined FLOAT daemon.
    """
    
    def __init__(self, dropzone_path: str, **kwargs):
        self.dropzone_path = Path(dropzone_path)
        self.observer = Observer()
        self.handler = StreamlinedFloatDaemon(dropzone_path, **kwargs)
        
        # Ensure dropzone directory exists
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
    parser.add_argument('dropzone_path', help='Path to dropzone folder to monitor')
    parser.add_argument('--vault-path', default='/Users/evan/vault',
                       help='Path to Obsidian vault')
    parser.add_argument('--chroma-path', default='/Users/evan/github/chroma-data',
                       help='Path to Chroma database')
    parser.add_argument('--enable-ollama', action='store_true',
                       help='Enable Ollama summarization')
    parser.add_argument('--disable-daily-updates', action='store_true',
                       help='Disable automatic daily context updates')
    parser.add_argument('--process-existing', action='store_true',
                       help='Process existing files before starting daemon')
    
    args = parser.parse_args()
    
    # Initialize daemon
    daemon = FloatDaemonManager(
        dropzone_path=args.dropzone_path,
        vault_path=args.vault_path,
        chroma_data_path=args.chroma_path,
        enable_ollama=args.enable_ollama,
        auto_update_daily_context=not args.disable_daily_updates
    )
    
    # Process existing files if requested
    if args.process_existing:
        daemon.process_existing_files()
    
    # Start monitoring
    daemon.start()
