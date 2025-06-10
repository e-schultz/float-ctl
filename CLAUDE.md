# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Running the Daemon
```bash
# Basic daemon startup (monitors dropzone folder)
python streamlined_float_daemon.py /path/to/dropzone/folder

# With Ollama summarization enabled
python streamlined_float_daemon.py /path/to/dropzone/folder --enable-ollama

# Process existing files before starting monitoring
python streamlined_float_daemon.py /path/to/dropzone/folder --process-existing

# Full configuration example
python streamlined_float_daemon.py ~/dropzone \
  --vault-path ~/vault \
  --chroma-path ~/github/chroma-data \
  --enable-ollama \
  --process-existing
```

### Testing Components
```bash
# Test Ollama summarizer standalone
python ollama_enhanced_float_summarizer.py

# Test .dis file generation
python float_dis_template_system.py

# Test comprehensive context with Ollama
python enhanced_comprehensive_context_ollama.py

# Test enhanced pattern detection
python enhanced_pattern_detector.py

# Test enhanced integration system
python enhanced_integration.py
```

## Architecture Overview

This is a FLOAT (Feed-Log-Offload-Archive-Trunk) knowledge management system that processes files dropped into a dropzone folder and integrates them with an Obsidian vault and ChromaDB vector database.

### Key Components

1. **Streamlined Daemon (`streamlined_float_daemon.py`)**: Main entry point that watches the dropzone folder and orchestrates basic file processing. Simplified to focus on monitoring and delegation.

2. **Enhanced Integration System (`enhanced_integration.py`)**: Central hub for sophisticated content analysis, tripartite routing, and cross-system coordination. Bridges daemon with specialized processing systems.

3. **Enhanced Pattern Detector (`enhanced_pattern_detector.py`)**: Comprehensive FLOAT signal analysis with 40+ pattern types including core signals, extended patterns, persona annotations, and platform integration detection.

4. **Enhanced Comprehensive Context (`enhanced_comprehensive_context_ollama.py`)**: Aggregates daily context from conversations and vault activity, generates conversation .dis files, and provides cross-referencing capabilities. Includes Ollama integration for intelligent summarization.

5. **Ollama Float Summarizer (`ollama_enhanced_float_summarizer.py`)**: Handles hierarchical multi-chunk summarization using local Ollama models. Intelligently chunks content based on type (conversation, document, etc.).

6. **Float .dis Generator (`float_dis_template_system.py`)**: Creates rich `.float_dis.md` files with comprehensive YAML frontmatter, enhanced auto-tagging, and Templater.js templates for Obsidian integration.

### Data Flow

1. **File Detection**: Daemon monitors dropzone folder for new files
2. **Basic Processing**: Daemon extracts content/metadata and performs initial analysis
3. **Enhanced Integration**: Sophisticated analysis via Enhanced Integration System:
   - **Pattern Analysis**: 40+ FLOAT patterns detected via Enhanced Pattern Detector
   - **Content Classification**: Tripartite domain classification (Concept/Framework/Metaphor)
   - **Signal Density**: Advanced signal analysis with threshold detection
   - **Platform Integration**: Detection of build tools and external service references
4. **Intelligent Routing**: Content routed to appropriate tripartite collections based on analysis
5. **Ollama Summarization**: AI-powered summaries generated (if enabled)
6. **Storage Optimization**: Domain-specific chunking strategies applied
7. **Rich .dis Generation**: Comprehensive `.float_dis.md` files with 30+ metadata fields
8. **Cross-Reference**: Vault and collection cross-references generated
9. **Daily Context**: Enhanced daily summaries updated with new content

### Enhanced FLOAT Pattern Detection

The Enhanced Pattern Detector recognizes 40+ sophisticated FLOAT methodology markers, supporting a comprehensive neurodivergent symbolic system for narrative-cognitive tracking:

**Core FLOAT Patterns:**
- `ctx::` - Ritual context markers for temporal anchors, mood tags, and cognitive states
- `highlight::` - Important insights or key points
- `signal::` - Key information and markers
- `float.dispatch({...})` - Finalized cognitive exports (PRESERVE - never summarize)
- Conversation links from Claude.ai or ChatGPT

**Extended FLOAT Patterns:**
- `expandOn::` - Areas for further exploration
- `relatesTo::` - Cross-references to related concepts
- `rememberWhen::` - Temporal memory anchors
- `storyTime::` - Narrative and experiential content
- `echoCopy::` - Content echoing and reinforcement

**Persona Annotation System:**
- `[sysop::]` - System operator perspectives and technical oversight
- `[karen::]` - Editorial conscience and after-hours creative director (internal support team)
- `[qtb::]` - Queer Techno Bard perspectives and creative expressions  
- `[lf1m::]` - Little Fucker needs a minute (processing time and reflection)
- `[any::]` - General annotations and broad contextual notes
- `[rawEvan::]` - Direct unfiltered perspectives
- Custom persona markers for neurodivergent symbolic narrative-cognitive tracking

**Platform Integration Detection:**
- lovable.dev, v0.dev, magicpatterns.com references
- GitHub repositories and issue tracking
- Build tools and deployment platforms
- External service integrations

**BBS Heritage Patterns:**
- float.dis, float.diis file references
- file_id.diz content detection
- Legacy system integration markers

**FLOAT Context Framework (Neurodivergent Symbolic System):**
- `ctx::` serves as ritual context marker for temporal anchors and mood tracking
- Persona recognition during different cognitive states (brain boot, karen mode, etc.)
- `float.dispatch({...})` denotes finalized cognitive exports (preserve, never summarize)
- Emotional tone tracking and transition state recognition
- Support for narrative-cognitive tracking across neurodivergent workflows
- Temporal anchors, mood tags, and cognitive state transitions

### ChromaDB Collections

**Tripartite Collections (Enhanced Routing):**
- `float_tripartite_v2_concept` - Conceptual domain storage (precision-optimized: 600/1200 chars)
- `float_tripartite_v2_framework` - Framework domain storage (structure-optimized: 900/1800 chars)
- `float_tripartite_v2_metaphor` - Metaphor domain storage (resonance-optimized: 800/1600 chars)

**Special Pattern Collections (Dual Routing):**
- `float_dispatch_bay` - Content with `float.dispatch()` patterns (topic branching and dispatch objects)
- `float_rfc` - Content with `float.rfc` patterns (FLOAT Request for Comments and specifications)  
- `float_echoCopy` - Content with `echoCopy::` patterns (echo/repetition for reinforcement learning)

*Note: Special pattern routing works alongside tripartite routing - content gets stored in both the appropriate tripartite collection(s) AND the special pattern collection(s) when patterns are detected.*

**Temporal Query Collections:**
All collections now include enhanced temporal metadata for date-based queries:
- `conversation_date` (YYYY-MM-DD format)
- `conversation_year`, `conversation_month` (for temporal grouping)  
- `conversation_day_of_week` (Monday, Tuesday, etc.)
- `conversation_timestamp_parsed` (ISO format)

**General Collections:**
- `float_dropzone_comprehensive` - General dropzone ingestion (fallback collection)
- `FLOAT.conversations` - Conversation-specific .dis files

**Enhanced Features:**
- Intelligent routing based on content analysis and confidence scores
- Domain-specific chunking strategies for optimal retrieval
- Rich metadata with 30+ fields for advanced querying
- Multi-domain routing for complex content
- Signal-preserving chunking for high-density FLOAT content

## Configuration

Key paths are configurable via command-line arguments or config file:
- Vault path: Default `/Users/evan/Documents/FLOAT.SHACK`
- Chroma data path: Default `/Users/evan/github/chroma-data`
- Dropzone path: Default `/Users/evan/github/processing-vault/src/float-dropzone`
- Log directory: Default `{dropzone_path}/.logs` (can be set via `log_dir` config option)
- Conversation .dis path: Default `{vault_path}/FLOAT.conversations`

Ollama configuration:
- URL: `http://localhost:11434`
- Models: Configurable, defaults to `llama3.1:8b`

Environment variables:
- `FLOAT_VAULT_PATH` - Override vault path
- `FLOAT_CHROMA_PATH` - Override Chroma data path 
- `FLOAT_DROPZONE_PATH` - Override dropzone path
- `FLOAT_LOG_DIR` - Override log directory path
- `FLOAT_ENABLE_OLLAMA` - Enable/disable Ollama (true/false)

## File Structure

Current active files in the system:
- `streamlined_float_daemon.py` - Main daemon (entry point, simplified)
- `enhanced_integration.py` - Enhanced ecosystem integration (central hub)
- `enhanced_pattern_detector.py` - Comprehensive pattern analysis (40+ patterns)
- `enhanced_comprehensive_context_ollama.py` - Context aggregation with Ollama
- `ollama_enhanced_float_summarizer.py` - Hierarchical summarization
- `float_dis_template_system.py` - .dis file generation (enhanced metadata)
- `conversation_dis_enhanced.py` - Advanced conversation analysis
- `cross_reference_system.py` - Vault cross-referencing
- `config.py` - Configuration management
- `logging_config.py` - Structured logging
- `error_recovery.py` - Error handling and recovery
- `performance_monitor.py` - Performance tracking
- `health_monitor.py` - System health monitoring
- `float-config.json` - Configuration file

## Architecture v2.0 Improvements

### Clean Separation of Concerns
- **Daemon**: Simplified to focus on file monitoring and basic processing
- **Enhanced Integration**: Central hub for sophisticated analysis and routing
- **Pattern Detector**: Dedicated system for comprehensive FLOAT signal analysis
- **Specialized Systems**: Cross-references, conversation processing, .dis generation

### Code Quality Improvements
- **Removed 400+ lines** of redundant and duplicate code
- **Eliminated dead imports** for non-existent fallback modules
- **Consolidated logic** into appropriate specialized systems
- **Single source of truth** for pattern detection and tripartite routing

### Enhanced Capabilities
- **40+ pattern types** vs. previous basic detection
- **Intelligent tripartite routing** with confidence scoring
- **Domain-specific chunking** strategies for optimal storage
- **Rich metadata generation** with 30+ fields for enhanced querying
- **Platform integration detection** for modern development workflows

## documentation

- ObsidianMD dataview documentation @docs/dataview.md
- ObsidianMD templater documentation @docs/templater.md
- Chroma documentation @docs/chroma.md
- Nushell documentation @docs/nushell.md

## Troubleshooting

### Common Issues and Solutions

**python-magic not available warning:**
```bash
# Install libmagic system library
brew install libmagic  # macOS
sudo apt-get install libmagic1  # Ubuntu
```

**Import errors on daemon startup:**
- Ensure all files are in the same directory
- Check that `streamlined_float_daemon.py` is the entry point
- Verify `enhanced_pattern_detector.py` is available
- Verify `enhanced_integration.py` is available
- Check python path includes the current directory

**Logging/permission errors:**
- Check that the configured `log_dir` path exists and is writable
- Verify dropzone path has correct permissions (755)
- Ensure ChromaDB data path is writable

**Templater syntax errors in Obsidian:**
- Issue was fixed in `float_dis_template_system.py`
- .dis files now generate clean static content
- No mixed EJS/Templater syntax

**Missing dependencies:**
- All required modules are in the local directory
- Enhanced Pattern Detector requires the comprehensive pattern analysis module
- Enhanced Integration System requires all specialized components
- No external pip installs needed beyond the core dependencies
- Check that Ollama is running if enabled

**Enhanced Integration Issues:**
- If pattern detection fails, check `enhanced_pattern_detector.py` availability
- Tripartite routing requires Enhanced Integration System to be properly initialized
- Cross-reference generation requires the dedicated CrossReferenceSystem
- Fallback modes available when enhanced systems are unavailable

## Memories
- after changes have been made, review the readme.md and claude.md and see if any changes need to be made to reflect the changes
```