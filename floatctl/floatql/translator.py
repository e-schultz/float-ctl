"""
Query Translator - Converts parsed FloatQL to ChromaDB/filesystem queries

Takes structured FloatQL parse results and translates them into
actual database queries and file system searches.
"""

from typing import Dict, List, Optional, Any
from pathlib import Path

class QueryTranslator:
    """Translates parsed FloatQL into executable queries"""
    
    def __init__(self, chroma_data_path: str):
        self.chroma_data_path = chroma_data_path
    
    def translate_to_chroma_query(self, parsed: Dict[str, Any]) -> Dict[str, Any]:
        """
        Translate parsed FloatQL to ChromaDB query parameters
        
        Returns dict with:
        - query_texts: List of text to search for
        - where: Metadata filter dict for ChromaDB
        - collections: Suggested collections to search
        """
        # Build text query from terms and patterns
        query_parts = []
        
        # Add text terms
        if parsed['text_terms']:
            query_parts.extend(parsed['text_terms'])
        
        # Add FLOAT patterns as text search too
        if parsed['float_patterns']:
            for pattern in parsed['float_patterns']:
                query_parts.append(f"{pattern}::")
        
        # Add persona patterns
        if parsed['persona_patterns']:
            for pattern in parsed['persona_patterns']:
                query_parts.append(f"[{pattern}::]")
        
        # Combine into search text
        query_text = ' '.join(query_parts) if query_parts else parsed['original_query']
        
        return {
            'query_texts': [query_text],
            'where': parsed['metadata_filters'],
            'collections': self._get_collection_names(parsed),
            'n_results': 10  # Default limit
        }
    
    def translate_to_filesystem_query(self, parsed: Dict[str, Any], vault_path: str) -> Dict[str, Any]:
        """
        Translate parsed FloatQL to filesystem search parameters
        
        Returns dict with:
        - search_paths: List of paths to search
        - patterns: File patterns to match
        - content_filters: Text patterns to search for in files
        """
        vault_path = Path(vault_path)
        
        search_paths = []
        patterns = ['*.md', '*.txt']  # Default file patterns
        content_filters = []
        
        # Add text terms as content filters
        if parsed['text_terms']:
            content_filters.extend(parsed['text_terms'])
        
        # Add FLOAT patterns
        if parsed['float_patterns']:
            for pattern in parsed['float_patterns']:
                content_filters.append(f"{pattern}::")
        
        # Add persona patterns  
        if parsed['persona_patterns']:
            for pattern in parsed['persona_patterns']:
                content_filters.append(f"[{pattern}::]")
        
        # Type-specific path targeting
        if 'log' in parsed['type_filters']:
            search_paths.append(vault_path / 'FLOAT.conversations')
        if 'conversation' in parsed['type_filters']:
            search_paths.append(vault_path / 'FLOAT.conversations')
        
        # Bridge-specific searches
        if parsed['bridge_ids']:
            search_paths.append(vault_path / 'FLOAT.conversations')
            for bridge_id in parsed['bridge_ids']:
                content_filters.append(bridge_id)
        
        # Default to full vault search if no specific paths
        if not search_paths:
            search_paths.append(vault_path)
        
        return {
            'search_paths': search_paths,
            'patterns': patterns,
            'content_filters': content_filters,
            'temporal_filters': parsed['temporal_filters']
        }
    
    def _get_collection_names(self, parsed: Dict[str, Any]) -> List[str]:
        """Get appropriate collection names based on parsed query"""
        collections = []
        
        # Bridge queries -> bridge collections
        if parsed['bridge_ids']:
            collections.extend(['float_dispatch_bay', 'FLOAT.conversations'])
        
        # Pattern-specific routing
        if 'dispatch' in parsed['float_patterns']:
            collections.append('float_dispatch_bay')
        if 'rfc' in parsed['float_patterns']:
            collections.append('float_rfc')
        if 'echoCopy' in parsed['float_patterns']:
            collections.append('float_echoCopy')
        
        # Type-specific routing
        if parsed['type_filters']:
            if 'log' in parsed['type_filters']:
                collections.append('FLOAT.conversations')
            if 'conversation' in parsed['type_filters']:
                collections.append('FLOAT.conversations')
        
        # Default tripartite collections
        if not collections:
            collections.extend([
                'float_tripartite_v2_concept',
                'float_tripartite_v2_framework', 
                'float_tripartite_v2_metaphor',
                'float_dropzone_comprehensive'
            ])
        
        return list(set(collections))  # Remove duplicates
    
    def build_compound_query(self, parsed: Dict[str, Any]) -> Dict[str, Any]:
        """
        Build a compound query that searches both ChromaDB and filesystem
        
        Returns execution plan for comprehensive search
        """
        chroma_query = self.translate_to_chroma_query(parsed)
        
        return {
            'type': 'compound',
            'chroma_query': chroma_query,
            'search_strategy': self._determine_search_strategy(parsed),
            'result_fusion': self._get_fusion_strategy(parsed)
        }
    
    def _determine_search_strategy(self, parsed: Dict[str, Any]) -> str:
        """Determine optimal search strategy based on query type"""
        if parsed['bridge_ids']:
            return 'bridge_focused'  # Search for specific bridge references
        elif parsed['temporal_filters']:
            return 'temporal_focused'  # Date-based search
        elif parsed['float_patterns'] or parsed['persona_patterns']:
            return 'pattern_focused'  # FLOAT pattern search
        else:
            return 'semantic_search'  # General semantic search
    
    def _get_fusion_strategy(self, parsed: Dict[str, Any]) -> str:
        """Determine how to combine results from different sources"""
        if parsed['bridge_ids']:
            return 'bridge_connections'  # Follow bridge connections
        elif len(parsed['text_terms']) > 0:
            return 'relevance_ranking'  # Rank by text relevance
        else:
            return 'pattern_grouping'  # Group by pattern types