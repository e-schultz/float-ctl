# FLOAT Complete Knowledge Ecosystem

A comprehensive file processing and knowledge management system that automates the ingestion, analysis, and organization of content into your Obsidian vault and ChromaDB vector database.

## Overview

FLOAT (Feed-Log-Offload-Archive-Trunk) is an intelligent knowledge management system that:

- **Monitors** a dropzone folder for new files with real-time processing
- **Deduplicates** content using advanced content-based hashing to prevent storage waste
- **Processes** various file types (text, markdown, JSON, PDF, Word docs) with content-aware analysis
- **Analyzes** content using local AI-powered summarization (Ollama) with specialized prompts
- **Classifies** content intelligently (daily logs vs conversations vs general documents)
- **Routes** content smartly to ChromaDB with precision tripartite collection routing
- **Generates** rich `.dis` files for Obsidian with enhanced metadata and cross-references
- **Maintains** daily context summaries and conversation analysis with temporal indexing
- **Provides** comprehensive monitoring, logging, error recovery, and health checks

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

#### Core Processing
1. **Streamlined Daemon** (`streamlined_float_daemon.py`) - Main file watcher and orchestrator
2. **Enhanced Integration** (`enhanced_integration.py`) - Deep ecosystem integration with sophisticated content classification
3. **Enhanced Pattern Detector** (`enhanced_pattern_detector.py`) - Comprehensive FLOAT signal analysis (40+ pattern types)
4. **Configuration System** (`config.py`) - Centralized configuration with environment variable support

#### AI-Powered Analysis
5. **Ollama Summarizer** (`ollama_enhanced_float_summarizer.py`) - Local AI summarization with hierarchical processing
6. **Enhanced Daily Context** (`enhanced_comprehensive_context_ollama.py`) - AI-powered daily log analysis
7. **Conversation Analysis** (`conversation_dis_enhanced.py`) - Advanced conversation processing with platform detection

#### Storage and Routing
8. **Tripartite Collection System** - Intelligent routing to concept/framework/metaphor domains
9. **Cross-Reference System** (`cross_reference_system.py`) - Bidirectional vault linking
10. **Temporal Query System** - Date-based conversation indexing and retrieval

#### Monitoring and Recovery
11. **Error Recovery** (`error_recovery.py`) - Robust error handling with quarantine system
12. **Performance Monitoring** (`performance_monitor.py`) - Real-time metrics and throughput tracking
13. **Health Monitoring** (`health_monitor.py`) - Component health checks and status reporting
14. **Logging System** (`logging_config.py`) - Structured logging with performance integration

## Installation

### Prerequisites

1. **Python 3.8+** with required packages:
   ```bash
   # Create and activate virtual environment (recommended)
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install all required dependencies
   pip install -r requirements.txt
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

Using configuration file (recommended):
```bash
python streamlined_float_daemon.py --config ~/float-config.json
```

Process existing files before starting monitoring:
```bash
python streamlined_float_daemon.py ~/float-dropzone --process-existing
```

With Ollama AI-powered summarization enabled:
```bash
python streamlined_float_daemon.py ~/float-dropzone --enable-ollama
```

Full configuration example:
```bash
python streamlined_float_daemon.py ~/float-dropzone \
  --vault-path ~/my-vault \
  --chroma-path ~/my-chroma \
  --enable-ollama \
  --process-existing \
  --max-file-size 100
```

### Content-Aware Processing

1. **Drop files** into your dropzone folder
2. **FLOAT intelligently processes** each file:
   - **Content Classification**: Detects daily logs, conversations, or general documents
   - **Metadata Extraction**: Comprehensive file analysis and frontmatter parsing
   - **AI-Powered Summarization**: Local Ollama models generate intelligent summaries
   - **Pattern Detection**: Identifies 40+ FLOAT methodology patterns
   - **Tripartite Routing**: Routes content to concept/framework/metaphor collections
   - **Smart Deduplication**: Prevents duplicate content storage using content-based hashing
   - **Cross-Reference Generation**: Creates bidirectional links across vault content
   - **Enhanced .dis Files**: Generates specialized documentation for different content types
   - **Daily Context Updates**: Maintains temporal context and conversation history

#### Processing Specialization by Content Type

**Daily Logs** (detected via frontmatter patterns):
- Extracts actionable items, mood indicators, and productivity signals
- Generates AI-powered daily insights and reflection points
- Creates specialized daily log .dis files with temporal navigation
- Routes to all tripartite collections for comprehensive indexing

**Conversations** (Claude.ai, ChatGPT exports):
- Platform-specific metadata extraction and conversation flow analysis
- Speaker statistics and dialogue structure analysis
- Topic extraction and technical depth assessment
- Enhanced conversation .dis files with Dataview integration

**General Documents**:
- Content structure analysis and FLOAT pattern recognition
- Intelligent chunking based on document type and complexity
- Basic .dis files with comprehensive metadata and Ollama summaries

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
- `[sysop::]` - System operator perspectives and technical oversight
- `[karen::]` - Editorial conscience and after-hours creative director (internal support team)
- `[qtb::]` - Queer Techno Bard perspectives and creative expressions
- `[lf1m::]` - Little Fucker needs a minute (processing time and reflection)
- `[any::]` - General annotations and broad contextual notes
- Custom persona markers for neurodivergent symbolic narrative-cognitive tracking

**Platform Integration:**
- Automatic detection of lovable.dev, v0.dev, magicpatterns.com references
- GitHub repository and issue linking
- Build tool and deployment platform recognition

### Example Workflows

#### Daily Log Processing
1. **Create daily log** with YAML frontmatter:
   ```markdown
   ---
   created: 2025-06-12T09:00:00
   type: log
   mood: "focused"
   tags: [daily]
   ---
   
   ## Brain Boot
   ctx:: Starting the day with clear priorities
   
   ## Key Tasks
   - Review FLOAT system improvements
   - highlight:: Configuration bug fix successful
   ```

2. **FLOAT processes**:
   - Detects as daily log via frontmatter patterns
   - Generates AI-powered insights and mood analysis
   - Extracts actionable items and productivity signals
   - Creates enhanced daily log .dis file in `FLOAT.conversations/`
   - Routes to all tripartite collections

3. **Result**: Rich daily log analysis with Ollama-generated summaries

#### Conversation Processing
1. **Export conversation** from Claude.ai or ChatGPT
2. **Save to dropzone** as JSON export or markdown
3. **FLOAT processes**:
   - Detects conversation platform and extracts metadata
   - Analyzes dialogue structure and participant statistics
   - Generates comprehensive AI summary with technical depth assessment
   - Creates conversation .dis file with cross-references
   - Routes to appropriate tripartite collections based on content

4. **Find in Obsidian**:
   - `FLOAT.conversations/20250612_143022_claude_ai_abc12345.conversation.float_dis.md`
   - Rich metadata, AI analysis, and Dataview navigation queries
   - Templater actions for code extraction and follow-ups

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

#### AI and Enhanced Processing
```json
{
  "enable_ollama": true,
  "ollama_url": "http://localhost:11434",
  "ollama_model": "llama3.1:8b",
  "enable_enhanced_integration": true,
  "enable_tripartite_routing": true,
  "auto_update_daily_context": true,
  "special_pattern_collections": {
    "dispatch": "float_dispatch_bay",
    "rfc": "float_rfc", 
    "echo_copy": "float_echoCopy"
  },
  "tripartite_collections": {
    "concept": "float_tripartite_v2_concept",
    "framework": "float_tripartite_v2_framework",
    "metaphor": "float_tripartite_v2_metaphor"
  },
  "enable_temporal_queries": true
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

### Smart Tripartite Collections

Content is intelligently routed to specialized collections using enhanced pattern analysis with strict precision thresholds to prevent "dumb spray" routing:

- **Concept Collection** (`float_tripartite_v2_concept`): Definitions, theories, principles, abstract ideas
  - Optimized for precision (600/1200 char chunks)
  - High-confidence classification (>0.6 threshold) for conceptual content
  
- **Framework Collection** (`float_tripartite_v2_framework`): Processes, methods, systems, workflows
  - Optimized for structure (900/1800 char chunks)
  - Platform integration and build tool references (>3 platform refs required)
  
- **Metaphor Collection** (`float_tripartite_v2_metaphor`): Analogies, experiences, intuitions, narratives
  - Optimized for resonance (800/1600 char chunks)
  - Persona annotations and experiential content

**Smart Routing Features:**
- **Content-based deduplication** prevents duplicate storage across collections
- **Precision thresholds** (0.6 for secondary domains) reduce noise
- **Signal density analysis** (>5% + 10+ signals) for ultra-high value content
- **Selective conversation routing** based on actual multi-domain confidence

### Special Pattern Collections

Content with specific FLOAT patterns gets additional routing to dedicated collections:

- **Dispatch Bay** (`float_dispatch_bay`): Content with `float.dispatch()` patterns
  - Topic branching and dispatch objects
  - Automatic routing alongside tripartite collections
  
- **RFC Collection** (`float_rfc`): Content with `float.rfc` patterns  
  - FLOAT Request for Comments and specification documents
  - Structured discussion and protocol definitions
  
- **Echo Copy Collection** (`float_echoCopy`): Content with `echoCopy::` patterns
  - Echo and repetition patterns for reinforcement learning
  - Cognitive anchoring and memory consolidation content

### Temporal Query Features

Enhanced date-based conversation queries for efficient temporal searches:

- **Automatic date parsing** from filenames, content, and conversation metadata
- **Normalized temporal metadata** (YYYY-MM-DD format, day of week, month/year)
- **Date-specific queries** - "What conversations did we have on June 1st?"
- **Date range queries** - "Show me conversations from last week"
- **Cross-collection temporal search** across all tripartite and special collections

**Usage Examples:**
```python
# Query conversations by specific date
results = integration.query_conversations_by_date('2025-06-01')

# Query conversations by date range  
results = integration.get_conversations_for_date_range('2025-06-01', '2025-06-07')
```

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

### Comprehensive Test Suite

FLOAT includes a robust testing framework with 34 comprehensive tests covering all major components:

```bash
# Run all tests
python -m pytest

# Run specific test categories
python run_tests.py --config          # Configuration tests
python run_tests.py --patterns        # Pattern detection tests  
python run_tests.py --daemon          # Daemon functionality tests

# Run with coverage reporting
python run_tests.py --coverage

# Run tests in parallel for faster execution
python run_tests.py --parallel

# Install test dependencies
python run_tests.py --install-deps
```

#### Test Categories

**Configuration Tests** (15 tests):
- Default configuration loading and validation
- Environment variable overrides and boolean handling
- Path expansion and conversation .dis path generation
- Config file creation, loading, and error handling
- Edge cases including empty environment variables

**Pattern Detection Tests** (16 tests):
- Core FLOAT patterns (ctx::, highlight::, signal::, float.dispatch())
- Persona annotations ([sysop::], [karen::], [qtb::], etc.)
- Extended patterns (expandOn::, relatesTo::, rememberWhen::)
- Signal density calculation and complexity analysis
- Code block detection and platform integration patterns
- Daily log and conversation detection
- Edge cases including malformed patterns and special characters

**Daemon Tests** (3 tests):
- Daemon initialization with proper mocking
- Configuration loading and validation
- Import verification and basic functionality

#### Test Framework Features

- **Comprehensive Fixtures**: Mock ChromaDB client, Ollama client, temporary directories
- **Realistic Test Data**: Sample content with actual FLOAT patterns
- **Robust Mocking**: All external dependencies properly mocked
- **Edge Case Coverage**: Empty content, None values, malformed input  
- **Test Categories**: Unit, integration, config, daemon, patterns markers
- **Performance Testing**: Parallel execution and timeout handling

### Test Individual Components

```bash
# Test Ollama summarizer
python ollama_enhanced_float_summarizer.py

# Test .dis file generation  
python float_dis_template_system.py

# Test enhanced context
python enhanced_comprehensive_context_ollama.py

# Test pattern detection
python enhanced_pattern_detector.py
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

### Development Testing

```bash
# Run tests with verbose output
python -m pytest -v

# Run specific test file
python -m pytest tests/test_config.py -v

# Run tests matching pattern
python -m pytest -k "test_pattern_detection" -v

# Run tests with coverage and HTML report
python -m pytest --cov=. --cov-report=html

# Run only fast tests (skip slow integration tests)
python run_tests.py --fast
```

## Troubleshooting

### Common Issues

**1. "AI Summary shows 'None'" - Ollama Integration Issues**

This indicates Ollama is not properly enabled or configured:

```bash
# Check Ollama is running
ollama list
curl http://localhost:11434/api/tags

# Verify FLOAT configuration
python -c "from config import FloatConfig; c=FloatConfig('float-config.json'); print('Ollama enabled:', c.get('enable_ollama'))"

# Check daemon status (if running)
cat ~/float-dropzone/.daemon_status.json | grep -A 10 ollama
```

**Fix: Ensure Ollama is enabled in configuration**
```json
{
  "enable_ollama": true,
  "ollama_url": "http://localhost:11434",
  "ollama_model": "llama3.1:8b"
}
```

**2. Ollama Connection Failed**
```bash
# Check Ollama status and start if needed
ollama list
ollama serve
# Pull model if missing
ollama pull llama3.1:8b
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

**5. Daily Logs Processed as Conversations**

FLOAT now properly detects daily logs via frontmatter patterns:

```yaml
---
type: log
uid: log::
title: 2025-06-12
mood: "focused"
tags: [daily]
---
```

If daily logs are still misclassified, check:
- Filename matches `YYYY-MM-DD.md` pattern
- Content includes daily log section markers ("## Brain Boot", "## Body Boot")
- Frontmatter contains daily log indicators

**6. Large File Processing**
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

When enabled (`"enable_enhanced_integration": true`), provides:

#### Content Classification
- **Daily Log Detection**: Comprehensive frontmatter and pattern analysis
- **Conversation Platform Detection**: Claude.ai, ChatGPT export recognition
- **Document Structure Analysis**: Markdown, JSON, PDF intelligent processing
- **FLOAT Pattern Recognition**: 40+ methodology patterns with signal density scoring

#### AI-Powered Analysis
- **Local Ollama Summarization**: Privacy-preserving AI analysis with specialized prompts
- **Hierarchical Processing**: Large files split and synthesized intelligently
- **Content-Specific Insights**: Daily log mood/productivity analysis, conversation flow analysis
- **Cross-Reference Generation**: Automatic vault and temporal linking

#### Specialized .dis File Generation
- **Daily Log .dis Files**: Enhanced with AI insights, actionable items, mood tracking
- **Conversation .dis Files**: Platform metadata, speaker analysis, topic extraction
- **General Document .dis Files**: Pattern analysis, tripartite classification, cross-references
- **Dataview Integration**: Dynamic queries for related content and navigation

#### Advanced Routing
- **Tripartite Collection System**: Intelligent concept/framework/metaphor classification
- **Special Pattern Collections**: Dedicated routing for dispatch, RFC, echoCopy patterns
- **Temporal Indexing**: Date-based metadata for efficient conversation queries
- **Multi-Domain Routing**: Complex content routed to multiple collections based on confidence scoring

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
- **Current Version**: 2.3.0
- **Compatibility**: Python 3.8+, Obsidian 1.0+
- **Dependencies**: See requirements.txt
- **Major Features**: Content deduplication, smart routing, enhanced AI integration

### Contributing

1. Fork the repository
2. Create feature branch
3. Add tests for new functionality
4. Submit pull request

### License

FLOAT Complete Knowledge Ecosystem is released under MIT License.

---

*For additional support, check the logs at `~/float-dropzone/.logs/` or review the health status at `~/float-dropzone/.status/`*