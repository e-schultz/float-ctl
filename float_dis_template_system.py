"""
FLOAT .dis Template System
Generates {filename}.float_dis.md files with YAML frontmatter, Chroma details, and Templater.js templates
"""

import json
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

class FloatDisGenerator:
    """
    Generates .float_dis.md files with rich metadata and interactive Obsidian templates.
    """
    
    def __init__(self):
        self.template_version = "1.0"
        
    def generate_float_dis(self, file_metadata: Dict, chroma_metadata: Dict, 
                          content_analysis: Dict, float_id: str) -> str:
        """
        Generate a complete .float_dis.md file with YAML frontmatter and Templater.js template.
        """
        
        # Generate YAML frontmatter
        frontmatter = self.generate_frontmatter(file_metadata, chroma_metadata, content_analysis, float_id)
        
        # Generate Templater.js template content
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
            
            # File information
            'original_file': {
                'name': file_metadata['filename'],
                'path': file_metadata.get('relative_path', ''),
                'extension': file_metadata['extension'],
                'size_bytes': file_metadata['size_bytes'],
                'size_human': self.format_file_size(file_metadata['size_bytes']),
                'mime_type': file_metadata.get('mime_type', 'unknown'),
                'file_type': file_metadata.get('file_type', 'unknown')
            },
            
            # Timestamps
            'timestamps': {
                'file_created': file_metadata['created_at'],
                'file_modified': file_metadata['modified_at'],
                'processed_at': datetime.now().isoformat(),
                'ingestion_date': datetime.now().strftime('%Y-%m-%d')
            },
            
            # Chroma collection details
            'chroma': {
                'collection_name': chroma_metadata.get('collection_name', ''),
                'chunk_count': chroma_metadata.get('chunk_count', 0),
                'total_chunks': chroma_metadata.get('total_chunks', 0),
                'chunk_ids': chroma_metadata.get('chunk_ids', []),
                'embedding_model': chroma_metadata.get('embedding_model', 'default'),
                'storage_path': chroma_metadata.get('storage_path', '')
            },
            
            # Content analysis
            'content': {
                'summary': content_analysis.get('summary', ''),
                'word_count': content_analysis.get('word_count', 0),
                'line_count': content_analysis.get('line_count', 0),
                'content_type': content_analysis.get('content_type', 'unknown'),
                'detected_patterns': content_analysis.get('detected_patterns', []),
                'language': content_analysis.get('language', 'unknown'),
                'encoding': content_analysis.get('encoding', 'utf-8')
            },
            
            # FLOAT pattern detection
            'float_patterns': {
                'has_ctx_markers': content_analysis.get('has_ctx_markers', False),
                'has_highlights': content_analysis.get('has_highlights', False),
                'has_float_dispatch': content_analysis.get('has_float_dispatch', False),
                'has_conversation_links': content_analysis.get('has_conversation_links', False),
                'ctx_count': content_analysis.get('ctx_count', 0),
                'highlight_count': content_analysis.get('highlight_count', 0),
                'signal_density': content_analysis.get('signal_density', 0.0)
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
        if content_analysis.get('has_float_dispatch'):
            tags.append('float/dispatch')
        if content_analysis.get('has_ctx_markers'):
            tags.append('float/ctx')
        if content_analysis.get('has_highlights'):
            tags.append('float/highlights')
        
        # Size-based tags
        size_bytes = file_metadata['size_bytes']
        if size_bytes > 1024*1024:  # > 1MB
            tags.append('size/large')
        elif size_bytes > 1024*100:  # > 100KB
            tags.append('size/medium')
        else:
            tags.append('size/small')
        
        return sorted(list(set(tags)))
    
    def generate_template_content(self, file_metadata: Dict, chroma_metadata: Dict, 
                                content_analysis: Dict, float_id: str) -> str:
        """
        Generate Templater.js template content for rich Obsidian display.
        """
        
        template_content = f'''# 🗂️ FLOAT Dropzone Index: {file_metadata['filename']}

```js
// FLOAT Display Template - Auto-generated
// Float ID: {float_id}
// Template Version: {self.template_version}
```

## 📋 File Overview

<% 
const fileData = {{
    name: "{file_metadata['filename']}",
    type: "{file_metadata['file_type']}",
    size: "{self.format_file_size(file_metadata['size_bytes'])}",
    created: "{file_metadata['created_at']}",
    floatId: "{float_id}"
}};
%>

| Field | Value |
|-------|-------|
| **Original File** | `<%= fileData.name %>` |
| **File Type** | <%= fileData.type %> |
| **Size** | <%= fileData.size %> |
| **Float ID** | `<%= fileData.floatId %>` |
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
<% 
const patterns = {{
    ctxMarkers: {str(content_analysis.get('has_ctx_markers', False)).lower()},
    highlights: {str(content_analysis.get('has_highlights', False)).lower()},
    dispatches: {str(content_analysis.get('has_float_dispatch', False)).lower()},
    conversations: {str(content_analysis.get('has_conversation_links', False)).lower()}
}};
%>

| Pattern | Detected | Count |
|---------|----------|-------|
| **ctx::** | <% patterns.ctxMarkers ? "✅" : "❌" %> | {content_analysis.get('ctx_count', 0)} |
| **highlight::** | <% patterns.highlights ? "✅" : "❌" %> | {content_analysis.get('highlight_count', 0)} |
| **float.dispatch** | <% patterns.dispatches ? "✅" : "❌" %> | N/A |
| **Conversation Links** | <% patterns.conversations ? "✅" : "❌" %> | N/A |

**Signal Density**: {content_analysis.get('signal_density', 0.0):.2%}

## 💾 Chroma Storage

### Collection Details
- **Collection**: `{chroma_metadata.get('collection_name', 'unknown')}`
- **Chunks**: {chroma_metadata.get('chunk_count', 0)} of {chroma_metadata.get('total_chunks', 0)}
- **Embedding Model**: {chroma_metadata.get('embedding_model', 'default')}

### Chunk Index
<% 
const chunks = {json.dumps(chroma_metadata.get('chunk_ids', []))};
%>

<% if (chunks.length > 0) {{ %>
```dataview
TABLE WITHOUT ID
  chunk as "Chunk ID",
  index as "Index"
FROM ""
WHERE file.name = this.file.name
FLATTEN [{', '.join([f'"{{id: "{chunk}", index: {i}}}"' for i, chunk in enumerate(chroma_metadata.get('chunk_ids', []))])}] as chunkData
FLATTEN chunkData.id as chunk, chunkData.index as index
```
<% }} else {{ %>
*No chunks indexed*
<% }} %>

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
<% 
// Templater.js code to find related documents
const relatedQuery = `float_id:"{float_id}" OR filename:"{file_metadata['filename']}"`;
%>

```dataview
LIST
FROM #float/dropzone 
WHERE file.name != this.file.name
AND (contains(file.frontmatter.content.summary, "{content_analysis.get('content_type', '').split()[0]}"))
SORT file.mtime DESC
LIMIT 5
```

## 📊 Processing Details

### Extraction Results
- **Method**: Automated dropzone processing
- **Success**: {str(content_analysis.get('extraction_successful', False))}
- **Chunking**: {chroma_metadata.get('chunking_strategy', 'content_aware')}
- **Errors**: {len(content_analysis.get('errors', []))}

<% if ({len(content_analysis.get('errors', []))}) > 0) {{ %>
### Processing Errors
{chr(10).join([f"- {error}" for error in content_analysis.get('errors', [])])}
<% }} %>

## 🔗 Actions

### Quick Actions
- [[{file_metadata['filename']}|📄 View Original File]]
- 🔍 **Search in Chroma**: [Query Collection](obsidian://advanced-uri?vault={{tp.file.folder}}&commandid=editor%3Afocus)
- 📝 **Create Note**: [[{file_metadata['filename'].replace(file_metadata['extension'], '')} - Analysis]]
- 🏷️ **Add Tags**: Add relevant tags in frontmatter

### Export Options
```js
// Export chunk data
const exportData = {{
    floatId: "{float_id}",
    filename: "{file_metadata['filename']}",
    chunks: {json.dumps(chroma_metadata.get('chunk_ids', []))},
    metadata: <% JSON.stringify(tp.frontmatter, null, 2) %>
}};

// Copy to clipboard
navigator.clipboard.writeText(JSON.stringify(exportData, null, 2));
```

---

<div style="background: #f0f0f0; padding: 10px; border-radius: 5px; margin-top: 20px;">
<small>
🤖 <strong>Auto-generated by FLOAT Dropzone Daemon v{self.template_version}</strong><br>
📅 Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}<br>
🔄 Auto-update: Enabled<br>
📍 Float ID: <code>{float_id}</code>
</small>
</div>'''
        
        return template_content
    
    def format_file_size(self, size_bytes: int) -> str:
        """Format file size in human-readable format."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.1f} TB"
    
    def create_float_dis_file(self, file_path: Path, file_metadata: Dict, 
                            chroma_metadata: Dict, content_analysis: Dict, 
                            float_id: str) -> Path:
        """
        Create the actual .float_dis.md file.
        """
        
        # Generate the .dis content
        dis_content = self.generate_float_dis(file_metadata, chroma_metadata, content_analysis, float_id)
        
        # Create .float_dis.md filename
        original_stem = file_path.stem
        dis_path = file_path.parent / f"{original_stem}.float_dis.md"
        
        # Write the file
        with open(dis_path, 'w', encoding='utf-8') as f:
            f.write(dis_content)
        
        return dis_path

# Integration with the existing daemon
class EnhancedFloatDropzoneHandler:
    """
    Enhanced dropzone handler that generates .float_dis.md files instead of .diz files.
    """
    
    def __init__(self, *args, **kwargs):
        # Initialize parent class
        super().__init__(*args, **kwargs)
        self.dis_generator = FloatDisGenerator()
    
    def enhanced_content_analysis(self, content: str, file_metadata: Dict) -> Dict:
        """
        Enhanced content analysis for .dis file generation.
        """
        
        lines = content.split('\\n')
        words = content.split()
        
        # Basic analysis
        analysis = {{
            'word_count': len(words),
            'line_count': len(lines),
            'char_count': len(content),
            'extraction_successful': True,
            'errors': [],
            'encoding': 'utf-8',
            'language': 'unknown'
        }}
        
        # Content type detection
        content_lower = content.lower()
        if 'conversation' in content_lower or 'chat' in content_lower:
            analysis['content_type'] = "Conversation/Chat export"
        elif content.strip().startswith('{') or content.strip().startswith('['):
            analysis['content_type'] = "JSON data structure"
        elif 'claude.ai' in content or 'chatgpt.com' in content:
            analysis['content_type'] = "AI conversation export"
        elif len([line for line in lines if line.startswith('#')]) > 3:
            analysis['content_type'] = "Markdown document"
        else:
            analysis['content_type'] = file_metadata.get('file_type', 'Unknown content')
        
        # FLOAT pattern detection
        import re
        
        ctx_matches = re.findall(r'ctx::', content)
        highlight_matches = re.findall(r'highlight::', content)
        dispatch_matches = re.findall(r'float\\.dispatch', content)
        conversation_links = re.findall(r'https://(?:claude\\.ai|chatgpt\\.com)', content)
        
        analysis.update({{
            'has_ctx_markers': len(ctx_matches) > 0,
            'has_highlights': len(highlight_matches) > 0,
            'has_float_dispatch': len(dispatch_matches) > 0,
            'has_conversation_links': len(conversation_links) > 0,
            'ctx_count': len(ctx_matches),
            'highlight_count': len(highlight_matches),
            'signal_density': (len(ctx_matches) + len(highlight_matches) + len(dispatch_matches)) / max(len(words), 1)
        }})
        
        # Generate summary
        topic = "No clear topic identified"
        for line in lines[:10]:
            line = line.strip()
            if len(line) > 10 and not line.startswith('#') and not line.startswith('-'):
                topic = line[:100] + "..." if len(line) > 100 else line
                break
        
        analysis['summary'] = f"{{analysis['content_type']}}. {{topic}}. {{len(lines)}} lines, {{len(words)}} words."
        
        # Add pattern descriptions
        pattern_notes = []
        if analysis['has_float_dispatch']:
            pattern_notes.append("Contains FLOAT dispatches")
        if analysis['has_ctx_markers']:
            pattern_notes.append("Contains context markers")
        if analysis['has_highlights']:
            pattern_notes.append("Contains highlights")
        if analysis['has_conversation_links']:
            pattern_notes.append("Contains conversation links")
        
        if pattern_notes:
            analysis['summary'] += " " + ". ".join(pattern_notes) + "."
        
        analysis['detected_patterns'] = pattern_notes
        
        return analysis
    
    def process_file_enhanced(self, file_path: Path):
        """
        Enhanced file processing that generates .float_dis.md files.
        """
        
        print(f"🔄 Processing: {{file_path.name}} (Enhanced .dis mode)")
        
        # Step 1: Basic file processing (from parent class)
        file_metadata = self.detect_file_type(file_path)
        content = self.extract_content(file_path, file_metadata)
        
        if not content:
            content = f"File: {{file_path.name}}\\nType: {{file_metadata['file_type']}}\\nSize: {{self.format_file_size(file_metadata['size_bytes'])}}"
            file_metadata['extraction_failed'] = True
        
        # Step 2: Enhanced content analysis
        content_analysis = self.enhanced_content_analysis(content, file_metadata)
        
        # Step 3: Generate float ID and process chunks
        content_hash = hashlib.md5(content.encode()).hexdigest()[:8]
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        float_id = f"float_{{timestamp}}_{{content_hash}}"
        
        chunks = self.chunk_content(content)
        
        # Step 4: Store in Chroma and collect metadata
        chunk_ids = []
        chroma_metadata = {{
            'collection_name': self.collection_name,
            'chunk_count': len(chunks),
            'total_chunks': len(chunks),
            'chunking_strategy': 'content_aware',
            'embedding_model': 'default',
            'storage_path': self.chroma_data_path
        }}
        
        try:
            for i, chunk in enumerate(chunks):
                chunk_id = f"{{float_id}}_chunk_{{i}}"
                chunk_ids.append(chunk_id)
                
                chunk_metadata = {{
                    'float_id': float_id,
                    'original_filename': file_metadata['filename'],
                    'chunk_index': i,
                    'total_chunks': len(chunks),
                    # ... other metadata
                }}
                
                self.collection.add(
                    documents=[chunk],
                    metadatas=[chunk_metadata],
                    ids=[chunk_id]
                )
            
            chroma_metadata['chunk_ids'] = chunk_ids
            print(f"   ✅ Stored {{len(chunks)}} chunks in Chroma")
            
        except Exception as e:
            print(f"   ❌ Chroma storage failed: {{e}}")
            content_analysis['errors'].append(f"Chroma storage failed: {{e}}")
        
        # Step 5: Generate .float_dis.md file
        try:
            file_metadata['relative_path'] = str(file_path.relative_to(self.dropzone_path))
            dis_path = self.dis_generator.create_float_dis_file(
                file_path, file_metadata, chroma_metadata, content_analysis, float_id
            )
            print(f"   ✅ Generated: {{dis_path.name}}")
            
        except Exception as e:
            print(f"   ❌ .dis file generation failed: {{e}}")
            content_analysis['errors'].append(f"Dis file generation failed: {{e}}")
        
        print(f"✅ Enhanced processing complete: {{file_path.name}} → {{float_id}}")

# Example usage and testing
if __name__ == "__main__":
    # Test .dis file generation
    generator = FloatDisGenerator()
    
    # Sample data
    file_metadata = {{
        'filename': 'test_export.json',
        'extension': '.json',
        'file_type': 'JSON data',
        'mime_type': 'application/json',
        'size_bytes': 89231,
        'created_at': '2025-06-08T14:30:22',
        'modified_at': '2025-06-08T14:30:22'
    }}
    
    chroma_metadata = {{
        'collection_name': 'float_dropzone_ingestion',
        'chunk_count': 3,
        'total_chunks': 3,
        'chunk_ids': ['float_20250608_143022_a7b3c89f_chunk_0', 'float_20250608_143022_a7b3c89f_chunk_1', 'float_20250608_143022_a7b3c89f_chunk_2'],
        'embedding_model': 'default'
    }}
    
    content_analysis = {{
        'summary': 'AI conversation export about nushell data processing. Contains multiple ctx:: markers and highlights.',
        'word_count': 2341,
        'line_count': 147,
        'content_type': 'AI conversation export',
        'has_ctx_markers': True,
        'has_highlights': True,
        'has_float_dispatch': True,
        'ctx_count': 5,
        'highlight_count': 3,
        'signal_density': 0.034
    }}
    
    float_id = 'float_20250608_143022_a7b3c89f'
    
    # Generate .dis content
    dis_content = generator.generate_float_dis(file_metadata, chroma_metadata, content_analysis, float_id)
    
    print("Generated .float_dis.md content:")
    print("=" * 80)
    print(dis_content)
