"""
FLOAT .dis Template System - Fixed Templater Syntax
Generates {filename}.float_dis.md files with YAML frontmatter and proper static content
"""

import json
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

class FloatDisGenerator:
    """
    Generates .float_dis.md files with rich metadata and clean static content.
    """
    
    def __init__(self):
        self.template_version = "1.0"
        
    def generate_float_dis(self, file_metadata: Dict, chroma_metadata: Dict, 
                          content_analysis: Dict, float_id: str) -> str:
        """
        Generate a complete .float_dis.md file with YAML frontmatter and static content.
        """
        
        # Generate YAML frontmatter
        frontmatter = self.generate_frontmatter(file_metadata, chroma_metadata, content_analysis, float_id)
        
        # Generate static template content
        template_content = self.generate_template_content(file_metadata, chroma_metadata, content_analysis, float_id)
        
        # Combine into full .dis file
        dis_content = f"""---
{yaml.dump(frontmatter, default_flow_style=False, sort_keys=False).strip()}
---

{template_content}
"""
        
        return dis_content
    
    def generate_frontmatter(self, file_metadata: Dict, chroma_metadata: Dict, 
                           content_analysis: Dict, float_id: str) -> Dict:
        """
        Generate comprehensive YAML frontmatter for the .dis file.
        """
        
        frontmatter = {
            # Core FLOAT metadata
            'float_id': float_id,
            'float_type': 'dropzone_ingestion',
            'float_version': self.template_version,
            'generated_at': datetime.now().isoformat(),
            
            # Original file metadata
            'original_file': {
                'name': file_metadata['filename'],
                'path': file_metadata.get('relative_path', file_metadata['filename']),
                'extension': file_metadata['extension'],
                'size_bytes': file_metadata['size_bytes'],
                'size_human': self.format_file_size(file_metadata['size_bytes']),
                'mime_type': file_metadata.get('mime_type', 'unknown'),
                'file_type': file_metadata.get('file_type', 'Unknown')
            },
            
            # Timestamps
            'timestamps': {
                'file_created': file_metadata.get('created_at'),
                'file_modified': file_metadata.get('modified_at'),
                'processed_at': datetime.now().isoformat(),
                'ingestion_date': datetime.now().strftime('%Y-%m-%d')
            },
            
            # Chroma storage metadata
            'chroma': {
                'collection_name': chroma_metadata.get('collection_name', 'unknown'),
                'chunk_count': chroma_metadata.get('chunk_count', 0),
                'total_chunks': chroma_metadata.get('total_chunks', 0),
                'chunk_ids': chroma_metadata.get('chunk_ids', []),
                'embedding_model': chroma_metadata.get('embedding_model', 'default'),
                'storage_path': chroma_metadata.get('storage_path', '')
            },
            
            # Content analysis
            'content': {
                'summary': content_analysis.get('summary', 'No summary available'),
                'word_count': content_analysis.get('word_count', 0),
                'line_count': content_analysis.get('line_count', 0),
                'content_type': content_analysis.get('content_type', 'Unknown'),
                'detected_patterns': content_analysis.get('detected_patterns', []),
                'language': content_analysis.get('language', 'unknown'),
                'encoding': content_analysis.get('encoding', 'utf-8')
            },
            
            # FLOAT patterns (enhanced from pattern detector)
            'float_patterns': {
                'has_ctx_markers': content_analysis.get('has_ctx_markers', False),
                'has_highlights': content_analysis.get('has_highlights', False),
                'has_float_dispatch': content_analysis.get('has_float_dispatch', False),
                'has_conversation_links': content_analysis.get('has_conversation_links', False),
                
                # Enhanced patterns from tripartite chunker
                'core_signals': content_analysis.get('float_patterns', {}).get('ctx_markers', 0) + 
                              content_analysis.get('float_patterns', {}).get('highlight_markers', 0) + 
                              content_analysis.get('float_patterns', {}).get('signal_markers', 0),
                'extended_patterns': content_analysis.get('float_patterns', {}).get('expand_on', 0) + 
                                   content_analysis.get('float_patterns', {}).get('relates_to', 0) + 
                                   content_analysis.get('float_patterns', {}).get('remember_when', 0) + 
                                   content_analysis.get('float_patterns', {}).get('story_time', 0),
                'persona_annotations': content_analysis.get('persona_count', 0),
                'dominant_persona': content_analysis.get('dominant_persona'),
                'signal_density': content_analysis.get('signal_density', 0.0),
                'has_high_signal_density': content_analysis.get('has_high_signal_density', False),
                'ctx_count': content_analysis.get('ctx_count', 0),
                'highlight_count': content_analysis.get('highlight_count', 0),
                'signal_density': content_analysis.get('signal_density', 0.0)
            },
            
            # Tripartite classification (enhanced from pattern detector)
            'tripartite': {
                'primary_domain': content_analysis.get('tripartite_domain', 'concept'),
                'confidence': content_analysis.get('tripartite_confidence', 0.0),
                'scores': content_analysis.get('tripartite_scores', {}),
                'routing': content_analysis.get('tripartite_routing', []),
                'content_complexity': content_analysis.get('content_complexity', 'medium'),
                'is_high_priority': content_analysis.get('is_high_priority', False)
            },
            
            # Platform integration analysis
            'platform_integration': {
                'has_platform_refs': content_analysis.get('has_platform_integration', False),
                'platform_count': content_analysis.get('platform_references', 0),
                'build_tools': content_analysis.get('build_tool_references', []),
                'external_services': content_analysis.get('external_service_references', [])
            },
            
            # Document structure analysis
            'document_structure': content_analysis.get('document_structure', {
                'heading_count': 0,
                'list_density': 0,
                'code_density': 0.0,
                'action_items': 0
            }),
            
            # Cross-reference potential
            'cross_references': {
                'score': content_analysis.get('cross_reference_score', 0.0),
                'has_potential': content_analysis.get('has_cross_reference_potential', False),
                'citation_count': content_analysis.get('citation_count', 0),
                'link_count': content_analysis.get('link_count', 0)
            },
            
            # Actionable insights
            'insights': {
                'actionable_items': content_analysis.get('actionable_insights', []),
                'priority_items': [item for item in content_analysis.get('actionable_insights', []) 
                                 if item.get('priority') == 'high'],
                'total_insights': len(content_analysis.get('actionable_insights', []))
            },
            
            # Processing metadata
            'processing': {
                'daemon_version': '1.0',
                'processing_method': 'automated_dropzone',
                'chunking_strategy': chroma_metadata.get('chunking_strategy', 'content_aware'),
                'content_extracted': content_analysis.get('extraction_successful', False),
                'errors': content_analysis.get('errors', [])
            },
            
            # Obsidian integration
            'obsidian': {
                'template_type': 'float_dis',
                'auto_update': True,
                'display_mode': 'rich',
                'tags': self.generate_auto_tags(file_metadata, content_analysis)
            }
        }
        
        return frontmatter
    
    def generate_auto_tags(self, file_metadata: Dict, content_analysis: Dict) -> List[str]:
        """
        Generate automatic tags based on file and content analysis.
        """
        tags = ['float/dropzone', 'auto-generated']
        
        # File type tags
        extension = file_metadata['extension'].lower()
        if extension in ['.json']:
            tags.append('data/json')
        elif extension in ['.pdf']:
            tags.append('document/pdf')
        elif extension in ['.md', '.txt']:
            tags.append('text/markdown')
        elif extension in ['.docx', '.doc']:
            tags.append('document/word')
        
        # Content type tags
        content_type = content_analysis.get('content_type', '').lower()
        if 'conversation' in content_type or 'chat' in content_type:
            tags.append('content/conversation')
        if 'export' in content_type:
            tags.append('content/export')
        
        # FLOAT pattern tags
        if content_analysis.get('has_ctx_markers'):
            tags.append('float/ctx')
        if content_analysis.get('has_highlights'):
            tags.append('float/highlight')
        if content_analysis.get('has_float_dispatch'):
            tags.append('float/dispatch')
        
        # Enhanced FLOAT pattern tags
        if content_analysis.get('has_high_signal_density'):
            tags.append('float/high-signal')
        if content_analysis.get('persona_count', 0) > 0:
            tags.append('float/persona')
        if content_analysis.get('has_platform_integration'):
            tags.append('float/platform-integration')
        
        # Tripartite classification tags
        tripartite_domain = content_analysis.get('tripartite_domain')
        if tripartite_domain:
            tags.append(f'tripartite/{tripartite_domain}')
        
        tripartite_confidence = content_analysis.get('tripartite_confidence', 0)
        if tripartite_confidence > 0.8:
            tags.append('tripartite/high-confidence')
        elif tripartite_confidence > 0.5:
            tags.append('tripartite/medium-confidence')
        else:
            tags.append('tripartite/low-confidence')
        
        # Content complexity tags
        complexity = content_analysis.get('content_complexity', 'medium')
        tags.append(f'complexity/{complexity}')
        
        # Priority tags
        if content_analysis.get('is_high_priority'):
            tags.append('priority/high')
        
        # Document structure tags
        doc_structure = content_analysis.get('document_structure', {})
        if doc_structure.get('code_density', 0) > 0.1:
            tags.append('content/code-heavy')
        if doc_structure.get('action_items', 0) > 0:
            tags.append('content/actionable')
        if doc_structure.get('heading_count', 0) > 5:
            tags.append('structure/well-organized')
        
        # Cross-reference potential tags
        if content_analysis.get('has_cross_reference_potential'):
            tags.append('cross-ref/potential')
        
        # Actionable insights tags
        insights_count = len(content_analysis.get('actionable_insights', []))
        if insights_count > 0:
            tags.append('insights/actionable')
        if insights_count > 3:
            tags.append('insights/rich')
        
        # Size tags
        size_bytes = file_metadata.get('size_bytes', 0)
        if size_bytes < 1024 * 10:  # < 10KB
            tags.append('size/tiny')
        elif size_bytes < 1024 * 100:  # < 100KB
            tags.append('size/small')
        elif size_bytes < 1024 * 1024:  # < 1MB
            tags.append('size/medium')
        else:
            tags.append('size/large')
        
        return tags
    
    def generate_template_content(self, file_metadata: Dict, chroma_metadata: Dict, 
                                content_analysis: Dict, float_id: str) -> str:
        """
        Generate clean static content for rich Obsidian display.
        """
        
        # Calculate human-readable file size and extract values
        size_bytes = file_metadata.get('size_bytes', 0)
        size_human = self.format_file_size(size_bytes)
        
        # Pre-compute values for clean template generation
        has_ctx_markers = content_analysis.get('has_ctx_markers', False)
        has_highlights = content_analysis.get('has_highlights', False)
        has_float_dispatch = content_analysis.get('has_float_dispatch', False)
        has_conversation_links = content_analysis.get('has_conversation_links', False)
        
        ctx_count = content_analysis.get('ctx_count', 0)
        highlight_count = content_analysis.get('highlight_count', 0)
        error_count = len(content_analysis.get('errors', []))
        
        chunk_ids = chroma_metadata.get('chunk_ids', [])
        
        # Safe content type handling
        content_type_words = content_analysis.get('content_type', 'content').split()
        first_content_type = content_type_words[0] if content_type_words else 'content'
        
        content = f"""# 🗂️ FLOAT Dropzone Index: {file_metadata['filename']}

```js
// FLOAT Display Template - Auto-generated
// Float ID: {float_id}
// Template Version: 1.0
```

## 📋 File Overview

| Field | Value |
|-------|-------|
| **Original File** | `{file_metadata['filename']}` |
| **File Type** | {file_metadata.get('file_type', 'Unknown')} |
| **Size** | {size_human} |
| **Float ID** | `{float_id}` |
| **Processed** | {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} |

## 🧠 Content Analysis

### Summary
{content_analysis.get('summary', 'No summary available')}

### Content Metrics
- **Words**: {content_analysis.get('word_count', 0):,}
- **Lines**: {content_analysis.get('line_count', 0):,}
- **Content Type**: {content_analysis.get('content_type', 'Unknown')}
- **Language**: {content_analysis.get('language', 'Unknown')}

### FLOAT Pattern Detection

| Pattern | Detected | Count |
|---------|----------|-------|
| **ctx::** | {"✅" if has_ctx_markers else "❌"} | {ctx_count} |
| **highlight::** | {"✅" if has_highlights else "❌"} | {highlight_count} |
| **float.dispatch** | {"✅" if has_float_dispatch else "❌"} | N/A |
| **Conversation Links** | {"✅" if has_conversation_links else "❌"} | N/A |

**Signal Density**: {content_analysis.get('signal_density', 0.0):.2%}

## 💾 Chroma Storage

### Collection Details
- **Collection**: `{chroma_metadata.get('collection_name', 'unknown')}`
- **Chunks**: {chroma_metadata.get('chunk_count', 0)} of {chroma_metadata.get('total_chunks', 0)}
- **Embedding Model**: {chroma_metadata.get('embedding_model', 'default')}

### Chunk Index
{f'''
- **Chunk ID**: `{chunk_ids[0]}`
- **Index**: 0
''' if chunk_ids else "*No chunks indexed*"}

## 🔍 Search & Query

### Quick Search
```js
// Search this document in Chroma
collection.query({{
    query_texts: ["your search term"],
    where: {{"float_id": "{float_id}"}},
    n_results: 5
}})
```

### Related Documents
```dataview
LIST
FROM #float/dropzone 
WHERE file.name != this.file.name
AND (contains(file.frontmatter.content.summary, "{first_content_type}"))
SORT file.mtime DESC
LIMIT 5
```

## 📊 Processing Details

### Extraction Results
- **Method**: Automated dropzone processing
- **Success**: {str(content_analysis.get('extraction_successful', False))}
- **Chunking**: {chroma_metadata.get('chunking_strategy', 'content_aware')}
- **Errors**: {error_count}

{f'''### Processing Errors
{chr(10).join([f"- {error}" for error in content_analysis.get('errors', [])])}''' if error_count > 0 else ""}

## 🔗 Actions

### Quick Actions
- [[{file_metadata['filename']}|📄 View Original File]]
- 🔍 **Search in Chroma**: Query Collection
- 📝 **Create Note**: [[{file_metadata['filename'].split('.')[0]} - Analysis]]
- 🏷️ **Add Tags**: Add relevant tags in frontmatter

### Export Options
```js
// Export chunk data
const exportData = {{
    floatId: "{float_id}",
    filename: "{file_metadata['filename']}",
    chunks: {json.dumps(chunk_ids)}
}};

// Copy to clipboard
navigator.clipboard.writeText(JSON.stringify(exportData, null, 2));
```

### Templater Quick Actions

<%*
// Create follow-up note
const followUpTitle = `Follow-up - {file_metadata['filename'].split('.')[0]}`;
const template = `# Follow-up Actions

Based on FLOAT analysis: [[<% tp.file.title %>]]

## Action Items
- [ ] 

## Key Insights
- 

## Related Files
- 
`;

// Only works when Templater is active
if (typeof tp !== 'undefined') {{
    // Button to create follow-up note
    const button = '<button onclick="createFollowUp()">Create Follow-up Note</button>';
}}
-%>

**Create Follow-up**: Use Templater's file creation commands

---

<div style="background: #f0f0f0; padding: 10px; border-radius: 5px; margin-top: 20px;">
<small>
🤖 <strong>Auto-generated by FLOAT Dropzone Daemon v1.0</strong><br>
📅 Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}<br>
🔄 Auto-update: Enabled<br>
📍 Float ID: <code>{float_id}</code>
</small>
</div>
"""
        
        return content
    
    def format_file_size(self, size_bytes: int) -> str:
        """
        Convert bytes to human readable format.
        """
        if size_bytes == 0:
            return "0 B"
        
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        
        return f"{size_bytes:.1f} TB"
    
    def create_float_dis_file(self, file_path: Path, file_metadata: Dict, chroma_metadata: Dict, 
                             content_analysis: Dict, float_id: str) -> Path:
        """
        Create the .float_dis.md file in the same directory as the source file.
        """
        
        # Generate .dis filename
        base_name = file_path.stem
        dis_filename = f"{base_name}.float_dis.md"
        dis_path = file_path.parent / dis_filename
        
        # Generate content
        dis_content = self.generate_float_dis(file_metadata, chroma_metadata, content_analysis, float_id)
        
        # Write file
        with open(dis_path, 'w', encoding='utf-8') as f:
            f.write(dis_content)
        
        return dis_path

if __name__ == "__main__":
    # Test the fixed generator
    print("Fixed FLOAT .dis generator test")
    
    # Sample data for testing
    sample_file_metadata = {
        'filename': 'test.json',
        'extension': '.json',
        'size_bytes': 1024,
        'file_type': 'JSON file',
        'created_at': '2025-06-09T12:00:00',
        'modified_at': '2025-06-09T12:00:00'
    }
    
    sample_chroma_metadata = {
        'collection_name': 'test_collection',
        'chunk_count': 1,
        'chunk_ids': ['test_chunk_1']
    }
    
    sample_content_analysis = {
        'summary': 'Test file',
        'word_count': 100,
        'has_ctx_markers': True,
        'ctx_count': 5
    }
    
    generator = FloatDisGenerator()
    result = generator.generate_float_dis(
        sample_file_metadata, 
        sample_chroma_metadata, 
        sample_content_analysis, 
        'test_float_id'
    )
    
    print("✅ Generated sample .dis content successfully")