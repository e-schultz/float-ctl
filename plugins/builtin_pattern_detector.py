"""
Built-in Pattern Detector Plugin for FLOAT

This plugin converts the existing EnhancedFloatPatternDetector into a proper plugin
using the memory-safe plugin architecture. It provides the same comprehensive
pattern detection capabilities while being safely loadable via entry points.

This is the reference implementation for pattern detector plugins.

Issue #14: Memory-safe plugin architecture foundation
"""

import re
import json
from typing import Dict, List, Optional, Set, Any
from pathlib import Path
from datetime import datetime

from plugin_base import PatternDetectorPlugin

class BuiltinPatternDetector(PatternDetectorPlugin):
    """
    Built-in pattern detector plugin implementing comprehensive FLOAT pattern recognition.
    
    This plugin provides the same functionality as the original EnhancedFloatPatternDetector
    but in a memory-safe plugin architecture using entry points.
    """
    
    @property
    def name(self) -> str:
        """
        Returns the name of the plugin.
        """
        return "builtin_pattern_detector"
    
    @property
    def version(self) -> str:
        """
        Return the version string of the built-in pattern detector plugin.
        """
        return "3.1.0"
    
    @property
    def description(self) -> str:
        """
        Returns a description of the plugin as a built-in comprehensive FLOAT pattern detector supporting over 40 pattern types.
        """
        return "Built-in comprehensive FLOAT pattern detector with 40+ pattern types"
    
    @property
    def author(self) -> str:
        """
        Return the author of the plugin.
        """
        return "FLOAT Core Team"
    
    @property
    def supported_patterns(self) -> List[str]:
        """
        Return a list of pattern categories supported by the built-in pattern detector.
        
        Returns:
            List of supported pattern category names as strings.
        """
        return [
            "ctx_markers", "highlight_markers", "signal_markers", "float_dispatch",
            "sysop_comments", "expand_on", "relates_to", "remember_when", "story_time",
            "echo_copy", "mood_markers", "persona_annotations", "platform_integration",
            "tripartite_classification", "document_structure", "cross_reference_potential"
        ]
    
    def initialize(self, config: Optional[Dict] = None, logger=None) -> bool:
        """
        Initializes the pattern detector plugin with pattern libraries and optional configuration.
        
        Returns:
            bool: True if initialization is successful.
        """
        super().initialize(config, logger)
        
        # Initialize pattern libraries
        self.patterns = self._initialize_enhanced_patterns()
        self.tripartite_patterns = self._initialize_tripartite_patterns()
        
        if self._logger:
            self._logger.info(f"Initialized {self.name} with {len(self.patterns)} core patterns")
        
        return True
    
    def detect_patterns(self, content: str, file_path: Optional[Path] = None) -> Dict[str, Any]:
        """
        Performs comprehensive pattern detection on the provided content and returns analysis results.
        
        Analyzes the input content for FLOAT patterns, document structure, persona annotations, platform references, and other supported categories. Returns a dictionary containing the analysis results, total patterns found, plugin metadata, and a success indicator. On error, returns a failure response with error details.
        """
        try:
            results = self.extract_comprehensive_patterns(content, file_path)
            
            # Ensure plugin interface compliance
            results.update({
                'success': True,
                'patterns_found': self._count_total_patterns(results),
                'analysis_results': results,
                'plugin_name': self.name,
                'plugin_version': self.version
            })
            
            return results
            
        except Exception as e:
            if self._logger:
                self._logger.error(f"Pattern detection failed: {e}")
            
            return {
                'success': False,
                'patterns_found': 0,
                'analysis_results': {},
                'error': str(e),
                'plugin_name': self.name,
                'plugin_version': self.version
            }
    
    def extract_comprehensive_patterns(self, content: str, file_path: Optional[Path] = None) -> Dict:
        """
        Performs comprehensive pattern extraction and content analysis on the provided text.
        
        Analyzes the content for core and extended FLOAT patterns, persona annotations, document structure, platform integration references, signal density, tripartite classification, cross-reference potential, and BBS heritage patterns. Returns a dictionary containing all extracted analyses and relevant metadata.
        
        Parameters:
            content (str): The text content to analyze.
            file_path (Optional[Path]): Optional file path associated with the content.
        
        Returns:
            Dict: A dictionary containing detailed pattern analysis results and metadata.
        """
        if not content or not content.strip():
            return self._empty_analysis_result()
        
        analysis = {
            'content_length': len(content),
            'word_count': len(content.split()),
            'line_count': len(content.split('\n')),
            'file_path': str(file_path) if file_path else None,
            'analyzed_at': datetime.now().isoformat()
        }
        
        # Core FLOAT pattern detection
        analysis['core_float_patterns'] = self._extract_core_float_patterns(content)
        
        # Extended FLOAT patterns
        analysis['extended_float_patterns'] = self._extract_extended_float_patterns(content)
        
        # Persona annotation analysis
        analysis['persona_analysis'] = self._extract_persona_patterns(content)
        
        # Document structure analysis
        analysis['document_structure'] = self._analyze_document_structure(content)
        
        # Platform integration patterns
        analysis['platform_integration'] = self._detect_platform_integration(content)
        
        # Signal analysis and density
        analysis['signal_analysis'] = self._calculate_signal_analysis(analysis)
        
        # Tripartite classification
        analysis['tripartite_classification'] = self._classify_tripartite_domain(content, analysis)
        
        # Cross-reference potential
        analysis['cross_reference_potential'] = self._analyze_cross_reference_potential(content, analysis)
        
        # BBS heritage patterns  
        analysis['bbs_heritage'] = self._detect_bbs_heritage_patterns(content)
        
        return analysis
    
    def is_high_priority_content(self, pattern_analysis: Dict) -> bool:
        """
        Determine whether the analyzed content qualifies as high priority based on signal density, presence of core FLOAT signals, persona annotations, or BBS heritage patterns.
        
        Returns:
            bool: True if any high-priority criteria are met; otherwise, False.
        """
        # High signal density
        signal_analysis = pattern_analysis.get('signal_analysis', {})
        if signal_analysis.get('has_high_signal_density', False):
            return True
        
        # Core FLOAT signals present
        core_patterns = pattern_analysis.get('core_float_patterns', {})
        if any(pattern.get('count', 0) > 0 for pattern in core_patterns.values()):
            return True
        
        # Persona annotations
        persona_analysis = pattern_analysis.get('persona_analysis', {})
        if persona_analysis.get('has_persona_system', False):
            return True
        
        # BBS heritage patterns
        bbs_heritage = pattern_analysis.get('bbs_heritage', {})
        if any(pattern.get('has_pattern', False) for pattern in bbs_heritage.values()):
            return True
        
        return False
    
    def get_content_complexity_assessment(self, pattern_analysis: Dict) -> str:
        """
        Classifies the complexity of analyzed content as 'low', 'medium', or 'high' based on word count, signal density, document structure, and platform references.
        
        Parameters:
            pattern_analysis (Dict): The analysis results containing word count, signal density, document structure, and platform integration data.
        
        Returns:
            str: The complexity classification of the content ('low', 'medium', or 'high').
        """
        word_count = pattern_analysis.get('word_count', 0)
        signal_density = pattern_analysis.get('signal_analysis', {}).get('signal_density_per_100_words', 0)
        
        structure = pattern_analysis.get('document_structure', {})
        code_density = structure.get('code', {}).get('code_density', 0)
        heading_count = structure.get('headings', {}).get('count', 0)
        
        # Calculate complexity score
        complexity_score = 0
        
        # Word count factor
        if word_count > 2000:
            complexity_score += 2
        elif word_count > 500:
            complexity_score += 1
        
        # Signal density factor
        if signal_density > 5:
            complexity_score += 2
        elif signal_density > 2:
            complexity_score += 1
        
        # Structure factor
        if code_density > 0.1 or heading_count > 10:
            complexity_score += 1
        
        # Platform integration
        platform_refs = pattern_analysis.get('platform_integration', {}).get('total_platform_references', 0)
        if platform_refs > 3:
            complexity_score += 1
        
        # Classify based on score
        if complexity_score >= 4:
            return 'high'
        elif complexity_score >= 2:
            return 'medium'
        else:
            return 'low'
    
    def extract_actionable_insights(self, pattern_analysis: Dict) -> List[Dict]:
        """
        Extracts actionable insights from the provided pattern analysis, including high-priority action items, FLOAT dispatch patterns, cross-reference opportunities, and platform integration suggestions.
        
        Parameters:
            pattern_analysis (Dict): The comprehensive pattern analysis result from content analysis.
        
        Returns:
            List[Dict]: A list of actionable insight dictionaries, each containing type, priority, content, and source fields.
        """
        insights = []
        
        # Action items from document structure
        structure = pattern_analysis.get('document_structure', {})
        action_items = structure.get('action_items', {}).get('items', [])
        for item in action_items[:5]:  # Limit to 5 most important
            insights.append({
                'type': 'action_item',
                'priority': 'high',
                'content': item,
                'source': 'document_structure_analysis'
            })
        
        # FLOAT dispatch patterns
        core_patterns = pattern_analysis.get('core_float_patterns', {})
        dispatch_data = core_patterns.get('float_dispatch', {})
        if dispatch_data.get('has_pattern', False):
            for match in dispatch_data.get('matches', [])[:3]:
                insights.append({
                    'type': 'float_dispatch',
                    'priority': 'high',
                    'content': f"Process dispatch: {match}",
                    'source': 'float_dispatch_detection'
                })
        
        # Cross-reference opportunities
        cross_ref = pattern_analysis.get('cross_reference_potential', {})
        if cross_ref.get('cross_reference_score', 0) > 0.5:
            insights.append({
                'type': 'cross_reference',
                'priority': 'medium',
                'content': 'High cross-reference potential - consider linking to related content',
                'source': 'cross_reference_analysis'
            })
        
        # Platform integration opportunities
        platform = pattern_analysis.get('platform_integration', {})
        if platform.get('has_platform_integration', False):
            platforms = platform.get('detected_platforms', [])
            if platforms:
                insights.append({
                    'type': 'platform_integration',
                    'priority': 'medium',
                    'content': f"Integrate with platforms: {', '.join(platforms[:3])}",
                    'source': 'platform_integration_analysis'
                })
        
        return insights
    
    def _initialize_enhanced_patterns(self) -> Dict:
        """
        Creates and returns a dictionary of compiled regular expressions for detecting core and extended FLOAT patterns, inline annotations, and line-level markers across all supported content types.
        """
        return {
            # Core FLOAT signals (existing + enhanced)
            'ctx_markers': re.compile(r'ctx::\s*([^\n]+)', re.IGNORECASE),
            'highlight_markers': re.compile(r'highlight::\s*([^\n]+)', re.IGNORECASE),
            'signal_markers': re.compile(r'signal::\s*([^\n]+)', re.IGNORECASE),
            'float_dispatch': re.compile(r'float\.dispatch\s*\([^)]*\)', re.IGNORECASE),
            'sysop_comments': re.compile(r'\[sysop::([^\]]+)\]', re.IGNORECASE),
            
            # Extended FLOAT annotation grammar
            'expand_on': re.compile(r'expandOn::\s*([^\n]+)', re.IGNORECASE),
            'relates_to': re.compile(r'relatesTo::\s*([^\n]+)', re.IGNORECASE),
            'remember_when': re.compile(r'rememberWhen::\s*([^\n]+)', re.IGNORECASE),
            'story_time': re.compile(r'storyTime::\s*([^\n]+)', re.IGNORECASE),
            'echo_copy': re.compile(r'echoCopy::\s*([^\n]*?)(?:\s*::|$)', re.IGNORECASE),
            'mood_markers': re.compile(r'\[mood::\s*([^\]]*)\]', re.IGNORECASE),
            
            # Inline patterns (bracketed format)
            'inline_expand_on': re.compile(r'\[expandOn::\s*([^\]]+)\]', re.IGNORECASE),
            'inline_relates_to': re.compile(r'\[relatesTo::\s*([^\]]+)\]', re.IGNORECASE),
            'inline_connect_to': re.compile(r'\[connectTo::\s*([^\]]+)\]', re.IGNORECASE),
            'inline_remember_when': re.compile(r'\[rememberWhen::\s*([^\]]+)\]', re.IGNORECASE),
            'inline_generic': re.compile(r'\[([a-zA-Z][a-zA-Z0-9]*)::\s*([^\]]+)\]'),
            
            # Line-level :: patterns
            'line_mood': re.compile(r'^\s*[-*]?\s*mood::\s*(.+)$', re.MULTILINE | re.IGNORECASE),
            'line_soundtrack': re.compile(r'^\s*[-*]?\s*soundtrack::\s*(.+)$', re.MULTILINE | re.IGNORECASE),
            'line_body_check': re.compile(r'^\s*[-*]?\s*bodyCheck::\s*(.+)$', re.MULTILINE | re.IGNORECASE),
            'line_impact': re.compile(r'^\s*[-*]?\s*impact::\s*(.+)$', re.MULTILINE | re.IGNORECASE),
            'line_boundary': re.compile(r'^\s*[-*]?\s*boundary::\s*(.+)$', re.MULTILINE | re.IGNORECASE),
            'line_progress': re.compile(r'^\s*[-*]?\s*progress::\s*(.+)$', re.MULTILINE | re.IGNORECASE),
        }
    
    def _initialize_tripartite_patterns(self) -> Dict:
        """
        Return sets of keywords used to identify concept, framework, and metaphor domains for tripartite content classification.
        """
        return {
            'concept_indicators': {
                'theory', 'principle', 'concept', 'definition', 'understanding',
                'knowledge', 'abstract', 'idea', 'notion', 'philosophy'
            },
            'framework_indicators': {
                'process', 'method', 'framework', 'system', 'workflow',
                'procedure', 'algorithm', 'implementation', 'steps', 'protocol'
            },
            'metaphor_indicators': {
                'like', 'metaphor', 'analogy', 'similar', 'reminds',
                'experience', 'feeling', 'intuition', 'sense', 'imagine'
            }
        }
    
    def _extract_core_float_patterns(self, content: str) -> Dict:
        """
        Extracts core FLOAT patterns from the provided content using predefined regular expressions.
        
        Returns:
            A dictionary mapping each core pattern name to its count, a limited list of matches (up to 10), and a presence flag.
        """
        results = {}
        
        for pattern_name, pattern_regex in self.patterns.items():
            if pattern_name.startswith(('ctx_', 'highlight_', 'signal_', 'float_', 'sysop_')):
                matches = pattern_regex.findall(content)
                results[pattern_name] = {
                    'count': len(matches),
                    'matches': matches[:10],  # Limit stored matches
                    'has_pattern': len(matches) > 0
                }
        
        return results
    
    def _extract_extended_float_patterns(self, content: str) -> Dict:
        """
        Extracts extended FLOAT patterns from the provided content.
        
        Searches for a predefined set of extended FLOAT patterns using compiled regular expressions. For each pattern, returns the count of matches, up to five example matches, and a flag indicating presence.
        
        Returns:
            Dictionary mapping each extended pattern name to its match count, sample matches, and presence flag.
        """
        results = {}
        
        extended_patterns = ['expand_on', 'relates_to', 'remember_when', 'story_time', 
                           'echo_copy', 'mood_markers', 'inline_expand_on', 'inline_relates_to',
                           'inline_connect_to', 'inline_remember_when', 'inline_generic',
                           'line_mood', 'line_soundtrack', 'line_body_check', 'line_impact',
                           'line_boundary', 'line_progress']
        
        for pattern_name in extended_patterns:
            if pattern_name in self.patterns:
                pattern_regex = self.patterns[pattern_name]
                matches = pattern_regex.findall(content)
                results[pattern_name] = {
                    'count': len(matches),
                    'matches': matches[:5],  # Limit stored matches
                    'has_pattern': len(matches) > 0
                }
        
        return results
    
    def _extract_persona_patterns(self, content: str) -> Dict:
        """
        Extracts persona annotation patterns from the content and summarizes their presence.
        
        Returns:
            A dictionary containing counts and sample matches for each persona type, total annotations found, whether any persona system is present, the dominant persona (if any), and the number of distinct personas detected.
        """
        persona_patterns = [
            ('sysop', r'\[sysop::([^\]]+)\]'),
            ('karen', r'\[karen::([^\]]+)\]'),
            ('qtb', r'\[qtb::([^\]]+)\]'),
            ('lf1m', r'\[lf1m::([^\]]+)\]'),
            ('rawEvan', r'\[rawEvan::([^\]]+)\]'),
            ('any', r'\[any::([^\]]+)\]')
        ]
        
        persona_data = {}
        total_annotations = 0
        dominant_persona = None
        max_count = 0
        
        for persona_name, pattern in persona_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            count = len(matches)
            total_annotations += count
            
            persona_data[persona_name] = {
                'count': count,
                'matches': matches[:3],  # Store first 3 matches
                'has_annotations': count > 0
            }
            
            if count > max_count:
                max_count = count
                dominant_persona = persona_name
        
        return {
            'personas': persona_data,
            'total_persona_annotations': total_annotations,
            'has_persona_system': total_annotations > 0,
            'dominant_persona': dominant_persona if max_count > 0 else None,
            'persona_diversity': len([p for p in persona_data.values() if p['has_annotations']])
        }
    
    def _analyze_document_structure(self, content: str) -> Dict:
        """
        Analyze the structural elements and formatting of the document content.
        
        Returns a dictionary summarizing headings (count, levels, titles), list items (bullet and numbered), code blocks and inline code (with density), detected action items, and an overall structure complexity assessment.
        """
        lines = content.split('\n')
        
        # Headings analysis
        heading_pattern = re.compile(r'^(#{1,6})\s+(.+)$', re.MULTILINE)
        headings = heading_pattern.findall(content)
        
        # Lists analysis
        list_items = re.findall(r'^\s*[-*+]\s+(.+)$', content, re.MULTILINE)
        numbered_items = re.findall(r'^\s*\d+\.\s+(.+)$', content, re.MULTILINE)
        
        # Code blocks
        code_blocks = re.findall(r'```[\s\S]*?```', content)
        inline_code = re.findall(r'`([^`]+)`', content)
        
        # Action items
        action_patterns = [
            r'TODO:?\s*(.+)',
            r'FIXME:?\s*(.+)',
            r'ACTION:?\s*(.+)',
            r'- \[ \]\s*(.+)',  # Markdown checkboxes
        ]
        
        action_items = []
        for pattern in action_patterns:
            action_items.extend(re.findall(pattern, content, re.IGNORECASE))
        
        return {
            'headings': {
                'count': len(headings),
                'levels': [len(level) for level, _ in headings],
                'titles': [title for _, title in headings[:5]]
            },
            'lists': {
                'bullet_items': len(list_items),
                'numbered_items': len(numbered_items),
                'total_list_items': len(list_items) + len(numbered_items)
            },
            'code': {
                'code_blocks': len(code_blocks),
                'inline_code': len(inline_code),
                'code_density': (len(''.join(code_blocks)) + len(''.join(inline_code))) / max(len(content), 1)
            },
            'action_items': {
                'count': len(action_items),
                'items': action_items[:10]  # Store first 10
            },
            'structure_complexity': self._calculate_structure_complexity(headings, list_items, code_blocks)
        }
    
    def _detect_platform_integration(self, content: str) -> Dict:
        """
        Detects references to known platform integration patterns within the provided content.
        
        Returns:
            dict: A dictionary containing counts and examples of detected platform references, total number of platform mentions, a flag indicating if any platform was detected, and a list of detected platform names.
        """
        platforms = {
            'lovable': r'lovable\.dev',
            'v0': r'v0\.dev',
            'magic_patterns': r'magicpatterns\.com',
            'github': r'github\.com/[\w-]+/[\w-]+',
            'claude': r'claude\.ai',
            'chatgpt': r'chat\.openai\.com'
        }
        
        detected = {}
        total_refs = 0
        
        for platform, pattern in platforms.items():
            matches = re.findall(pattern, content, re.IGNORECASE)
            count = len(matches)
            total_refs += count
            
            detected[platform] = {
                'count': count,
                'matches': matches[:3],
                'detected': count > 0
            }
        
        return {
            'platforms': detected,
            'total_platform_references': total_refs,
            'has_platform_integration': total_refs > 0,
            'detected_platforms': [name for name, data in detected.items() if data['detected']]
        }
    
    def _calculate_signal_analysis(self, analysis: Dict) -> Dict:
        """
        Compute signal analysis metrics including total signals, signal density, and signal-to-noise ratio based on extracted pattern counts.
        
        Parameters:
            analysis (Dict): Dictionary containing pattern extraction results and word count.
        
        Returns:
            Dict: Metrics including total core signals, extended patterns, persona annotations, overall signal count, signal density per 100 words, high density flag, and signal-to-noise ratio.
        """
        word_count = analysis.get('word_count', 1)
        
        # Count core signals
        core_signals = 0
        core_patterns = analysis.get('core_float_patterns', {})
        for pattern_data in core_patterns.values():
            core_signals += pattern_data.get('count', 0)
        
        # Count extended signals
        extended_signals = 0
        extended_patterns = analysis.get('extended_float_patterns', {})
        for pattern_data in extended_patterns.values():
            extended_signals += pattern_data.get('count', 0)
        
        # Count persona annotations
        persona_signals = analysis.get('persona_analysis', {}).get('total_persona_annotations', 0)
        
        total_signals = core_signals + extended_signals + persona_signals
        signal_density_per_100_words = (total_signals / word_count) * 100
        
        return {
            'total_core_signals': core_signals,
            'total_extended_patterns': extended_signals,
            'total_persona_annotations': persona_signals,
            'total_signals': total_signals,
            'signal_density_per_100_words': signal_density_per_100_words,
            'has_high_signal_density': signal_density_per_100_words > 2.0,
            'signal_to_noise_ratio': total_signals / max(word_count, 1)
        }
    
    def _classify_tripartite_domain(self, content: str, analysis: Dict) -> Dict:
        """
        Classifies the content into conceptual domains of concept, framework, or metaphor based on keyword indicators.
        
        Returns:
            A dictionary containing normalized domain scores, the primary domain, confidence level, and a flag indicating if the content spans multiple domains.
        """
        content_lower = content.lower()
        
        # Score each domain
        scores = {
            'concept': 0,
            'framework': 0,
            'metaphor': 0
        }
        
        # Check indicators
        for domain, indicators in self.tripartite_patterns.items():
            domain_name = domain.replace('_indicators', '')
            if domain_name in scores:
                for indicator in indicators:
                    count = content_lower.count(indicator)
                    scores[domain_name] += count
        
        # Normalize scores
        total_score = sum(scores.values())
        if total_score > 0:
            normalized_scores = {k: v / total_score for k, v in scores.items()}
        else:
            normalized_scores = {'concept': 1.0, 'framework': 0.0, 'metaphor': 0.0}
        
        # Determine primary domain
        primary_domain = max(normalized_scores, key=normalized_scores.get)
        confidence = normalized_scores[primary_domain]
        
        return {
            'scores': normalized_scores,
            'primary_domain': primary_domain,
            'confidence': confidence,
            'is_multi_domain': len([s for s in normalized_scores.values() if s > 0.3]) > 1
        }
    
    def _analyze_cross_reference_potential(self, content: str, analysis: Dict) -> Dict:
        """
        Evaluates the content's potential for cross-referencing based on detected signals, platform references, document structure, and presence of links or mentions.
        
        Parameters:
            content (str): The text content to analyze.
            analysis (Dict): The existing pattern analysis results for the content.
        
        Returns:
            Dict: A dictionary containing the cross-reference score (0.0–1.0), the number of detected links or mentions, and a flag indicating high cross-reference potential.
        """
        # Factors that increase cross-reference potential
        score = 0.0
        
        # FLOAT patterns increase potential
        total_signals = analysis.get('signal_analysis', {}).get('total_signals', 0)
        if total_signals > 0:
            score += min(total_signals * 0.1, 0.5)
        
        # Platform references
        platform_refs = analysis.get('platform_integration', {}).get('total_platform_references', 0)
        if platform_refs > 0:
            score += min(platform_refs * 0.05, 0.3)
        
        # Document structure
        headings = analysis.get('document_structure', {}).get('headings', {}).get('count', 0)
        if headings > 2:
            score += 0.2
        
        # Links and references in content
        link_patterns = [
            r'\[\[([^\]]+)\]\]',  # Wiki links
            r'\[([^\]]+)\]\([^)]+\)',  # Markdown links
            r'@\w+',  # Mentions
        ]
        
        link_count = 0
        for pattern in link_patterns:
            link_count += len(re.findall(pattern, content))
        
        if link_count > 0:
            score += min(link_count * 0.05, 0.4)
        
        return {
            'cross_reference_score': min(score, 1.0),
            'link_count': link_count,
            'has_high_potential': score > 0.5
        }
    
    def _detect_bbs_heritage_patterns(self, content: str) -> Dict:
        """
        Detects legacy BBS-related patterns such as 'float.dis', 'float.diis', 'file_id.diz', and 'float.rfc' within the provided content.
        
        Returns:
            A dictionary mapping each BBS heritage pattern to its count, up to three example matches, and a presence flag.
        """
        patterns = {
            'float_dis': re.compile(r'float\.dis', re.IGNORECASE),
            'float_diis': re.compile(r'float\.diis', re.IGNORECASE),
            'file_id_diz': re.compile(r'file_id\.diz', re.IGNORECASE),
            'float_rfc': re.compile(r'float\.rfc', re.IGNORECASE)
        }
        
        results = {}
        for pattern_name, pattern_regex in patterns.items():
            matches = pattern_regex.findall(content)
            results[pattern_name] = {
                'count': len(matches),
                'matches': matches[:3],
                'has_pattern': len(matches) > 0
            }
        
        return results
    
    def _calculate_structure_complexity(self, headings: List, list_items: List, code_blocks: List) -> str:
        """
        Assess the structural complexity of content based on the number of headings, list items, and code blocks.
        
        Returns:
            str: 'low', 'medium', or 'high' indicating the overall structure complexity.
        """
        complexity_score = 0
        
        if len(headings) > 5:
            complexity_score += 1
        if len(list_items) > 10:
            complexity_score += 1
        if len(code_blocks) > 3:
            complexity_score += 1
        
        if complexity_score >= 2:
            return 'high'
        elif complexity_score == 1:
            return 'medium'
        else:
            return 'low'
    
    def _count_total_patterns(self, analysis_results: Dict) -> int:
        """
        Return the total number of patterns detected across core FLOAT patterns, extended patterns, and persona annotations.
        
        Parameters:
            analysis_results (Dict): The analysis results containing pattern detection data.
        
        Returns:
            int: The total count of all detected patterns and annotations.
        """
        total = 0
        
        # Core patterns
        core_patterns = analysis_results.get('core_float_patterns', {})
        for pattern_data in core_patterns.values():
            total += pattern_data.get('count', 0)
        
        # Extended patterns
        extended_patterns = analysis_results.get('extended_float_patterns', {})
        for pattern_data in extended_patterns.values():
            total += pattern_data.get('count', 0)
        
        # Persona annotations
        total += analysis_results.get('persona_analysis', {}).get('total_persona_annotations', 0)
        
        return total
    
    def _empty_analysis_result(self) -> Dict:
        """
        Return a default analysis result dictionary representing empty or invalid content.
        
        Returns:
            Dict: An analysis result with zero counts and default values for all analysis categories.
        """
        return {
            'content_length': 0,
            'word_count': 0,
            'line_count': 0,
            'core_float_patterns': {},
            'extended_float_patterns': {},
            'persona_analysis': {
                'personas': {},
                'total_persona_annotations': 0,
                'has_persona_system': False
            },
            'signal_analysis': {
                'total_signals': 0,
                'signal_density_per_100_words': 0,
                'has_high_signal_density': False
            },
            'tripartite_classification': {
                'primary_domain': 'concept',
                'confidence': 0.0,
                'scores': {'concept': 1.0, 'framework': 0.0, 'metaphor': 0.0}
            }
        }