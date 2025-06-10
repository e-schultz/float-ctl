# FLOAT Complete Knowledge Ecosystem

A comprehensive file processing and knowledge management system that automates the ingestion, analysis, and organization of content into your Obsidian vault and ChromaDB vector database.

## Overview

FLOAT (Feed-Log-Offload-Archive-Trunk) is an intelligent knowledge management system that:

- **Monitors** a dropzone folder for new files
- **Processes** various file types (text, markdown, JSON, PDF, Word docs)
- **Analyzes** content using AI-powered summarization (Ollama)
- **Stores** content in ChromaDB with intelligent routing to tripartite collections
- **Generates** rich `.dis` files for Obsidian with cross-references and metadata
- **Maintains** daily context summaries and conversation analysis
- **Provides** comprehensive monitoring, logging, and error recovery

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Dropzone      │───▶│   FLOAT Daemon   │───▶│  Obsidian Vault │
│   (Monitor)     │    │   (Process)      │    │  (.dis files)   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │    ChromaDB      │
                       │  (Vector Store)  │
                       └──────────────────┘
```

### Key Components

1. **Streamlined Daemon** (`streamlined_float_daemon.py`) - Main file watcher and orchestrator
2. **Enhanced Integration** (`enhanced_integration.py`) - Deep ecosystem integration with sophisticated analysis
3. **Enhanced Pattern Detector** (`enhanced_pattern_detector.py`) - Comprehensive FLOAT signal analysis (40+ pattern types)
4. **Configuration System** (`config.py`) - Centralized configuration management
5. **Error Recovery** (`error_recovery.py`) - Robust error handling and retry logic
6. **Performance Monitoring** (`performance_monitor.py`) - Real-time performance tracking
7. **Health Monitoring** (`health_monitor.py`) - System health checks
8. **Cross-Reference System** (`cross_reference_system.py`) - Bidirectional vault linking
9. **Conversation Analysis** (`conversation_dis_enhanced.py`) - Advanced conversation processing
10. **Logging System** (`logging_config.py`) - Structured logging with rotation

## Installation

### Prerequisites

1. **Python 3.8+** with the following packages:
   ```bash
   pip install watchdog chromadb pathlib python-magic PyPDF2 mammoth
   ```

2. **libmagic** (for enhanced file type detection):
   ```bash
   # macOS
   brew install libmagic
   
   # Ubuntu/Debian
   sudo apt-get install libmagic1
   
   # CentOS/RHEL
   sudo yum install file-devel
   ```

3. **Ollama** (optional but recommended):
   ```bash
   # Install Ollama
   curl -fsSL https://ollama.ai/install.sh | sh
   
   # Pull a model
   ollama pull llama3.1:8b
   ```

4. **Obsidian** with the following plugins:
   - Templater (for .dis file templates)
   - Dataview (for dynamic queries)

### Setup

1. **Clone or download** the FLOAT system files to a directory (e.g., `/Users/evan/github/float-log/`)

2. **Create required directories**:
   ```bash
   mkdir -p ~/vault/FLOAT.conversations
   mkdir -p ~/vault/FLOAT.logs
   mkdir -p ~/vault/FLOAT.references
   mkdir -p ~/float-dropzone
   mkdir -p ~/github/chroma-data
   ```

3. **Create configuration file**:
   ```bash
   python streamlined_float_daemon.py --create-config ~/float-config.json
   ```

4. **Edit configuration** to match your paths:
   ```json
   {
     "vault_path": "~/vault",
     "chroma_data_path": "~/github/chroma-data",
     "dropzone_path": "~/float-dropzone",
     "enable_ollama": true,
     "ollama_model": "llama3.1:8b",
     "max_file_size_mb": 50,
     "auto_update_daily_context": true
   }
   ```

## Usage

### Basic Usage

Start the daemon to monitor your dropzone folder:

```bash
python streamlined_float_daemon.py ~/float-dropzone
```

### Advanced Usage

Using configuration file:
```bash
python streamlined_float_daemon.py --config ~/float-config.json
```

Process existing files before starting:
```bash
python streamlined_float_daemon.py ~/float-dropzone --process-existing
```

With custom settings:
```bash
python streamlined_float_daemon.py ~/float-dropzone \
  --vault-path ~/my-vault \
  --chroma-path ~/my-chroma \
  --enable-ollama \
  --max-file-size 100
```

### File Processing

1. **Drop files** into your dropzone folder
2. **FLOAT automatically**:
   - Extracts content and metadata
   - Generates AI summaries (if Ollama enabled)
   - Routes content to appropriate ChromaDB collections
   - Creates rich `.dis` files in your Obsidian vault
   - Updates daily context summaries
   - Generates cross-references

### Supported File Types

- **Text files**: `.txt`, `.md`, `.log`
- **Documents**: `.pdf`, `.docx`, `.doc`
- **Data**: `.json`, `.csv`, `.html`
- **Code**: `.py`, `.js`, `.yaml`, `.yml`

### FLOAT Patterns

Enhance your content with FLOAT methodology markers:

**Core Patterns:**
- `ctx::temporal context` - Temporal/situational notes
- `highlight::important insight` - Key insights and highlights
- `signal::key information` - Important signals and markers
- `float.dispatch(topic)` - Topic branching and dispatch objects

**Extended Patterns:**
- `expandOn::topic` - Areas for further exploration
- `relatesTo::concept` - Cross-references to related ideas
- `rememberWhen::context` - Temporal memory anchors
- `storyTime::narrative` - Narrative and experiential content

**Persona Annotations:**
- `[sysop::admin comment]` - System operator perspectives
- `[any::general note]` - General annotations
- Custom persona markers for context-specific insights

**Platform Integration:**
- Automatic detection of lovable.dev, v0.dev, magicpatterns.com references
- GitHub repository and issue linking
- Build tool and deployment platform recognition

### Example Workflow

1. **Export a conversation** from Claude.ai or ChatGPT
2. **Save to dropzone** as `my-conversation.txt`
3. **FLOAT processes**:
   - Detects it's a conversation
   - Extracts participants, topics, code blocks
   - Generates comprehensive summary
   - Creates conversation .dis file
   - Routes to tripartite collections
   - Updates cross-references

4. **Find in Obsidian**:
   - `FLOAT.conversations/20241208_143022_claude_ai_abc12345.conversation.float_dis.md`
   - Rich metadata, analysis, and Templater actions
   - Dataview queries for related content

## Configuration

### Configuration File

Create with: `python streamlined_float_daemon.py --create-config config.json`

#### Core Settings
```json
{
  "vault_path": "~/vault",
  "chroma_data_path": "~/github/chroma-data", 
  "dropzone_path": "~/float-dropzone",
  "conversation_dis_path": "~/vault/FLOAT.conversations"
}
```

#### Processing Settings
```json
{
  "max_file_size_mb": 50,
  "chunk_size": 2000,
  "chunk_overlap": 200,
  "retry_attempts": 3,
  "process_hidden_files": false,
  "delete_after_processing": false
}
```

#### AI and Enhancement
```json
{
  "enable_ollama": true,
  "ollama_url": "http://localhost:11434",
  "ollama_model": "llama3.1:8b",
  "enable_enhanced_integration": true,
  "enable_tripartite_routing": true
}
```

#### Monitoring and Logging
```json
{
  "log_level": "INFO",
  "log_dir": null,
  "log_file": null,
  "enable_performance_monitoring": true,
  "enable_health_checks": true,
  "health_check_interval": 60
}
```

### Environment Variables

Override config with environment variables:
```bash
export FLOAT_VAULT_PATH=~/my-vault
export FLOAT_CHROMA_PATH=~/my-chroma
export FLOAT_DROPZONE_PATH=~/my-dropzone
export FLOAT_LOG_DIR=~/my-logs
export OLLAMA_URL=http://localhost:11434
export FLOAT_ENABLE_OLLAMA=true
```

### Tripartite Collections

Content is intelligently routed to specialized collections using enhanced pattern analysis:

- **Concept Collection** (`float_tripartite_v2_concept`): Definitions, theories, principles, abstract ideas
  - Optimized for precision (600/1200 char chunks)
  - High-confidence classification for conceptual content
  
- **Framework Collection** (`float_tripartite_v2_framework`): Processes, methods, systems, workflows
  - Optimized for structure (900/1800 char chunks)
  - Platform integration and build tool references
  
- **Metaphor Collection** (`float_tripartite_v2_metaphor`): Analogies, experiences, intuitions, narratives
  - Optimized for resonance (800/1600 char chunks)
  - Persona annotations and experiential content

**Enhanced Routing Features:**
- Automatic domain classification with confidence scoring
- Multi-domain routing for complex content
- High-signal content distributed across all domains
- Content complexity assessment for optimal chunking

## Monitoring and Health

### Performance Dashboard

Check real-time performance:
```bash
cat ~/float-dropzone/.logs/performance_metrics.json
```

### Health Status

Monitor system health:
```bash
cat ~/float-dropzone/.status/health_status.json
```

### Logs

View detailed logs:
```bash
tail -f ~/float-dropzone/.logs/float_daemon.log
```

### Error Recovery

FLOAT includes comprehensive error recovery:

- **Automatic retries** with exponential backoff
- **Quarantine system** for problematic files
- **Memory-safe processing** for large files
- **Graceful degradation** when components fail

## Obsidian Integration

### .dis File Structure

Each processed file generates a rich `.float_dis.md` file:

```markdown
---
float_id: float_20241208_143022_abc12345
conversation_id: claude_abc123
platform: claude_ai
topics: ["AI", "Programming", "FLOAT"]
signal_count: 5
---

# 💬 Educational: claude_abc123

## Conversation Overview
- **Platform**: Claude AI
- **Type**: Educational
- **Technical Depth**: High
- **Turn Count**: 15

## Speaker Analysis
### Human
- **Turns**: 8
- **Average Length**: 150 characters

### Claude
- **Turns**: 7
- **Average Length**: 800 characters

## FLOAT Signal Analysis
### By Type
- **ctx**: 3 signals
- **highlight**: 2 signals

## Cross-References
[Dynamic Dataview queries for related content]

## Templater Actions
[Quick actions for code extraction and follow-ups]
```

### Templater Integration

.dis files include ready-to-use Templater actions:

- **Extract Code Blocks** - Create separate notes with all code
- **Create Follow-up Note** - Generate action items and next steps
- **Link Related Conversations** - Connect to similar discussions

### Dataview Queries

Find related content automatically:

```dataview
LIST FROM "FLOAT.conversations"
WHERE contains(file.frontmatter.topics, "AI")
SORT file.ctime DESC
LIMIT 5
```

## Testing and Validation

### Test Individual Components

```bash
# Test Ollama summarizer
python ollama_enhanced_float_summarizer.py

# Test .dis file generation  
python float_dis_template_system.py

# Test enhanced context
python enhanced_comprehensive_context_ollama.py
```

### Validate Configuration

```bash
python -c "from config import FloatConfig; c = FloatConfig(); print(c.validate())"
```

### Process Test File

```bash
echo "ctx::test content highlight::important" > ~/float-dropzone/test.txt
# Watch logs for processing
```

## Troubleshooting

### Common Issues

**1. Ollama Connection Failed**
```bash
# Check Ollama status
ollama list
# Restart if needed
ollama serve
```

**2. ChromaDB Errors**
```bash
# Check permissions
ls -la ~/github/chroma-data
# Recreate if corrupted
rm -rf ~/github/chroma-data && mkdir -p ~/github/chroma-data
```

**3. Vault Path Issues**
```bash
# Verify paths exist
ls -la ~/vault/FLOAT.conversations
# Create if missing
mkdir -p ~/vault/{FLOAT.conversations,FLOAT.logs,FLOAT.references}
```

**4. Permission Errors**
```bash
# Fix dropzone permissions
chmod 755 ~/float-dropzone
# Check file ownership
ls -la ~/float-dropzone
```

**5. Large File Processing**
- Files over 50MB are automatically previewed
- Adjust `max_file_size_mb` in config for larger files
- Check memory usage with performance monitor

### Debug Mode

Enable verbose logging:
```json
{
  "log_level": "DEBUG"
}
```

View detailed processing:
```bash
tail -f ~/float-dropzone/.logs/float_daemon.log | grep DEBUG
```

### Recovery Options

**Reset ChromaDB collections**:
```bash
python -c "
from enhanced_comprehensive_context_ollama import EnhancedComprehensiveDailyContext
ctx = EnhancedComprehensiveDailyContext()
ctx.client.reset()
"
```

**Clear quarantine folder**:
```bash
rm -rf ~/float-dropzone/.quarantine/*
```

**Rebuild conversation index**:
```bash
rm ~/vault/FLOAT.conversations/_conversation_index.json
# Will rebuild on next conversation processing
```

## Advanced Features

### Enhanced Integration Mode

When enabled, provides:
- **Deep conversation analysis** with speaker statistics
- **Tripartite collection routing** based on content type
- **Advanced cross-referencing** with vault search
- **Rich .dis file generation** with Templater actions

### Cross-Reference System

Automatically generates:
- **Vault references** to existing notes
- **Topic connections** via hashtags and concepts
- **Temporal links** to daily notes
- **Conversation links** between related discussions
- **Bidirectional backlinks** in referenced files

### Performance Optimization

- **Parallel processing** of components
- **Intelligent chunking** based on content type
- **Memory-safe extraction** for large files
- **Cached summaries** to avoid reprocessing
- **Health monitoring** with automatic recovery

## API and Extensibility

### Custom Processors

Extend with custom file processors:
```python
class CustomProcessor:
    def process_file(self, file_path, content, metadata):
        # Custom processing logic
        return enhanced_analysis
```

### Plugin Architecture

Add plugins to the daemon:
```python
daemon.register_plugin(CustomProcessor())
```

### Webhook Integration

Configure webhooks for external notifications:
```json
{
  "webhooks": {
    "on_file_processed": "https://api.example.com/notify",
    "on_error": "https://api.example.com/alert"
  }
}
```

## Support and Development

### Version Information
- **Current Version**: 1.0
- **Compatibility**: Python 3.8+, Obsidian 1.0+
- **Dependencies**: See requirements.txt

### Contributing

1. Fork the repository
2. Create feature branch
3. Add tests for new functionality
4. Submit pull request

### License

FLOAT Complete Knowledge Ecosystem is released under MIT License.

---

*For additional support, check the logs at `~/float-dropzone/.logs/` or review the health status at `~/float-dropzone/.status/`*