# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Running the Daemon
```bash
# Basic daemon startup (monitors dropzone folder)
python streamlined_daemon_architecture.py /path/to/dropzone/folder

# With Ollama summarization enabled
python streamlined_daemon_architecture.py /path/to/dropzone/folder --enable-ollama

# Process existing files before starting monitoring
python streamlined_daemon_architecture.py /path/to/dropzone/folder --process-existing

# Full configuration example
python streamlined_daemon_architecture.py ~/dropzone \
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
```

## Architecture Overview

This is a FLOAT (Feed-Log-Offload-Archive-Trunk) knowledge management system that processes files dropped into a dropzone folder and integrates them with an Obsidian vault and ChromaDB vector database.

### Key Components

1. **Streamlined Daemon (`streamlined_daemon_architecture.py`)**: Main entry point that watches the dropzone folder and orchestrates processing.

2. **Enhanced Comprehensive Context (`enhanced_comprehensive_context_ollama.py`)**: Aggregates daily context from conversations and vault activity, generates conversation .dis files, and provides cross-referencing capabilities. Includes Ollama integration for intelligent summarization.

3. **Ollama Float Summarizer (`ollama_enhanced_float_summarizer.py`)**: Handles hierarchical multi-chunk summarization using local Ollama models. Intelligently chunks content based on type (conversation, document, etc.).

4. **Float .dis Generator (`float_dis_template_system.py`)**: Creates rich `.float_dis.md` files with YAML frontmatter and Templater.js templates for Obsidian integration.

### Data Flow

1. Files are dropped into the dropzone folder
2. Daemon detects new files and extracts content/metadata
3. Content is analyzed for FLOAT patterns (ctx::, highlight::, float.dispatch)
4. Ollama generates intelligent summaries (if enabled)
5. Content is chunked and stored in ChromaDB collections
6. A `.float_dis.md` file is generated with metadata and Obsidian templates
7. Daily context is updated to include the new content

### FLOAT Pattern Detection

The system recognizes specific FLOAT methodology markers:
- `ctx::` - Context markers for temporal/situational notes
- `highlight::` - Important insights or key points
- `float.dispatch` - Dispatch objects for topic branching
- Conversation links from Claude.ai or ChatGPT

### ChromaDB Collections

- `float_tripartite_v2_concept` - Conceptual domain storage
- `float_tripartite_v2_framework` - Framework domain storage
- `float_tripartite_v2_metaphor` - Metaphor domain storage
- `float_dropzone_comprehensive` - General dropzone ingestion
- `FLOAT.conversations` - Conversation-specific .dis files

## Configuration

Key paths are configurable via command-line arguments:
- Vault path: Default `/Users/evan/vault`
- Chroma data path: Default `/Users/evan/github/chroma-data`
- Conversation .dis path: Default `{vault_path}/FLOAT.conversations`

Ollama configuration:
- URL: `http://localhost:11434`
- Models: Configurable, defaults to `llama3.1:8b`