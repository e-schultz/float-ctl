"""
Cross-reference system for FLOAT ecosystem
Generates and maintains cross-references between vault, Chroma, and processed files
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from datetime import datetime
from collections import defaultdict, Counter
import hashlib

class CrossReferenceSystem:
    """Generate and maintain cross-references between FLOAT systems"""
    
    def __init__(self, vault_path: Path, chroma_client, config: Dict, logger=None):
        self.vault_path = vault_path
        self.chroma_client = chroma_client
        self.config = config
        self.logger = logger
        
        # Cross-reference storage
        self.cross_ref_cache = {}
        self.reference_index = defaultdict(list)
        
        # Reference directories
        self.reference_dir = vault_path / "FLOAT.references"
        self.reference_dir.mkdir(exist_ok=True)
        
        self.link_index_file = self.reference_dir / "link_index.json"
        
        # Initialize reference patterns
        self._initialize_reference_patterns()
        
        # Load existing reference index
        self._load_reference_index()
    
    def _initialize_reference_patterns(self):
        """Initialize patterns for detecting references"""
        self.reference_patterns = {
            # Obsidian-style links
            'obsidian_link': re.compile(r'\[\[([^\]]+)\]\]'),
            'markdown_link': re.compile(r'\[([^\]]+)\]\(([^)]+)\)'),
            
            # FLOAT patterns
            'float_id': re.compile(r'float_\d{8}_\d{6}_[a-f0-9]{8}'),
            'conversation_id': re.compile(r'conversation[_-]?([a-zA-Z0-9_-]+)', re.IGNORECASE),
            
            # Topic and concept references
            'hashtag': re.compile(r'#(\w+)'),
            'concept_ref': re.compile(r'concept::([^:]+)', re.IGNORECASE),
            'framework_ref': re.compile(r'framework::([^:]+)', re.IGNORECASE),
            'metaphor_ref': re.compile(r'metaphor::([^:]+)', re.IGNORECASE),
            
            # Date references
            'date_ref': re.compile(r'\b(\d{4}-\d{2}-\d{2})\b'),
            
            # External links
            'url': re.compile(r'https?://[^\s<>"]+'),
            
            # FLOAT signals
            'ctx_signal': re.compile(r'ctx::([^:]+)', re.IGNORECASE),
            'highlight_signal': re.compile(r'highlight::([^:]+)', re.IGNORECASE)
        }
    
    def _load_reference_index(self):
        """Load existing reference index from disk"""
        try:
            if self.link_index_file.exists():
                with open(self.link_index_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.reference_index = defaultdict(list, data.get('references', {}))
                    self.cross_ref_cache = data.get('cache', {})
                if self.logger:
                    self.logger.info(f"Loaded reference index with {len(self.reference_index)} entries")
        except Exception as e:
            if self.logger:
                self.logger.warning(f"Failed to load reference index: {e}")
    
    def _save_reference_index(self):
        """Save reference index to disk"""
        try:
            index_data = {
                'references': dict(self.reference_index),
                'cache': self.cross_ref_cache,
                'last_updated': datetime.now().isoformat(),
                'version': '1.0'
            }
            
            with open(self.link_index_file, 'w', encoding='utf-8') as f:
                json.dump(index_data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to save reference index: {e}")
    
    def generate_cross_references(self, file_analysis: Dict, enhanced_analysis: Dict = None) -> Dict:
        """Generate comprehensive cross-references for processed file"""
        
        cross_refs = {
            'vault_references': [],
            'chroma_references': [],
            'conversation_links': [],
            'topic_connections': [],
            'signal_references': [],
            'temporal_links': [],
            'external_links': []
        }
        
        content = file_analysis.get('content', '')
        if not content:
            return cross_refs
        
        float_id = file_analysis.get('float_id')
        metadata = file_analysis.get('metadata', {})
        
        # Extract all reference types
        cross_refs['vault_references'] = self._find_vault_references(content, float_id)
        cross_refs['chroma_references'] = self._find_chroma_references(file_analysis, enhanced_analysis)
        cross_refs['conversation_links'] = self._extract_conversation_links(content)
        cross_refs['topic_connections'] = self._find_topic_connections(content, enhanced_analysis)
        cross_refs['signal_references'] = self._extract_signal_references(content)
        cross_refs['temporal_links'] = self._find_temporal_links(content)
        cross_refs['external_links'] = self._extract_external_links(content)
        
        # Update vault files with bidirectional references
        self._update_vault_references(file_analysis, cross_refs)
        
        # Update reference index
        self._update_reference_index(float_id, cross_refs, metadata)
        
        # Cache results
        self.cross_ref_cache[float_id] = cross_refs
        
        return cross_refs
    
    def _find_vault_references(self, content: str, float_id: str) -> List[Dict]:
        """Find references to vault files"""
        references = []
        
        # Extract Obsidian-style links
        obsidian_links = self.reference_patterns['obsidian_link'].findall(content)
        for link in obsidian_links:
            # Clean up link text
            link_parts = link.split('|')
            note_name = link_parts[0].strip()
            display_text = link_parts[1].strip() if len(link_parts) > 1 else note_name
            
            references.append({
                'type': 'obsidian_link',
                'target': note_name,
                'display_text': display_text,
                'exists': self._check_vault_file_exists(note_name)
            })
        
        # Extract markdown links to local files
        markdown_links = self.reference_patterns['markdown_link'].findall(content)
        for text, url in markdown_links:
            if not url.startswith('http') and not url.startswith('/'):
                references.append({
                    'type': 'markdown_link',
                    'target': url,
                    'display_text': text,
                    'exists': self._check_vault_file_exists(url)
                })
        
        # Find topic-based references using key terms
        key_terms = self._extract_key_terms(content)
        for term in key_terms[:10]:  # Limit to top 10 terms
            vault_matches = self._search_vault_for_term(term)
            references.extend(vault_matches)
        
        return self._deduplicate_references(references)
    
    def _find_chroma_references(self, file_analysis: Dict, enhanced_analysis: Dict = None) -> List[Dict]:
        """Find references to ChromaDB collections and documents"""
        references = []
        
        # Direct collection references from tripartite routing
        if enhanced_analysis and enhanced_analysis.get('tripartite_routing'):
            for collection_type in enhanced_analysis['tripartite_routing']:
                collection_name = self.config.get('tripartite_collections', {}).get(
                    collection_type, f'float_tripartite_v2_{collection_type}'
                )
                references.append({
                    'type': 'tripartite_collection',
                    'collection': collection_name,
                    'domain': collection_type,
                    'reason': 'content_routing'
                })
        
        # Float ID references
        content = file_analysis.get('content', '')
        float_ids = self.reference_patterns['float_id'].findall(content)
        for referenced_float_id in float_ids:
            if referenced_float_id != file_analysis.get('float_id'):
                references.append({
                    'type': 'float_id_reference',
                    'target_float_id': referenced_float_id,
                    'collection': 'float_dropzone_comprehensive'
                })
        
        # Conversation ID cross-references
        conv_ids = self.reference_patterns['conversation_id'].findall(content)
        for conv_id in conv_ids:
            references.append({
                'type': 'conversation_reference',
                'conversation_id': conv_id,
                'collection': 'FLOAT.conversations'
            })
        
        return references
    
    def _extract_conversation_links(self, content: str) -> List[Dict]:
        """Extract conversation-related links"""
        links = []
        
        # Conversation URLs
        urls = self.reference_patterns['url'].findall(content)
        for url in urls:
            if 'claude.ai' in url or 'chatgpt.com' in url or 'chat.openai.com' in url:
                platform = 'claude_ai' if 'claude.ai' in url else 'chatgpt'
                links.append({
                    'type': 'conversation_url',
                    'url': url,
                    'platform': platform,
                    'title': f"{platform.title()} Conversation"
                })
        
        # Conversation ID references
        conv_ids = self.reference_patterns['conversation_id'].findall(content)
        for conv_id in conv_ids:
            links.append({
                'type': 'conversation_id',
                'conversation_id': conv_id,
                'title': f"Conversation {conv_id}"
            })
        
        return links
    
    def _find_topic_connections(self, content: str, enhanced_analysis: Dict = None) -> List[str]:
        """Find topic connections"""
        topics = set()
        
        # From enhanced analysis
        if enhanced_analysis and enhanced_analysis.get('topics'):
            topics.update(enhanced_analysis['topics'])
        
        # Extract hashtags
        hashtags = self.reference_patterns['hashtag'].findall(content)
        topics.update(hashtags)
        
        # Extract concept/framework/metaphor references
        for pattern_name in ['concept_ref', 'framework_ref', 'metaphor_ref']:
            matches = self.reference_patterns[pattern_name].findall(content)
            topics.update(match.strip() for match in matches)
        
        return list(topics)
    
    def _extract_signal_references(self, content: str) -> List[Dict]:
        """Extract FLOAT signal references (ctx::, highlight::)"""
        signals = []
        
        # Context signals
        ctx_matches = self.reference_patterns['ctx_signal'].findall(content)
        for match in ctx_matches:
            signals.append({
                'type': 'ctx_signal',
                'content': match.strip(),
                'importance': 'context'
            })
        
        # Highlight signals
        highlight_matches = self.reference_patterns['highlight_signal'].findall(content)
        for match in highlight_matches:
            signals.append({
                'type': 'highlight_signal',
                'content': match.strip(),
                'importance': 'highlight'
            })
        
        return signals
    
    def _find_temporal_links(self, content: str) -> List[Dict]:
        """Find temporal references (dates, time periods)"""
        temporal_links = []
        
        # Date references
        dates = self.reference_patterns['date_ref'].findall(content)
        for date in dates:
            temporal_links.append({
                'type': 'date_reference',
                'date': date,
                'target': f"FLOAT.logs/{date}.md"
            })
        
        return temporal_links
    
    def _extract_external_links(self, content: str) -> List[Dict]:
        """Extract external links"""
        links = []
        
        urls = self.reference_patterns['url'].findall(content)
        for url in urls:
            # Skip conversation URLs (handled separately)
            if not any(domain in url for domain in ['claude.ai', 'chatgpt.com', 'chat.openai.com']):
                links.append({
                    'type': 'external_link',
                    'url': url,
                    'domain': self._extract_domain(url)
                })
        
        return links
    
    def _extract_key_terms(self, content: str) -> List[str]:
        """Extract key terms from content for reference searching"""
        words = re.findall(r'\b[a-zA-Z]{4,}\b', content.lower())
        
        # Filter common words
        stop_words = {
            'that', 'this', 'with', 'from', 'they', 'have', 'been', 'were', 
            'said', 'each', 'which', 'their', 'will', 'about', 'would', 
            'there', 'could', 'other', 'some', 'what', 'know', 'just',
            'first', 'into', 'over', 'think', 'also', 'back', 'after',
            'work', 'well', 'way', 'even', 'new', 'want', 'because',
            'any', 'these', 'give', 'day', 'most', 'us'
        }
        words = [w for w in words if w not in stop_words]
        
        # Get most common terms
        term_counts = Counter(words)
        return [term for term, count in term_counts.most_common(30) if count > 1]
    
    def _search_vault_for_term(self, term: str) -> List[Dict]:
        """Search vault files for a specific term"""
        matches = []
        
        # This is a simplified search - in practice, you'd want more sophisticated matching
        # For now, we'll create potential links based on common patterns
        potential_files = [
            f"{term.title()}.md",
            f"Notes on {term.title()}.md",
            f"{term} - Concept.md",
            f"{term} Framework.md"
        ]
        
        for potential_file in potential_files:
            if self._check_vault_file_exists(potential_file):
                matches.append({
                    'type': 'term_match',
                    'target': potential_file,
                    'term': term,
                    'relevance': 'potential_match',
                    'exists': True
                })
        
        return matches
    
    def _check_vault_file_exists(self, filename: str) -> bool:
        """Check if a vault file exists"""
        # Handle various file path formats
        if not filename.endswith('.md'):
            filename += '.md'
        
        # Check in main vault
        vault_file = self.vault_path / filename
        if vault_file.exists():
            return True
        
        # Check in common subdirectories
        common_dirs = ['FLOAT.conversations', 'FLOAT.logs', 'FLOAT.references', 'Notes', 'Daily']
        for dir_name in common_dirs:
            dir_path = self.vault_path / dir_name / filename
            if dir_path.exists():
                return True
        
        return False
    
    def _deduplicate_references(self, references: List[Dict]) -> List[Dict]:
        """Remove duplicate references"""
        seen = set()
        unique_refs = []
        
        for ref in references:
            # Create a hash of the reference for deduplication
            ref_key = f"{ref.get('type', '')}:{ref.get('target', '')}"
            if ref_key not in seen:
                seen.add(ref_key)
                unique_refs.append(ref)
        
        return unique_refs
    
    def _extract_domain(self, url: str) -> str:
        """Extract domain from URL"""
        try:
            from urllib.parse import urlparse
            return urlparse(url).netloc
        except:
            return 'unknown'
    
    def _update_vault_references(self, file_analysis: Dict, cross_refs: Dict):
        """Update vault files with references to new content"""
        try:
            float_id = file_analysis.get('float_id')
            metadata = file_analysis.get('metadata', {})
            
            # Create a reference note for this file
            ref_note_path = self.reference_dir / f"{float_id}_references.md"
            ref_content = self._generate_reference_note(file_analysis, cross_refs)
            
            with open(ref_note_path, 'w', encoding='utf-8') as f:
                f.write(ref_content)
            
            if self.logger:
                self.logger.info(f"Created reference note: {ref_note_path.name}")
            
            # Update backlinks in referenced files
            self._create_backlinks(file_analysis, cross_refs)
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to update vault references: {e}")
    
    def _generate_reference_note(self, file_analysis: Dict, cross_refs: Dict) -> str:
        """Generate markdown reference note"""
        metadata = file_analysis.get('metadata', {})
        analysis = file_analysis.get('analysis', {})
        
        content = f"""# Reference: {metadata.get('filename', 'Unknown')}

## File Information
- **Original**: `{metadata.get('filename', 'Unknown')}`
- **Type**: {analysis.get('content_classification', analysis.get('content_type', 'Unknown'))}
- **Processed**: {file_analysis.get('processed_at', 'Unknown')}
- **Float ID**: `{file_analysis.get('float_id', 'Unknown')}`
- **Size**: {metadata.get('size_bytes', 0):,} bytes

## Summary
{analysis.get('summary', 'No summary available')}

## Cross-References

### Vault References
{chr(10).join([f"- [[{ref['target']}]] ({'✅ exists' if ref.get('exists') else '❌ missing'})" for ref in cross_refs.get('vault_references', [])[:10]])}

### Conversation Links
{chr(10).join([f"- [{link['title']}]({link['url']})" for link in cross_refs.get('conversation_links', [])])}

### Topic Connections
{', '.join([f"#{topic}" for topic in cross_refs.get('topic_connections', [])])}

### FLOAT Signals
{chr(10).join([f"- **{signal['type']}**: {signal['content']}" for signal in cross_refs.get('signal_references', [])[:5]])}

### Temporal Links
{chr(10).join([f"- [[{link['target']}]] ({link['date']})" for link in cross_refs.get('temporal_links', [])])}

### External Links
{chr(10).join([f"- [{link['domain']}]({link['url']})" for link in cross_refs.get('external_links', [])[:5]])}

## ChromaDB Collections
{chr(10).join([f"- `{ref['collection']}` ({ref.get('reason', 'unknown')})" for ref in cross_refs.get('chroma_references', [])])}

---
*Auto-generated by FLOAT Cross-Reference System on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        return content
    
    def _create_backlinks(self, file_analysis: Dict, cross_refs: Dict):
        """Create backlinks in referenced vault files"""
        float_id = file_analysis.get('float_id')
        filename = file_analysis.get('metadata', {}).get('filename', 'Unknown')
        
        # Add backlinks to referenced vault files
        for ref in cross_refs.get('vault_references', []):
            if ref.get('exists') and ref.get('type') == 'obsidian_link':
                self._add_backlink_to_file(ref['target'], float_id, filename)
    
    def _add_backlink_to_file(self, target_file: str, float_id: str, source_filename: str):
        """Add backlink to a vault file"""
        try:
            # Find the actual file path
            if not target_file.endswith('.md'):
                target_file += '.md'
            
            target_path = self.vault_path / target_file
            if not target_path.exists():
                return
            
            # Read existing content
            with open(target_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if backlink already exists
            backlink_marker = f"<!-- FLOAT_BACKLINK_{float_id} -->"
            if backlink_marker in content:
                return
            
            # Add backlink section
            backlink_section = f"""

## FLOAT References
{backlink_marker}
- Referenced by: [[{float_id}_references|{source_filename}]] ({datetime.now().strftime('%Y-%m-%d')})
"""
            
            # Append to file
            with open(target_path, 'a', encoding='utf-8') as f:
                f.write(backlink_section)
            
        except Exception as e:
            if self.logger:
                self.logger.warning(f"Failed to add backlink to {target_file}: {e}")
    
    def _update_reference_index(self, float_id: str, cross_refs: Dict, metadata: Dict):
        """Update the reference index with new cross-references"""
        try:
            # Index by various reference types
            for ref_type, refs in cross_refs.items():
                if isinstance(refs, list):
                    for ref in refs:
                        if ref_type == 'vault_references':
                            key = f"vault:{ref.get('target', '')}"
                        elif ref_type == 'conversation_links':
                            conv_id = ref.get('conversation_id', '')
                            url = ref.get('url', '')
                            key = f"conversation:{conv_id or url or 'unknown'}"
                        elif ref_type == 'topic_connections':
                            key = f"topic:{ref}"
                        else:
                            continue
                        
                        self.reference_index[key].append({
                            'float_id': float_id,
                            'filename': metadata.get('filename'),
                            'timestamp': datetime.now().isoformat()
                        })
                elif isinstance(refs, list) and ref_type == 'topic_connections':
                    for topic in refs:
                        key = f"topic:{topic}"
                        self.reference_index[key].append({
                            'float_id': float_id,
                            'filename': metadata.get('filename'),
                            'timestamp': datetime.now().isoformat()
                        })
            
            # Save updated index
            self._save_reference_index()
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to update reference index: {e}")
    
    def get_references_for_topic(self, topic: str) -> List[Dict]:
        """Get all references for a specific topic"""
        key = f"topic:{topic}"
        return self.reference_index.get(key, [])
    
    def get_references_for_vault_file(self, filename: str) -> List[Dict]:
        """Get all references to a specific vault file"""
        key = f"vault:{filename}"
        return self.reference_index.get(key, [])
    
    def search_references(self, query: str) -> Dict[str, List[Dict]]:
        """Search through all references"""
        results = defaultdict(list)
        query_lower = query.lower()
        
        for key, refs in self.reference_index.items():
            if query_lower in key.lower():
                ref_type, ref_target = key.split(':', 1)
                results[ref_type].extend(refs)
        
        return dict(results)

if __name__ == "__main__":
    # Test cross-reference system
    from pathlib import Path
    
    # This would normally be initialized with real Chroma client and config
    print("Cross-reference system test placeholder")
    
    # test_system = CrossReferenceSystem(
    #     Path("/Users/evan/vault"),
    #     chroma_client,
    #     config
    # )
    
    print("Cross-reference system test complete")