"""
Ollama Summarizer Plugin for FLOAT

This plugin converts the existing OllamaFloatSummarizer into a proper plugin
using the memory-safe plugin architecture. It provides the same comprehensive
summarization capabilities including hierarchical multi-chunk processing for large files.

Issue #14: Memory-safe plugin architecture - Ollama Summarizer conversion
"""

import json
import requests
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path

from plugin_base import SummarizerPlugin


class OllamaSummarizerPlugin(SummarizerPlugin):
    """
    Ollama-powered summarization plugin with hierarchical multi-chunk processing.
    
    This plugin provides the same functionality as the original OllamaFloatSummarizer
    but in a memory-safe plugin architecture using entry points.
    """
    
    @property
    def name(self) -> str:
        return "ollama_summarizer"
    
    @property
    def version(self) -> str:
        return "3.1.0"
    
    @property
    def description(self) -> str:
        return "Local Ollama-powered AI summarization with hierarchical multi-chunk processing"
    
    @property
    def author(self) -> str:
        return "FLOAT Core Team"
    
    @property
    def requires_float_version(self) -> str:
        return "3.1.0"
    
    @property
    def max_content_length(self) -> int:
        """Maximum content length supported by the summarizer."""
        return 200000  # Supports larger content through chunking
    
    @property
    def supports_streaming(self) -> bool:
        """Indicates whether the summarizer supports streaming/chunked processing."""
        return True  # Supports hierarchical chunking
    
    def initialize(self, config: Optional[Dict] = None, logger=None) -> bool:
        """Initialize the Ollama summarizer plugin with configuration."""
        super().initialize(config, logger)
        
        # Initialize configuration
        self._config = config or {}
        self.ollama_url = self._config.get('ollama_url', 'http://localhost:11434')
        self.model = self._config.get('ollama_model', 'llama3.1:8b')
        self.chunk_model = self._config.get('ollama_chunk_model', 'llama3.1:8b')
        self.final_model = self._config.get('ollama_final_model', 'llama3.1:8b')
        
        # Configuration parameters
        self.max_chunk_size = self._config.get('max_chunk_size', 4000)
        self.max_chunks_per_batch = self._config.get('max_chunks_per_batch', 10)
        
        # Test Ollama connection
        self.ollama_available = self._test_ollama_connection()
        
        if self._logger:
            if self.ollama_available:
                self._logger.info(f"Initialized {self.name} with Ollama at {self.ollama_url}")
            else:
                self._logger.warning(f"Initialized {self.name} but Ollama unavailable - will use fallback")
        
        return True
    
    def summarize_content(self, content: str, file_metadata: Dict[str, Any], 
                         processing_hints: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate a summary of the provided content using Ollama AI.
        
        This is the plugin interface method that wraps the comprehensive summarization logic.
        """
        try:
            # Prepare content analysis from metadata if available
            content_analysis = file_metadata.get('content_analysis', {})
            
            # Use the comprehensive summarization logic
            result = self._generate_comprehensive_summary(
                content, 
                file_metadata, 
                content_analysis, 
                processing_hints
            )
            
            # Ensure plugin interface compliance
            result.update({
                'success': True,
                'plugin_name': self.name,
                'plugin_version': self.version,
                'ollama_available': self.ollama_available
            })
            
            return result
            
        except Exception as e:
            if self._logger:
                self._logger.error(f"Summarization failed: {e}")
            
            return {
                'success': False,
                'summary': None,
                'error': str(e),
                'plugin_name': self.name,
                'plugin_version': self.version,
                'ollama_available': self.ollama_available
            }
    
    def _test_ollama_connection(self) -> bool:
        """Test if Ollama is available and model is accessible."""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get('models', [])
                available_models = [m['name'] for m in models]
                
                if self._logger:
                    self._logger.info(f"🤖 Ollama connected. Available models: {', '.join(available_models[:3])}...")
                
                if self.model not in available_models:
                    if self._logger:
                        self._logger.warning(f"Model {self.model} not found. Using first available model.")
                    if available_models:
                        self.model = available_models[0]
                        self.chunk_model = available_models[0]
                        self.final_model = available_models[0]
                
                return True
            else:
                if self._logger:
                    self._logger.warning(f"Ollama connection failed: {response.status_code}")
                return False
        except Exception as e:
            if self._logger:
                self._logger.warning(f"Ollama not available: {e}")
            return False
    
    def _generate_comprehensive_summary(self, content: str, file_metadata: Dict, 
                                      content_analysis: Dict, processing_hints: str = None) -> Dict:
        """
        Generate comprehensive summary using hierarchical chunking approach.
        
        This method implements the core summarization logic from the original OllamaFloatSummarizer.
        """
        start_time = datetime.now()
        
        # Basic content analysis
        word_count = len(content.split())
        char_count = len(content)
        
        result = {
            'content_stats': {
                'word_count': word_count,
                'char_count': char_count,
                'processing_time': 0,
                'chunking_strategy': 'single',
                'chunks_processed': 1
            },
            'summary': None,
            'chunk_summaries': [],
            'processing_metadata': {
                'ollama_available': self.ollama_available,
                'model_used': self.model,
                'processing_hints': processing_hints
            }
        }
        
        try:
            # Decide on processing strategy based on content size
            if len(content) <= self.max_chunk_size:
                # Single chunk processing
                summary_result = self._generate_single_summary(content, file_metadata, content_analysis)
                result['summary'] = summary_result.get('summary')
                result['content_stats']['chunking_strategy'] = 'single'
            else:
                # Multi-chunk hierarchical processing
                chunks = self._chunk_content_for_summarization(content)
                result['content_stats']['chunking_strategy'] = 'hierarchical'
                result['content_stats']['chunks_processed'] = len(chunks)
                
                if self.ollama_available:
                    # Generate chunk summaries
                    chunk_summaries = []
                    for i, chunk in enumerate(chunks):
                        chunk_summary = self._generate_chunk_summary(chunk, i, len(chunks))
                        chunk_summaries.append(chunk_summary)
                    
                    result['chunk_summaries'] = chunk_summaries
                    
                    # Synthesize final summary
                    final_summary = self._synthesize_final_summary(chunk_summaries, file_metadata, content_analysis)
                    result['summary'] = final_summary.get('summary')
                else:
                    # Fallback processing for large content
                    result['summary'] = self._generate_fallback_summary(content, file_metadata, content_analysis)
            
            # Calculate processing time
            processing_time = (datetime.now() - start_time).total_seconds()
            result['content_stats']['processing_time'] = processing_time
            
            return result
            
        except Exception as e:
            if self._logger:
                self._logger.error(f"Comprehensive summarization failed: {e}")
            
            # Return fallback summary
            result['summary'] = self._generate_fallback_summary(content, file_metadata, content_analysis)
            result['processing_metadata']['error'] = str(e)
            result['processing_metadata']['fallback_used'] = True
            
            return result
    
    def _generate_single_summary(self, content: str, file_metadata: Dict, content_analysis: Dict) -> Dict:
        """Generate summary for single chunk content."""
        if not self.ollama_available:
            return {'summary': self._generate_fallback_summary(content, file_metadata, content_analysis)}
        
        # Construct prompt for single content summarization
        prompt = self._build_summarization_prompt(content, file_metadata, content_analysis)
        
        try:
            response = self._call_ollama(prompt, self.model)
            if response and response.get('success'):
                return {'summary': response.get('response', '').strip()}
            else:
                return {'summary': self._generate_fallback_summary(content, file_metadata, content_analysis)}
        except Exception as e:
            if self._logger:
                self._logger.error(f"Single summary generation failed: {e}")
            return {'summary': self._generate_fallback_summary(content, file_metadata, content_analysis)}
    
    def _generate_chunk_summary(self, chunk: str, chunk_index: int, total_chunks: int) -> Dict:
        """Generate summary for a single chunk."""
        if not self.ollama_available:
            return self._generate_fallback_chunk_summary(chunk, chunk_index)
        
        prompt = f"""Please summarize this chunk ({chunk_index + 1} of {total_chunks}) of content. Focus on:
- Key topics and main points
- Important details and insights
- Context that would be valuable for understanding the overall document

Content chunk:
{chunk}

Summary:"""
        
        try:
            response = self._call_ollama(prompt, self.chunk_model)
            if response and response.get('success'):
                return {
                    'chunk_index': chunk_index,
                    'summary': response.get('response', '').strip(),
                    'char_count': len(chunk),
                    'word_count': len(chunk.split())
                }
            else:
                return self._generate_fallback_chunk_summary(chunk, chunk_index)
        except Exception as e:
            if self._logger:
                self._logger.error(f"Chunk {chunk_index} summary failed: {e}")
            return self._generate_fallback_chunk_summary(chunk, chunk_index)
    
    def _synthesize_final_summary(self, chunk_summaries: List[Dict], file_metadata: Dict, content_analysis: Dict) -> Dict:
        """Synthesize final summary from chunk summaries."""
        if not self.ollama_available or not chunk_summaries:
            return {'summary': 'Summary unavailable - Ollama not accessible'}
        
        # Combine chunk summaries
        combined_summaries = "\n\n".join([
            f"Section {cs['chunk_index'] + 1}: {cs['summary']}" 
            for cs in chunk_summaries if cs.get('summary')
        ])
        
        file_type = file_metadata.get('content_type', 'document')
        
        prompt = f"""Based on these section summaries from a {file_type}, create a comprehensive final summary:

{combined_summaries}

Please provide a cohesive summary that:
- Captures the main themes and key points
- Maintains logical flow and context
- Highlights important insights and conclusions
- Is concise but comprehensive

Final Summary:"""
        
        try:
            response = self._call_ollama(prompt, self.final_model)
            if response and response.get('success'):
                return {'summary': response.get('response', '').strip()}
            else:
                # Fallback to combining summaries
                return {'summary': f"Document summary based on {len(chunk_summaries)} sections:\n\n" + combined_summaries}
        except Exception as e:
            if self._logger:
                self._logger.error(f"Final summary synthesis failed: {e}")
            return {'summary': f"Document summary based on {len(chunk_summaries)} sections:\n\n" + combined_summaries}
    
    def _build_summarization_prompt(self, content: str, file_metadata: Dict, content_analysis: Dict) -> str:
        """Build appropriate summarization prompt based on content type and analysis."""
        content_type = file_metadata.get('content_type', 'document')
        file_name = file_metadata.get('filename', 'document')
        
        # Extract relevant analysis info
        signal_analysis = content_analysis.get('signal_analysis', {})
        has_float_patterns = signal_analysis.get('total_signals', 0) > 0
        
        if content_type == 'AI conversation export':
            prompt = f"""Summarize this AI conversation export from {file_name}:

{content}

Focus on:
- Main topics discussed
- Key insights and conclusions
- Important decisions or outcomes
- Technical details or solutions

Summary:"""
        elif has_float_patterns:
            prompt = f"""Summarize this FLOAT methodology document:

{content}

Pay special attention to:
- FLOAT patterns (ctx::, highlight::, signal::)
- Actionable insights and tasks
- Process flows and methodologies
- Cross-references and connections

Summary:"""
        else:
            prompt = f"""Summarize this {content_type}:

{content}

Provide a clear, concise summary focusing on:
- Main topics and themes
- Key points and insights
- Important conclusions or outcomes

Summary:"""
        
        return prompt
    
    def _call_ollama(self, prompt: str, model: str) -> Dict:
        """Make API call to Ollama."""
        try:
            payload = {
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "max_tokens": 500
                }
            }
            
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    'success': True,
                    'response': result.get('response', ''),
                    'model': model
                }
            else:
                return {'success': False, 'error': f"HTTP {response.status_code}"}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _chunk_content_for_summarization(self, content: str) -> List[str]:
        """Intelligent chunking for summarization that preserves content boundaries."""
        if len(content) <= self.max_chunk_size:
            return [content]
        
        chunks = []
        
        # Strategy 1: Try conversation-aware chunking for chat exports
        if self._is_conversation_content(content):
            chunks = self._chunk_conversation_content(content)
        # Strategy 2: Try document structure chunking (headers, paragraphs)
        elif self._has_document_structure(content):
            chunks = self._chunk_document_content(content)
        # Strategy 3: Fallback to semantic chunking
        else:
            chunks = self._chunk_semantic_content(content)
        
        # Ensure no chunk exceeds max size
        final_chunks = []
        for chunk in chunks:
            if len(chunk) > self.max_chunk_size:
                # Hard split oversized chunks
                final_chunks.extend([
                    chunk[i:i+self.max_chunk_size] 
                    for i in range(0, len(chunk), self.max_chunk_size)
                ])
            else:
                final_chunks.append(chunk)
        
        return [chunk for chunk in final_chunks if len(chunk.strip()) > 100]
    
    def _is_conversation_content(self, content: str) -> bool:
        """Detect if content looks like a conversation/chat export."""
        import re
        conversation_markers = [
            r'## (?:HUMAN|ASSISTANT|USER)',
            r'"role":\s*"(?:user|assistant|human)"',
            r'ChatGPT|Claude|GPT-',
            r'Human:|Assistant:|AI:'
        ]
        
        for pattern in conversation_markers:
            if re.search(pattern, content, re.IGNORECASE):
                return True
        return False
    
    def _has_document_structure(self, content: str) -> bool:
        """Detect if content has clear document structure."""
        import re
        structure_indicators = [
            len(re.findall(r'^#+\s', content, re.MULTILINE)) > 3,  # Multiple headers
            len(re.findall(r'\n\n', content)) > 10,                # Multiple paragraphs
            content.count('```') > 2,                               # Code blocks
        ]
        return any(structure_indicators)
    
    def _chunk_conversation_content(self, content: str) -> List[str]:
        """Chunk conversation content on message boundaries."""
        import re
        
        # Split on conversation turn markers
        patterns = [
            r'(## (?:HUMAN|ASSISTANT|USER))',
            r'(\n(?:Human|Assistant|AI):\s)',
            r'("role":\s*"(?:user|assistant)")',
        ]
        
        for pattern in patterns:
            parts = re.split(pattern, content, flags=re.IGNORECASE)
            if len(parts) > 3:  # Found meaningful splits
                chunks = []
                current_chunk = ""
                
                for part in parts:
                    if len(current_chunk + part) > self.max_chunk_size and current_chunk:
                        chunks.append(current_chunk.strip())
                        current_chunk = part
                    else:
                        current_chunk += part
                
                if current_chunk.strip():
                    chunks.append(current_chunk.strip())
                
                return [chunk for chunk in chunks if len(chunk.strip()) > 50]
        
        # Fallback to paragraph chunking
        return self._chunk_document_content(content)
    
    def _chunk_document_content(self, content: str) -> List[str]:
        """Chunk document content on structural boundaries."""
        import re
        
        # Try to split on headers first
        header_splits = re.split(r'\n(#+\s.+)', content)
        if len(header_splits) > 3:
            chunks = []
            current_chunk = ""
            
            for part in header_splits:
                if len(current_chunk + part) > self.max_chunk_size and current_chunk:
                    chunks.append(current_chunk.strip())
                    current_chunk = part
                else:
                    current_chunk += part
            
            if current_chunk.strip():
                chunks.append(current_chunk.strip())
            
            return [chunk for chunk in chunks if len(chunk.strip()) > 50]
        
        # Fallback to paragraph chunking
        paragraphs = content.split('\n\n')
        chunks = []
        current_chunk = ""
        
        for paragraph in paragraphs:
            if len(current_chunk + paragraph) > self.max_chunk_size and current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = paragraph
            else:
                current_chunk += "\n\n" + paragraph if current_chunk else paragraph
        
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        
        return [chunk for chunk in chunks if len(chunk.strip()) > 50]
    
    def _chunk_semantic_content(self, content: str) -> List[str]:
        """Fallback semantic chunking based on sentences and paragraphs."""
        # Simple sentence-aware chunking
        sentences = content.replace('!', '.').replace('?', '.').split('.')
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
                
            if len(current_chunk + sentence) > self.max_chunk_size and current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = sentence
            else:
                current_chunk += ". " + sentence if current_chunk else sentence
        
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        
        return [chunk for chunk in chunks if len(chunk.strip()) > 50]
    
    def _generate_fallback_summary(self, content: str, file_metadata: Dict, content_analysis: Dict) -> str:
        """Generate basic fallback summary when Ollama is unavailable."""
        word_count = len(content.split())
        char_count = len(content)
        
        # Extract basic insights from content analysis
        signal_count = content_analysis.get('signal_analysis', {}).get('total_signals', 0)
        content_type = file_metadata.get('content_type', 'document')
        filename = file_metadata.get('filename', 'unknown')
        
        summary_parts = [
            f"📄 {content_type.title()}: {filename}",
            f"📊 Content: {word_count:,} words, {char_count:,} characters"
        ]
        
        if signal_count > 0:
            summary_parts.append(f"🔍 FLOAT signals detected: {signal_count}")
        
        # Add content type specific insights
        if content_type == 'AI conversation export':
            # Count conversation turns
            import re
            turns = len(re.findall(r'(?:Human:|Assistant:|AI:|## (?:HUMAN|ASSISTANT))', content, re.IGNORECASE))
            if turns > 0:
                summary_parts.append(f"💬 Conversation turns: {turns}")
        
        summary_parts.append("⚠️ Detailed AI summary unavailable (Ollama not accessible)")
        
        return "\n".join(summary_parts)
    
    def _generate_fallback_chunk_summary(self, chunk: str, chunk_index: int) -> Dict:
        """Generate fallback chunk summary when Ollama is unavailable."""
        return {
            'chunk_index': chunk_index,
            'summary': f"Chunk {chunk_index + 1}: {len(chunk.split())} words, {len(chunk)} characters",
            'char_count': len(chunk),
            'word_count': len(chunk.split()),
            'fallback': True
        }