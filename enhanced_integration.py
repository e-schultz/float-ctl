"""
Enhanced integration system for FLOAT ecosystem
Bridges daemon, daily context, and conversation processing
Now includes sophisticated pattern detection from tripartite chunker
"""

import re
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from urllib.parse import urlparse

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
    
    def _initialize_cross_reference_system(self):
        """Initialize cross-reference system"""
        try:
            from cross_reference_system import CrossReferenceSystem
            chroma_client = self.daemon.components['context'].client
            self.cross_ref_system = CrossReferenceSystem(
                self.vault_path,
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
        
        # Step 5: Cross-reference generation
        if self.cross_ref_system:
            cross_references = self.cross_ref_system.generate_cross_references(file_analysis, enhanced_analysis)
            file_analysis['cross_references'] = cross_references
        else:
            self.logger.warning("Cross-reference system not available - skipping cross-reference generation")
            file_analysis['cross_references'] = {'vault_references': [], 'chroma_references': [], 'conversation_links': [], 'topic_connections': []}
        
        # Step 6: Enhanced conversation .dis file generation
        if enhanced_analysis.get('is_conversation'):
            if self.conversation_dis_enhanced:
                conversation_dis_path = self.conversation_dis_enhanced.generate_conversation_dis(file_analysis, enhanced_analysis)
            else:
                conversation_dis_path = self._generate_conversation_dis_file(file_analysis, enhanced_analysis)
            file_analysis['conversation_dis_path'] = conversation_dis_path
        
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
        
        # Conversation detection (keep existing logic)
        conversation_analysis = self._analyze_conversation_content(content, metadata)
        enhanced.update(conversation_analysis)
        
        # Content classification
        enhanced['content_classification'] = self._classify_content_type(content, basic_analysis)
        
        # Topic extraction
        enhanced['topics'] = self._extract_topics(content)
        
        # Tripartite routing decisions
        enhanced['tripartite_routing'] = self._determine_tripartite_routing(content, enhanced)
        
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
        
        # Priority classification
        if basic_analysis.get('content_type') == 'AI conversation export':
            return 'ai_conversation'
        elif '"powered_by": "Claude Exporter' in content:
            return 'ai_conversation_chrome_export'
        elif '"powered_by": "ChatGPT Exporter' in content:
            return 'ai_conversation_chrome_export'
        elif 'conversation' in content_lower or 'chat' in content_lower:
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
            primary_domain = enhanced_analysis.get('tripartite_domain', 'concept')
            confidence = enhanced_analysis.get('tripartite_confidence', 0.0)
            scores = enhanced_analysis.get('tripartite_scores', {})
            
            routing = []
            
            # Always include the primary domain
            routing.append(primary_domain)
            
            # Include secondary domains if they have significant scores
            confidence_threshold = 0.3
            for domain, score in scores.items():
                normalized_score = score / max(sum(scores.values()), 1)
                if domain != primary_domain and normalized_score > confidence_threshold:
                    routing.append(domain)
            
            # Special routing rules for high-signal content
            if enhanced_analysis.get('has_high_signal_density', False):
                # High-signal content goes to all domains
                routing = ['concept', 'framework', 'metaphor']
            
            # Conversation-specific routing
            if enhanced_analysis.get('is_conversation'):
                # Conversations often contain all three elements
                if len(routing) == 1:  # If only primary domain, add others
                    for domain in ['concept', 'framework', 'metaphor']:
                        if domain not in routing:
                            routing.append(domain)
            
            # Platform integration content goes to framework
            if enhanced_analysis.get('has_platform_integration', False):
                if 'framework' not in routing:
                    routing.append('framework')
            
            # Persona annotations indicate high-value content for all domains
            if enhanced_analysis.get('has_persona_annotations', False):
                routing = ['concept', 'framework', 'metaphor']
            
            return routing
        
        else:
            # Fallback to basic keyword-based routing
            return self._basic_tripartite_routing(content, enhanced_analysis)
    
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
    
    def _process_new_conversations(self, enhanced_summary: Dict, file_analysis: Dict):
        """Process any new conversations discovered in enhanced daily summary"""
        # This would integrate with the enhanced daily context system
        # to identify conversations that need .dis file generation
        pass

if __name__ == "__main__":
    # Test enhanced integration
    print("Enhanced integration system test")
    
    # This would normally be called with a real daemon instance
    # integration = EnhancedSystemIntegration(daemon)
    print("Enhanced integration test placeholder")