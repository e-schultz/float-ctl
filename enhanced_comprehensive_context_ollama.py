"""
Enhanced Comprehensive Daily Context with Ollama Integration
Generates .float_dis.md files for conversations and uses Ollama for intelligent summarization
"""

import json
import re
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import chromadb
from ollama_enhanced_float_summarizer import OllamaFloatSummarizer
from float_dis_template_system import FloatDisGenerator

class EnhancedComprehensiveDailyContext:
    """
    Enhanced version that:
    1. Uses Ollama for intelligent summarization
    2. Generates .float_dis.md files for conversations
    3. Creates conversation indexes in vault
    4. Provides rich cross-referencing
    """
    
    def __init__(self, 
                 vault_path: str = "/Users/evan/vault",
                 data_path: str = "/Users/evan/github/chroma-data",
                 collection_base: str = "float_tripartite_v2",
                 enable_ollama: bool = True,
                 conversation_dis_path: str = None):
        
        self.vault_path = Path(vault_path)
        self.data_path = data_path
        self.collection_base = collection_base
        self.client = chromadb.PersistentClient(path=data_path)
        
        # Set up conversation .dis file storage
        if conversation_dis_path:
            self.conversation_dis_path = Path(conversation_dis_path)
        else:
            self.conversation_dis_path = self.vault_path / "FLOAT.conversations"
        
        self.conversation_dis_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize Ollama summarizer
        if enable_ollama:
            try:
                self.summarizer = OllamaFloatSummarizer()
                self.ollama_enabled = True
                print("🤖 Ollama summarization enabled")
            except Exception as e:
                print(f"⚠️ Ollama not available: {e}")
                self.summarizer = None
                self.ollama_enabled = False
        else:
            self.summarizer = None
            self.ollama_enabled = False
        
        # Initialize .dis generator
        self.dis_generator = FloatDisGenerator()
        
        print(f"🏠 Vault: {self.vault_path}")
        print(f"💬 Conversation .dis files: {self.conversation_dis_path}")
        print(f"🧠 Ollama: {'Enabled' if self.ollama_enabled else 'Disabled'}")
    
    def get_conversation_summaries_for_date_enhanced(self, target_date: str) -> List[Dict]:
        """
        Enhanced conversation summaries that include Ollama-generated insights.
        """
        
        conversations = {}
        
        # Query all tripartite collections for the date
        for domain in ['concept', 'framework', 'metaphor']:
            collection_name = f"{self.collection_base}_{domain}"
            
            try:
                collection = self.client.get_collection(name=collection_name)
                
                results = collection.get(
                    where={"conversation_date": target_date},
                    include=['documents', 'metadatas'],
                    limit=100  # Higher limit for comprehensive analysis
                )
                
                # Group by conversation_id and collect all chunks
                for doc, metadata in zip(results['documents'], results['metadatas']):
                    conv_id = metadata.get('conversation_id')
                    if not conv_id:
                        continue
                        
                    if conv_id not in conversations:
                        conversations[conv_id] = {
                            'conversation_id': conv_id,
                            'title': metadata.get('conversation_title', 'Untitled'),
                            'signal_count': 0,
                            'domains': set(),
                            'chunk_count': 0,
                            'all_content': [],
                            'created_at': metadata.get('created_at', ''),
                            'source': metadata.get('source', 'unknown')
                        }
                    
                    conversations[conv_id]['domains'].add(domain)
                    conversations[conv_id]['signal_count'] += metadata.get('signal_count', 0)
                    conversations[conv_id]['chunk_count'] += 1
                    conversations[conv_id]['all_content'].append(doc)
                        
            except Exception as e:
                print(f"⚠️ Error querying {collection_name}: {e}")
        
        # Process conversations with Ollama summaries
        enhanced_conversations = []
        
        for conv_data in conversations.values():
            conv_data['domains'] = list(conv_data['domains'])
            
            # Combine all chunks for full conversation content
            full_content = '\n\n---\n\n'.join(conv_data['all_content'])
            conv_data['full_content'] = full_content
            conv_data['content_length'] = len(full_content)
            
            # Generate enhanced summary with Ollama
            if self.ollama_enabled and full_content:
                enhanced_summary = self._generate_conversation_summary_ollama(conv_data)
                conv_data['ollama_summary'] = enhanced_summary
                conv_data['summary'] = enhanced_summary.get('summary', self._fallback_summary(conv_data))
            else:
                conv_data['summary'] = self._fallback_summary(conv_data)
            
            # Generate .float_dis.md file for this conversation
            self._generate_conversation_dis_file(conv_data, target_date)
            
            # Clean up for return (remove full content to save memory)
            del conv_data['all_content']
            del conv_data['full_content']
            
            enhanced_conversations.append(conv_data)
        
        # Sort by signal count (highest first)
        enhanced_conversations.sort(key=lambda x: x['signal_count'], reverse=True)
        
        return enhanced_conversations
    
    def _generate_conversation_summary_ollama(self, conv_data: Dict) -> Dict:
        """
        Generate intelligent conversation summary using Ollama.
        """
        
        if not self.summarizer:
            return {'error': 'Ollama not available'}
        
        # Prepare metadata for summarizer
        file_metadata = {
            'filename': f"{conv_data['title']}.json",
            'extension': '.json',
            'file_type': 'Conversation export',
            'mime_type': 'application/json',
            'size_bytes': conv_data['content_length']
        }
        
        content_analysis = {
            'content_type': 'AI conversation export',
            'word_count': len(conv_data['full_content'].split()),
            'line_count': len(conv_data['full_content'].split('\n')),
            'signal_count': conv_data['signal_count'],
            'domains': conv_data['domains'],
            'chunk_count': conv_data['chunk_count']
        }
        
        try:
            return self.summarizer.generate_comprehensive_summary(
                conv_data['full_content'], 
                file_metadata, 
                content_analysis
            )
        except Exception as e:
            print(f"⚠️ Ollama summary failed for {conv_data['conversation_id']}: {e}")
            return {'error': str(e)}
    
    def _fallback_summary(self, conv_data: Dict) -> str:
        """Fallback summary when Ollama is not available."""
        return f"{conv_data['title']} - {conv_data['chunk_count']} chunks, {conv_data['signal_count']} signals, domains: {', '.join(conv_data['domains'])}"
    
    def _generate_conversation_dis_file(self, conv_data: Dict, date: str):
        """
        Generate .float_dis.md file for a conversation.
        """
        
        try:
            # Create safe filename from conversation title
            safe_title = re.sub(r'[^\w\s-]', '', conv_data['title'])
            safe_title = re.sub(r'[-\s]+', '-', safe_title)
            
            # Create unique filename
            conv_id_short = conv_data['conversation_id'][:8]
            filename = f"{date}_{conv_id_short}_{safe_title}.float_dis.md"
            dis_file_path = self.conversation_dis_path / filename
            
            # Prepare metadata for .dis generator
            file_metadata = {
                'filename': f"{conv_data['title']}.conversation",
                'extension': '.conversation',
                'file_type': 'AI Conversation Export',
                'mime_type': 'application/conversation',
                'size_bytes': conv_data['content_length'],
                'created_at': conv_data.get('created_at', ''),
                'modified_at': conv_data.get('created_at', ''),
                'relative_path': f"conversations/{filename}"
            }
            
            chroma_metadata = {
                'collection_name': f"{self.collection_base}_*",
                'chunk_count': conv_data['chunk_count'],
                'total_chunks': conv_data['chunk_count'],
                'chunk_ids': [f"{conv_data['conversation_id']}_chunk_{i}" for i in range(conv_data['chunk_count'])],
                'embedding_model': 'default',
                'storage_path': self.data_path
            }
            
            content_analysis = {
                'summary': conv_data['summary'],
                'word_count': len(conv_data.get('full_content', '').split()) if 'full_content' in conv_data else 0,
                'content_type': 'AI conversation export',
                'signal_count': conv_data['signal_count'],
                'domains': conv_data['domains'],
                'conversation_id': conv_data['conversation_id'],
                'source_platform': conv_data.get('source', 'unknown'),
                'has_ollama_summary': 'ollama_summary' in conv_data,
                'processing_date': date
            }
            
            # Generate .dis content
            dis_content = self.dis_generator.generate_float_dis(
                file_metadata, chroma_metadata, content_analysis, 
                f"conv_{conv_data['conversation_id'][:12]}"
            )
            
            # Add conversation-specific enhancements to the template
            enhanced_dis_content = self._enhance_conversation_dis_content(
                dis_content, conv_data, date
            )
            
            # Write .dis file
            with open(dis_file_path, 'w', encoding='utf-8') as f:
                f.write(enhanced_dis_content)
            
            print(f"   📝 Generated conversation .dis: {filename}")
            
            return dis_file_path
            
        except Exception as e:
            print(f"⚠️ Failed to generate conversation .dis file: {e}")
            return None
    
    def _enhance_conversation_dis_content(self, base_content: str, conv_data: Dict, date: str) -> str:
        """
        Add conversation-specific enhancements to the .dis file content.
        """
        
        # Add conversation-specific sections
        conversation_enhancements = f"""

## 💬 Conversation Details

### Platform Information
- **Source**: {conv_data.get('source', 'Unknown').title()}
- **Conversation ID**: `{conv_data['conversation_id']}`
- **Date**: {date}
- **Signal Density**: {conv_data['signal_count'] / max(conv_data['chunk_count'], 1):.2f} signals/chunk

### Domain Distribution
{chr(10).join([f"- **{domain.title()}**: Present" for domain in conv_data['domains']])}

### Related Daily Notes
```dataview
LIST
FROM "FLOAT.logs"
WHERE contains(file.content, "{conv_data['conversation_id']}")
OR contains(file.content, "{conv_data['title']}")
SORT file.mtime DESC
LIMIT 5
```

### Query This Conversation
```js
// Search this specific conversation
collection.query({{
    query_texts: ["your search term"],
    where: {{"conversation_id": "{conv_data['conversation_id']}"}},
    n_results: 10
}})
```

### Cross-References
```dataview
TABLE WITHOUT ID
  file.link as "Related Files",
  length(file.outlinks) as "Links"
FROM ""
WHERE contains(file.content, "{conv_data['conversation_id'][:8]}")
AND file.name != this.file.name
SORT file.mtime DESC
LIMIT 10
```

## 🔗 Conversation Actions

### Quick Links
- 🔍 **Search in Vault**: [[{conv_data['title']}]]
- 📅 **Daily Log**: [[FLOAT.logs/{date}]]
- 🗂️ **All Conversations**: [[FLOAT.conversations/]]

### Export Conversation
```js
// Export full conversation data
const conversationData = {{
    id: "{conv_data['conversation_id']}",
    title: "{conv_data['title']}",
    date: "{date}",
    domains: {json.dumps(conv_data['domains'])},
    signalCount: {conv_data['signal_count']},
    chunkCount: {conv_data['chunk_count']}
}};

navigator.clipboard.writeText(JSON.stringify(conversationData, null, 2));
```

---

*Generated from tripartite collection analysis on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        # Insert conversation enhancements before the final footer
        enhanced_content = base_content.replace(
            '<div style="background: #f0f0f0',
            conversation_enhancements + '\n<div style="background: #f0f0f0'
        )
        
        return enhanced_content
    
    def create_comprehensive_daily_summary_enhanced(self, target_date: str) -> Dict:
        """
        Enhanced comprehensive daily summary with Ollama integration and conversation .dis generation.
        """
        
        print(f"📅 Creating enhanced daily summary for {target_date}...")
        
        # Get enhanced conversation summaries (includes .dis generation)
        conversations = self.get_conversation_summaries_for_date_enhanced(target_date)
        
        # Get vault activity
        vault_activity = self.get_vault_activity_for_date(target_date)
        
        # Get daily note content
        daily_content = self.extract_daily_note_content(target_date)
        
        # Cross-reference conversations with daily notes
        cross_reference_data = self.cross_reference_conversations_with_notes(conversations, daily_content)
        
        # Generate comprehensive daily summary with Ollama
        daily_summary_ollama = self._generate_daily_summary_ollama(
            target_date, conversations, vault_activity, daily_content, cross_reference_data
        )
        
        # Create comprehensive summary structure
        summary = {
            'date': target_date,
            'day_of_week': datetime.strptime(target_date, '%Y-%m-%d').strftime('%A'),
            
            # Enhanced metrics
            'metrics': {
                'conversation_count': len(conversations),
                'total_signal_count': sum(conv['signal_count'] for conv in conversations),
                'vault_files_touched': vault_activity.get('total_files', 0),
                'daily_notes_found': len(daily_content.get('found_notes', [])),
                'conversation_dis_generated': len([c for c in conversations if 'ollama_summary' in c]),
                'ollama_success_rate': len([c for c in conversations if c.get('ollama_summary', {}).get('success', False)]) / max(len(conversations), 1)
            },
            
            # Enhanced conversations with .dis files
            'conversations': {
                'high_signal': [conv for conv in conversations if conv['signal_count'] > 2],
                'with_summaries': [conv for conv in conversations if 'ollama_summary' in conv],
                'primary_domains': self._get_primary_domains(conversations),
                'key_topics': [conv['title'] for conv in conversations[:5]]
            },
            
            'vault_activity': vault_activity,
            'daily_notes': daily_content,
            'cross_references': cross_reference_data,
            
            # Ollama-generated daily summary
            'ollama_daily_summary': daily_summary_ollama,
            'summary_text': daily_summary_ollama.get('summary', self._generate_fallback_daily_summary(target_date, conversations, vault_activity))
        }
        
        return summary
    
    def _generate_daily_summary_ollama(self, date: str, conversations: List[Dict], 
                                     vault_activity: Dict, daily_content: Dict, 
                                     cross_reference_data: Dict) -> Dict:
        """
        Generate intelligent daily summary using Ollama.
        """
        
        if not self.ollama_enabled:
            return {'error': 'Ollama not available'}
        
        # Prepare context for Ollama
        context_text = self._prepare_daily_context_for_ollama(
            date, conversations, vault_activity, daily_content, cross_reference_data
        )
        
        system_prompt = """You are creating a comprehensive daily summary for a FLOAT knowledge management system. 

Analyze the day's activities and create a summary that captures:
1. Key themes and patterns across conversations and vault activity
2. FLOAT methodology usage (ctx::, highlights, dispatches, ritual patterns)
3. Knowledge flow between conversations, notes, and vault files
4. Insights about workflow, productivity, and cognitive patterns
5. Notable connections and cross-references

Focus on what makes this day significant for future reference and pattern recognition. Be concise but insightful."""

        user_prompt = f"""Analyze this day's activities and create a comprehensive summary:

DATE: {date}

{context_text}

Create a daily summary that captures:
- Overall day themes and energy
- Key conversations and their significance  
- FLOAT pattern usage and ritual elements
- Knowledge management workflow insights
- Cross-system integration observations
- Notable patterns or breakthroughs

Summary:"""

        try:
            import requests
            
            response = requests.post(
                f"{self.summarizer.ollama_url}/api/generate",
                json={
                    "model": self.summarizer.final_model,
                    "prompt": f"<|im_start|>system\n{system_prompt}<|im_end|>\n<|im_start|>user\n{user_prompt}<|im_end|>\n<|im_start|>assistant\n",
                    "stream": False,
                    "options": {
                        "temperature": 0.4,
                        "top_p": 0.9,
                        "max_tokens": 500
                    }
                },
                timeout=90
            )
            
            if response.status_code == 200:
                result = response.json()
                summary_text = result.get('response', '').strip()
                
                return {
                    'summary': summary_text,
                    'model_used': self.summarizer.final_model,
                    'success': True,
                    'generated_at': datetime.now().isoformat()
                }
            else:
                print(f"⚠️ Ollama daily summary error: {response.status_code}")
                return self._fallback_daily_summary_ollama(date, conversations, vault_activity)
                
        except Exception as e:
            print(f"⚠️ Failed to generate daily summary with Ollama: {e}")
            return self._fallback_daily_summary_ollama(date, conversations, vault_activity)
    
    def _prepare_daily_context_for_ollama(self, date: str, conversations: List[Dict], 
                                        vault_activity: Dict, daily_content: Dict, 
                                        cross_reference_data: Dict) -> str:
        """
        Prepare comprehensive context text for Ollama daily summary generation.
        """
        
        context_parts = []
        
        # Conversation summaries
        if conversations:
            context_parts.append("CONVERSATIONS:")
            for conv in conversations[:5]:  # Top 5 conversations
                summary = conv.get('summary', conv['title'])[:200]
                context_parts.append(f"- {conv['title']} ({conv['signal_count']} signals): {summary}")
        
        # Vault activity
        if vault_activity.get('total_files', 0) > 0:
            context_parts.append("\nVAULT ACTIVITY:")
            context_parts.append(f"- Files touched: {vault_activity['total_files']}")
            if vault_activity.get('created_files'):
                created = [f['name'] for f in vault_activity['created_files'][:3]]
                context_parts.append(f"- Created: {', '.join(created)}")
            if vault_activity.get('modified_files'):
                modified = [f['name'] for f in vault_activity['modified_files'][:3]]
                context_parts.append(f"- Modified: {', '.join(modified)}")
        
        # Daily notes content
        if daily_content.get('found_notes'):
            context_parts.append("\nDAILY NOTES:")
            for note in daily_content['found_notes'][:2]:
                content_preview = note.get('content', '')[:300]
                context_parts.append(f"- {note['name']}: {content_preview}")
        
        # Cross-references
        if cross_reference_data.get('matched_conversations'):
            context_parts.append(f"\nINTEGRATION: {len(cross_reference_data['matched_conversations'])} conversations linked in vault notes")
        
        return '\n'.join(context_parts)
    
    def _fallback_daily_summary_ollama(self, date: str, conversations: List[Dict], vault_activity: Dict) -> Dict:
        """Fallback when Ollama daily summary fails."""
        
        summary = f"{date}: {len(conversations)} conversations, {sum(c['signal_count'] for c in conversations)} total signals"
        if vault_activity.get('total_files', 0) > 0:
            summary += f", {vault_activity['total_files']} vault files touched"
        
        return {
            'summary': summary,
            'model_used': 'fallback',
            'success': False,
            'generated_at': datetime.now().isoformat()
        }
    
    def _generate_fallback_daily_summary(self, date: str, conversations: List[Dict], vault_activity: Dict) -> str:
        """Generate fallback daily summary text."""
        
        summary_parts = [f"{date}"]
        
        if conversations:
            summary_parts.append(f"{len(conversations)} conversations")
            total_signals = sum(c['signal_count'] for c in conversations)
            if total_signals > 0:
                summary_parts.append(f"{total_signals} signals")
        
        if vault_activity.get('total_files', 0) > 0:
            summary_parts.append(f"{vault_activity['total_files']} vault files")
        
        return " - ".join(summary_parts) + "."
    
    def _get_primary_domains(self, conversations: List[Dict]) -> List[str]:
        """Get primary tripartite domains for conversations."""
        domain_counts = {}
        for conv in conversations:
            for domain in conv['domains']:
                domain_counts[domain] = domain_counts.get(domain, 0) + 1
        
        return sorted(domain_counts.keys(), key=lambda x: domain_counts[x], reverse=True)
    
    def get_vault_activity_for_date(self, date_str: str) -> Dict:
        """Get vault activity for a specific date (simplified version)"""
        try:
            return {
                'date': date_str,
                'notes_created': 0,
                'notes_modified': 0,
                'total_activity': 0
            }
        except Exception as e:
            self.logger.warning(f"Failed to get vault activity for {date_str}: {e}")
            return {'date': date_str, 'total_activity': 0}
    
    # Include all other methods from the original ComprehensiveDailyContext
    # (extract_daily_note_content, etc.)
    # These remain the same but now work with the enhanced system

# Usage example
if __name__ == "__main__":
    # Test enhanced system
    enhanced_context = EnhancedComprehensiveDailyContext(
        vault_path="/Users/evan/vault",
        enable_ollama=True
    )
    
    # Generate enhanced daily summary with conversation .dis files
    test_date = "2025-06-01"
    enhanced_summary = enhanced_context.create_comprehensive_daily_summary_enhanced(test_date)
    
    print("\n" + "="*60)
    print(f"ENHANCED DAILY SUMMARY: {test_date}")
    print("="*60)
    print(enhanced_summary['summary_text'])
    print(f"\nConversation .dis files generated: {enhanced_summary['metrics']['conversation_dis_generated']}")
    print(f"Ollama success rate: {enhanced_summary['metrics']['ollama_success_rate']:.1%}")
