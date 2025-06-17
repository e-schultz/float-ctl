"""
LF1M (Little Fucker needs a Minute) Core Processing Module

Extracted from streamlined_float_daemon.py for CLI and daemon use.
Handles file processing, search operations, and ChromaDB interactions.
"""

import os
import sys
import time
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Union

# Add the parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

class LF1M:
    """Core FLOAT processing engine extracted from daemon"""
    
    def __init__(self, config_path: str = None, **config_overrides):
        """Initialize LF1M with configuration"""
        # Load configuration
        from config import FloatConfig
        from logging_config import setup_logging
        
        self.config = FloatConfig(config_path)
        self.config.update(config_overrides)
        
        # Setup logging
        self.logger = setup_logging(self.config.config)
        
        # Set up paths from config
        self.dropzone_path = Path(self.config.get('dropzone_path'))
        self.vault_path = Path(self.config.get('vault_path'))
        self.chroma_data_path = self.config.get('chroma_data_path')
        
        # Initialize components
        self.components = self._initialize_components()
        
        # Initialize enhanced integration
        self.enhanced_integration = None
        if self.config.get('enable_enhanced_integration', True):
            try:
                from enhanced_integration import EnhancedSystemIntegration
                self.enhanced_integration = EnhancedSystemIntegration(self)
                self.logger.info("Enhanced integration system initialized")
            except Exception as e:
                self.logger.warning(f"Enhanced integration not available: {e}")
        
        self.logger.info("LF1M core initialized")
    
    def _initialize_components(self) -> Dict:
        """Initialize processing components"""
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
    
    def process_file(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Process a single file through the FLOAT pipeline.
        Main entry point for CLI processing.
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            return {
                'success': False,
                'error': 'File not found',
                'file_path': str(file_path)
            }
        
        try:
            self.logger.info(f"Processing file: {file_path.name}")
            
            if self.enhanced_integration:
                result = self.enhanced_integration.process_file_with_enhanced_integration(file_path)
                # Enhanced integration returns a different format, standardize it
                if isinstance(result, dict):
                    result['success'] = True
                    result['processed_at'] = datetime.now().isoformat()
                else:
                    result = {
                        'success': True,
                        'float_id': getattr(result, 'float_id', None),
                        'processed_at': datetime.now().isoformat()
                    }
            else:
                result = self._process_file_basic(file_path)
                result['success'] = True
                result['processed_at'] = datetime.now().isoformat()
            
            self.logger.info(f"Successfully processed: {file_path.name}")
            return result
            
        except Exception as e:
            self.logger.error(f"Error processing {file_path.name}: {e}", exc_info=True)
            return {
                'success': False,
                'error': str(e),
                'file_path': str(file_path)
            }
    
    def process_folder(self, folder_path: Union[str, Path], recursive: bool = True) -> List[Dict[str, Any]]:
        """Process all files in a folder"""
        folder_path = Path(folder_path)
        
        if not folder_path.exists() or not folder_path.is_dir():
            return [{
                'success': False,
                'error': 'Folder not found or not a directory',
                'folder_path': str(folder_path)
            }]
        
        results = []
        pattern = "**/*" if recursive else "*"
        
        for file_path in folder_path.glob(pattern):
            if file_path.is_file() and not self._should_skip_file(file_path):
                result = self.process_file(file_path)
                results.append(result)
        
        return results
    
    def search_collections(self, query: str, collections: List[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search across ChromaDB collections.
        Basic text search - FloatQL parsing handled in commands/search.py
        """
        try:
            import chromadb
            client = chromadb.PersistentClient(path=self.chroma_data_path)
            
            if collections is None:
                # Default collections to search
                collections = [
                    'float_tripartite_v2_concept',
                    'float_tripartite_v2_framework', 
                    'float_tripartite_v2_metaphor',
                    'float_dropzone_comprehensive'
                ]
            
            all_results = []
            
            for collection_name in collections:
                try:
                    collection = client.get_collection(collection_name)
                    results = collection.query(
                        query_texts=[query],
                        n_results=limit
                    )
                    
                    # Format results
                    for i, doc in enumerate(results['documents'][0]):
                        all_results.append({
                            'collection': collection_name,
                            'document': doc,
                            'metadata': results['metadatas'][0][i] if results['metadatas'][0] else {},
                            'distance': results['distances'][0][i] if results['distances'][0] else None,
                            'id': results['ids'][0][i] if results['ids'][0] else None
                        })
                        
                except Exception as e:
                    self.logger.warning(f"Error searching collection {collection_name}: {e}")
                    continue
            
            # Sort by distance (similarity)
            all_results.sort(key=lambda x: x['distance'] or float('inf'))
            
            return all_results[:limit]
            
        except Exception as e:
            self.logger.error(f"Search error: {e}")
            return []
    
    def get_daemon_status(self) -> Dict[str, Any]:
        """Get status of the lf1m daemon if running"""
        try:
            status_file = self.dropzone_path / '.daemon_status.json'
            if status_file.exists():
                with open(status_file, 'r') as f:
                    status = json.load(f)
                return status
            else:
                return {'status': 'stopped', 'message': 'No status file found'}
        except Exception as e:
            return {'status': 'unknown', 'error': str(e)}
    
    def list_collections(self) -> List[Dict[str, Any]]:
        """List all ChromaDB collections with counts"""
        try:
            import chromadb
            client = chromadb.PersistentClient(path=self.chroma_data_path)
            
            collections = []
            for collection in client.list_collections():
                collections.append({
                    'name': collection.name,
                    'count': collection.count()
                })
            
            return collections
            
        except Exception as e:
            self.logger.error(f"Error listing collections: {e}")
            return []
    
    def _process_file_basic(self, file_path: Path) -> Dict[str, Any]:
        """Basic file processing without enhanced integration"""
        # Extract content and metadata
        file_metadata = self._extract_file_metadata(file_path)
        content = self._extract_file_content(file_path, file_metadata)
        
        # Generate float ID
        float_id = self._generate_float_id(file_path, content)
        
        # Use context aggregator for basic analysis
        file_analysis = {
            'float_id': float_id,
            'content': content,
            'metadata': file_metadata,
            'analysis': {'patterns': [], 'classification': {}}
        }
        
        # Store in ChromaDB
        storage_result = self._store_in_comprehensive_collections(file_analysis)
        
        # Generate .dis file
        dis_file_path = self._generate_dis_file(file_path, file_analysis, storage_result)
        
        return {
            'float_id': float_id,
            'dis_file': str(dis_file_path),
            'storage_result': storage_result
        }
    
    def _should_skip_file(self, file_path: Path) -> bool:
        """Check if file should be skipped during processing"""
        return (
            file_path.suffix in ['.tmp', '.part', '.diz', '.crdownload'] or 
            file_path.name.startswith('.') or 
            file_path.name.endswith('.float_dis.md') or
            'Unconfirmed' in file_path.name
        )
    
    def _extract_file_metadata(self, file_path: Path) -> Dict[str, Any]:
        """Extract basic file metadata"""
        stat = file_path.stat()
        return {
            'file_name': file_path.name,
            'file_path': str(file_path),
            'size_bytes': stat.st_size,
            'created_at': datetime.fromtimestamp(stat.st_ctime).isoformat(),
            'modified_at': datetime.fromtimestamp(stat.st_mtime).isoformat(),
            'extension': file_path.suffix.lower()
        }
    
    def _extract_file_content(self, file_path: Path, metadata: Dict[str, Any]) -> str:
        """Extract content from file based on type"""
        try:
            if metadata['extension'] in ['.txt', '.md', '.markdown']:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            else:
                # For other file types, return basic info
                return f"Binary file: {file_path.name} ({metadata['size_bytes']} bytes)"
        except Exception as e:
            self.logger.warning(f"Could not read file {file_path.name}: {e}")
            return ""
    
    def _generate_float_id(self, file_path: Path, content: str) -> str:
        """Generate consistent float ID for file"""
        import hashlib
        
        # Use file name + first 1000 chars of content for ID
        id_source = f"{file_path.name}:{content[:1000]}"
        return hashlib.md5(id_source.encode()).hexdigest()[:12]
    
    def _chunk_content(self, content: str, chunk_size: int = 2000) -> List[str]:
        """Simple content chunking for enhanced integration compatibility"""
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
    
    def _store_in_comprehensive_collections(self, file_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Store file in appropriate ChromaDB collections"""
        try:
            # Use existing context system for storage
            if hasattr(self.components['context'], 'store_content_in_tripartite_collections'):
                return self.components['context'].store_content_in_tripartite_collections(file_analysis)
            else:
                # Fallback to basic storage
                return {'success': True, 'collection': 'float_dropzone_comprehensive', 'chunk_count': 1}
        except Exception as e:
            self.logger.error(f"Storage error: {e}")
            return {'success': False, 'error': str(e)}
    
    def _generate_dis_file(self, file_path: Path, file_analysis: Dict[str, Any], storage_result: Dict[str, Any]) -> Path:
        """Generate .float_dis.md file"""
        try:
            if self.components['dis_generator']:
                return self.components['dis_generator'].generate_dis_file(
                    file_path, file_analysis, storage_result
                )
            else:
                # Create basic .dis file
                dis_path = file_path.with_suffix('.float_dis.md')
                with open(dis_path, 'w') as f:
                    f.write(f"# {file_path.name}\n\nFloat ID: {file_analysis['float_id']}\n")
                return dis_path
        except Exception as e:
            self.logger.error(f"Error generating .dis file: {e}")
            return file_path.with_suffix('.float_dis.md')
    
    def process_dropzone_file(self, file_path: Path) -> Dict[str, Any]:
        """
        Process dropzone file - wrapper for compatibility with enhanced integration.
        This mimics the daemon's process_dropzone_file method.
        """
        try:
            # Extract content and metadata
            file_metadata = self._extract_file_metadata(file_path)
            content = self._extract_file_content(file_path, file_metadata)
            
            # Generate float ID
            float_id = self._generate_float_id(file_path, content)
            
            # Create file analysis structure
            file_analysis = {
                'float_id': float_id,
                'content': content,
                'metadata': file_metadata,
                'analysis': {'patterns': [], 'classification': {}},
                'file_path': str(file_path)
            }
            
            # Use enhanced context for analysis if available
            if hasattr(self.components['context'], 'analyze_content_for_tripartite_routing'):
                analysis_result = self.components['context'].analyze_content_for_tripartite_routing(
                    content, file_metadata
                )
                file_analysis['analysis'].update(analysis_result)
            
            # Generate Ollama summary if available
            if self.components['ollama_enabled'] and content:
                try:
                    # Create basic content analysis for Ollama summarizer
                    content_analysis = file_analysis.get('analysis', {})
                    if not content_analysis:
                        content_analysis = {'patterns': [], 'classification': {}}
                    
                    summary = self.components['summarizer'].generate_comprehensive_summary(
                        content, 
                        file_metadata,
                        content_analysis
                    )
                    file_analysis['ollama_summary'] = summary
                except Exception as e:
                    self.logger.warning(f"Ollama summary generation failed: {e}")
                    file_analysis['ollama_summary'] = None
            
            return {
                'success': True,
                'float_id': float_id,
                'file_analysis': file_analysis,
                'processed_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error in process_dropzone_file: {e}")
            return {
                'success': False,
                'error': str(e),
                'file_path': str(file_path)
            }