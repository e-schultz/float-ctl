"""
Streamlined FLOAT .dis Template System - Issue #4
Follows "shacks not cathedrals" philosophy with minimal, useful output
"""

import json
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

class StreamlinedFloatDisGenerator:
    """
    Generates focused .float_dis.md files with essential metadata only.
    Philosophy: surgical and useful, not comprehensive and verbose.
    """
    
    def __init__(self):
        self.template_version = "2.0"
        
    def generate_float_dis(self, file_metadata: Dict, chroma_metadata: Dict, 
                          content_analysis: Dict, float_id: str, 
                          enhanced_patterns: Dict = None) -> str:
        """
        Generate a streamlined .float_dis.md file focused on essential information.
        """
        
        # Generate minimal frontmatter
        frontmatter = self.generate_minimal_frontmatter(
            file_metadata, chroma_metadata, content_analysis, float_id, enhanced_patterns
        )
        
        # Generate focused content
        template_content = self.generate_focused_content(
            file_metadata, chroma_metadata, content_analysis, float_id, enhanced_patterns
        )
        
        # Combine into streamlined .dis file
        dis_content = f"""---
{yaml.dump(frontmatter, default_flow_style=False, sort_keys=False).strip()}
---

{template_content}
"""
        
        return dis_content
    
    def generate_minimal_frontmatter(self, file_metadata: Dict, chroma_metadata: Dict, 
                                   content_analysis: Dict, float_id: str,
                                   enhanced_patterns: Dict = None) -> Dict:
        """
        Generate minimal YAML frontmatter focused on essential metadata.
        """
        
        # Extract enhanced pattern counts if available
        enhanced_data = enhanced_patterns or {}
        extended_patterns = enhanced_data.get('extended_float_patterns', {})
        
        # Count enhanced patterns
        inline_pattern_count = sum([
            extended_patterns.get('inline_expand_on', {}).get('count', 0),
            extended_patterns.get('inline_relates_to', {}).get('count', 0),
            extended_patterns.get('inline_connect_to', {}).get('count', 0),
            extended_patterns.get('inline_remember_when', {}).get('count', 0),
        ])
        
        line_pattern_count = sum([
            extended_patterns.get('line_mood', {}).get('count', 0),
            extended_patterns.get('line_boundary', {}).get('count', 0),
            extended_patterns.get('line_progress', {}).get('count', 0),
            extended_patterns.get('line_issue', {}).get('count', 0),
        ])
        
        frontmatter = {
            # Essential identification
            'float_id': float_id,
            'generated': datetime.now().strftime('%Y-%m-%d %H:%M'),
            
            # Core file info
            'source_file': file_metadata['filename'],
            'size': self.format_file_size(file_metadata['size_bytes']),
            'type': content_analysis.get('content_type', 'document'),
            
            # Storage info
            'chroma_collection': chroma_metadata.get('collection_name', 'unknown'),
            'chunks': chroma_metadata.get('chunk_count', 0),
            
            # Pattern summary (only if patterns exist)
            'float_patterns': self._summarize_patterns(content_analysis, enhanced_patterns),
            
            # Obsidian integration
            'tags': self._generate_obsidian_tags(content_analysis, enhanced_patterns)
        }
        
        # Only include non-empty sections
        frontmatter = {k: v for k, v in frontmatter.items() if v}
        
        return frontmatter
    
    def _summarize_patterns(self, content_analysis: Dict, enhanced_patterns: Dict = None) -> Dict:
        """Generate concise pattern summary."""
        if not enhanced_patterns:
            return {}
        
        core_patterns = enhanced_patterns.get('core_float_patterns', {})
        extended_patterns = enhanced_patterns.get('extended_float_patterns', {})
        
        # Count significant patterns only
        ctx_count = core_patterns.get('ctx_markers', {}).get('count', 0)
        highlight_count = core_patterns.get('highlight_markers', {}).get('count', 0)
        
        # Enhanced patterns from Issue #3
        inline_count = sum([
            extended_patterns.get('inline_expand_on', {}).get('count', 0),
            extended_patterns.get('inline_relates_to', {}).get('count', 0),
            extended_patterns.get('inline_connect_to', {}).get('count', 0),
        ])
        
        line_count = sum([
            extended_patterns.get('line_mood', {}).get('count', 0),
            extended_patterns.get('line_boundary', {}).get('count', 0),
            extended_patterns.get('line_progress', {}).get('count', 0),
        ])
        
        patterns = {}
        if ctx_count > 0:
            patterns['ctx'] = ctx_count
        if highlight_count > 0:
            patterns['highlights'] = highlight_count
        if inline_count > 0:
            patterns['inline'] = inline_count
        if line_count > 0:
            patterns['line_level'] = line_count
            
        return patterns
    
    def _generate_obsidian_tags(self, content_analysis: Dict, enhanced_patterns: Dict = None) -> List[str]:
        """Generate useful Obsidian tags."""
        tags = ['float/processed']
        
        # Content type tag
        content_type = content_analysis.get('content_type', '').lower()
        if content_type:
            tags.append(f'type/{content_type}')
        
        # Pattern density tag
        if enhanced_patterns:
            signal_analysis = enhanced_patterns.get('signal_analysis', {})
            density = signal_analysis.get('signal_density', 0)
            if density > 0.05:  # 5% threshold
                tags.append('float/high-signal')
        
        return tags
    
    def generate_focused_content(self, file_metadata: Dict, chroma_metadata: Dict, 
                               content_analysis: Dict, float_id: str,
                               enhanced_patterns: Dict = None) -> str:
        """
        Generate focused template content that's actually useful.
        """
        
        filename = file_metadata['filename']
        summary = content_analysis.get('summary', 'No summary available')
        
        # Extract key patterns for display
        pattern_section = self._generate_pattern_section(enhanced_patterns)
        
        # Templater-compatible content
        content = f"""# 📄 {filename}

## Summary
{self._format_summary(summary)}

{pattern_section}

## Quick Actions
- [[{filename}|📖 View Original]]
- `float_id: {float_id}`

## Templater Integration
```javascript
// Access this content in other templates:
// <%* const floatData = {{
//   id: "{float_id}",
//   file: "{filename}",
//   collection: "{chroma_metadata.get('collection_name', 'unknown')}"
// }}; %>
```

---
*Generated by FLOAT v{self.template_version} • {datetime.now().strftime('%Y-%m-%d %H:%M')}*"""
        
        return content
    
    def _generate_pattern_section(self, enhanced_patterns: Dict = None) -> str:
        """Generate useful pattern summary if patterns exist."""
        if not enhanced_patterns:
            return ""
        
        core_patterns = enhanced_patterns.get('core_float_patterns', {})
        extended_patterns = enhanced_patterns.get('extended_float_patterns', {})
        
        pattern_lines = []
        
        # Core FLOAT patterns
        ctx_count = core_patterns.get('ctx_markers', {}).get('count', 0)
        if ctx_count > 0:
            pattern_lines.append(f"- **Context markers**: {ctx_count}")
        
        highlight_count = core_patterns.get('highlight_markers', {}).get('count', 0)
        if highlight_count > 0:
            pattern_lines.append(f"- **Highlights**: {highlight_count}")
        
        # Enhanced patterns (Issue #3)
        inline_expand = extended_patterns.get('inline_expand_on', {}).get('count', 0)
        if inline_expand > 0:
            pattern_lines.append(f"- **Inline expansions**: {inline_expand}")
        
        boundary_count = extended_patterns.get('line_boundary', {}).get('count', 0)
        if boundary_count > 0:
            pattern_lines.append(f"- **Boundaries**: {boundary_count}")
        
        progress_count = extended_patterns.get('line_progress', {}).get('count', 0)
        if progress_count > 0:
            pattern_lines.append(f"- **Progress notes**: {progress_count}")
        
        if pattern_lines:
            return f"""## FLOAT Patterns
{chr(10).join(pattern_lines)}
"""
        
        return ""
    
    def _format_summary(self, summary: str) -> str:
        """Format summary to be more readable."""
        if not summary or summary == "No summary available":
            return "*No summary available*"
        
        # Truncate overly long summaries
        if len(summary) > 500:
            return summary[:497] + "..."
        
        return summary
    
    def format_file_size(self, size_bytes: int) -> str:
        """Format file size in human-readable format."""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        
        return f"{size_bytes:.1f} {size_names[i]}"