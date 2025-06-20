"""
Ollama-Enhanced FLOAT Summarizer
Local AI summarization with multi-chunk hierarchical processing for large files
Integrates with dropzone daemon for intelligent content analysis
"""

import json
import requests
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import hashlib
import re

class OllamaFloatSummarizer:
    """
    Local Ollama-powered summarization with FLOAT-aware content analysis.
    Handles large files through hierarchical multi-chunk summarization.
    """
    
    def __init__(self, 
                 ollama_url: str = "http://localhost:11434",
                 model: str = "llama3.1:8b",
                 chunk_model: str = "llama3.1:8b",
                 final_model: str = "llama3.1:8b"):
        self.ollama_url = ollama_url
        self.model = model
        self.chunk_model = chunk_model  # Fast model for chunk summaries
        self.final_model = final_model  # Better model for final synthesis
        self.max_chunk_size = 4000      # Conservative context window
        self.max_chunks_per_batch = 10  # Reasonable batch size
        
        # Test Ollama connection
        self._test_ollama_connection()
    
    def _test_ollama_connection(self):
        """Test if Ollama is available and model is accessible."""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get('models', [])
                available_models = [m['name'] for m in models]
                print(f"🤖 Ollama connected. Available models: {', '.join(available_models[:3])}...")
                
                if self.model not in available_models:
                    print(f"⚠️ Model {self.model} not found. Using first available model.")
                    if available_models:
                        self.model = available_models[0]
                        self.chunk_model = available_models[0]
                        self.final_model = available_models[0]
            else:
                print(f"⚠️ Ollama connection failed: {response.status_code}")
        except Exception as e:
            print(f"⚠️ Ollama not available: {e}")
            print("   Falling back to basic content analysis")
    
    def chunk_content_for_summarization(self, content: str) -> List[str]:
        """
        Intelligent chunking for summarization that preserves conversation boundaries.
        """
        
        # If content is small enough, return as single chunk
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
        
        return final_chunks
    
    def _is_conversation_content(self, content: str) -> bool:
        """Detect if content looks like a conversation/chat export."""
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
        structure_indicators = [
            len(re.findall(r'^#+\s', content, re.MULTILINE)) > 3,  # Multiple headers
            len(re.findall(r'\n\n', content)) > 10,                # Multiple paragraphs
            content.count('```') > 2,                               # Code blocks
        ]
        return any(structure_indicators)
    
    def _chunk_conversation_content(self, content: str) -> List[str]:
        """Chunk conversation content on message boundaries."""
        
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
                
                for i, part in enumerate(parts):
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
        
        # Try header-based chunking first
        header_splits = re.split(r'\n(#+\s[^\n]+)', content)
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
            
            return [chunk for chunk in chunks if len(chunk.strip()) > 100]
        
        # Fallback to paragraph chunking
        paragraphs = content.split('\n\n')
        chunks = []
        current_chunk = ""
        
        for paragraph in paragraphs:
            if len(current_chunk + paragraph) > self.max_chunk_size and current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = paragraph
            else:
                current_chunk += '\n\n' + paragraph if current_chunk else paragraph
        
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        
        return [chunk for chunk in chunks if len(chunk.strip()) > 50]
    
    def _chunk_semantic_content(self, content: str) -> List[str]:
        """Fallback semantic chunking on sentence boundaries."""
        
        # Split into sentences (simple approach)
        sentences = re.split(r'[.!?]+\s+', content)
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk + sentence) > self.max_chunk_size and current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = sentence
            else:
                current_chunk += ' ' + sentence if current_chunk else sentence
        
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        
        return [chunk for chunk in chunks if len(chunk.strip()) > 30]
    
    def generate_chunk_summary(self, chunk: str, chunk_index: int, 
                             total_chunks: int, file_metadata: Dict,
                             processing_hints: str = None, batch_context: Dict = None) -> Dict:
        """
        Generate summary for a single chunk using Ollama.
        """
        
        # Build dynamic system prompt based on hints
        base_system_prompt = """You are a FLOAT-aware content analyst. Your task is to summarize chunks of documents for knowledge management.

Focus on:
1. Key topics and themes
2. FLOAT patterns (ctx::, highlight::, float.dispatch, ritual language)
3. Technical vs philosophical vs experiential content
4. Important decisions, insights, or outcomes
5. Cross-references and connections"""

        # Add processing hints if provided
        if processing_hints:
            system_prompt = f"{base_system_prompt}\n\nAdditionally, please focus on: {processing_hints}"
        else:
            system_prompt = f"{base_system_prompt}\n\nKeep summaries concise but informative. Preserve important context for later synthesis."

        # Build user prompt with batch context
        if batch_context:
            batch_info = f"""
This is file {batch_context.get('current_file_index', 0) + 1} of {batch_context.get('total_files', 1)} in a batch about: {batch_context.get('domain', 'unknown domain')}
Bundle type: {batch_context.get('type', 'mixed')}, Bundle approach: {batch_context.get('bundle', 'merge')}"""
        else:
            batch_info = ""
        
        user_prompt = f"""Summarize this chunk ({chunk_index + 1} of {total_chunks}) from file: {file_metadata.get('filename', 'unknown')}{batch_info}

CHUNK CONTENT:
{chunk}

Provide a structured summary covering:
- Main topics (2-3 key themes)
- FLOAT patterns detected (if any)
- Key insights or decisions
- Content type (technical/philosophical/experiential)
- Notable quotes or concepts (if any)
{f"- Aspects related to: {processing_hints}" if processing_hints else ""}

Summary:"""

        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.chunk_model,
                    "prompt": f"<|im_start|>system\n{system_prompt}<|im_end|>\n<|im_start|>user\n{user_prompt}<|im_end|>\n<|im_start|>assistant\n",
                    "stream": False,
                    "options": {
                        "temperature": 0.3,
                        "top_p": 0.9,
                        "max_tokens": 400
                    }
                },
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                summary_text = result.get('response', '').strip()
                
                return {
                    'chunk_index': chunk_index,
                    'summary': summary_text,
                    'model_used': self.chunk_model,
                    'success': True,
                    'chunk_size': len(chunk),
                    'generated_at': datetime.now().isoformat()
                }
            else:
                print(f"⚠️ Ollama API error for chunk {chunk_index}: {response.status_code}")
                return self._fallback_chunk_summary(chunk, chunk_index)
                
        except Exception as e:
            print(f"⚠️ Failed to generate summary for chunk {chunk_index}: {e}")
            return self._fallback_chunk_summary(chunk, chunk_index)
    
    def _fallback_chunk_summary(self, chunk: str, chunk_index: int) -> Dict:
        """Fallback summary generation when Ollama is unavailable."""
        
        lines = chunk.split('\n')
        words = chunk.split()
        
        # Extract first meaningful line as topic
        topic = "No clear topic identified"
        for line in lines[:5]:
            line = line.strip()
            if len(line) > 20 and not line.startswith('#') and not line.startswith('-'):
                topic = line[:80] + "..." if len(line) > 80 else line
                break
        
        # Basic pattern detection
        float_patterns = []
        if 'ctx::' in chunk:
            float_patterns.append('ctx:: markers')
        if 'highlight::' in chunk:
            float_patterns.append('highlights')
        if 'float.dispatch' in chunk:
            float_patterns.append('dispatches')
        
        pattern_text = f" FLOAT patterns: {', '.join(float_patterns)}." if float_patterns else ""
        
        summary = f"Chunk {chunk_index + 1}: {topic}. {len(lines)} lines, {len(words)} words.{pattern_text}"
        
        return {
            'chunk_index': chunk_index,
            'summary': summary,
            'model_used': 'fallback',
            'success': False,
            'chunk_size': len(chunk),
            'generated_at': datetime.now().isoformat()
        }
    
    def synthesize_final_summary(self, chunk_summaries: List[Dict], 
                               file_metadata: Dict, content_analysis: Dict,
                               processing_hints: str = None, batch_context: Dict = None) -> Dict:
        """
        Synthesize chunk summaries into a final comprehensive summary.
        """
        
        if not chunk_summaries:
            return self._fallback_final_summary(file_metadata, content_analysis)
        
        # Prepare chunk summaries for synthesis
        summaries_text = "\n".join([
            f"Chunk {summary['chunk_index'] + 1}: {summary['summary']}"
            for summary in chunk_summaries
        ])
        
        # Build system prompt with processing hints
        base_system_prompt = """You are synthesizing chunk summaries into a comprehensive document summary for FLOAT knowledge management.

Create a coherent overview that:
1. Identifies overarching themes and topics
2. Highlights important FLOAT patterns and signals
3. Captures key insights, decisions, or outcomes
4. Describes the content type and structure
5. Notes connections and cross-references
6. Assesses the document's knowledge value"""

        if processing_hints:
            system_prompt = f"{base_system_prompt}\n\nSpecial focus required on: {processing_hints}\n\nBe concise but comprehensive. Focus on what makes this document valuable for future reference, especially regarding the specified focus areas."
        else:
            system_prompt = f"{base_system_prompt}\n\nBe concise but comprehensive. Focus on what makes this document valuable for future reference."

        # Build user prompt with batch context
        batch_info = ""
        if batch_context:
            batch_info = f"""
BATCH CONTEXT: File {batch_context.get('current_file_index', 0) + 1} of {batch_context.get('total_files', 1)}
Domain: {batch_context.get('domain', 'unknown')}
Bundle approach: {batch_context.get('bundle', 'individual')}
"""
        
        user_prompt = f"""Synthesize these chunk summaries into a comprehensive document summary:

DOCUMENT: {file_metadata.get('filename', 'Unknown')}
TYPE: {content_analysis.get('content_type', 'Unknown')}
SIZE: {len(chunk_summaries)} chunks, {sum(s['chunk_size'] for s in chunk_summaries):,} characters{batch_info}

CHUNK SUMMARIES:
{summaries_text}

FLOAT PATTERNS DETECTED:
- ctx:: markers: {content_analysis.get('ctx_count', 0)}
- highlights: {content_analysis.get('highlight_count', 0)}
- float.dispatch: {'Yes' if content_analysis.get('has_float_dispatch') else 'No'}
- conversation links: {'Yes' if content_analysis.get('has_conversation_links') else 'No'}

Create a comprehensive summary that synthesizes the key themes, insights, and value of this document{f', with special attention to: {processing_hints}' if processing_hints else ''}:"""

        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.final_model,
                    "prompt": f"<|im_start|>system\n{system_prompt}<|im_end|>\n<|im_start|>user\n{user_prompt}<|im_end|>\n<|im_start|>assistant\n",
                    "stream": False,
                    "options": {
                        "temperature": 0.4,
                        "top_p": 0.9,
                        "max_tokens": 600
                    }
                },
                timeout=90
            )
            
            if response.status_code == 200:
                result = response.json()
                final_summary = result.get('response', '').strip()
                
                return {
                    'summary': final_summary,
                    'model_used': self.final_model,
                    'synthesis_method': 'ollama_hierarchical',
                    'chunk_count': len(chunk_summaries),
                    'success': True,
                    'generated_at': datetime.now().isoformat(),
                    'chunk_summaries': chunk_summaries
                }
            else:
                print(f"⚠️ Ollama synthesis error: {response.status_code}")
                return self._fallback_final_summary(file_metadata, content_analysis, chunk_summaries)
                
        except Exception as e:
            print(f"⚠️ Failed to synthesize final summary: {e}")
            return self._fallback_final_summary(file_metadata, content_analysis, chunk_summaries)
    
    def _fallback_final_summary(self, file_metadata: Dict, content_analysis: Dict, 
                              chunk_summaries: List[Dict] = None) -> Dict:
        """Fallback final summary when Ollama synthesis fails."""
        
        # Extract key information
        filename = file_metadata.get('filename', 'Unknown file')
        content_type = content_analysis.get('content_type', 'Unknown content')
        word_count = content_analysis.get('word_count', 0)
        
        # Build fallback summary
        summary_parts = [
            f"{content_type} file: {filename}",
            f"Contains {word_count:,} words"
        ]
        
        # Add FLOAT pattern information
        patterns = []
        if content_analysis.get('has_ctx_markers'):
            patterns.append(f"{content_analysis.get('ctx_count', 0)} ctx:: markers")
        if content_analysis.get('has_highlights'):
            patterns.append(f"{content_analysis.get('highlight_count', 0)} highlights")
        if content_analysis.get('has_float_dispatch'):
            patterns.append("FLOAT dispatches")
        
        if patterns:
            summary_parts.append(f"FLOAT patterns: {', '.join(patterns)}")
        
        # Add chunk information if available
        if chunk_summaries:
            summary_parts.append(f"Processed in {len(chunk_summaries)} chunks")
            
            # Extract key themes from chunk summaries
            all_summaries = ' '.join([s['summary'] for s in chunk_summaries])
            if 'conversation' in all_summaries.lower():
                summary_parts.append("Contains conversation content")
            if 'technical' in all_summaries.lower():
                summary_parts.append("Contains technical content")
        
        fallback_summary = '. '.join(summary_parts) + '.'
        
        return {
            'summary': fallback_summary,
            'model_used': 'fallback',
            'synthesis_method': 'rule_based',
            'chunk_count': len(chunk_summaries) if chunk_summaries else 0,
            'success': False,
            'generated_at': datetime.now().isoformat(),
            'chunk_summaries': chunk_summaries or []
        }
    
    def generate_comprehensive_summary(self, content: str, file_metadata: Dict, 
                                     content_analysis: Dict, processing_hints: str = None,
                                     batch_context: Dict = None) -> Dict:
        """
        Main entry point for comprehensive summary generation.
        Handles both single-chunk and multi-chunk documents.
        
        Args:
            content: Document content to summarize
            file_metadata: File metadata dictionary
            content_analysis: Content analysis results
            processing_hints: Optional hints to guide processing (e.g., from git commit)
            batch_context: Optional batch processing context
        """
        
        print(f"🤖 Generating Ollama summary for {file_metadata.get('filename', 'unknown')}")
        
        # Step 1: Chunk the content
        chunks = self.chunk_content_for_summarization(content)
        print(f"   Split into {len(chunks)} chunks for processing")
        
        # Step 2: Generate chunk summaries
        chunk_summaries = []
        
        if len(chunks) == 1:
            # Single chunk - direct summarization
            print(f"   Processing single chunk ({len(content):,} chars)")
            chunk_summary = self.generate_chunk_summary(
                chunks[0], 0, 1, file_metadata, 
                processing_hints=processing_hints,
                batch_context=batch_context
            )
            chunk_summaries.append(chunk_summary)
            
            # For single chunks, the chunk summary IS the final summary
            final_summary = {
                'summary': chunk_summary['summary'],
                'model_used': chunk_summary['model_used'],
                'synthesis_method': 'single_chunk',
                'chunk_count': 1,
                'success': chunk_summary['success'],
                'generated_at': chunk_summary['generated_at'],
                'chunk_summaries': [chunk_summary]
            }
            
        else:
            # Multi-chunk - hierarchical summarization
            print(f"   Processing {len(chunks)} chunks hierarchically...")
            
            for i, chunk in enumerate(chunks):
                print(f"     Chunk {i+1}/{len(chunks)} ({len(chunk):,} chars)")
                chunk_summary = self.generate_chunk_summary(
                    chunk, i, len(chunks), file_metadata,
                    processing_hints=processing_hints,
                    batch_context=batch_context
                )
                chunk_summaries.append(chunk_summary)
            
            # Step 3: Synthesize final summary
            print(f"   Synthesizing final summary from {len(chunk_summaries)} chunk summaries")
            final_summary = self.synthesize_final_summary(
                chunk_summaries, file_metadata, content_analysis,
                processing_hints=processing_hints,
                batch_context=batch_context
            )
        
        # Step 4: Add processing metadata
        final_summary.update({
            'processing_stats': {
                'original_size': len(content),
                'chunk_count': len(chunks),
                'successful_chunks': sum(1 for s in chunk_summaries if s['success']),
                'processing_time': 'calculated_separately',
                'chunking_strategy': self._detect_chunking_strategy(content),
                'ollama_available': True  # We got this far
            }
        })
        
        success_rate = sum(1 for s in chunk_summaries if s['success']) / len(chunk_summaries)
        print(f"✅ Summary complete: {success_rate:.1%} success rate")
        
        return final_summary
    
    def _detect_chunking_strategy(self, content: str) -> str:
        """Detect which chunking strategy was used."""
        if self._is_conversation_content(content):
            return 'conversation_aware'
        elif self._has_document_structure(content):
            return 'document_structure'
        else:
            return 'semantic_fallback'

# Integration with the dropzone daemon
class OllamaEnhancedDropzoneHandler:
    """
    Enhanced dropzone handler with Ollama summarization.
    """
    
    def __init__(self, *args, **kwargs):
        # Extract Ollama settings
        ollama_settings = {
            'ollama_url': kwargs.pop('ollama_url', 'http://localhost:11434'),
            'model': kwargs.pop('ollama_model', 'llama3.1:8b'),
            'chunk_model': kwargs.pop('ollama_chunk_model', 'llama3.1:8b'),
            'final_model': kwargs.pop('ollama_final_model', 'llama3.1:8b')
        }
        
        # Initialize parent class
        super().__init__(*args, **kwargs)
        
        # Initialize Ollama summarizer
        self.summarizer = OllamaFloatSummarizer(**ollama_settings)
        
    def enhanced_content_analysis_with_ollama(self, content: str, file_metadata: Dict) -> Dict:
        """
        Enhanced content analysis that includes Ollama-generated summaries.
        """
        
        # Start with basic analysis
        analysis = self.enhanced_content_analysis(content, file_metadata)  # From parent class
        
        # Generate Ollama summary
        start_time = datetime.now()
        
        try:
            ollama_summary = self.summarizer.generate_comprehensive_summary(
                content, file_metadata, analysis
            )
            
            processing_time = (datetime.now() - start_time).total_seconds()
            ollama_summary['processing_stats']['processing_time'] = f"{processing_time:.1f}s"
            
            # Integrate Ollama summary into analysis
            analysis.update({
                'summary': ollama_summary['summary'],
                'ollama_summary_data': ollama_summary,
                'summary_method': 'ollama_enhanced',
                'summary_success': ollama_summary['success']
            })
            
            print(f"   🤖 Ollama summary: {len(ollama_summary['summary'])} chars in {processing_time:.1f}s")
            
        except Exception as e:
            print(f"   ⚠️ Ollama summary failed: {e}")
            analysis['summary_method'] = 'fallback_only'
            analysis['summary_success'] = False
            analysis['ollama_error'] = str(e)
        
        return analysis

# Usage example and CLI enhancement
if __name__ == "__main__":
    # Test the Ollama summarizer
    summarizer = OllamaFloatSummarizer()
    
    # Test content
    test_content = '''
    # Test Conversation Export
    
    ## HUMAN
    ctx:: 2025-06-08 - exploring nushell data processing
    
    Can you help me understand how to process this JSON data with nushell?
    
    highlight:: nushell is particularly good at structured data manipulation
    
    ## ASSISTANT
    
    Absolutely! Nushell excels at JSON processing. Here's how you can work with your data:
    
    ```nu
    open data.json | select name age | where age > 25
    ```
    
    This demonstrates nushell's pipeline approach to data transformation.
    
    ## HUMAN
    
    That's exactly what I needed! Can you show me more complex transformations?
    
    float.dispatch({
      topic: "nushell advanced patterns",
      context: "data processing pipeline design"
    })
    '''
    
    file_metadata = {
        'filename': 'test_nushell_conversation.json',
        'extension': '.json',
        'file_type': 'JSON conversation export',
        'mime_type': 'application/json',
        'size_bytes': len(test_content)
    }
    
    content_analysis = {
        'content_type': 'AI conversation export',
        'word_count': len(test_content.split()),
        'line_count': len(test_content.split('\n')),
        'has_ctx_markers': True,
        'has_highlights': True,
        'has_float_dispatch': True,
        'ctx_count': 1,
        'highlight_count': 1
    }