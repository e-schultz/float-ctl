"""
FloatQL Parser - Parses :: notation into structured queries

Handles patterns like:
- ctx::meeting
- highlight::important
- created:today
- bridge::CB-YYYYMMDD-HHMM-XXXX
- [sysop::] or [karen::]
"""

import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple

class FloatQLParser:
    """Parser for FloatQL syntax - converts :: notation to structured queries"""
    
    def __init__(self):
        # FLOAT pattern regex - matches pattern:: or [pattern::]
        self.float_pattern_re = re.compile(r'(?:\[(\w+)::\]|(\w+)::)')
        
        # Temporal patterns - created:, modified:, date:
        self.temporal_re = re.compile(r'(created|modified|date):(\w+)')
        
        # Bridge pattern - CB-YYYYMMDD-HHMM-XXXX
        self.bridge_re = re.compile(r'bridge::(CB-\d{8}-\d{4}-\w+)')
        
        # Type pattern - type:log, type:conversation
        self.type_re = re.compile(r'type:(\w+)')
    
    def parse(self, query: str) -> Dict[str, Any]:
        """
        Parse a FloatQL query string into structured components
        
        Returns:
        {
            'text_terms': ['word1', 'word2'],           # Regular search terms
            'float_patterns': ['ctx', 'highlight'],     # FLOAT :: patterns  
            'persona_patterns': ['sysop', 'karen'],     # [pattern::] annotations
            'temporal_filters': {'created': 'today'},   # Date-based filters
            'type_filters': ['log', 'conversation'],    # Content type filters
            'bridge_ids': ['CB-20250611-1510-N1CK'],    # Bridge references
            'metadata_filters': {...}                   # Translated metadata filters
        }
        """
        result = {
            'text_terms': [],
            'float_patterns': [],
            'persona_patterns': [],
            'temporal_filters': {},
            'type_filters': [],
            'bridge_ids': [],
            'metadata_filters': {},
            'original_query': query
        }
        
        remaining_query = query
        
        # Extract FLOAT patterns (both pattern:: and [pattern::])
        for match in self.float_pattern_re.finditer(query):
            persona_pattern = match.group(1)  # [pattern::]
            float_pattern = match.group(2)    # pattern::
            
            if persona_pattern:
                result['persona_patterns'].append(persona_pattern)
            if float_pattern:
                result['float_patterns'].append(float_pattern)
            
            # Remove from remaining query
            remaining_query = remaining_query.replace(match.group(0), '', 1)
        
        # Extract temporal filters
        for match in self.temporal_re.finditer(query):
            field = match.group(1)
            value = match.group(2)
            result['temporal_filters'][field] = self._parse_temporal_value(value)
            
            # Remove from remaining query
            remaining_query = remaining_query.replace(match.group(0), '', 1)
        
        # Extract bridge IDs
        for match in self.bridge_re.finditer(query):
            bridge_id = match.group(1)
            result['bridge_ids'].append(bridge_id)
            
            # Remove from remaining query
            remaining_query = remaining_query.replace(match.group(0), '', 1)
        
        # Extract type filters
        for match in self.type_re.finditer(query):
            type_value = match.group(1)
            result['type_filters'].append(type_value)
            
            # Remove from remaining query
            remaining_query = remaining_query.replace(match.group(0), '', 1)
        
        # Extract remaining text terms
        text_terms = remaining_query.strip().split()
        result['text_terms'] = [term for term in text_terms if term and len(term) > 1]
        
        # Build metadata filters for ChromaDB
        result['metadata_filters'] = self._build_metadata_filters(result)
        
        return result
    
    def _parse_temporal_value(self, value: str) -> str:
        """Parse temporal values like 'today', 'yesterday', 'week' into date strings"""
        now = datetime.now()
        
        if value.lower() == 'today':
            return now.strftime('%Y-%m-%d')
        elif value.lower() == 'yesterday':
            return (now - timedelta(days=1)).strftime('%Y-%m-%d')
        elif value.lower() == 'week':
            return (now - timedelta(days=7)).strftime('%Y-%m-%d')
        elif value.lower() == 'month':
            return (now - timedelta(days=30)).strftime('%Y-%m-%d')
        else:
            # Try to parse as date
            try:
                parsed_date = datetime.strptime(value, '%Y-%m-%d')
                return parsed_date.strftime('%Y-%m-%d')
            except ValueError:
                return value  # Return as-is if can't parse
    
    def _build_metadata_filters(self, parsed: Dict[str, Any]) -> Dict[str, Any]:
        """Build ChromaDB metadata filters from parsed components"""
        filters = {}
        
        # FLOAT patterns -> context_markers
        if parsed['float_patterns']:
            filters['context_markers'] = {'$in': parsed['float_patterns']}
        
        # Persona patterns -> persona_annotations  
        if parsed['persona_patterns']:
            filters['persona_annotations'] = {'$in': parsed['persona_patterns']}
        
        # Type filters -> content_type
        if parsed['type_filters']:
            filters['content_type'] = {'$in': parsed['type_filters']}
        
        # Temporal filters -> date fields
        for field, date_value in parsed['temporal_filters'].items():
            if field == 'created':
                filters['conversation_date'] = {'$gte': date_value}
            elif field == 'modified':
                filters['modified_date'] = {'$gte': date_value}
            elif field == 'date':
                filters['conversation_date'] = date_value
        
        # Bridge IDs -> bridge_references
        if parsed['bridge_ids']:
            filters['bridge_references'] = {'$in': parsed['bridge_ids']}
        
        return filters
    
    def is_floatql_query(self, query: str) -> bool:
        """Check if query contains FloatQL syntax"""
        return (
            '::' in query or 
            re.search(r'(created|modified|date|type):', query) or
            re.search(r'bridge::', query)
        )
    
    def extract_search_terms(self, parsed: Dict[str, Any]) -> str:
        """Extract just the text search terms for basic search"""
        return ' '.join(parsed['text_terms'])
    
    def get_suggested_collections(self, parsed: Dict[str, Any]) -> List[str]:
        """Suggest which collections to search based on parsed query"""
        collections = []
        
        # Bridge queries should search bridge collections
        if parsed['bridge_ids']:
            collections.extend(['float_dispatch_bay', 'FLOAT.conversations'])
        
        # Type-specific collections
        if 'log' in parsed['type_filters']:
            collections.append('FLOAT.conversations')
        if 'conversation' in parsed['type_filters']:
            collections.append('FLOAT.conversations')
        
        # Pattern-specific routing
        if 'dispatch' in parsed['float_patterns']:
            collections.append('float_dispatch_bay')
        if 'rfc' in parsed['float_patterns']:
            collections.append('float_rfc')
        if 'echoCopy' in parsed['float_patterns']:
            collections.append('float_echoCopy')
        
        # Default to tripartite collections if no specific routing
        if not collections:
            collections.extend([
                'float_tripartite_v2_concept',
                'float_tripartite_v2_framework', 
                'float_tripartite_v2_metaphor'
            ])
        
        return list(set(collections))  # Remove duplicates