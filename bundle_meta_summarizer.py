"""
Bundle Meta Summarizer
Generates meta-level summaries for batches of processed files
Treats bundles as conceptual wholes with cross-document synthesis
"""

from datetime import datetime
from typing import Dict, List, Optional
import hashlib
import requests

class BundleMetaSummarizer:
    """
    Creates meta-summaries for bundles of documents processed together.
    Synthesizes themes, connections, and evolution across documents.
    """
    
    def __init__(self, ollama_summarizer=None):
        """
        Initialize with optional Ollama summarizer for AI-powered synthesis.
        
        Args:
            ollama_summarizer: OllamaFloatSummarizer instance for AI summaries
        """
        self.ollama_summarizer = ollama_summarizer
        self.has_ollama = ollama_summarizer is not None
        
    def generate_bundle_summary(self, batch_results: List[Dict], 
                              batch_context: Dict, 
                              processing_hints: str = None) -> str:
        """
        Generate a comprehensive meta-summary for the entire bundle.
        
        Args:
            batch_results: List of processing results from individual files
            batch_context: Context about the batch (type, bundle, domain, etc.)
            processing_hints: Processing hints from git commit message
            
        Returns:
            Markdown-formatted bundle meta-summary
        """
        
        # Generate bundle ID
        bundle_id = self._generate_bundle_id(batch_context)
        
        # Extract successful results
        successful_results = [r for r in batch_results if not r.get('error')]
        failed_results = [r for r in batch_results if r.get('error')]
        
        # Generate meta-summary using Ollama if available
        if self.has_ollama and successful_results:
            ollama_meta = self._generate_ollama_meta_summary(
                successful_results, batch_context, processing_hints
            )
        else:
            ollama_meta = None
        
        # Build the bundle summary document
        summary = self._build_bundle_document(
            bundle_id=bundle_id,
            batch_context=batch_context,
            successful_results=successful_results,
            failed_results=failed_results,
            processing_hints=processing_hints,
            ollama_meta=ollama_meta
        )
        
        return summary
    
    def _generate_bundle_id(self, batch_context: Dict) -> str:
        """Generate unique bundle ID based on timestamp and context."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        context_str = f"{batch_context.get('type', 'unknown')}_{batch_context.get('domain', 'unknown')}"
        context_hash = hashlib.md5(context_str.encode()).hexdigest()[:8]
        return f"bundle_{timestamp}_{context_hash}"
    
    def _generate_ollama_meta_summary(self, successful_results: List[Dict],
                                    batch_context: Dict,
                                    processing_hints: str) -> Optional[Dict]:
        """Generate AI-powered meta-summary across all documents."""
        
        if not self.ollama_summarizer:
            return None
        
        # Collect all individual summaries
        summaries = []
        for i, result in enumerate(successful_results):
            summary = result.get('summary', 'No summary available')
            filename = result.get('filename', f'Document {i+1}')
            summaries.append(f"### {filename}\n{summary}")
        
        combined_summaries = "\n\n".join(summaries)
        
        # Build system prompt for meta-summarization
        system_prompt = f"""You are synthesizing multiple document summaries into a unified bundle analysis.

This bundle represents: {batch_context.get('domain', 'unknown domain')}
Bundle type: {batch_context.get('type', 'mixed')}
Processing focus: {processing_hints or 'General analysis'}

Your task:
1. Identify cross-document themes and patterns
2. Trace the evolution of ideas across documents
3. Highlight connections and relationships
4. Synthesize insights that emerge from the bundle as a whole
5. Focus especially on: {processing_hints}

Create a cohesive narrative that treats these documents as a conceptual unit."""

        user_prompt = f"""Synthesize these {len(successful_results)} document summaries into a unified bundle analysis:

{combined_summaries}

Generate a meta-analysis that captures:
- Common themes across all documents
- Evolution and progression of ideas
- Key insights that emerge from the collection
- Connections and cross-references between documents
- Overall value of this bundle as a knowledge unit
- Specific findings related to: {processing_hints}"""

        try:
            response = requests.post(
                f"{self.ollama_summarizer.ollama_url}/api/generate",
                json={
                    "model": self.ollama_summarizer.final_model,
                    "prompt": f"<|im_start|>system\n{system_prompt}<|im_end|>\n<|im_start|>user\n{user_prompt}<|im_end|>\n<|im_start|>assistant\n",
                    "stream": False,
                    "options": {
                        "temperature": 0.5,
                        "top_p": 0.9,
                        "max_tokens": 800
                    }
                },
                timeout=120
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    'meta_summary': result.get('response', '').strip(),
                    'success': True,
                    'model_used': self.ollama_summarizer.final_model
                }
        except Exception as e:
            print(f"⚠️ Ollama meta-summary failed: {e}")
        
        return None
    
    def _build_bundle_document(self, bundle_id: str, batch_context: Dict,
                             successful_results: List[Dict],
                             failed_results: List[Dict],
                             processing_hints: str,
                             ollama_meta: Optional[Dict]) -> str:
        """Build the complete bundle summary document."""
        
        # Calculate bundle statistics
        total_size = sum(r.get('file_analysis', {}).get('metadata', {}).get('size_bytes', 0) 
                        for r in successful_results)
        total_size_mb = total_size / (1024 * 1024)
        
        # Build frontmatter
        frontmatter = f"""---
bundle_id: {bundle_id}
bundle_type: git_batch
processing_hints: "{processing_hints or 'None provided'}"
file_count: {len(successful_results)}
failed_count: {len(failed_results)}
total_size: {total_size_mb:.1f}MB
processing_date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
domain: {batch_context.get('domain', 'unknown')}
type: {batch_context.get('type', 'mixed')}
bundle: {batch_context.get('bundle', 'merge')}
---

# Bundle Summary: {batch_context.get('domain', 'Processing Bundle')}

## Processing Focus
{processing_hints or 'General analysis - no specific focus provided'}

## Bundle Overview
- **Files Processed**: {len(successful_results)}
- **Total Size**: {total_size_mb:.1f}MB
- **Domain**: {batch_context.get('domain', 'unknown')}
- **Bundle Type**: {batch_context.get('type', 'mixed')}
- **Bundle Approach**: {batch_context.get('bundle', 'merge')}
"""

        # Add AI meta-summary if available
        if ollama_meta and ollama_meta.get('success'):
            frontmatter += f"""
## Cross-Document Synthesis

{ollama_meta['meta_summary']}
"""
        
        # Add individual document summaries
        frontmatter += "\n## Individual Document Summaries\n"
        
        for i, result in enumerate(successful_results):
            float_id = result.get('float_id', 'unknown')
            filename = result.get('filename', f'Document {i+1}')
            summary = result.get('summary', 'No summary available')
            
            # Extract key metrics
            analysis = result.get('file_analysis', {}).get('analysis', {})
            word_count = analysis.get('word_count', 0)
            content_type = analysis.get('content_type', 'unknown')
            
            frontmatter += f"""
### {i+1}. {filename}
- **Float ID**: `{float_id}`
- **Type**: {content_type}
- **Size**: {word_count:,} words

{summary}
"""
        
        # Add failed files section if any
        if failed_results:
            frontmatter += "\n## Failed Processing\n"
            for result in failed_results:
                frontmatter += f"- {result.get('file', 'Unknown')}: {result.get('error', 'Unknown error')}\n"
        
        # Add insights section based on processing hints
        if processing_hints and ollama_meta:
            frontmatter += f"""
## Insights Following Processing Hints

Based on "{processing_hints}":

*This section synthesizes findings specifically related to the processing focus across all documents in the bundle.*
"""
        
        # Add metadata footer
        frontmatter += f"""
---

<div style="background: #f0f0f0; padding: 10px; border-radius: 5px; margin-top: 20px;">
<small>
🎯 <strong>Bundle Meta-Summary</strong><br>
📚 Bundle ID: <code>{bundle_id}</code><br>
📅 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br>
🤖 AI Synthesis: {'Enabled' if ollama_meta else 'Not available'}<br>
📝 Processing Hints: {processing_hints or 'None'}
</small>
</div>
"""
        
        return frontmatter


if __name__ == "__main__":
    # Test the bundle meta summarizer
    print("Bundle Meta Summarizer - Test Mode")
    
    # Mock data for testing
    test_results = [
        {
            'float_id': 'float_20250618_test1',
            'filename': 'test_doc1.md',
            'summary': 'This document discusses FLOAT patterns and resilience.',
            'file_analysis': {
                'metadata': {'size_bytes': 1024000},
                'analysis': {'word_count': 500, 'content_type': 'Markdown document'}
            }
        },
        {
            'float_id': 'float_20250618_test2',
            'filename': 'test_doc2.pdf',
            'summary': 'Technical implementation of remember forward concept.',
            'file_analysis': {
                'metadata': {'size_bytes': 2048000},
                'analysis': {'word_count': 1000, 'content_type': 'PDF document'}
            }
        }
    ]
    
    test_context = {
        'type': 'mixed',
        'bundle': 'merge',
        'domain': 'AI/ecosystem',
        'total_files': 2
    }
    
    summarizer = BundleMetaSummarizer()
    result = summarizer.generate_bundle_summary(
        test_results, 
        test_context,
        "focus on resilience patterns and remember forward concept"
    )
    
    print("\n" + "="*60)
    print(result)