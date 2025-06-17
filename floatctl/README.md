# floatctl - FLOAT Command-Line Interface

`floatctl` is a CLI tool that exposes the lf1m daemon's file processing pipeline for direct command-line use, plus adds FloatQL search syntax that maps your natural `::` notation to ChromaDB/filesystem queries.

## What We Built

### ✅ Core Features (Working)

**File Processing**
```bash
floatctl process ./chat-export.md     # Process single file
floatctl process ./exports/ --recursive  # Process folder
```

**Search & Query** 
```bash
# Basic text search
floatctl search "redux patterns" --limit 5

# FloatQL pattern search  
floatctl query "ctx::meeting" --explain
floatctl query "[karen::] boundaries"
floatctl query "highlight::important" 
```

**Collections Management**
```bash
floatctl collections                  # List all ChromaDB collections
```

**Daemon Status**
```bash
floatctl daemon status              # Check daemon status
```

### 🚧 FloatQL Syntax (Implemented Parser)

The FloatQL parser recognizes and processes:

**FLOAT Patterns:**
- `ctx::meeting` - Context markers
- `highlight::important` - Highlighted content  
- `signal::key` - Signal markers

**Persona Annotations:**
- `[sysop::]` - System operator notes
- `[karen::]` - Editorial conscience  
- `[qtb::]` - Queer Techno Bard
- `[lf1m::]` - Little fucker needs a minute

**Temporal Filters:**
- `created:today` - Created today
- `modified:yesterday` - Modified yesterday  
- `date:2025-06-13` - Specific date

**Bridge References:**
- `bridge::CB-20250611-1510-N1CK` - Specific bridge IDs

**Type Filters:**
- `type:log` - Daily logs
- `type:conversation` - Conversations

### 📁 Architecture

```
floatctl/
├── cli.py                    # Click-based CLI entry point
├── core/
│   └── lf1m.py              # Extracted daemon core logic
├── commands/
│   └── search.py            # Enhanced search with FloatQL
├── floatql/
│   ├── parser.py            # FloatQL syntax parser
│   └── translator.py       # Query translation layer
└── __init__.py
```

## Installation & Usage

### Install
```bash
# From the float-log directory
pip install -e .
```

### Basic Usage
```bash
# Help
floatctl --help
floatctl query --help

# Process files
floatctl process ~/Downloads/claude-conversation.md

# Search collections  
floatctl search "boundaries as care" --limit 3

# FloatQL queries
floatctl query "ctx::meeting nick::" --explain
floatctl query "[karen::] creative" --limit 2

# Collections info
floatctl collections
```

## Example Usage Scenarios

### Daily Workflow
```bash
# Morning: Process yesterday's conversations
floatctl process ~/exports/2025-06-13/

# Search for meeting context using FloatQL
floatctl query "ctx::meeting prep"

# Check collections
floatctl collections
```

### Research Session  
```bash
# Find Redux-related content
floatctl query "redux:: architecture" --explain

# Search persona annotations
floatctl query "[sysop::] technical" --limit 5
```

## What's Working vs. Planned

### ✅ Working Now
- **File processing**: Single files and folders through full FLOAT pipeline
- **Basic search**: Text search across ChromaDB collections
- **FloatQL parsing**: Complete parser for `::` notation syntax
- **Collection management**: List and browse ChromaDB collections
- **Enhanced integration**: Uses existing daemon components

### 🚧 In Progress 
- **Bridge operations**: `bridge::restore`, `bridge::query`, connection following
- **Daemon control**: Start/stop daemon from CLI
- **Reprocess commands**: Re-run dropzone processing

### 🔮 Future
- **Plugin interface**: Extensible processing plugins
- **Cross-system search**: Vault + ChromaDB unified search
- **Export formats**: Markdown, JSON output for research workflows

## Technical Notes

### Core LF1M Module
- Extracted from `streamlined_float_daemon.py`
- Reuses all existing components (Ollama, ChromaDB, pattern detection)
- Compatible with enhanced integration system
- Maintains same processing quality as daemon

### FloatQL Implementation
- **Parser**: Recognizes 40+ FLOAT pattern types
- **Translator**: Converts to ChromaDB metadata queries
- **Collection routing**: Smart collection selection based on patterns
- **Explain mode**: Shows how queries are parsed and executed

### Integration
- Works alongside existing daemon (doesn't interfere)
- Uses same config files and ChromaDB instance
- Leverages existing enhanced pattern detector
- Compatible with all current FLOAT workflows

## Test Results

```bash
# Successful tests
✅ floatctl collections           # Lists 51 collections, 119k+ docs
✅ floatctl search "redux"        # Basic text search working  
✅ floatctl query "ctx::" --explain  # FloatQL parsing working
✅ floatctl process /tmp/test.md  # File processing working

# Processing output example:
Processing file: test_floatctl.md
✓ Processed - Float ID: 1901878be5ba
- Detected patterns and routed to concept collection
- Generated cross-references 
- Updated daily context
```

## Bridge for Next Session

**CB-20250613-FLOATCTL-MVP**

floatctl MVP is **working**! Core functionality complete:
- ✅ File processing via CLI (`floatctl process`)
- ✅ Basic and FloatQL search (`floatctl search/query`) 
- ✅ Collections management (`floatctl collections`)
- ✅ FloatQL parser handles all `::` notation patterns
- ✅ Enhanced integration with existing daemon components

**Next priorities:**
1. Bridge operations for CB-XXXX reference handling
2. Daemon start/stop control 
3. Reprocess dropzone command

The "little fucker needs a minute" (lf1m) core is extracted and working. You can now `floatctl process` files directly without copying to dropzone, and search with natural `ctx::` syntax.