"""
Enhanced integration system for FLOAT ecosystem
Bridges daemon, daily context, and conversation processing
Now includes sophisticated pattern detection from tripartite chunker
"""

import re
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
from urllib.parse import urlparse

try:
    import frontmatter
    FRONTMATTER_AVAILABLE = True
except ImportError:
    FRONTMATTER_AVAILABLE = False
    frontmatter = None

class EnhancedSystemIntegration:
    """Enhanced integration between daemon and daily context systems"""
    
    def __init__(self, daemon, logger=None):
        self.daemon = daemon
        self.logger = logger or daemon.logger
        self.enhanced_context = None
        self.vault_path = daemon.vault_path
        self.config = daemon.config
        
        # Initialize paths
        self.conversation_dis_path = Path(self.config.get('conversation_dis_path', 
                                                         str(self.vault_path / 'FLOAT.conversations')))
        self.conversation_dis_path.mkdir(exist_ok=True)
        
        # Initialize enhanced pattern detector
        self._initialize_enhanced_pattern_detector()
        
        # Initialize enhanced context if available
        self._initialize_enhanced_context()
        
        # Initialize cross-reference system
        self._initialize_cross_reference_system()
        
        # Initialize enhanced conversation dis generator
        self._initialize_conversation_dis_system()
        
        # Initialize temporal query capabilities
        self._initialize_temporal_features()
        
        # Conversation detection patterns
        self._initialize_conversation_patterns()
    
    def _initialize_enhanced_pattern_detector(self):
        """Initialize enhanced pattern detector from tripartite chunker"""
        try:
            from enhanced_pattern_detector import EnhancedFloatPatternDetector
            self.pattern_detector = EnhancedFloatPatternDetector()
            self.logger.info("Enhanced pattern detector initialized")
        except Exception as e:
            self.logger.warning(f"Enhanced pattern detector not available: {e}")
            self.pattern_detector = None
    
    def _initialize_enhanced_context(self):
        """Initialize enhanced daily context if available"""
        try:
            if hasattr(self.daemon.components.get('context'), 'create_comprehensive_daily_summary_enhanced'):
                self.enhanced_context = self.daemon.components['context']
                self.logger.info("Enhanced daily context integration enabled")
            else:
                self.logger.warning("Enhanced daily context not available, using basic integration")
        except Exception as e:
            self.logger.error(f"Enhanced context initialization failed: {e}")
        
        # Initialize Ollama summarizer if enabled
        self._initialize_ollama_summarizer()
    
    def _initialize_ollama_summarizer(self):
        """Initialize Ollama summarizer for enhanced content analysis"""
        try:
            enable_ollama = self.config.get('enable_ollama', False) or \
                          self.daemon.config.get('enable_ollama', False)
            
            if enable_ollama:
                from ollama_enhanced_float_summarizer import OllamaFloatSummarizer
                self.ollama_summarizer = OllamaFloatSummarizer()
                self.ollama_enabled = True
                self.logger.info("Ollama summarizer initialized for enhanced analysis")
            else:
                self.ollama_summarizer = None
                self.ollama_enabled = False
                self.logger.info("Ollama summarizer disabled")
        except Exception as e:
            self.logger.warning(f"Ollama summarizer initialization failed: {e}")
            self.ollama_summarizer = None
            self.ollama_enabled = False
    
    def _initialize_cross_reference_system(self):
        """Initialize cross-reference system"""
        try:
            from cross_reference_system import CrossReferenceSystem
            chroma_client = self.daemon.components['context'].client
            self.cross_ref_system = CrossReferenceSystem(
                Path(self.vault_path),  # Ensure it's a Path object
                chroma_client,
                self.config.config,
                self.logger
            )
            self.logger.info("Cross-reference system initialized")
        except Exception as e:
            self.logger.warning(f"Cross-reference system not available: {e}")
            self.cross_ref_system = None
    
    def _initialize_conversation_dis_system(self):
        """Initialize enhanced conversation dis generation system"""
        try:
            from conversation_dis_enhanced import ConversationDisEnhanced
            self.conversation_dis_enhanced = ConversationDisEnhanced(
                self.daemon.components.get('dis_generator'),
                self.vault_path,
                self.config.config,
                self.logger
            )
            self.logger.info("Enhanced conversation dis system initialized")
        except Exception as e:
            self.logger.warning(f"Enhanced conversation dis system not available: {e}")
            self.conversation_dis_enhanced = None
        
        # Initialize streamlined dis generator (Issue #4)
        try:
            from streamlined_dis_template import StreamlinedFloatDisGenerator
            self.streamlined_dis_generator = StreamlinedFloatDisGenerator()
            self.logger.info("Streamlined .dis generator initialized (Issue #4: 80% size reduction)")
        except Exception as e:
            self.logger.warning(f"Streamlined .dis generator not available: {e}")
            self.streamlined_dis_generator = None
    
    def _initialize_conversation_patterns(self):
        """Initialize patterns for detecting conversation content"""
        self.conversation_patterns = {
            'claude_ai': re.compile(r'claude\.ai', re.IGNORECASE),
            'chatgpt': re.compile(r'chatgpt\.com|chat\.openai\.com', re.IGNORECASE),
            'conversation_export': re.compile(r'conversation.*export|chat.*export', re.IGNORECASE),
            'dialogue_markers': re.compile(r'^(Human|Assistant|User|AI|Claude|GPT):', re.MULTILINE),
            'conversation_id': re.compile(r'conversation[_-]?id[:\s]*([a-zA-Z0-9_-]+)', re.IGNORECASE),
            'chat_url': re.compile(r'https?://(?:claude\.ai|chatgpt\.com|chat\.openai\.com)/[^\s]+', re.IGNORECASE)
        }
    
    def process_file_with_enhanced_integration(self, file_path: Path) -> Dict:
        """Process file with full enhanced ecosystem integration"""
        
        # Step 1: Basic file processing through daemon
        result = self.daemon.process_dropzone_file(file_path)
        
        if not result or not result.get('file_analysis'):
            return result
        
        file_analysis = result['file_analysis']
        
        # Step 2: Enhanced analysis and routing
        enhanced_analysis = self._perform_enhanced_analysis(file_analysis)
        file_analysis['enhanced_analysis'] = enhanced_analysis
        
        # Step 3: Enhanced daily context integration
        if self.enhanced_context:
            self._integrate_with_enhanced_daily_context(file_analysis, enhanced_analysis)
        
        # Step 4: Tripartite collection routing
        self._route_to_tripartite_collections(file_analysis, enhanced_analysis)
        
        # Step 4.5: Special pattern collection routing
        self._route_to_special_pattern_collections(file_analysis, enhanced_analysis)
        
        # Step 5: Cross-reference generation
        if self.cross_ref_system:
            cross_references = self.cross_ref_system.generate_cross_references(file_analysis, enhanced_analysis)
            file_analysis['cross_references'] = cross_references
        else:
            self.logger.warning("Cross-reference system not available - skipping cross-reference generation")
            file_analysis['cross_references'] = {'vault_references': [], 'chroma_references': [], 'conversation_links': [], 'topic_connections': []}
        
        # Step 6: Enhanced .dis file generation
        if enhanced_analysis.get('is_conversation'):
            if self.conversation_dis_enhanced:
                conversation_dis_path = self.conversation_dis_enhanced.generate_conversation_dis(file_analysis, enhanced_analysis)
            else:
                conversation_dis_path = self._generate_conversation_dis_file(file_analysis, enhanced_analysis)
            file_analysis['conversation_dis_path'] = conversation_dis_path
        elif enhanced_analysis.get('content_classification') == 'daily_log':
            # Generate enhanced daily log .dis file
            daily_log_dis_path = self._generate_daily_log_dis_file(file_analysis, enhanced_analysis)
            file_analysis['daily_log_dis_path'] = daily_log_dis_path
        
        # Update result with enhanced data
        result['file_analysis'] = file_analysis
        return result
    
    def _perform_enhanced_analysis(self, file_analysis: Dict) -> Dict:
        """Perform enhanced content analysis using sophisticated pattern detection"""
        content = file_analysis.get('content', '')
        metadata = file_analysis.get('metadata', {})
        basic_analysis = file_analysis.get('analysis', {})
        file_path = Path(metadata.get('file_path', '')) if metadata.get('file_path') else None
        
        enhanced = {
            'is_conversation': False,
            'conversation_platform': 'unknown',
            'conversation_id': 'unknown',
            'participants': [],
            'topics': [],
            'signal_density': 0.0,
            'content_classification': 'unknown',
            'tripartite_routing': [],
            'pattern_analysis': {}
        }
        
        if not content:
            return enhanced
        
        # Enhanced pattern detection using tripartite chunker patterns
        if self.pattern_detector:
            pattern_analysis = self.pattern_detector.extract_comprehensive_patterns(content, file_path)
            enhanced['pattern_analysis'] = pattern_analysis
            
            # Use tripartite classification
            tripartite = pattern_analysis.get('tripartite_classification', {})
            enhanced['tripartite_domain'] = tripartite.get('primary_domain', 'concept')
            enhanced['tripartite_confidence'] = tripartite.get('confidence', 0.0)
            enhanced['tripartite_scores'] = tripartite.get('scores', {})
            
            # Enhanced signal density from pattern analysis
            signal_analysis = pattern_analysis.get('signal_analysis', {})
            enhanced['signal_density'] = signal_analysis.get('signal_density_per_100_words', 0.0) / 100
            enhanced['total_signals'] = signal_analysis.get('total_core_signals', 0)
            enhanced['extended_patterns'] = signal_analysis.get('total_extended_patterns', 0)
            enhanced['has_high_signal_density'] = signal_analysis.get('has_high_signal_density', False)
            
            # Content complexity assessment
            enhanced['content_complexity'] = self.pattern_detector.get_content_complexity_assessment(pattern_analysis)
            enhanced['is_high_priority'] = self.pattern_detector.is_high_priority_content(pattern_analysis)
            
            # Actionable insights
            enhanced['actionable_insights'] = self.pattern_detector.extract_actionable_insights(pattern_analysis)
            
            # Platform integration analysis
            platform_analysis = pattern_analysis.get('platform_integration', {})
            enhanced['has_platform_integration'] = platform_analysis.get('has_platform_integration', False)
            enhanced['platform_references'] = platform_analysis.get('total_platform_references', 0)
            
            # Persona analysis
            persona_analysis = pattern_analysis.get('persona_analysis', {})
            enhanced['has_persona_annotations'] = persona_analysis.get('has_persona_system', False)
            enhanced['persona_count'] = persona_analysis.get('total_persona_annotations', 0)
            enhanced['dominant_persona'] = persona_analysis.get('dominant_persona')
            
            # Cross-reference potential
            cross_ref = pattern_analysis.get('cross_reference_potential', {})
            enhanced['cross_reference_score'] = cross_ref.get('cross_reference_score', 0.0)
            enhanced['has_cross_reference_potential'] = cross_ref.get('cross_reference_score', 0.0) > 0.3
            
            # Document structure analysis
            structure = pattern_analysis.get('document_structure', {})
            enhanced['document_structure'] = {
                'heading_count': structure.get('headings', {}).get('count', 0),
                'list_density': structure.get('lists', {}).get('total_list_items', 0),
                'code_density': structure.get('code', {}).get('code_density', 0.0),
                'action_items': structure.get('action_items', {}).get('count', 0)
            }
            
            # FLOAT-specific patterns
            core_patterns = pattern_analysis.get('core_float_patterns', {})
            extended_patterns = pattern_analysis.get('extended_float_patterns', {})
            
            enhanced['float_patterns'] = {
                'ctx_markers': core_patterns.get('ctx_markers', {}).get('count', 0),
                'highlight_markers': core_patterns.get('highlight_markers', {}).get('count', 0),
                'signal_markers': core_patterns.get('signal_markers', {}).get('count', 0),
                'float_dispatch': core_patterns.get('float_dispatch', {}).get('has_pattern', False),
                'sysop_comments': core_patterns.get('sysop_comments', {}).get('count', 0),
                'expand_on': extended_patterns.get('expand_on', {}).get('count', 0),
                'relates_to': extended_patterns.get('relates_to', {}).get('count', 0),
                'remember_when': extended_patterns.get('remember_when', {}).get('count', 0),
                'story_time': extended_patterns.get('story_time', {}).get('count', 0),
                'mood_markers': extended_patterns.get('mood_markers', {}).get('count', 0)
            }
        else:
            # Fallback to basic analysis
            self.logger.warning("Using fallback analysis - enhanced pattern detector not available")
            enhanced = self._perform_basic_enhanced_analysis(content, metadata, basic_analysis)
        
        # Content classification FIRST - before conversation detection
        enhanced['content_classification'] = self._classify_content_type(content, basic_analysis)
        
        # Only run conversation detection if it's NOT a daily log
        if enhanced['content_classification'] != 'daily_log':
            conversation_analysis = self._analyze_conversation_content(content, metadata)
            enhanced.update(conversation_analysis)
        else:
            # Set default conversation analysis for daily logs
            enhanced.update({
                'is_conversation': False,
                'conversation_platform': 'unknown',
                'conversation_id': 'unknown',
                'participants': [],
                'message_count': 0
            })
        
        # Topic extraction
        enhanced['topics'] = self._extract_topics(content)
        
        # Tripartite routing decisions
        enhanced['tripartite_routing'] = self._determine_tripartite_routing(content, enhanced)
        
        # Special handling for daily logs
        if enhanced.get('content_classification') == 'daily_log':
            enhanced.update(self._analyze_daily_log_content(content, metadata))
        
        return enhanced
    
    def _perform_basic_enhanced_analysis(self, content: str, metadata: Dict, basic_analysis: Dict) -> Dict:
        """Fallback basic analysis when enhanced pattern detector is not available"""
        enhanced = {
            'tripartite_domain': 'concept',
            'tripartite_confidence': 0.5,
            'tripartite_scores': {'concept': 1, 'framework': 0, 'metaphor': 0},
            'signal_density': 0.0,
            'total_signals': 0,
            'extended_patterns': 0,
            'has_high_signal_density': False,
            'content_complexity': 'medium',
            'is_high_priority': False,
            'actionable_insights': [],
            'has_platform_integration': False,
            'platform_references': 0,
            'has_persona_annotations': False,
            'persona_count': 0,
            'dominant_persona': None,
            'cross_reference_score': 0.0,
            'has_cross_reference_potential': False,
            'document_structure': {
                'heading_count': 0,
                'list_density': 0,
                'code_density': 0.0,
                'action_items': 0
            },
            'float_patterns': {
                'ctx_markers': basic_analysis.get('ctx_count', 0),
                'highlight_markers': basic_analysis.get('highlight_count', 0),
                'signal_markers': 0,
                'float_dispatch': False,
                'sysop_comments': 0,
                'expand_on': 0,
                'relates_to': 0,
                'remember_when': 0,
                'story_time': 0,
                'mood_markers': 0
            }
        }
        
        # Basic signal density calculation
        ctx_count = basic_analysis.get('ctx_count', 0)
        highlight_count = basic_analysis.get('highlight_count', 0)
        word_count = basic_analysis.get('word_count', 1)
        enhanced['signal_density'] = (ctx_count + highlight_count) / word_count
        enhanced['total_signals'] = ctx_count + highlight_count
        
        return enhanced
    
    def is_daily_log(self, content: str, metadata: Dict) -> bool:
        """Check if content is a daily log rather than a conversation"""
        
        # Priority 1: Check frontmatter for definitive daily log indicators
        if content.startswith('---'):
            frontmatter_end = content.find('---', 3)
            if frontmatter_end > 0:
                frontmatter = content[3:frontmatter_end]
                
                # Check for explicit daily log frontmatter patterns
                if any(pattern in frontmatter for pattern in [
                    'type: log',
                    'uid: log::',
                    'title: 2025-',  # Daily log title pattern
                    '- daily',       # daily tag
                    'mood: ',        # mood field
                    'soundtrack: '   # soundtrack field
                ]):
                    return True
                
                # Check for weekly/quarterly patterns
                if re.search(r'week: \d{4}-W\d{2}', frontmatter) or \
                   re.search(r'quarter: \d{4}-Q[1-4]', frontmatter) or \
                   re.search(r'y\d{4}/q[1-4]/w\d{2}', frontmatter):
                    return True
        
        # Priority 2: Check filename pattern
        filename = metadata.get('filename', '')
        if re.match(r'^\d{4}-\d{2}-\d{2}\.md$', filename):
            return True
        
        # Priority 3: Check content markers
        content_lower = content.lower()
        daily_log_markers = [
            'type: log',
            'daily log',
            '## brain boot',
            '## body boot',
            '## daily tasks',
            '## today\'s focus',
            '<< [[float.logs/',
            '>> [[float.logs/'
        ]
        
        if any(marker in content_lower for marker in daily_log_markers):
            return True
        
        # Priority 4: Check for daily log structure patterns
        if '## Brain Boot' in content and '## Body Boot' in content:
            return True
        
        # Priority 5: Check for navigation patterns specific to logs
        if re.search(r'<< \[\[FLOAT\.logs/\d{4}-\d{2}-\d{2}\]\]', content):
            return True
        
        return False
    
    def _extract_daily_log_frontmatter(self, content: str) -> Dict:
        """Extract and parse daily log frontmatter using python-frontmatter library"""
        frontmatter_data = {}
        
        if FRONTMATTER_AVAILABLE and frontmatter:
            try:
                # Parse frontmatter using the library
                post = frontmatter.loads(content)
                metadata = post.metadata
                
                # Extract key fields we care about
                important_fields = ['created', 'uid', 'title', 'type', 'status', 'week', 'quarter', 'mood', 'soundtrack', 'tags']
                
                for field in important_fields:
                    if field in metadata:
                        frontmatter_data[field] = metadata[field]
                
                return frontmatter_data
                
            except Exception as e:
                # Fallback to manual parsing if frontmatter library fails
                if hasattr(self, 'logger') and self.logger:
                    self.logger.warning(f"Frontmatter library parsing failed, using fallback: {e}")
        
        # Fallback manual parsing (existing logic)
        if content.startswith('---'):
            frontmatter_end = content.find('---', 3)
            if frontmatter_end > 0:
                frontmatter_section = content[3:frontmatter_end].strip()
                
                # Parse key frontmatter fields
                for line in frontmatter_section.split('\n'):
                    line = line.strip()
                    if ':' in line and not line.startswith('-'):
                        try:
                            key, value = line.split(':', 1)
                            key = key.strip()
                            value = value.strip().strip('"').strip("'")
                            
                            # Store important fields
                            if key in ['created', 'uid', 'title', 'type', 'status', 'week', 'quarter', 'mood', 'soundtrack']:
                                frontmatter_data[key] = value
                        except ValueError:
                            continue
                
                # Extract tags separately
                if 'tags:' in frontmatter_section:
                    tags_section = frontmatter_section[frontmatter_section.find('tags:'):].split('\n')
                    tags = []
                    for line in tags_section[1:]:
                        if line.strip().startswith('-'):
                            tag = line.strip().lstrip('-').strip()
                            if tag:
                                tags.append(tag)
                        elif not line.strip() or not line.startswith(' '):
                            break
                    frontmatter_data['tags'] = tags
        
        return frontmatter_data
    
    def _analyze_daily_log_content(self, content: str, metadata: Dict) -> Dict:
        """Analyze daily log content for specific insights"""
        analysis = {
            'daily_log_insights': {},
            'actionable_items': [],
            'mood_indicators': [],
            'productivity_signals': [],
            'learning_notes': [],
            'frontmatter_data': {},
            'ollama_summary': None,
            'ollama_insights': []
        }
        
        # Extract frontmatter data
        frontmatter_data = self._extract_daily_log_frontmatter(content)
        analysis['frontmatter_data'] = frontmatter_data
        
        # Generate Ollama-powered summary and insights if available
        if self.ollama_enabled and self.ollama_summarizer:
            try:
                ollama_analysis = self._generate_ollama_daily_log_analysis(content, frontmatter_data)
                analysis['ollama_summary'] = ollama_analysis.get('summary')
                analysis['ollama_insights'] = ollama_analysis.get('insights', [])
                
                # Enhance extracted items with Ollama insights
                ollama_actionables = ollama_analysis.get('actionable_items', [])
                if ollama_actionables:
                    analysis['actionable_items'].extend(ollama_actionables)
                    
                ollama_mood = ollama_analysis.get('mood_analysis')
                if ollama_mood:
                    analysis['mood_indicators'].append(f"Ollama analysis: {ollama_mood}")
                    
            except Exception as e:
                if hasattr(self, 'logger') and self.logger:
                    self.logger.warning(f"Ollama daily log analysis failed: {e}")
                analysis['ollama_summary'] = "Ollama analysis unavailable"
        
        # Extract actionable items from daily logs
        action_patterns = [
            re.compile(r'(?:TODO|FIXME|ACTION|NEXT):?\s*(.+)', re.IGNORECASE),
            re.compile(r'- \[ \]\s*(.+)'),  # Markdown checkboxes
            re.compile(r'(?:need to|should|must|will)\s+(.+)', re.IGNORECASE),
            re.compile(r'(?:follow up|reach out|contact|schedule)\s+(.+)', re.IGNORECASE)
        ]
        
        for pattern in action_patterns:
            matches = pattern.findall(content)
            analysis['actionable_items'].extend(matches[:5])  # Limit to 5 per pattern
        
        # Extract mood and energy indicators
        mood_patterns = [
            re.compile(r'(?:feeling|mood|energy):\s*([^.\n]+)', re.IGNORECASE),
            re.compile(r'\[mood::\s*([^\]]+)\]', re.IGNORECASE),
            re.compile(r'(?:tired|energetic|focused|distracted|motivated|anxious)\b', re.IGNORECASE)
        ]
        
        for pattern in mood_patterns:
            matches = pattern.findall(content)
            analysis['mood_indicators'].extend(matches[:3])
        
        # Add frontmatter mood if available
        frontmatter_mood = frontmatter_data.get('mood', '').strip()
        if frontmatter_mood and frontmatter_mood != '""' and frontmatter_mood:
            analysis['mood_indicators'].insert(0, f"Frontmatter mood: {frontmatter_mood}")
        
        # Extract productivity and focus signals
        productivity_patterns = [
            re.compile(r'(?:completed|finished|done|accomplished)\s+(.+)', re.IGNORECASE),
            re.compile(r'(?:struggled with|difficulty|blocked by)\s+(.+)', re.IGNORECASE),
            re.compile(r'(?:breakthrough|insight|realization)\s*:?\s*(.+)', re.IGNORECASE)
        ]
        
        for pattern in productivity_patterns:
            matches = pattern.findall(content)
            analysis['productivity_signals'].extend(matches[:3])
        
        # Extract learning and reflection notes
        learning_patterns = [
            re.compile(r'(?:learned|discovered|realized)\s+(.+)', re.IGNORECASE),
            re.compile(r'(?:note to self|remember|important)\s*:?\s*(.+)', re.IGNORECASE),
            re.compile(r'(?:reflection|thinking about)\s*:?\s*(.+)', re.IGNORECASE)
        ]
        
        for pattern in learning_patterns:
            matches = pattern.findall(content)
            analysis['learning_notes'].extend(matches[:3])
        
        # Analyze daily log structure
        sections = self._analyze_daily_log_sections(content)
        analysis['daily_log_insights'] = {
            'has_brain_boot': '## brain boot' in content.lower(),
            'has_body_boot': '## body boot' in content.lower(), 
            'has_daily_tasks': '## daily tasks' in content.lower(),
            'total_actionable_items': len(analysis['actionable_items']),
            'mood_tracking_present': len(analysis['mood_indicators']) > 0,
            'productivity_tracking': len(analysis['productivity_signals']) > 0,
            'learning_capture': len(analysis['learning_notes']) > 0,
            'log_sections': sections,
            'signal_to_noise_ratio': self._calculate_daily_log_signal_ratio(analysis),
            # Frontmatter insights
            'log_date': frontmatter_data.get('created', '').split('T')[0] if frontmatter_data.get('created') else metadata.get('filename', '').replace('.md', ''),
            'log_uid': frontmatter_data.get('uid', ''),
            'log_status': frontmatter_data.get('status', ''),
            'log_week': frontmatter_data.get('week', ''),
            'log_quarter': frontmatter_data.get('quarter', ''),
            'log_tags': frontmatter_data.get('tags', []),
            'has_soundtrack': bool(frontmatter_data.get('soundtrack', '').strip()),
            'soundtrack': frontmatter_data.get('soundtrack', '').strip()
        }
        
        return analysis
    
    def _generate_ollama_daily_log_analysis(self, content: str, frontmatter_data: Dict) -> Dict:
        """Generate Ollama-powered analysis for daily logs"""
        try:
            # Create a specialized prompt for daily log analysis
            log_date = frontmatter_data.get('created', '').split('T')[0] if frontmatter_data.get('created') else 'Unknown'
            mood = frontmatter_data.get('mood', '').strip('"')
            
            prompt = f"""Analyze this daily log entry from {log_date}. 

Content:
{content[:3000]}  # Limit content to avoid context overflow

Please provide:
1. A 2-3 sentence summary of the day's key activities and outcomes
2. 3-5 actionable items or follow-ups that need attention
3. Mood/energy assessment based on the content
4. 2-3 key insights or learning points
5. Overall productivity assessment

Focus on extracting meaningful insights that would be useful for reflection and planning.

Respond in JSON format:
{{
    "summary": "Brief summary of the day",
    "actionable_items": ["item1", "item2", "item3"],
    "mood_analysis": "mood and energy assessment", 
    "insights": ["insight1", "insight2"],
    "productivity_assessment": "overall productivity evaluation"
}}"""

            # Use Ollama to generate analysis
            import requests
            response = requests.post(
                f"{self.ollama_summarizer.ollama_url}/api/generate",
                json={
                    "model": self.ollama_summarizer.model,
                    "prompt": prompt,
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
                response_text = result.get('response', '').strip()
                try:
                    # Parse JSON response
                    analysis_text = response_text
                    # Handle cases where response might have markdown formatting
                    if '```json' in analysis_text:
                        analysis_text = analysis_text.split('```json')[1].split('```')[0]
                    elif '```' in analysis_text:
                        analysis_text = analysis_text.split('```')[1].split('```')[0]
                    
                    analysis_data = json.loads(analysis_text)
                    return analysis_data
                except json.JSONDecodeError as e:
                    # Fallback if JSON parsing fails
                    return {
                        'summary': response_text[:200] + "..." if response_text else "No response",
                        'actionable_items': [],
                        'mood_analysis': mood or "Not specified",
                        'insights': [],
                        'productivity_assessment': "Analysis parsing failed"
                    }
            else:
                return {
                    'summary': "Ollama response unavailable",
                    'actionable_items': [],
                    'mood_analysis': mood or "Not specified", 
                    'insights': [],
                    'productivity_assessment': "Ollama unavailable"
                }
        except Exception as e:
            return {
                'summary': f"Ollama analysis failed: {str(e)}",
                'actionable_items': [],
                'mood_analysis': frontmatter_data.get('mood', '').strip('"') or "Not specified",
                'insights': [],
                'productivity_assessment': "Analysis failed"
            }
    
    def _analyze_daily_log_sections(self, content: str) -> Dict:
        """Analyze the structure of daily log sections"""
        sections = {}
        lines = content.split('\n')
        current_section = None
        
        for line in lines:
            if line.startswith('## '):
                section_name = line[3:].strip().lower()
                current_section = section_name
                sections[section_name] = {'line_count': 0, 'has_content': False}
            elif current_section and line.strip():
                sections[current_section]['line_count'] += 1
                if not line.startswith('#') and not line.startswith('---'):
                    sections[current_section]['has_content'] = True
        
        return sections
    
    def _calculate_daily_log_signal_ratio(self, analysis: Dict) -> float:
        """Calculate signal-to-noise ratio for daily logs"""
        signal_count = (
            len(analysis.get('actionable_items', [])) * 2 +  # Weight actionable items higher
            len(analysis.get('mood_indicators', [])) +
            len(analysis.get('productivity_signals', [])) +
            len(analysis.get('learning_notes', []))
        )
        
        # Estimate total content based on analysis length
        total_content_estimate = len(str(analysis)) / 10  # Rough estimate
        
        return signal_count / max(total_content_estimate, 1)
    
    def _analyze_conversation_content(self, content: str, metadata: Dict) -> Dict:
        """Analyze content to determine if it's a conversation and extract metadata"""
        analysis = {
            'is_conversation': False,
            'conversation_platform': 'unknown',
            'conversation_id': 'unknown',
            'participants': [],
            'message_count': 0
        }
        
        # Check for Chrome plugin export formats
        if '"powered_by": "Claude Exporter' in content:
            analysis['is_conversation'] = True
            analysis['conversation_platform'] = 'claude_ai'
            
            # Extract dates from metadata
            import json
            try:
                # Try to parse the JSON to get metadata
                content_data = json.loads(content)
                if 'metadata' in content_data and 'dates' in content_data['metadata']:
                    created = content_data['metadata']['dates'].get('created', '')
                    # Use created date as a conversation ID
                    analysis['conversation_id'] = f"claude_export_{created.replace('/', '_').replace(' ', '_').replace(':', '')}"
                elif 'metadata' in content_data and 'title' in content_data['metadata']:
                    # Use title if dates not available
                    title = content_data['metadata']['title'][:50]  # Limit length
                    analysis['conversation_id'] = f"claude_export_{title.replace(' ', '_')}"
                
                # Count messages if available
                if 'messages' in content_data:
                    analysis['message_count'] = len(content_data.get('messages', []))
                    analysis['participants'] = ['User', 'Claude']
                    
                # Extract conversation URLs if available
                if 'metadata' in content_data and 'url' in content_data['metadata']:
                    analysis['conversation_urls'] = [content_data['metadata']['url']]
                    
            except json.JSONDecodeError:
                # Fallback if JSON parsing fails - try to extract from filename
                filename = metadata.get('filename', '')
                if 'claude' in filename.lower():
                    analysis['conversation_id'] = f"claude_export_{filename.split('.')[0][:20]}"
        
        elif '"powered_by": "ChatGPT Exporter' in content:
            analysis['is_conversation'] = True
            analysis['conversation_platform'] = 'chatgpt'
            
            # Extract dates and user info from metadata
            import json
            try:
                # Try to parse the JSON to get metadata
                content_data = json.loads(content)
                if 'metadata' in content_data:
                    # Extract user name if available
                    user_name = 'User'
                    if 'user' in content_data['metadata'] and 'name' in content_data['metadata']['user']:
                        user_name = content_data['metadata']['user']['name']
                    
                    # Extract dates
                    if 'dates' in content_data['metadata']:
                        created = content_data['metadata']['dates'].get('created', '')
                        # Use created date as a conversation ID
                        analysis['conversation_id'] = f"chatgpt_export_{created.replace('/', '_').replace(' ', '_').replace(':', '')}"
                    elif 'title' in content_data['metadata']:
                        # Use title if dates not available
                        title = content_data['metadata']['title'][:50]  # Limit length
                        analysis['conversation_id'] = f"chatgpt_export_{title.replace(' ', '_')}"
                    
                    # Extract conversation URLs if available
                    if 'url' in content_data['metadata']:
                        analysis['conversation_urls'] = [content_data['metadata']['url']]
                    
                    analysis['participants'] = [user_name, 'ChatGPT']
                
                # Count messages if available
                if 'messages' in content_data:
                    analysis['message_count'] = len(content_data.get('messages', []))
            except json.JSONDecodeError:
                # Fallback if JSON parsing fails - try to extract from filename
                filename = metadata.get('filename', '')
                if 'chatgpt' in filename.lower():
                    analysis['conversation_id'] = f"chatgpt_export_{filename.split('.')[0][:20]}"
        
        # Check for conversation platforms
        for platform, pattern in [('claude_ai', self.conversation_patterns['claude_ai']),
                                 ('chatgpt', self.conversation_patterns['chatgpt'])]:
            if pattern.search(content) or pattern.search(metadata.get('filename', '')):
                if analysis['conversation_platform'] == 'unknown':  # Don't override if already detected
                    analysis['conversation_platform'] = platform
                analysis['is_conversation'] = True
                break
        
        # Check for dialogue markers
        dialogue_matches = self.conversation_patterns['dialogue_markers'].findall(content)
        if len(dialogue_matches) > 3:  # Multiple dialogue exchanges
            analysis['is_conversation'] = True
            analysis['participants'] = list(set(dialogue_matches))
            analysis['message_count'] = len(dialogue_matches)
        
        # Extract conversation ID
        conv_id_match = self.conversation_patterns['conversation_id'].search(content)
        if conv_id_match:
            analysis['conversation_id'] = conv_id_match.group(1)
        
        # Extract chat URLs for conversation linking
        chat_urls = self.conversation_patterns['chat_url'].findall(content)
        if chat_urls:
            analysis['conversation_urls'] = chat_urls
            analysis['is_conversation'] = True
        
        return analysis
    
    def _classify_content_type(self, content: str, basic_analysis: Dict) -> str:
        """Classify content type for enhanced processing"""
        content_lower = content.lower()
        metadata = basic_analysis.get('metadata', {})
        
        # Check if it's a daily log first using comprehensive detection
        if self.is_daily_log(content, metadata):
            return 'daily_log'
        
        # Priority classification
        if basic_analysis.get('content_type') == 'AI conversation export':
            return 'ai_conversation'
        elif '"powered_by": "Claude Exporter' in content:
            return 'ai_conversation_chrome_export'
        elif '"powered_by": "ChatGPT Exporter' in content:
            return 'ai_conversation_chrome_export'
        elif 'conversation' in content_lower or 'chat' in content_lower:
            # Double-check it's not a daily log talking about conversations
            metadata = basic_analysis.get('metadata', {})
            if not self.is_daily_log(content, metadata):
                return 'conversation'
        elif content.strip().startswith('{') or content.strip().startswith('['):
            return 'structured_data'
        elif len([line for line in content.split('\n') if line.startswith('#')]) > 3:
            return 'markdown_document'
        elif 'research' in content_lower or 'analysis' in content_lower:
            return 'research_document'
        elif 'meeting' in content_lower or 'notes' in content_lower:
            return 'meeting_notes'
        else:
            return 'general_document'
    
    def _extract_topics(self, content: str) -> List[str]:
        """Extract key topics from content"""
        # Simple topic extraction (could be enhanced with NLP)
        words = re.findall(r'\b[A-Z][a-z]+\b', content)  # Capitalized words
        
        # Filter common words and get most frequent
        from collections import Counter
        stop_words = {'The', 'This', 'That', 'And', 'But', 'For', 'With', 'From'}
        topics = [w for w in words if w not in stop_words and len(w) > 3]
        
        # Get top topics
        topic_counts = Counter(topics)
        return [topic for topic, count in topic_counts.most_common(10) if count > 1]
    
    def _determine_tripartite_routing(self, content: str, enhanced_analysis: Dict) -> List[str]:
        """Determine which tripartite collections should receive this content using enhanced classification"""
        
        # Use enhanced pattern detector classification if available
        if 'tripartite_domain' in enhanced_analysis:
            return self._determine_tripartite_routing_smart(content, enhanced_analysis)
        
        else:
            # Fallback to basic keyword-based routing
            return self._basic_tripartite_routing(content, enhanced_analysis)
    
    def _determine_tripartite_routing_smart(self, content: str, enhanced_analysis: Dict) -> List[str]:
        """Determine tripartite routing with MUCH higher thresholds to prevent 'dumb spray'."""
        
        primary_domain = enhanced_analysis.get('tripartite_domain', 'concept')
        confidence = enhanced_analysis.get('tripartite_confidence', 0.0)
        scores = enhanced_analysis.get('tripartite_scores', {})
        
        routing = [primary_domain]  # Always include primary
        
        # MUCH HIGHER thresholds for secondary domains
        SECONDARY_THRESHOLD = 0.6  # Was 0.3, now 0.6
        HIGH_SIGNAL_THRESHOLD = 0.8  # New threshold for multi-domain
        
        # Only add secondary domains with high confidence
        for domain, score in scores.items():
            if domain != primary_domain:
                normalized_score = score / max(sum(scores.values()), 1)
                if normalized_score > SECONDARY_THRESHOLD:
                    routing.append(domain)
        
        # Special cases with MUCH stricter criteria
        signal_density = enhanced_analysis.get('signal_density', 0.0)
        
        # High-signal content: Only if EXTREMELY high density
        if (signal_density > 0.05 and  # 5% signal density (was 2%)
            enhanced_analysis.get('total_signals', 0) > 10):  # AND 10+ signals
            routing = ['concept', 'framework', 'metaphor']
            self.logger.info("Ultra-high signal content → all domains", 
                            extra={'signal_density': signal_density, 
                                   'total_signals': enhanced_analysis.get('total_signals', 0)})
        
        # Conversations: Only multi-domain if they're actually multi-domain
        elif enhanced_analysis.get('is_conversation'):
            # Only route to all if confidence is high for multiple domains
            multi_domain_count = sum(1 for domain, score in scores.items() 
                                   if (score / max(sum(scores.values()), 1)) > HIGH_SIGNAL_THRESHOLD)
            
            if multi_domain_count < 2:  # If not truly multi-domain, stick to primary + maybe one
                routing = [primary_domain]
                best_secondary = max((d for d, s in scores.items() if d != primary_domain), 
                                   key=lambda d: scores[d], default=None)
                if best_secondary and (scores[best_secondary] / sum(scores.values())) > SECONDARY_THRESHOLD:
                    routing.append(best_secondary)
        
        # Platform integration: Only add framework if not already primary
        if (enhanced_analysis.get('has_platform_integration', False) and 
            'framework' not in routing and
            enhanced_analysis.get('platform_references', 0) > 3):  # Significant platform content
            routing.append('framework')
        
        # Persona annotations: Be more selective
        if enhanced_analysis.get('has_persona_annotations', False):
            persona_count = enhanced_analysis.get('persona_annotation_count', 0)
            if persona_count > 2:  # Only if multiple persona annotations
                routing = ['concept', 'framework', 'metaphor']
        
        self.logger.info(f"Smart routing decision: {routing}", 
                        extra={'primary': primary_domain, 'confidence': confidence, 
                               'secondary_scores': {d: scores.get(d, 0) for d in routing if d != primary_domain}})
        
        return routing
    
    def _basic_tripartite_routing(self, content: str, enhanced_analysis: Dict) -> List[str]:
        """Fallback basic tripartite routing when enhanced classification is not available"""
        routing = []
        content_lower = content.lower()
        
        # Concept collection indicators
        concept_indicators = ['definition', 'theory', 'principle', 'concept', 'abstract',
                            'philosophy', 'idea', 'notion', 'understanding', 'knowledge']
        if any(indicator in content_lower for indicator in concept_indicators):
            routing.append('concept')
        
        # Framework collection indicators  
        framework_indicators = ['process', 'method', 'framework', 'system', 'workflow',
                              'procedure', 'protocol', 'algorithm', 'implementation', 'steps']
        if any(indicator in content_lower for indicator in framework_indicators):
            routing.append('framework')
        
        # Metaphor collection indicators
        metaphor_indicators = ['like', 'metaphor', 'analogy', 'similar to', 'reminds me',
                             'experience', 'feeling', 'intuition', 'sense', 'imagine']
        if any(indicator in content_lower for indicator in metaphor_indicators):
            routing.append('metaphor')
        
        # Conversation-specific routing
        if enhanced_analysis.get('is_conversation'):
            # Conversations often contain all three elements
            if not routing:  # If no specific indicators, route to all
                routing = ['concept', 'framework', 'metaphor']
        
        return routing
    
    def _integrate_with_enhanced_daily_context(self, file_analysis: Dict, enhanced_analysis: Dict):
        """Integrate with enhanced daily context system"""
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            
            # Trigger enhanced daily summary update
            if hasattr(self.enhanced_context, 'create_comprehensive_daily_summary_enhanced'):
                enhanced_summary = self.enhanced_context.create_comprehensive_daily_summary_enhanced(today)
                
                # Check if this file created new conversations that need .dis files
                if enhanced_analysis.get('is_conversation'):
                    self._process_new_conversations(enhanced_summary, file_analysis)
                
                self.logger.info(f"Enhanced daily context updated for {today}", 
                               extra={'float_id': file_analysis.get('float_id')})
            
        except Exception as e:
            self.logger.error(f"Enhanced daily context integration failed: {e}")
    
    def _route_to_tripartite_collections(self, file_analysis: Dict, enhanced_analysis: Dict):
        """Route content to appropriate tripartite collections"""
        try:
            content = file_analysis.get('content', '')
            if not content:
                return
            
            routing = enhanced_analysis.get('tripartite_routing', [])
            if not routing:
                return
            
            float_id = file_analysis.get('float_id')
            metadata = file_analysis.get('metadata', {})
            
            # Get Chroma client
            chroma_client = self.daemon.components['context'].client
            
            for collection_type in routing:
                try:
                    collection_name = self.config.get('tripartite_collections', {}).get(
                        collection_type, f'float_tripartite_v2_{collection_type}'
                    )
                    
                    collection = chroma_client.get_or_create_collection(
                        name=collection_name,
                        metadata={
                            "description": f"FLOAT tripartite {collection_type} domain",
                            "enhanced_routing": True
                        }
                    )
                    
                    # Chunk content for storage
                    chunks = self.daemon._chunk_content(content)
                    
                    # Store with enhanced metadata
                    for i, chunk in enumerate(chunks):
                        chunk_id = f"{float_id}_{collection_type}_chunk_{i}"
                        
                        # Ensure all metadata values are valid (no None values)
                        chunk_metadata = {
                            'float_id': str(float_id or 'unknown'),
                            'original_filename': str(metadata.get('filename') or 'unknown'),
                            'chunk_index': int(i),
                            'total_chunks': int(len(chunks)),
                            'collection_type': str(collection_type or 'unknown'),
                            'tripartite_domain': str(collection_type or 'unknown'),
                            'content_classification': str(enhanced_analysis.get('content_classification') or 'unknown'),
                            'is_conversation': str(enhanced_analysis.get('is_conversation', False)),
                            'conversation_platform': str(enhanced_analysis.get('conversation_platform') or 'unknown'),
                            'signal_density': float(enhanced_analysis.get('signal_density', 0.0)),
                            'processed_at': str(file_analysis.get('processed_at') or datetime.now().isoformat()),
                            'enhanced_routing': 'true'
                        }
                        
                        # Add temporal metadata if enabled
                        chunk_metadata = self.enhance_metadata_with_temporal_info(
                            chunk_metadata, content, metadata, enhanced_analysis
                        )
                        
                        collection.add(
                            documents=[chunk],
                            metadatas=[chunk_metadata],
                            ids=[chunk_id]
                        )
                    
                    self.logger.info(f"Routed to {collection_name}: {len(chunks)} chunks",
                                   extra={'float_id': float_id, 'collection': collection_name})
                    
                except Exception as e:
                    self.logger.error(f"Failed to route to {collection_type} collection: {e}")
                    
        except Exception as e:
            self.logger.error(f"Tripartite routing failed: {e}")
    
    def _route_to_special_pattern_collections(self, file_analysis: Dict, enhanced_analysis: Dict):
        """Route content with special patterns to dedicated collections"""
        try:
            content = file_analysis.get('content', '')
            if not content:
                return
                
            pattern_analysis = enhanced_analysis.get('pattern_analysis', {})
            core_patterns = pattern_analysis.get('core_float_patterns', {})
            extended_patterns = pattern_analysis.get('extended_float_patterns', {})
            
            float_id = file_analysis.get('float_id')
            metadata = file_analysis.get('metadata', {})
            
            # Get Chroma client
            chroma_client = self.daemon.components['context'].client
            
            # Get special pattern collection config
            special_collections = self.config.get('special_pattern_collections', {})
            
            collections_to_route = []
            
            # Check for float.dispatch patterns
            if core_patterns.get('float_dispatch', {}).get('has_pattern', False):
                if 'dispatch' in special_collections:
                    collections_to_route.append(('dispatch', special_collections['dispatch']))
            
            # Check for float.rfc patterns  
            if pattern_analysis.get('bbs_heritage', {}).get('float_rfc', {}).get('has_pattern', False):
                if 'rfc' in special_collections:
                    collections_to_route.append(('rfc', special_collections['rfc']))
            
            # Check for echoCopy:: patterns
            if extended_patterns.get('echo_copy', {}).get('has_pattern', False):
                if 'echo_copy' in special_collections:
                    collections_to_route.append(('echo_copy', special_collections['echo_copy']))
            
            # Route to special pattern collections
            for pattern_type, collection_name in collections_to_route:
                try:
                    collection = chroma_client.get_or_create_collection(
                        name=collection_name,
                        metadata={
                            "description": f"FLOAT special pattern collection: {pattern_type}",
                            "pattern_type": pattern_type,
                            "enhanced_routing": True
                        }
                    )
                    
                    # Chunk content for storage
                    chunks = self.daemon._chunk_content(content)
                    
                    # Store with enhanced metadata
                    for i, chunk in enumerate(chunks):
                        chunk_id = f"{float_id}_{pattern_type}_chunk_{i}"
                        
                        # Enhanced metadata for special patterns
                        chunk_metadata = {
                            'float_id': str(float_id or 'unknown'),
                            'original_filename': str(metadata.get('filename') or 'unknown'),
                            'chunk_index': int(i),
                            'total_chunks': int(len(chunks)),
                            'collection_type': str(pattern_type),
                            'pattern_type': str(pattern_type),
                            'content_classification': str(enhanced_analysis.get('content_classification') or 'unknown'),
                            'is_conversation': str(enhanced_analysis.get('is_conversation', False)),
                            'conversation_platform': str(enhanced_analysis.get('conversation_platform') or 'unknown'),
                            'signal_density': float(enhanced_analysis.get('signal_density', 0.0)),
                            'processed_at': str(file_analysis.get('processed_at') or datetime.now().isoformat()),
                            'special_pattern_routing': 'true',
                            'tripartite_also_routed': str(len(enhanced_analysis.get('tripartite_routing', [])) > 0)
                        }
                        
                        # Add pattern-specific metadata
                        if pattern_type == 'dispatch':
                            dispatch_patterns = core_patterns.get('float_dispatch', {})
                            chunk_metadata.update({
                                'dispatch_count': int(dispatch_patterns.get('count', 0)),
                                'has_dispatch_payload': str(len(dispatch_patterns.get('matches', [])) > 0)
                            })
                        elif pattern_type == 'rfc':
                            rfc_patterns = pattern_analysis.get('bbs_heritage', {}).get('float_rfc', {})
                            chunk_metadata.update({
                                'rfc_count': int(rfc_patterns.get('count', 0)),
                                'rfc_topics': str(rfc_patterns.get('matches', [])[:3])  # First 3 topics
                            })
                        elif pattern_type == 'echo_copy':
                            echo_patterns = extended_patterns.get('echo_copy', {})
                            chunk_metadata.update({
                                'echo_copy_count': int(echo_patterns.get('count', 0)),
                                'echo_copy_content': str(echo_patterns.get('matches', [])[:3])  # First 3 matches
                            })
                        
                        # Add temporal metadata to special pattern collections too
                        chunk_metadata = self.enhance_metadata_with_temporal_info(
                            chunk_metadata, content, metadata, enhanced_analysis
                        )
                        
                        collection.add(
                            documents=[chunk],
                            metadatas=[chunk_metadata],
                            ids=[chunk_id]
                        )
                    
                    self.logger.info(f"Routed to special pattern collection {collection_name}: {len(chunks)} chunks",
                                   extra={'float_id': float_id, 'collection': collection_name, 'pattern_type': pattern_type})
                    
                except Exception as e:
                    self.logger.error(f"Failed to route to special pattern collection {pattern_type}: {e}")
                    
        except Exception as e:
            self.logger.error(f"Special pattern routing failed: {e}")
    
    
    def _generate_conversation_dis_file(self, file_analysis: Dict, enhanced_analysis: Dict) -> Optional[Path]:
        """Generate enhanced .dis file specifically for conversation content"""
        
        try:
            # Create conversation-specific filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            platform = enhanced_analysis.get('conversation_platform', 'unknown')
            conv_id = enhanced_analysis.get('conversation_id', 'unknown')[:8]
            
            filename = f"{timestamp}_{platform}_{conv_id}.conversation.float_dis.md"
            dis_path = self.conversation_dis_path / filename
            
            # Generate enhanced conversation .dis content
            dis_content = self._create_conversation_dis_content(file_analysis, enhanced_analysis)
            
            # Write file
            with open(dis_path, 'w', encoding='utf-8') as f:
                f.write(dis_content)
            
            self.logger.info(f"Generated conversation .dis file: {dis_path.name}",
                           extra={'float_id': file_analysis.get('float_id')})
            
            return dis_path
            
        except Exception as e:
            self.logger.error(f"Failed to generate conversation .dis file: {e}")
            return None
    
    def _create_conversation_dis_content(self, file_analysis: Dict, enhanced_analysis: Dict) -> str:
        """Create enhanced .dis file content for conversations"""
        metadata = file_analysis.get('metadata', {})
        analysis = file_analysis.get('analysis', {})
        cross_refs = file_analysis.get('cross_references', {})
        
        # Create YAML frontmatter
        frontmatter = {
            'float_id': file_analysis.get('float_id'),
            'conversation_id': enhanced_analysis.get('conversation_id', 'unknown'),
            'platform': enhanced_analysis.get('conversation_platform'),
            'participants': enhanced_analysis.get('participants'),
            'message_count': enhanced_analysis.get('message_count', 0),
            'topics': enhanced_analysis.get('topics'),
            'signal_density': round(enhanced_analysis.get('signal_density', 0), 4),
            'content_classification': enhanced_analysis.get('content_classification'),
            'tripartite_routing': enhanced_analysis.get('tripartite_routing'),
            'processed_at': file_analysis.get('processed_at'),
            'original_file': metadata.get('filename'),
            'file_size_bytes': metadata.get('size_bytes', 0)
        }
        
        yaml_header = "---\n"
        for key, value in frontmatter.items():
            if value is not None:
                yaml_header += f"{key}: {json.dumps(value) if isinstance(value, (list, dict)) else value}\n"
        yaml_header += "---\n\n"
        
        # Create content
        content = f"""# 💬 Conversation Analysis: {enhanced_analysis.get('conversation_id', 'Unknown')}

## Platform Details
- **Platform**: {enhanced_analysis.get('conversation_platform', 'Unknown').replace('_', ' ').title()}
- **Conversation ID**: `{enhanced_analysis.get('conversation_id', 'Unknown')}`
- **Participants**: {', '.join(enhanced_analysis.get('participants', []))}
- **Messages**: {enhanced_analysis.get('message_count', 0)}
- **Signal Density**: {enhanced_analysis.get('signal_density', 0):.4f} signals/word

## Content Classification
**Type**: {enhanced_analysis.get('content_classification', 'unknown').replace('_', ' ').title()}

## Topic Analysis
{chr(10).join([f"- **{topic}**" for topic in enhanced_analysis.get('topics', [])[:10]])}

## Tripartite Routing
This content has been routed to the following collections:
{chr(10).join([f"- `float_tripartite_v2_{domain}`" for domain in enhanced_analysis.get('tripartite_routing', [])])}

## Cross-References

### Conversation Links
{chr(10).join([f"- [{link.get('title', 'Conversation')}]({link.get('url', '#')})" for link in cross_refs.get('conversation_links', []) if link and isinstance(link, dict)])}

### Topic Connections
{', '.join(cross_refs.get('topic_connections', [])[:10])}

## Navigation

### Related Conversations
```dataview
LIST
FROM "FLOAT.conversations"
WHERE contains(file.frontmatter.topics, "{enhanced_analysis.get('topics', [''])[0] if enhanced_analysis.get('topics') else ''}")
AND file.name != this.file.name
SORT file.ctime DESC
LIMIT 5
```

### Related Daily Notes
```dataview
LIST
FROM "FLOAT.logs"
WHERE contains(file.content, "{enhanced_analysis.get('conversation_id', '')[:12]}")
SORT file.mtime DESC
LIMIT 3
```

## Processing Details
- **Float ID**: `{file_analysis.get('float_id')}`
- **Original File**: `{metadata.get('filename', 'Unknown')}`
- **Processed**: {file_analysis.get('processed_at', 'Unknown')}
- **File Size**: {metadata.get('size_bytes', 0):,} bytes

---

*Enhanced conversation processing powered by FLOAT Enhanced Integration*
"""
        
        return yaml_header + content
    
    def _generate_daily_log_dis_file(self, file_analysis: Dict, enhanced_analysis: Dict) -> Optional[Path]:
        """Generate enhanced .dis file specifically for daily log content"""
        
        try:
            # Create daily log-specific filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            log_date = enhanced_analysis.get('daily_log_insights', {}).get('log_date', 'unknown')
            
            filename = f"{timestamp}_daily_log_{log_date}.float_dis.md"
            dis_path = self.conversation_dis_path / filename
            
            # Generate enhanced daily log .dis content
            dis_content = self._create_daily_log_dis_content(file_analysis, enhanced_analysis)
            
            # Write file
            with open(dis_path, 'w', encoding='utf-8') as f:
                f.write(dis_content)
            
            self.logger.info(f"Generated daily log .dis file: {dis_path.name}",
                           extra={'float_id': file_analysis.get('float_id')})
            
            return dis_path
            
        except Exception as e:
            self.logger.error(f"Failed to generate daily log .dis file: {e}")
            return None
    
    def _create_daily_log_dis_content(self, file_analysis: Dict, enhanced_analysis: Dict) -> str:
        """Create enhanced .dis file content for daily logs"""
        metadata = file_analysis.get('metadata', {})
        cross_refs = file_analysis.get('cross_references', {})
        daily_insights = enhanced_analysis.get('daily_log_insights', {})
        
        # Extract log date from filename or metadata
        filename = metadata.get('filename', '')
        log_date = filename.replace('.md', '') if filename.endswith('.md') else 'unknown'
        
        # Create YAML frontmatter
        frontmatter = {
            'float_id': file_analysis.get('float_id'),
            'content_type': 'daily_log',
            'log_date': daily_insights.get('log_date', log_date),
            'log_uid': daily_insights.get('log_uid', ''),
            'log_status': daily_insights.get('log_status', ''),
            'log_week': daily_insights.get('log_week', ''),
            'log_quarter': daily_insights.get('log_quarter', ''),
            'log_tags': daily_insights.get('log_tags', []),
            'has_soundtrack': daily_insights.get('has_soundtrack', False),
            'soundtrack': daily_insights.get('soundtrack', ''),
            'filename': metadata.get('filename'),
            'signal_density': enhanced_analysis.get('signal_density', 0),
            'actionable_items_count': len(enhanced_analysis.get('actionable_items', [])),
            'mood_tracking': len(enhanced_analysis.get('mood_indicators', [])) > 0,
            'productivity_signals': len(enhanced_analysis.get('productivity_signals', [])),
            'learning_notes': len(enhanced_analysis.get('learning_notes', [])),
            'has_brain_boot': daily_insights.get('has_brain_boot', False),
            'has_body_boot': daily_insights.get('has_body_boot', False),
            'has_daily_tasks': daily_insights.get('has_daily_tasks', False),
            'signal_to_noise_ratio': daily_insights.get('signal_to_noise_ratio', 0),
            'processed_at': file_analysis.get('processed_at'),
            'tripartite_routing': enhanced_analysis.get('tripartite_routing', []),
            'file_size_bytes': metadata.get('size_bytes', 0)
        }
        
        yaml_header = "---\n"
        for key, value in frontmatter.items():
            if value is not None:
                yaml_header += f"{key}: {json.dumps(value) if isinstance(value, (list, dict)) else value}\n"
        yaml_header += "---\n\n"
        
        # Create enhanced content
        actionable_items = enhanced_analysis.get('actionable_items', [])
        mood_indicators = enhanced_analysis.get('mood_indicators', [])
        productivity_signals = enhanced_analysis.get('productivity_signals', [])
        learning_notes = enhanced_analysis.get('learning_notes', [])
        log_sections = daily_insights.get('log_sections', {})
        
        content = f"""# 📅 Daily Log Analysis: {log_date}

## 🤖 AI Summary
{enhanced_analysis.get('ollama_summary', 'Ollama summary not available')}

## 📊 Log Metadata
- **Date**: {daily_insights.get('log_date', log_date)}
- **UID**: `{daily_insights.get('log_uid', 'N/A')}`
- **Status**: {daily_insights.get('log_status', 'unknown').title()}
- **Week**: {daily_insights.get('log_week', 'N/A')}
- **Quarter**: {daily_insights.get('log_quarter', 'N/A')}
- **Soundtrack**: {daily_insights.get('soundtrack', 'None') if daily_insights.get('has_soundtrack') else 'None'}

## 🏗️ Log Structure
- **Brain Boot**: {'✅' if daily_insights.get('has_brain_boot') else '❌'}
- **Body Boot**: {'✅' if daily_insights.get('has_body_boot') else '❌'}
- **Daily Tasks**: {'✅' if daily_insights.get('has_daily_tasks') else '❌'}
- **Signal-to-Noise Ratio**: {daily_insights.get('signal_to_noise_ratio', 0):.3f}

## 🏷️ Tags
{chr(10).join([f'- #{tag}' for tag in daily_insights.get('log_tags', [])]) if daily_insights.get('log_tags') else '- No tags found'}

## 📋 Actionable Items ({len(actionable_items)} found)
{chr(10).join([f"- {item[:100]}{'...' if len(item) > 100 else ''}" for item in actionable_items[:10]]) if actionable_items else "- No actionable items detected"}

## 💭 Mood & Energy Tracking
{chr(10).join([f"- {mood}" for mood in mood_indicators[:5]]) if mood_indicators else "- No mood indicators detected"}

## 🚀 Productivity Signals
{chr(10).join([f"- {signal[:100]}{'...' if len(signal) > 100 else ''}" for signal in productivity_signals[:5]]) if productivity_signals else "- No productivity signals detected"}

## 📚 Learning & Insights
{chr(10).join([f"- {note[:100]}{'...' if len(note) > 100 else ''}" for note in learning_notes[:5]]) if learning_notes else "- No learning notes detected"}

## 🎯 AI-Generated Insights
{chr(10).join([f"- {insight}" for insight in enhanced_analysis.get('ollama_insights', [])]) if enhanced_analysis.get('ollama_insights') else "- AI insights not available"}

## 📊 Section Analysis
{chr(10).join([f"- **{section.title()}**: {data.get('line_count', 0)} lines, {'✅ has content' if data.get('has_content') else '❌ empty'}" for section, data in log_sections.items()]) if log_sections else "- No sections detected"}

## 🎯 Key Metrics
- **Total Actionable Items**: {len(actionable_items)}
- **Mood Tracking Present**: {'Yes' if mood_indicators else 'No'}
- **Productivity Tracking**: {'Yes' if productivity_signals else 'No'}
- **Learning Capture**: {'Yes' if learning_notes else 'No'}
- **Signal Density**: {enhanced_analysis.get('signal_density', 0):.4f} signals/word

## 🔗 Tripartite Routing
This daily log has been routed to:
{chr(10).join([f"- `float_tripartite_v2_{domain}`" for domain in enhanced_analysis.get('tripartite_routing', [])]) if enhanced_analysis.get('tripartite_routing') else "- No tripartite routing"}

## 🗂️ Navigation

### Related Daily Logs
```dataview
LIST
FROM "FLOAT.logs"
WHERE file.name != this.file.name
AND file.name CONTAINS "{log_date[:7]}"
SORT file.name DESC
LIMIT 5
```

### Action Items Follow-up
```dataview
TASK
WHERE !completed
AND contains(text, "{log_date}")
```

### Mood Patterns
```dataview
TABLE mood_tracking, signal_to_noise_ratio
FROM #daily-log
WHERE mood_tracking = true
SORT file.ctime DESC
LIMIT 10
```

## 🛠️ Quick Actions

### Daily Log Review
- **Yesterday**: [[{(datetime.strptime(log_date, '%Y-%m-%d') - timedelta(days=1)).strftime('%Y-%m-%d') if log_date != 'unknown' else 'unknown'}]]
- **Tomorrow**: [[{(datetime.strptime(log_date, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d') if log_date != 'unknown' else 'unknown'}]]
- **Weekly Review**: Create weekly summary from {log_date}

### Extract Actions
Use Templater to extract actionable items:
```javascript
// Extract all actionable items
const actionItems = {json.dumps(actionable_items[:5], indent=2) if actionable_items else '[]'};
```

## 📈 Analysis Summary
- **Overall Quality**: {'High' if daily_insights.get('signal_to_noise_ratio', 0) > 0.3 else 'Medium' if daily_insights.get('signal_to_noise_ratio', 0) > 0.1 else 'Low'}
- **Actionability**: {'High' if len(actionable_items) > 5 else 'Medium' if len(actionable_items) > 0 else 'Low'}
- **Self-Awareness**: {'High' if mood_indicators and productivity_signals else 'Medium' if mood_indicators or productivity_signals else 'Low'}
- **Learning Value**: {'High' if len(learning_notes) > 3 else 'Medium' if len(learning_notes) > 0 else 'Low'}

## 📝 Processing Details
- **Float ID**: `{file_analysis.get('float_id')}`
- **Original File**: `{metadata.get('filename', 'Unknown')}`
- **Processed**: {file_analysis.get('processed_at', 'Unknown')}
- **File Size**: {metadata.get('size_bytes', 0):,} bytes

---

*Enhanced daily log analysis powered by FLOAT Enhanced Integration*
"""
        
        return yaml_header + content
    
    def _process_new_conversations(self, enhanced_summary: Dict, file_analysis: Dict):
        """Process any new conversations discovered in enhanced daily summary"""
        # This would integrate with the enhanced daily context system
        # to identify conversations that need .dis file generation
        pass
    
    def _initialize_temporal_features(self):
        """Initialize temporal query capabilities"""
        self.temporal_enabled = self.config.get('enable_temporal_queries', True)
        if self.temporal_enabled:
            self.logger.info("Temporal query features enabled")
        else:
            self.logger.info("Temporal query features disabled")
    
    def parse_conversation_date(self, content: str, metadata: Dict, enhanced_analysis: Dict) -> Optional[str]:
        """
        Extract and normalize conversation date from various sources.
        Returns YYYY-MM-DD format or None if no date found.
        """
        import re
        
        # Try different date sources in order of preference
        date_candidates = []
        
        # From conversation analysis
        if enhanced_analysis.get('is_conversation'):
            if 'conversation_id' in enhanced_analysis:
                conv_id = enhanced_analysis['conversation_id']
                date_candidates.append(conv_id)
        
        # From file metadata
        date_candidates.extend([
            metadata.get('filename', ''),
            metadata.get('created_at', ''),
            metadata.get('modified_at', ''),
        ])
        
        # From content (look for date patterns in first 500 chars)
        content_preview = content[:500] if content else ''
        date_candidates.append(content_preview)
        
        # Date extraction patterns
        date_patterns = [
            r'(\d{4}-\d{2}-\d{2})',  # YYYY-MM-DD
            r'(\d{4}/\d{2}/\d{2})',  # YYYY/MM/DD  
            r'(\d{2}/\d{2}/\d{4})',  # MM/DD/YYYY
            r'(\d{4}-\d{1,2}-\d{1,2})',  # YYYY-M-D
            r'(\d{4}\d{2}\d{2})',  # YYYYMMDD
        ]
        
        for candidate in date_candidates:
            if not candidate:
                continue
                
            for pattern in date_patterns:
                match = re.search(pattern, str(candidate))
                if match:
                    date_str = match.group(1)
                    try:
                        # Normalize to YYYY-MM-DD format
                        if '/' in date_str:
                            if date_str.startswith('20'):  # YYYY/MM/DD
                                parts = date_str.split('/')
                                normalized = f"{parts[0]}-{parts[1].zfill(2)}-{parts[2].zfill(2)}"
                            else:  # MM/DD/YYYY
                                parts = date_str.split('/')
                                normalized = f"{parts[2]}-{parts[0].zfill(2)}-{parts[1].zfill(2)}"
                        elif '-' in date_str:  # YYYY-MM-DD format
                            parts = date_str.split('-')
                            normalized = f"{parts[0]}-{parts[1].zfill(2)}-{parts[2].zfill(2)}"
                        elif len(date_str) == 8:  # YYYYMMDD
                            normalized = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"
                        else:
                            continue
                            
                        # Validate date
                        datetime.strptime(normalized, '%Y-%m-%d')
                        return normalized
                        
                    except (ValueError, IndexError):
                        continue
        
        return None
    
    def enhance_metadata_with_temporal_info(self, chunk_metadata: Dict, content: str, 
                                          file_metadata: Dict, enhanced_analysis: Dict) -> Dict:
        """Add temporal metadata to chunk for efficient date-based queries"""
        
        if not self.temporal_enabled:
            return chunk_metadata
        
        # Parse conversation date
        conversation_date = self.parse_conversation_date(content, file_metadata, enhanced_analysis)
        
        # Add temporal metadata
        temporal_metadata = {
            'conversation_date': conversation_date,
            'conversation_year': conversation_date[:4] if conversation_date else None,
            'conversation_month': conversation_date[:7] if conversation_date else None,  # YYYY-MM
            'conversation_day_of_week': None,
            'conversation_timestamp_parsed': None,
        }
        
        # Calculate additional temporal info if we have a valid date
        if conversation_date:
            try:
                date_obj = datetime.strptime(conversation_date, '%Y-%m-%d')
                temporal_metadata.update({
                    'conversation_day_of_week': date_obj.strftime('%A'),  # Monday, Tuesday, etc.
                    'conversation_timestamp_parsed': date_obj.isoformat(),
                })
            except ValueError:
                pass
        
        # Merge with existing metadata
        enhanced_metadata = chunk_metadata.copy()
        enhanced_metadata.update(temporal_metadata)
        
        return enhanced_metadata
    
    def query_conversations_by_date(self, target_date: str, max_results: int = 5) -> List[Dict]:
        """
        Query conversations by specific date across all tripartite collections.
        
        Args:
            target_date: Date in YYYY-MM-DD format (e.g., "2025-06-01")
            max_results: Maximum results to return per collection
        
        Returns:
            List of conversation summaries for the date
        """
        if not self.temporal_enabled:
            self.logger.warning("Temporal queries are disabled")
            return []
        
        self.logger.info(f"Searching for conversations on {target_date}")
        
        all_results = []
        chroma_client = self.daemon.components['context'].client
        
        # Query tripartite collections
        tripartite_collections = self.config.get('tripartite_collections', {})
        
        for domain, collection_name in tripartite_collections.items():
            try:
                collection = chroma_client.get_collection(name=collection_name)
                
                # Query by exact date match
                results = collection.get(
                    where={"conversation_date": target_date},
                    include=['documents', 'metadatas'],
                    limit=max_results
                )
                
                # Process results
                for doc, metadata in zip(results['documents'], results['metadatas']):
                    all_results.append({
                        'domain': domain,
                        'conversation_title': metadata.get('original_filename', 'Untitled'),
                        'conversation_id': metadata.get('conversation_id', metadata.get('float_id')),
                        'conversation_platform': metadata.get('conversation_platform', 'unknown'),
                        'chunk_content_preview': doc[:200] + "..." if len(doc) > 200 else doc,
                        'signal_density': metadata.get('signal_density', 0.0),
                        'metadata': metadata
                    })
                    
            except Exception as e:
                self.logger.warning(f"Error querying {collection_name} for temporal data: {e}")
        
        # Deduplicate by conversation_id and sort
        seen_conversations = {}
        for result in all_results:
            conv_id = result['conversation_id']
            if conv_id not in seen_conversations:
                seen_conversations[conv_id] = result
            else:
                # Keep the one with higher signal density
                existing = seen_conversations[conv_id]
                if result['signal_density'] > existing['signal_density']:
                    seen_conversations[conv_id] = result
        
        unique_results = list(seen_conversations.values())
        unique_results.sort(key=lambda x: (x['conversation_title'], x['domain']))
        
        return unique_results[:max_results]
    
    def get_conversations_for_date_range(self, start_date: str, end_date: str = None, 
                                       max_results: int = 10) -> List[Dict]:
        """
        Get conversations for a date range across tripartite collections.
        
        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format (optional, defaults to start_date)
            max_results: Maximum results to return
        """
        if not self.temporal_enabled:
            self.logger.warning("Temporal queries are disabled")
            return []
        
        if end_date is None:
            end_date = start_date
        
        self.logger.info(f"Querying conversations from {start_date} to {end_date}")
        
        all_results = []
        chroma_client = self.daemon.components['context'].client
        tripartite_collections = self.config.get('tripartite_collections', {})
        
        for domain, collection_name in tripartite_collections.items():
            try:
                collection = chroma_client.get_collection(name=collection_name)
                
                # Build where clause for date range
                if start_date == end_date:
                    where_clause = {"conversation_date": start_date}
                else:
                    where_clause = {
                        "$and": [
                            {"conversation_date": {"$gte": start_date}},
                            {"conversation_date": {"$lte": end_date}}
                        ]
                    }
                
                results = collection.get(
                    where=where_clause,
                    include=['documents', 'metadatas'],
                    limit=max_results
                )
                
                # Process results
                for doc, metadata in zip(results['documents'], results['metadatas']):
                    all_results.append({
                        'date': metadata.get('conversation_date'),
                        'domain': domain,
                        'title': metadata.get('original_filename', 'Untitled'),
                        'conversation_id': metadata.get('conversation_id', metadata.get('float_id')),
                        'platform': metadata.get('conversation_platform', 'unknown'),
                        'summary': doc[:300] + "..." if len(doc) > 300 else doc,
                        'signal_density': metadata.get('signal_density', 0.0)
                    })
                    
            except Exception as e:
                self.logger.warning(f"Error querying {collection_name} for date range: {e}")
        
        # Deduplicate and sort by date
        seen_conversations = {}
        for result in all_results:
            key = f"{result['date']}::{result['conversation_id']}"
            if key not in seen_conversations:
                seen_conversations[key] = result
            else:
                # Keep the one with higher signal density
                existing = seen_conversations[key]
                if result['signal_density'] > existing['signal_density']:
                    seen_conversations[key] = result
        
        unique_results = list(seen_conversations.values())
        unique_results.sort(key=lambda x: (x['date'] or '', x['title']))
        
        return unique_results[:max_results]

if __name__ == "__main__":
    # Test enhanced integration
    print("Enhanced integration system test")
    
    # This would normally be called with a real daemon instance
    # integration = EnhancedSystemIntegration(daemon)
    print("Enhanced integration test placeholder")