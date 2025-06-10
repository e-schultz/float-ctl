"""
Enhanced Pattern Detection System for FLOAT Daemon
Integrates sophisticated pattern recognition from tripartite chunker for all file types.

This module brings conversation-level intelligence to general file processing.
"""

import re
import json
from typing import Dict, List, Tuple, Optional, Set
from pathlib import Path
from datetime import datetime


class EnhancedFloatPatternDetector:
    """
    Enhanced pattern detection system incorporating patterns from the tripartite chunker.
    Provides sophisticated FLOAT signal detection for any file type.
    """
    
    def __init__(self):
        self.patterns = self._initialize_enhanced_patterns()
        self.tripartite_patterns = self._initialize_tripartite_patterns()
        
    def _initialize_enhanced_patterns(self) -> Dict:
        """Initialize comprehensive pattern library for all content types."""
        return {
            # Core FLOAT signals (existing + enhanced)
            'ctx_markers': re.compile(r'ctx::\s*([^\n]+)', re.IGNORECASE),
            'highlight_markers': re.compile(r'highlight::\s*([^\n]+)', re.IGNORECASE),
            'signal_markers': re.compile(r'signal::\s*([^\n]+)', re.IGNORECASE),
            'float_dispatch': re.compile(r'float\.dispatch\s*\([^)]*\)', re.IGNORECASE),
            'sysop_comments': re.compile(r'\[sysop::([^\]]+)\]', re.IGNORECASE),
            
            # Extended FLOAT annotation grammar (from tripartite chunker)
            'expand_on': re.compile(r'expandOn::\s*([^\n]+)', re.IGNORECASE),
            'relates_to': re.compile(r'relatesTo::\s*([^\n]+)', re.IGNORECASE),
            'remember_when': re.compile(r'rememberWhen::\s*([^\n]+)', re.IGNORECASE),
            'story_time': re.compile(r'storyTime::\s*([^\n]+)', re.IGNORECASE),
            'echo_copy': re.compile(r'echoCopy::\s*([^\n]*?)(?:\s*::|$)', re.IGNORECASE),
            'mood_markers': re.compile(r'\[mood::\s*([^\]]*)\]', re.IGNORECASE),
            
            # Persona annotation system (from tripartite chunker)
            'persona_annotations': re.compile(r'\[([^:]+)::[^\]]+\]'),
            'any_combo': re.compile(r'\[any::[^\]]+\]', re.IGNORECASE),
            'lf1m_notes': re.compile(r'\[lf1m::[^\]]+\]', re.IGNORECASE),
            'qtb_notes': re.compile(r'\[qtb::[^\]]+\]', re.IGNORECASE),
            'karen_notes': re.compile(r'\[karen::[^\]]+\]', re.IGNORECASE),
            'sysop_notes': re.compile(r'\[sysop::[^\]]+\]', re.IGNORECASE),
            'little_fucker': re.compile(r'\[little-fucker::[^\]]+\]', re.IGNORECASE),
            
            # BBS heritage patterns (from tripartite chunker)
            'float_dis': re.compile(r'float[_\.]di[sz]', re.IGNORECASE),
            'float_diis': re.compile(r'float[_\.]diis', re.IGNORECASE),
            'file_id_diz': re.compile(r'file_id\.diz', re.IGNORECASE),
            
            # Build platform integration (from tripartite chunker)
            'lovable_refs': re.compile(r'lovable\.(?:dev|app)', re.IGNORECASE),
            'v0_refs': re.compile(r'v0\.dev', re.IGNORECASE),
            'magic_patterns': re.compile(r'magicpatterns\.com', re.IGNORECASE),
            'github_refs': re.compile(r'github\.com', re.IGNORECASE),
            'thought_buckets': re.compile(r'(?:thought|build)\s+buckets?', re.IGNORECASE),
            
            # FLOAT structural patterns
            'ritual_ast': re.compile(r'ritual(?:AST|_\w+)', re.IGNORECASE),
            'doctrine_volume': re.compile(r'doctrine(?:Volume|_\w+)', re.IGNORECASE),
            'float_rfc': re.compile(r'float\.rfc(?:\s+([^\n]+))?', re.IGNORECASE),
            'bridge_patterns': re.compile(r'CB-\d{8}-\d{4}-[A-Z0-9]{4}'),
            
            # Neurodivergent experience patterns
            'neurodivergent': re.compile(r'(?:neurodivergent|adhd|autistic|divergent)', re.IGNORECASE),
            'embodied': re.compile(r'(?:embodied|lived|felt|visceral)', re.IGNORECASE),
            
            # Metaphorical language patterns
            'shack_cathedral': re.compile(r'(?:shacks?\s+not\s+cathedrals?|cathedral\s+vs\s+shack)', re.IGNORECASE),
            'ritual_language': re.compile(r'(?:ritual|sacred|ceremony|blessing)', re.IGNORECASE),
            'feral_duality': re.compile(r'(?:feral|tame)\s+(?:duality|reality)', re.IGNORECASE),
            'rotfield': re.compile(r'(?:rot|compost|ferment|decay)', re.IGNORECASE),
            
            # Document structure patterns (for any file type)
            'headings': re.compile(r'^#+\s+(.+)$', re.MULTILINE),
            'bullet_points': re.compile(r'^\s*[-*+]\s+(.+)$', re.MULTILINE),
            'numbered_lists': re.compile(r'^\s*\d+\.\s+(.+)$', re.MULTILINE),
            'action_items': re.compile(r'(?:TODO|FIXME|NOTE|IMPORTANT|HACK|XXX):\s*(.+)', re.IGNORECASE),
            'citations': re.compile(r'\[([^\]]+)\]\(([^)]+)\)'),
            
            # Code patterns
            'code_blocks': re.compile(r'```(\w+)?\n(.*?)\n```', re.DOTALL),
            'inline_code': re.compile(r'`([^`]+)`'),
            'api_endpoints': re.compile(r'(?:GET|POST|PUT|DELETE)\s+[/\w-]+'),
            
            # Technical patterns
            'implementation': re.compile(r'(?:implement|build|create|setup|configure)', re.IGNORECASE),
            'architecture': re.compile(r'(?:architecture|system|design|pattern)', re.IGNORECASE),
            'workflow': re.compile(r'(?:workflow|process|pipeline|flow)', re.IGNORECASE),
            'yaml_json': re.compile(r'(?:yaml|json|api|endpoint)', re.IGNORECASE),
            
            # Narrative patterns
            'story_markers': re.compile(r'(?:imagine|think of|like|similar to)', re.IGNORECASE),
            'experience': re.compile(r'(?:feel|experience|journey|path)', re.IGNORECASE),
            'philosophy': re.compile(r'(?:philosophy|approach|mindset|thinking)', re.IGNORECASE),
            'personal_pronouns': re.compile(r'\b(?:I|you|we|your|my)\b'),
            'casual_language': re.compile(r'(?:basically|essentially|really|actually)', re.IGNORECASE),
            'examples': re.compile(r'(?:for example|such as|like when|imagine if)', re.IGNORECASE),
            
            # Concept patterns
            'definition': re.compile(r'(?:what is|explain|define)\s+[\w\s]+', re.IGNORECASE),
            'clarification': re.compile(r'(?:to clarify|in other words|meaning)', re.IGNORECASE),
            'atomic_knowledge': re.compile(r'(?:atomic|precise|specific|exact)', re.IGNORECASE),
            
            # Sigils and special markers
            'sigils': re.compile(r'\{[■∴ψΞ|>~≈🕯️∞⧉📖⚑🛠️🧠]+\}'),
            
            # Contact information
            'email_addresses': re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),
            'phone_numbers': re.compile(r'\b\d{3}-\d{3}-\d{4}\b'),
            'version_numbers': re.compile(r'v?\d+\.\d+(?:\.\d+)?'),
        }
    
    def _initialize_tripartite_patterns(self) -> Dict:
        """Initialize tripartite classification patterns from the chunker."""
        return {
            'concept': {
                'patterns': [
                    'ctx_markers', 'highlight_markers', 'signal_markers', 'float_dispatch',
                    'sysop_comments', 'expand_on', 'relates_to', 'remember_when',
                    'definition', 'clarification', 'atomic_knowledge', 'inline_code', 'code_blocks'
                ],
                'topics': ['question', 'definition', 'concept', 'clarification', 'signal'],
                'target_chars': 600,
                'hard_limit': 1200,
                'priority': 'precision'
            },
            'framework': {
                'patterns': [
                    'implementation', 'architecture', 'workflow', 'yaml_json',
                    'ritual_ast', 'doctrine_volume', 'float_rfc', 'persona_annotations',
                    'numbered_lists', 'bullet_points', 'action_items'
                ],
                'topics': ['technical', 'implementation', 'architecture', 'workflow', 'system'],
                'target_chars': 900,
                'hard_limit': 1800,
                'priority': 'structure'
            },
            'metaphor': {
                'patterns': [
                    'shack_cathedral', 'ritual_language', 'feral_duality', 'rotfield',
                    'story_markers', 'experience', 'philosophy', 'personal_pronouns',
                    'casual_language', 'examples', 'neurodivergent', 'embodied'
                ],
                'topics': ['narrative', 'philosophy', 'experience', 'metaphor', 'ritual'],
                'target_chars': 800,
                'hard_limit': 1600,
                'priority': 'resonance'
            }
        }
    
    def extract_comprehensive_patterns(self, content: str, file_path: Optional[Path] = None) -> Dict:
        """
        Extract all FLOAT patterns from content with enhanced analysis.
        Returns comprehensive pattern analysis for any file type.
        """
        
        if not content:
            return self._empty_pattern_result()
        
        # Core pattern extraction
        core_patterns = self._extract_core_float_patterns(content)
        
        # Extended pattern extraction
        extended_patterns = self._extract_extended_float_patterns(content)
        
        # Document structure analysis
        structure_patterns = self._extract_document_structure(content)
        
        # Content classification
        classification = self._classify_content_tripartite(content)
        
        # Signal analysis
        signal_analysis = self._analyze_signal_density(content, core_patterns, extended_patterns)
        
        # Platform and tool integration analysis
        platform_analysis = self._analyze_platform_integration(content)
        
        # Persona and annotation analysis
        persona_analysis = self._analyze_persona_annotations(content)
        
        # Cross-reference potential
        cross_ref_analysis = self._analyze_cross_reference_potential(content, file_path)
        
        return {
            'core_float_patterns': core_patterns,
            'extended_float_patterns': extended_patterns,
            'document_structure': structure_patterns,
            'tripartite_classification': classification,
            'signal_analysis': signal_analysis,
            'platform_integration': platform_analysis,
            'persona_analysis': persona_analysis,
            'cross_reference_potential': cross_ref_analysis,
            'analysis_metadata': {
                'content_length': len(content),
                'word_count': len(content.split()),
                'line_count': len(content.split('\n')),
                'analysis_timestamp': datetime.now().isoformat(),
                'pattern_detector_version': '2.0'
            }
        }
    
    def _extract_core_float_patterns(self, content: str) -> Dict:
        """Extract core FLOAT patterns."""
        patterns = {}
        
        # Extract each core pattern
        for pattern_name in ['ctx_markers', 'highlight_markers', 'signal_markers', 
                           'float_dispatch', 'sysop_comments']:
            if pattern_name in self.patterns:
                matches = self.patterns[pattern_name].findall(content)
                patterns[pattern_name] = {
                    'count': len(matches),
                    'matches': matches[:10],  # Limit to first 10 for metadata
                    'has_pattern': len(matches) > 0
                }
        
        return patterns
    
    def _extract_extended_float_patterns(self, content: str) -> Dict:
        """Extract extended FLOAT annotation grammar patterns."""
        patterns = {}
        
        extended_pattern_names = [
            'expand_on', 'relates_to', 'remember_when', 'story_time', 
            'echo_copy', 'mood_markers'
        ]
        
        for pattern_name in extended_pattern_names:
            if pattern_name in self.patterns:
                matches = self.patterns[pattern_name].findall(content)
                patterns[pattern_name] = {
                    'count': len(matches),
                    'matches': matches[:5],  # Fewer matches for metadata
                    'has_pattern': len(matches) > 0
                }
        
        return patterns
    
    def _extract_document_structure(self, content: str) -> Dict:
        """Analyze document structure patterns."""
        structure = {}
        
        # Headings
        headings = self.patterns['headings'].findall(content)
        structure['headings'] = {
            'count': len(headings),
            'levels': self._analyze_heading_levels(content),
            'titles': headings[:5]  # First 5 headings
        }
        
        # Lists
        bullet_points = self.patterns['bullet_points'].findall(content)
        numbered_lists = self.patterns['numbered_lists'].findall(content)
        
        structure['lists'] = {
            'bullet_points': len(bullet_points),
            'numbered_lists': len(numbered_lists),
            'total_list_items': len(bullet_points) + len(numbered_lists)
        }
        
        # Code patterns
        code_blocks = self.patterns['code_blocks'].findall(content)
        inline_code = self.patterns['inline_code'].findall(content)
        
        structure['code'] = {
            'code_blocks': len(code_blocks),
            'inline_code': len(inline_code),
            'code_languages': [lang for lang, _ in code_blocks if lang],
            'code_density': (len(code_blocks) + len(inline_code)) / max(len(content.split('\n')), 1)
        }
        
        # Action items
        action_items = self.patterns['action_items'].findall(content)
        structure['action_items'] = {
            'count': len(action_items),
            'items': action_items[:5]
        }
        
        return structure
    
    def _classify_content_tripartite(self, content: str) -> Dict:
        """Classify content using tripartite system (concept/framework/metaphor)."""
        scores = {'concept': 0, 'framework': 0, 'metaphor': 0}
        pattern_matches = {'concept': [], 'framework': [], 'metaphor': []}
        
        # Score each domain based on pattern matches
        for domain, domain_info in self.tripartite_patterns.items():
            for pattern_name in domain_info['patterns']:
                if pattern_name in self.patterns:
                    matches = self.patterns[pattern_name].findall(content)
                    if matches:
                        # Weight core FLOAT patterns higher
                        weight = 3 if pattern_name in ['ctx_markers', 'highlight_markers', 'float_dispatch'] else 1
                        scores[domain] += len(matches) * weight
                        pattern_matches[domain].append(pattern_name)
        
        # Apply edge case rules (from tripartite chunker)
        self._apply_tripartite_edge_cases(content, scores)
        
        # Determine primary domain
        primary_domain = max(scores, key=scores.get) if any(scores.values()) else 'concept'
        confidence = scores[primary_domain] / max(sum(scores.values()), 1)
        
        return {
            'primary_domain': primary_domain,
            'confidence': confidence,
            'scores': scores,
            'pattern_matches': pattern_matches,
            'explanation': self._explain_tripartite_classification(primary_domain, pattern_matches[primary_domain], scores)
        }
    
    def _apply_tripartite_edge_cases(self, content: str, scores: Dict):
        """Apply edge case rules from tripartite chunker."""
        content_lower = content.lower()
        
        # Strong concept indicators
        if any(marker in content for marker in ['ctx::', 'signal::', 'highlight::']):
            scores['concept'] += 5
        
        # BBS heritage patterns
        bbs_patterns = ['float_dis', 'float.diz', 'float_diis', 'file_id.diz']
        if any(pattern in content_lower for pattern in bbs_patterns):
            scores['metaphor'] += 5  # Cultural significance
            scores['concept'] += 3   # High conceptual value
        
        # Build platform integration
        build_platforms = ['lovable.dev', 'v0.dev', 'magicpatterns.com', 'github.com']
        if any(platform in content_lower for platform in build_platforms):
            scores['framework'] += 4
        
        # Thought buckets
        if re.search(r'(?:thought|build)\s+buckets?', content_lower):
            scores['concept'] += 3
        
        # Mood tracking
        if '[mood::' in content:
            scores['metaphor'] += 4
        
        # FLOAT RFC patterns
        if 'float.rfc' in content_lower or 'rfc::' in content_lower:
            scores['framework'] += 4
        
        # Neurodivergent content
        if 'neurodivergent' in content_lower:
            if any(tech in content_lower for tech in ['workflow', 'system', 'productivity', 'tool']):
                scores['framework'] += 3
            else:
                scores['metaphor'] += 3
        
        # Shacks not cathedrals
        if 'shack' in content_lower and 'cathedral' in content_lower:
            scores['metaphor'] += 5
    
    def _analyze_signal_density(self, content: str, core_patterns: Dict, extended_patterns: Dict) -> Dict:
        """Analyze FLOAT signal density and distribution."""
        total_signals = sum(p.get('count', 0) for p in core_patterns.values())
        total_extended = sum(p.get('count', 0) for p in extended_patterns.values())
        
        word_count = len(content.split())
        line_count = len(content.split('\n'))
        
        return {
            'total_core_signals': total_signals,
            'total_extended_patterns': total_extended,
            'signal_density_per_100_words': (total_signals / max(word_count, 1)) * 100,
            'signal_density_per_100_lines': (total_signals / max(line_count, 1)) * 100,
            'has_high_signal_density': (total_signals / max(word_count, 1)) > 0.02,  # 2% threshold
            'dominant_signal_type': self._identify_dominant_signal_type(core_patterns),
            'signal_distribution': {
                'core_signals': total_signals,
                'extended_patterns': total_extended,
                'structural_patterns': len(self.patterns['headings'].findall(content)),
                'code_patterns': len(self.patterns['code_blocks'].findall(content))
            }
        }
    
    def _analyze_platform_integration(self, content: str) -> Dict:
        """Analyze build platform and tool integration patterns."""
        platforms = {}
        
        platform_patterns = ['lovable_refs', 'v0_refs', 'magic_patterns', 'github_refs', 'thought_buckets']
        
        for pattern_name in platform_patterns:
            if pattern_name in self.patterns:
                matches = self.patterns[pattern_name].findall(content)
                platforms[pattern_name] = {
                    'count': len(matches),
                    'has_pattern': len(matches) > 0
                }
        
        total_platform_refs = sum(p['count'] for p in platforms.values())
        
        return {
            'platforms': platforms,
            'total_platform_references': total_platform_refs,
            'has_platform_integration': total_platform_refs > 0,
            'primary_platform': max(platforms, key=lambda x: platforms[x]['count']) if platforms else None
        }
    
    def _analyze_persona_annotations(self, content: str) -> Dict:
        """Analyze persona annotation system patterns."""
        personas = {}
        
        persona_patterns = ['any_combo', 'lf1m_notes', 'qtb_notes', 'karen_notes', 'sysop_notes', 'little_fucker']
        
        for pattern_name in persona_patterns:
            if pattern_name in self.patterns:
                matches = self.patterns[pattern_name].findall(content)
                personas[pattern_name] = {
                    'count': len(matches),
                    'has_pattern': len(matches) > 0
                }
        
        # Extract all persona annotations
        all_persona_matches = self.patterns['persona_annotations'].findall(content)
        persona_counts = {}
        for persona in all_persona_matches:
            persona_counts[persona] = persona_counts.get(persona, 0) + 1
        
        total_persona_annotations = sum(p['count'] for p in personas.values())
        
        return {
            'specific_personas': personas,
            'all_persona_annotations': persona_counts,
            'total_persona_annotations': total_persona_annotations,
            'has_persona_system': total_persona_annotations > 0,
            'dominant_persona': max(persona_counts, key=persona_counts.get) if persona_counts else None,
            'persona_diversity': len(persona_counts)
        }
    
    def _analyze_cross_reference_potential(self, content: str, file_path: Optional[Path] = None) -> Dict:
        """Analyze potential for cross-referencing with other content."""
        
        # Extract citations and links
        citations = self.patterns['citations'].findall(content)
        
        # Extract email addresses and contact info
        emails = self.patterns['email_addresses'].findall(content)
        phones = self.patterns['phone_numbers'].findall(content)
        
        # Extract version numbers and technical identifiers
        versions = self.patterns['version_numbers'].findall(content)
        
        # Extract bridge patterns
        bridge_patterns = self.patterns['bridge_patterns'].findall(content)
        
        # Analyze temporal references
        temporal_refs = self._extract_temporal_references(content)
        
        return {
            'citations': {
                'count': len(citations),
                'links': citations[:5]  # First 5 citations
            },
            'contact_information': {
                'emails': emails,
                'phones': phones,
                'has_contact_info': len(emails) + len(phones) > 0
            },
            'technical_identifiers': {
                'versions': versions,
                'bridge_patterns': bridge_patterns,
                'has_technical_ids': len(versions) + len(bridge_patterns) > 0
            },
            'temporal_references': temporal_refs,
            'cross_reference_score': self._calculate_cross_reference_score(citations, emails, versions, temporal_refs),
            'file_context': {
                'file_name': file_path.name if file_path else None,
                'file_extension': file_path.suffix if file_path else None,
                'file_size_estimate': len(content)
            }
        }
    
    def _extract_temporal_references(self, content: str) -> Dict:
        """Extract temporal references and date patterns."""
        
        # Date patterns
        date_patterns = [
            re.compile(r'\d{4}-\d{2}-\d{2}'),  # YYYY-MM-DD
            re.compile(r'\d{2}/\d{2}/\d{4}'),  # MM/DD/YYYY
            re.compile(r'(?:yesterday|today|tomorrow)', re.IGNORECASE),
            re.compile(r'(?:last|next)\s+(?:week|month|year)', re.IGNORECASE)
        ]
        
        temporal_refs = {}
        for i, pattern in enumerate(date_patterns):
            matches = pattern.findall(content)
            temporal_refs[f'pattern_{i}'] = matches
        
        all_matches = [match for matches in temporal_refs.values() for match in matches]
        
        return {
            'total_temporal_references': len(all_matches),
            'temporal_patterns': temporal_refs,
            'has_temporal_context': len(all_matches) > 0
        }
    
    def _calculate_cross_reference_score(self, citations: List, emails: List, versions: List, temporal_refs: Dict) -> float:
        """Calculate a cross-reference potential score."""
        score = 0.0
        
        # Citations contribute to cross-reference potential
        score += len(citations) * 0.3
        
        # Contact information suggests networking potential
        score += len(emails) * 0.2
        
        # Technical identifiers suggest system integration
        score += len(versions) * 0.1
        
        # Temporal references suggest event tracking
        score += temporal_refs['total_temporal_references'] * 0.1
        
        return min(score, 1.0)  # Cap at 1.0
    
    def _analyze_heading_levels(self, content: str) -> Dict:
        """Analyze heading hierarchy in content."""
        lines = content.split('\n')
        heading_levels = {}
        
        for line in lines:
            if line.strip().startswith('#'):
                level = len(line) - len(line.lstrip('#'))
                heading_levels[level] = heading_levels.get(level, 0) + 1
        
        return heading_levels
    
    def _identify_dominant_signal_type(self, core_patterns: Dict) -> Optional[str]:
        """Identify the most prominent signal type."""
        if not core_patterns:
            return None
            
        max_count = 0
        dominant_type = None
        
        for pattern_name, pattern_data in core_patterns.items():
            count = pattern_data.get('count', 0)
            if count > max_count:
                max_count = count
                dominant_type = pattern_name
        
        return dominant_type
    
    def _explain_tripartite_classification(self, domain: str, patterns: List[str], scores: Dict) -> str:
        """Generate explanation for tripartite classification."""
        if not patterns:
            return f"Classified as {domain} by default (no strong patterns detected)"
        
        top_patterns = patterns[:3]
        score_info = f"Scores: {scores}"
        return f"Classified as {domain} based on patterns: {', '.join(top_patterns)}. {score_info}"
    
    def _empty_pattern_result(self) -> Dict:
        """Return empty pattern result for invalid input."""
        return {
            'core_float_patterns': {},
            'extended_float_patterns': {},
            'document_structure': {},
            'tripartite_classification': {
                'primary_domain': 'concept',
                'confidence': 0.0,
                'scores': {'concept': 0, 'framework': 0, 'metaphor': 0},
                'pattern_matches': {'concept': [], 'framework': [], 'metaphor': []},
                'explanation': 'No content to analyze'
            },
            'signal_analysis': {
                'total_core_signals': 0,
                'total_extended_patterns': 0,
                'signal_density_per_100_words': 0.0,
                'has_high_signal_density': False
            },
            'platform_integration': {'total_platform_references': 0, 'has_platform_integration': False},
            'persona_analysis': {'total_persona_annotations': 0, 'has_persona_system': False},
            'cross_reference_potential': {'cross_reference_score': 0.0},
            'analysis_metadata': {
                'content_length': 0,
                'word_count': 0,
                'analysis_timestamp': datetime.now().isoformat(),
                'pattern_detector_version': '2.0'
            }
        }
    
    def is_high_priority_content(self, pattern_analysis: Dict) -> bool:
        """Determine if content should be prioritized based on pattern analysis."""
        
        # High priority if it has core FLOAT signals
        core_signals = pattern_analysis.get('signal_analysis', {}).get('total_core_signals', 0)
        if core_signals > 0:
            return True
        
        # High priority if it has persona annotations
        persona_count = pattern_analysis.get('persona_analysis', {}).get('total_persona_annotations', 0)
        if persona_count > 0:
            return True
        
        # High priority if it has high signal density
        if pattern_analysis.get('signal_analysis', {}).get('has_high_signal_density', False):
            return True
        
        # High priority if it has BBS heritage patterns
        bbs_patterns = ['float_dis', 'float_diis', 'file_id_diz']
        content = str(pattern_analysis)  # Quick check in serialized form
        if any(pattern in content.lower() for pattern in bbs_patterns):
            return True
        
        return False
    
    def get_content_complexity_assessment(self, pattern_analysis: Dict) -> str:
        """Assess content complexity based on pattern analysis."""
        
        metadata = pattern_analysis.get('analysis_metadata', {})
        word_count = metadata.get('word_count', 0)
        
        signal_count = pattern_analysis.get('signal_analysis', {}).get('total_core_signals', 0)
        structure = pattern_analysis.get('document_structure', {})
        code_density = structure.get('code', {}).get('code_density', 0)
        
        # Calculate complexity score
        complexity_score = 0
        
        # Word count factor
        if word_count > 5000:
            complexity_score += 3
        elif word_count > 2000:
            complexity_score += 2
        elif word_count > 500:
            complexity_score += 1
        
        # Signal density factor
        if signal_count > 10:
            complexity_score += 2
        elif signal_count > 5:
            complexity_score += 1
        
        # Code density factor
        if code_density > 0.1:
            complexity_score += 2
        elif code_density > 0.05:
            complexity_score += 1
        
        # Structure complexity
        heading_count = structure.get('headings', {}).get('count', 0)
        if heading_count > 20:
            complexity_score += 2
        elif heading_count > 10:
            complexity_score += 1
        
        # Classify complexity
        if complexity_score >= 6:
            return 'high'
        elif complexity_score >= 3:
            return 'medium'
        else:
            return 'low'
    
    def extract_actionable_insights(self, pattern_analysis: Dict) -> List[Dict]:
        """Extract actionable insights from pattern analysis."""
        insights = []
        
        # Check for action items
        structure = pattern_analysis.get('document_structure', {})
        action_items = structure.get('action_items', {}).get('items', [])
        
        for item in action_items:
            insights.append({
                'type': 'action_item',
                'content': item,
                'priority': 'high' if any(word in item.lower() for word in ['urgent', 'asap', 'critical']) else 'medium',
                'source': 'document_structure'
            })
        
        # Check for FLOAT dispatch patterns
        core_patterns = pattern_analysis.get('core_float_patterns', {})
        if core_patterns.get('float_dispatch', {}).get('has_pattern', False):
            insights.append({
                'type': 'float_dispatch',
                'content': 'Content contains FLOAT dispatch patterns',
                'priority': 'high',
                'source': 'core_float_patterns'
            })
        
        # Check for cross-reference opportunities
        cross_ref = pattern_analysis.get('cross_reference_potential', {})
        if cross_ref.get('cross_reference_score', 0) > 0.5:
            insights.append({
                'type': 'cross_reference_opportunity',
                'content': f"High cross-reference potential (score: {cross_ref.get('cross_reference_score', 0):.2f})",
                'priority': 'medium',
                'source': 'cross_reference_analysis'
            })
        
        # Check for platform integration opportunities
        platform = pattern_analysis.get('platform_integration', {})
        if platform.get('has_platform_integration', False):
            insights.append({
                'type': 'platform_integration',
                'content': f"Content references external platforms ({platform.get('total_platform_references', 0)} references)",
                'priority': 'medium',
                'source': 'platform_analysis'
            })
        
        return insights