"""
Enhanced .dis file generation specifically for conversations
Creates rich documentation with advanced conversation analysis and Obsidian integration
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from urllib.parse import urlparse

class ConversationDisEnhanced:
    """Enhanced .dis file generation specifically for conversations"""
    
    def __init__(self, dis_generator, vault_path: Path, config: Dict, logger=None):
        self.dis_generator = dis_generator
        self.vault_path = vault_path
        self.config = config
        self.logger = logger
        
        # Conversation storage path
        self.conversation_path = vault_path / "FLOAT.conversations"
        self.conversation_path.mkdir(exist_ok=True)
        
        # Initialize conversation analysis patterns
        self._initialize_conversation_patterns()
        
        # Conversation index
        self.conversation_index = {}
        self._load_conversation_index()
    
    def _initialize_conversation_patterns(self):
        """Initialize patterns for advanced conversation analysis"""
        self.patterns = {
            # Speaker identification
            'claude_speaker': re.compile(r'^(Claude|Assistant):\s*(.*)$', re.MULTILINE | re.IGNORECASE),
            'human_speaker': re.compile(r'^(Human|User):\s*(.*)$', re.MULTILINE | re.IGNORECASE),
            'gpt_speaker': re.compile(r'^(ChatGPT|GPT|AI):\s*(.*)$', re.MULTILINE | re.IGNORECASE),
            
            # Conversation structure
            'message_boundary': re.compile(r'^(Human|User|Claude|Assistant|ChatGPT|GPT|AI):', re.MULTILINE),
            'code_blocks': re.compile(r'```(\w+)?\n(.*?)\n```', re.DOTALL),
            'inline_code': re.compile(r'`([^`]+)`'),
            
            # FLOAT patterns
            'ctx_markers': re.compile(r'ctx::([^:]+)', re.IGNORECASE),
            'highlight_markers': re.compile(r'highlight::([^:]+)', re.IGNORECASE),
            'dispatch_patterns': re.compile(r'float\.dispatch\(([^)]+)\)', re.IGNORECASE),
            
            # Topic and intent patterns
            'questions': re.compile(r'\?[^\?]*$', re.MULTILINE),
            'requests': re.compile(r'^(can you|could you|please|help me|i need|how do i)', re.IGNORECASE | re.MULTILINE),
            'explanations': re.compile(r'^(let me explain|here\'s how|this is|the reason)', re.IGNORECASE | re.MULTILINE),
            
            # URLs and references
            'conversation_urls': re.compile(r'https?://(?:claude\.ai|chatgpt\.com|chat\.openai\.com)/[^\s<>"]+'),
            'file_references': re.compile(r'`([^`]*\.[a-zA-Z0-9]+)`'),
            
            # Conversation metadata
            'conversation_id': re.compile(r'conversation[_-]?id[:\s]*([a-zA-Z0-9_-]+)', re.IGNORECASE),
            'timestamp_patterns': re.compile(r'\b(\d{4}-\d{2}-\d{2}(?:\s+\d{2}:\d{2}(?::\d{2})?)?)\b')
        }
    
    def _load_conversation_index(self):
        """Load existing conversation index"""
        index_file = self.conversation_path / "_conversation_index.json"
        try:
            if index_file.exists():
                with open(index_file, 'r', encoding='utf-8') as f:
                    self.conversation_index = json.load(f)
        except Exception as e:
            if self.logger:
                self.logger.warning(f"Failed to load conversation index: {e}")
            self.conversation_index = {}
    
    def _save_conversation_index(self):
        """Save conversation index"""
        index_file = self.conversation_path / "_conversation_index.json"
        try:
            with open(index_file, 'w', encoding='utf-8') as f:
                json.dump(self.conversation_index, f, indent=2, ensure_ascii=False)
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to save conversation index: {e}")
    
    def generate_conversation_dis(self, file_analysis: Dict, enhanced_analysis: Dict) -> Optional[Path]:
        """Generate enhanced .dis file for conversation content"""
        
        if not enhanced_analysis.get('is_conversation'):
            return None
        
        try:
            # Perform deep conversation analysis
            conversation_analysis = self._analyze_conversation_structure(
                file_analysis, enhanced_analysis
            )
            
            # Generate conversation-specific .dis file
            dis_path = self._create_conversation_dis_file(
                file_analysis, enhanced_analysis, conversation_analysis
            )
            
            # Update conversation index
            self._update_conversation_index(
                enhanced_analysis, conversation_analysis, dis_path
            )
            
            if self.logger:
                self.logger.info(f"Generated enhanced conversation .dis: {dis_path.name}")
            
            return dis_path
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to generate conversation .dis file: {e}")
            return None
    
    def _analyze_conversation_structure(self, file_analysis: Dict, enhanced_analysis: Dict) -> Dict:
        """Perform deep analysis of conversation structure"""
        content = file_analysis.get('content', '')
        
        analysis = {
            'speakers': [],
            'turn_count': 0,
            'message_lengths': [],
            'code_blocks': [],
            'questions_asked': [],
            'topics_discussed': [],
            'float_signals': [],
            'conversation_flow': [],
            'technical_depth': 'unknown',
            'conversation_type': 'unknown',
            'key_insights': [],
            'file_references': [],
            'timestamps': []
        }
        
        # Analyze speakers and turns
        analysis.update(self._analyze_speakers_and_turns(content))
        
        # Analyze content patterns
        analysis.update(self._analyze_content_patterns(content))
        
        # Analyze FLOAT signals
        analysis['float_signals'] = self._extract_float_signals(content)
        
        # Analyze conversation flow
        analysis['conversation_flow'] = self._analyze_conversation_flow(content)
        
        # Determine conversation characteristics
        analysis['technical_depth'] = self._assess_technical_depth(content, analysis)
        analysis['conversation_type'] = self._classify_conversation_type(content, analysis)
        
        # Extract key insights
        analysis['key_insights'] = self._extract_key_insights(content, analysis)
        
        return analysis
    
    def _analyze_speakers_and_turns(self, content: str) -> Dict:
        """Analyze conversation speakers and turn-taking"""
        speakers = set()
        turns = []
        current_speaker = None
        current_content = []
        
        lines = content.split('\n')
        
        for line in lines:
            # Check for speaker change
            speaker_match = self.patterns['message_boundary'].match(line)
            if speaker_match:
                # Save previous speaker's content
                if current_speaker and current_content:
                    turns.append({
                        'speaker': current_speaker,
                        'content': '\n'.join(current_content).strip(),
                        'length': len('\n'.join(current_content))
                    })
                
                # Start new speaker turn
                current_speaker = speaker_match.group(1).lower()
                speakers.add(current_speaker)
                current_content = [line[len(speaker_match.group(0)):].strip()]
            else:
                if current_content is not None:
                    current_content.append(line)
        
        # Save last speaker's content
        if current_speaker and current_content:
            turns.append({
                'speaker': current_speaker,
                'content': '\n'.join(current_content).strip(),
                'length': len('\n'.join(current_content))
            })
        
        # Calculate statistics
        message_lengths = [turn.get('length', 0) for turn in turns if isinstance(turn, dict)]
        speaker_stats = {}
        for speaker in speakers:
            speaker_turns = [turn for turn in turns if isinstance(turn, dict) and turn.get('speaker') == speaker]
            speaker_stats[speaker] = {
                'turn_count': len(speaker_turns),
                'avg_length': sum(turn.get('length', 0) for turn in speaker_turns) / len(speaker_turns) if speaker_turns else 0,
                'total_length': sum(turn.get('length', 0) for turn in speaker_turns)
            }
        
        return {
            'speakers': list(speakers),
            'speaker_stats': speaker_stats,
            'turn_count': len(turns),
            'message_lengths': message_lengths,
            'conversation_turns': turns
        }
    
    def _analyze_content_patterns(self, content: str) -> Dict:
        """Analyze content patterns and structure"""
        analysis = {}
        
        # Code analysis
        code_blocks = self.patterns['code_blocks'].findall(content)
        analysis['code_blocks'] = [
            {'language': lang or 'unknown', 'code': code.strip(), 'length': len(code)}
            for lang, code in code_blocks
        ]
        
        inline_code = self.patterns['inline_code'].findall(content)
        analysis['inline_code_count'] = len(inline_code)
        
        # Question analysis
        questions = self.patterns['questions'].findall(content)
        analysis['questions_asked'] = [q.strip() for q in questions if len(q.strip()) > 5]
        
        # File references
        file_refs = self.patterns['file_references'].findall(content)
        analysis['file_references'] = list(set(file_refs))
        
        # URL analysis
        urls = self.patterns['conversation_urls'].findall(content)
        analysis['conversation_urls'] = urls
        
        # Timestamp extraction
        timestamps = self.patterns['timestamp_patterns'].findall(content)
        analysis['timestamps'] = list(set(timestamps))
        
        return analysis
    
    def _extract_float_signals(self, content: str) -> List[Dict]:
        """Extract and analyze FLOAT signals"""
        signals = []
        
        # Context markers
        ctx_matches = self.patterns['ctx_markers'].findall(content)
        for match in ctx_matches:
            signals.append({
                'type': 'ctx',
                'content': match.strip(),
                'importance': 'context',
                'category': self._categorize_signal(match)
            })
        
        # Highlight markers
        highlight_matches = self.patterns['highlight_markers'].findall(content)
        for match in highlight_matches:
            signals.append({
                'type': 'highlight',
                'content': match.strip(),
                'importance': 'highlight',
                'category': self._categorize_signal(match)
            })
        
        # Dispatch patterns
        dispatch_matches = self.patterns['dispatch_patterns'].findall(content)
        for match in dispatch_matches:
            signals.append({
                'type': 'dispatch',
                'content': match.strip(),
                'importance': 'dispatch',
                'category': 'action'
            })
        
        return signals
    
    def _categorize_signal(self, signal_content: str) -> str:
        """Categorize FLOAT signal by content"""
        content_lower = signal_content.lower()
        
        if any(word in content_lower for word in ['question', 'ask', 'how', 'what', 'why']):
            return 'inquiry'
        elif any(word in content_lower for word in ['important', 'key', 'crucial', 'significant']):
            return 'importance'
        elif any(word in content_lower for word in ['todo', 'action', 'next', 'follow']):
            return 'action'
        elif any(word in content_lower for word in ['insight', 'learning', 'understanding']):
            return 'insight'
        else:
            return 'general'
    
    def _analyze_conversation_flow(self, content: str) -> List[Dict]:
        """Analyze the flow and progression of conversation"""
        flow = []
        
        # This is a simplified flow analysis
        # In practice, you might want more sophisticated NLP
        
        sections = content.split('\n\n')
        for i, section in enumerate(sections):
            if len(section.strip()) > 50:  # Substantial content
                flow_item = {
                    'section': i + 1,
                    'type': self._classify_section_type(section),
                    'length': len(section),
                    'has_code': '```' in section,
                    'has_questions': '?' in section,
                    'has_float_signals': 'ctx::' in section or 'highlight::' in section
                }
                flow.append(flow_item)
        
        return flow
    
    def _classify_section_type(self, section: str) -> str:
        """Classify a conversation section"""
        section_lower = section.lower()
        
        if section.startswith(('Human:', 'User:')):
            if '?' in section:
                return 'user_question'
            elif any(word in section_lower for word in ['please', 'can you', 'help']):
                return 'user_request'
            else:
                return 'user_statement'
        elif section.startswith(('Claude:', 'Assistant:', 'ChatGPT:')):
            if '```' in section:
                return 'ai_code_response'
            elif len(section) > 500:
                return 'ai_detailed_response'
            else:
                return 'ai_response'
        else:
            return 'content'
    
    def _assess_technical_depth(self, content: str, analysis: Dict) -> str:
        """Assess the technical depth of the conversation"""
        code_density = len(analysis.get('code_blocks', [])) / max(len(content) / 1000, 1)
        technical_terms = len(re.findall(r'\b(?:function|class|method|algorithm|database|API|framework|library|implementation)\b', content, re.IGNORECASE))
        
        if code_density > 2 or technical_terms > 10:
            return 'high'
        elif code_density > 0.5 or technical_terms > 5:
            return 'medium'
        else:
            return 'low'
    
    def _classify_conversation_type(self, content: str, analysis: Dict) -> str:
        """Classify the type of conversation"""
        content_lower = content.lower()
        
        # Check for patterns
        if any(word in content_lower for word in ['debug', 'error', 'fix', 'bug', 'problem']):
            return 'troubleshooting'
        elif any(word in content_lower for word in ['learn', 'explain', 'understand', 'how does']):
            return 'educational'
        elif len(analysis.get('code_blocks', [])) > 3:
            return 'coding_session'
        elif any(word in content_lower for word in ['brainstorm', 'idea', 'concept', 'design']):
            return 'brainstorming'
        elif any(word in content_lower for word in ['review', 'feedback', 'opinion', 'thoughts']):
            return 'review_session'
        else:
            return 'general_discussion'
    
    def _extract_key_insights(self, content: str, analysis: Dict) -> List[str]:
        """Extract key insights from the conversation"""
        insights = []
        
        # Insights from FLOAT signals
        for signal in analysis.get('float_signals', []):
            if isinstance(signal, dict) and signal.get('type') in ['highlight', 'ctx']:
                content = signal.get('content', '')
                if content:
                    insights.append(content)
        
        # Insights from questions and answers
        turns = analysis.get('conversation_turns', [])
        for i, turn in enumerate(turns):
            if not isinstance(turn, dict):
                continue
            if turn.get('speaker') in ['human', 'user'] and '?' in turn.get('content', ''):
                # Look for the AI response
                if i + 1 < len(turns) and isinstance(turns[i + 1], dict) and turns[i + 1].get('speaker') in ['claude', 'assistant', 'chatgpt']:
                    response = turns[i + 1].get('content', '')
                    if len(response) > 100:  # Substantial response
                        # Extract first sentence as insight
                        sentences = response.split('.')
                        if sentences and len(sentences[0]) > 20:
                            insights.append(sentences[0].strip())
        
        return insights[:5]  # Limit to top 5 insights
    
    def _create_conversation_dis_file(self, file_analysis: Dict, enhanced_analysis: Dict, conversation_analysis: Dict) -> Path:
        """Create enhanced conversation .dis file"""
        
        # Create filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        platform = enhanced_analysis.get('conversation_platform', 'unknown')
        conv_id = enhanced_analysis.get('conversation_id', 'unknown')[:8]
        
        filename = f"{timestamp}_{platform}_{conv_id}.conversation.float_dis.md"
        dis_path = self.conversation_path / filename
        
        # Generate content
        dis_content = self._create_enhanced_dis_content(
            file_analysis, enhanced_analysis, conversation_analysis
        )
        
        # Write file
        with open(dis_path, 'w', encoding='utf-8') as f:
            f.write(dis_content)
        
        return dis_path
    
    def _create_enhanced_dis_content(self, file_analysis: Dict, enhanced_analysis: Dict, conversation_analysis: Dict) -> str:
        """Create enhanced .dis file content for conversations"""
        metadata = file_analysis.get('metadata', {})
        cross_refs = file_analysis.get('cross_references', {})
        
        # Enhanced frontmatter
        frontmatter = {
            'float_id': file_analysis.get('float_id'),
            'conversation_id': enhanced_analysis.get('conversation_id'),
            'platform': enhanced_analysis.get('conversation_platform'),
            'conversation_type': conversation_analysis.get('conversation_type'),
            'technical_depth': conversation_analysis.get('technical_depth'),
            'participants': enhanced_analysis.get('participants'),
            'speakers': conversation_analysis.get('speakers'),
            'turn_count': conversation_analysis.get('turn_count', 0),
            'message_count': enhanced_analysis.get('message_count', 0),
            'topics': enhanced_analysis.get('topics'),
            'signal_count': len(conversation_analysis.get('float_signals', [])),
            'code_blocks': len(conversation_analysis.get('code_blocks', [])),
            'questions_count': len(conversation_analysis.get('questions_asked', [])),
            'file_references': conversation_analysis.get('file_references'),
            'timestamps': conversation_analysis.get('timestamps'),
            'processed_at': file_analysis.get('processed_at'),
            'original_file': metadata.get('filename'),
            'file_size_bytes': metadata.get('size_bytes', 0)
        }
        
        yaml_header = "---\n"
        for key, value in frontmatter.items():
            if value is not None:
                if isinstance(value, (list, dict)):
                    yaml_header += f"{key}: {json.dumps(value)}\n"
                else:
                    yaml_header += f"{key}: {value}\n"
        yaml_header += "---\n\n"
        
        # Create enhanced content
        platform_name = enhanced_analysis.get('conversation_platform', 'Unknown').replace('_', ' ').title()
        conv_type = conversation_analysis.get('conversation_type', 'unknown').replace('_', ' ').title()
        
        content = f"""# 💬 {conv_type}: {enhanced_analysis.get('conversation_id', 'Unknown')}

## Conversation Overview
- **Platform**: {platform_name}
- **Type**: {conv_type}
- **Technical Depth**: {conversation_analysis.get('technical_depth', 'unknown').title()}
- **Participants**: {', '.join(enhanced_analysis.get('participants', []))}
- **Turn Count**: {conversation_analysis.get('turn_count', 0)}
- **Duration**: {self._estimate_conversation_duration(conversation_analysis)}

## Speaker Analysis
{self._generate_speaker_analysis(conversation_analysis)}

## Content Analysis
- **Code Blocks**: {len(conversation_analysis.get('code_blocks', []))}
- **Questions Asked**: {len(conversation_analysis.get('questions_asked', []))}
- **FLOAT Signals**: {len(conversation_analysis.get('float_signals', []))}
- **File References**: {len(conversation_analysis.get('file_references', []))}

### Programming Languages Used
{self._generate_language_analysis(conversation_analysis)}

### Key Questions
{chr(10).join([f"- {q[:100]}..." if len(q) > 100 else f"- {q}" for q in conversation_analysis.get('questions_asked', [])[:5]])}

## FLOAT Signal Analysis
{self._generate_signal_analysis(conversation_analysis)}

## Key Insights
{chr(10).join([f"- {insight}" for insight in conversation_analysis.get('key_insights', [])])}

## Topics Discussed
{chr(10).join([f"- **{topic}**" for topic in enhanced_analysis.get('topics', [])])}

## Conversation Flow
{self._generate_flow_analysis(conversation_analysis)}

## Cross-References

### Related Conversations
```dataview
LIST FROM "FLOAT.conversations"
WHERE contains(file.frontmatter.topics, "{enhanced_analysis.get('topics', ['unknown'])[0] if enhanced_analysis.get('topics') and len(enhanced_analysis.get('topics', [])) > 0 else 'unknown'}")
AND file.name != this.file.name
SORT file.ctime DESC
LIMIT 5
```

### Related Files
{chr(10).join([f"- `{ref}`" for ref in conversation_analysis.get('file_references', [])])}

### External Links
{chr(10).join([f"- [{link.get('title', 'Link') if link and isinstance(link, dict) else 'Link'}]({link.get('url', '#') if link and isinstance(link, dict) else '#'})" for link in cross_refs.get('conversation_links', []) if link and isinstance(link, dict)])}

## Processing Details
- **Float ID**: `{file_analysis.get('float_id')}`
- **Original File**: `{metadata.get('filename', 'Unknown')}`
- **Processed**: {file_analysis.get('processed_at', 'Unknown')}
- **File Size**: {metadata.get('size_bytes', 0):,} bytes

## Templater Quick Actions

### Extract Code
```javascript
<%*
// Extract all code blocks for reference
const content = tp.file.content;
const codeBlocks = content.match(/```[\\s\\S]*?```/g) || [];
const extractedCode = codeBlocks.join('\\n\\n');
await tp.file.create_new("Extracted Code - " + tp.file.title, extractedCode, "Code Extracts");
%>
```

### Create Follow-up Note
```javascript
<%*
const followUpTitle = `Follow-up - ${tp.file.title}`;
const template = `# Follow-up Actions

Based on conversation: [[${tp.file.title}]]

## Action Items
- [ ] 

## Questions to Explore
- 

## Code to Implement
- 

## Research Topics
- 
`;
await tp.file.create_new(followUpTitle, template);
%>
```

---

*Enhanced conversation analysis powered by FLOAT Conversation Dis Enhanced System*
"""
        
        return yaml_header + content
    
    def _estimate_conversation_duration(self, analysis: Dict) -> str:
        """Estimate conversation duration based on content"""
        turn_count = analysis.get('turn_count', 0)
        total_length = sum(analysis.get('message_lengths', []))
        
        # Rough estimation based on turn count and content length
        if turn_count > 50 or total_length > 20000:
            return "Extended (1+ hours)"
        elif turn_count > 20 or total_length > 10000:
            return "Medium (30-60 minutes)"
        elif turn_count > 10 or total_length > 5000:
            return "Short (15-30 minutes)"
        else:
            return "Brief (< 15 minutes)"
    
    def _generate_speaker_analysis(self, analysis: Dict) -> str:
        """Generate speaker analysis section"""
        speaker_stats = analysis.get('speaker_stats', {})
        
        analysis_text = ""
        for speaker, stats in speaker_stats.items():
            if not isinstance(stats, dict):
                continue
            analysis_text += f"### {speaker.title()}\n"
            analysis_text += f"- **Turns**: {stats.get('turn_count', 0)}\n"
            analysis_text += f"- **Average Length**: {stats.get('avg_length', 0):.0f} characters\n"
            analysis_text += f"- **Total Content**: {stats.get('total_length', 0):,} characters\n\n"
        
        return analysis_text
    
    def _generate_language_analysis(self, analysis: Dict) -> str:
        """Generate programming language analysis"""
        code_blocks = analysis.get('code_blocks', [])
        
        if not code_blocks:
            return "- No code blocks detected"
        
        languages = {}
        for block in code_blocks:
            if not isinstance(block, dict):
                continue
            lang = block.get('language', 'unknown')
            if lang not in languages:
                languages[lang] = {'count': 0, 'total_length': 0}
            languages[lang]['count'] += 1
            languages[lang]['total_length'] += block.get('length', 0)
        
        lang_analysis = ""
        for lang, stats in languages.items():
            lang_analysis += f"- **{lang.title()}**: {stats['count']} blocks, {stats['total_length']:,} characters\\n"
        
        return lang_analysis
    
    def _generate_signal_analysis(self, analysis: Dict) -> str:
        """Generate FLOAT signal analysis"""
        signals = analysis.get('float_signals', [])
        
        if not signals:
            return "- No FLOAT signals detected"
        
        signal_analysis = ""
        by_type = {}
        by_category = {}
        
        for signal in signals:
            if not isinstance(signal, dict):
                continue
            signal_type = signal.get('type', 'unknown')
            category = signal.get('category', 'unknown')
            
            if signal_type not in by_type:
                by_type[signal_type] = []
            by_type[signal_type].append(signal)
            
            if category not in by_category:
                by_category[category] = 0
            by_category[category] += 1
        
        signal_analysis += f"### By Type\\n"
        for signal_type, signals_list in by_type.items():
            signal_analysis += f"- **{signal_type}**: {len(signals_list)} signals\\n"
        
        signal_analysis += f"\\n### By Category\\n"
        for category, count in by_category.items():
            signal_analysis += f"- **{category.title()}**: {count} signals\\n"
        
        return signal_analysis
    
    def _generate_flow_analysis(self, analysis: Dict) -> str:
        """Generate conversation flow analysis"""
        flow = analysis.get('conversation_flow', [])
        
        if not flow:
            return "- No flow analysis available"
        
        flow_analysis = ""
        for item in flow[:10]:  # Limit to first 10 sections
            if not isinstance(item, dict):
                continue
            section = item.get('section', 'Unknown')
            item_type = item.get('type', 'unknown').replace('_', ' ').title()
            flow_analysis += f"- **Section {section}**: {item_type}"
            if item.get('has_code'):
                flow_analysis += " (with code)"
            if item.get('has_questions'):
                flow_analysis += " (with questions)"
            if item.get('has_float_signals'):
                flow_analysis += " (with signals)"
            flow_analysis += "\\n"
        
        return flow_analysis
    
    def _update_conversation_index(self, enhanced_analysis: Dict, conversation_analysis: Dict, dis_path: Path):
        """Update conversation index with new conversation"""
        try:
            conv_id = enhanced_analysis.get('conversation_id', 'unknown')
            
            index_entry = {
                'conversation_id': conv_id,
                'platform': enhanced_analysis.get('conversation_platform'),
                'conversation_type': conversation_analysis.get('conversation_type'),
                'technical_depth': conversation_analysis.get('technical_depth'),
                'turn_count': conversation_analysis.get('turn_count', 0),
                'topics': enhanced_analysis.get('topics', []),
                'dis_file': dis_path.name,
                'created_at': datetime.now().isoformat()
            }
            
            self.conversation_index[conv_id] = index_entry
            self._save_conversation_index()
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to update conversation index: {e}")

if __name__ == "__main__":
    # Test conversation dis enhanced
    print("Conversation dis enhanced test placeholder")
    
    # This would normally be called with real parameters
    # conv_dis = ConversationDisEnhanced(dis_generator, vault_path, config)
    print("Conversation dis enhanced test complete")