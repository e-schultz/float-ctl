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

#### Comprehensive Test Suite
```bash
# Install test dependencies
pip install -r requirements-dev.txt

# Run all tests
python run_tests.py

# Run all tests with coverage report
python run_tests.py --coverage

# Run specific test categories
python run_tests.py --unit          # Unit tests only
python run_tests.py --integration   # Integration tests only  
python run_tests.py --config        # Configuration tests only
python run_tests.py --daemon        # Daemon functionality tests
python run_tests.py --patterns      # Pattern detection tests

# Run tests in parallel (faster)
python run_tests.py --parallel

# Run specific test file
python run_tests.py --file tests/test_config.py

# Skip slow tests (fast development cycle)
python run_tests.py --fast

# Using pytest directly
pytest tests/ -v                    # All tests with verbose output
pytest tests/test_config.py -v      # Specific test file
pytest -m unit                      # Unit tests only
pytest -m "not slow"                # Skip slow tests
pytest --cov=. --cov-report=html    # With coverage report
```

#### Individual Component Testing
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

# Test configuration validation
python -c "from config import FloatConfig; c = FloatConfig(); print('Config valid:', c.validate())"

# Debug configuration issues
python -c "from config import FloatConfig; c=FloatConfig('float-config.json'); print('Ollama enabled:', c.get('enable_ollama'))"
```

## Development Environment Setup

### First-Time Setup
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install all dependencies from pinned requirements
pip install -r requirements.txt

# Install development dependencies (if creating tests)
pip install pytest pytest-cov black flake8 mypy

# Verify installation
python -c "from config import FloatConfig; print('✅ FLOAT modules loaded successfully')"
```

### Testing Framework

FLOAT includes a comprehensive test suite with pytest-based testing infrastructure.

#### Test Structure
```
tests/
├── __init__.py              # Test suite initialization
├── conftest.py              # Shared fixtures and configuration
├── test_config.py           # Configuration management tests
├── test_daemon.py           # Core daemon functionality tests
├── test_pattern_detector.py # Pattern detection tests
├── test_integration.py      # Integration tests (future)
└── data/                    # Test data files
```

#### Quick Testing Commands
```bash
# Install test dependencies
pip install -r requirements-dev.txt

# Run all tests with custom runner
./run_tests.py

# Run specific test categories
./run_tests.py --config      # Configuration tests
./run_tests.py --daemon      # Daemon functionality  
./run_tests.py --patterns    # Pattern detection tests
./run_tests.py --unit        # Unit tests only

# Development testing (fast)
./run_tests.py --fast        # Skip slow tests
./run_tests.py --parallel    # Run in parallel

# Coverage reporting
./run_tests.py --coverage    # Generate HTML coverage report
```

#### Advanced Testing
```bash
# Direct pytest commands
pytest tests/ -v                           # All tests, verbose
pytest tests/test_config.py::TestFloatConfig::test_default_config_loading -v
pytest -m "unit and not slow"              # Fast unit tests only
pytest --cov=. --cov-report=html           # Coverage report
pytest -x --pdb                            # Stop on first failure, debug

# Test specific functionality
pytest tests/test_config.py -k "environment" -v  # Environment variable tests
pytest tests/test_daemon.py -k "deduplication"   # Deduplication tests
pytest tests/test_pattern_detector.py -k "float" # FLOAT pattern tests

# Parallel execution for speed
pytest -n auto                             # Auto-detect CPU cores
pytest -n 4                                # Use 4 processes
```

#### Test Categories and Markers
```bash
# Test markers for categorization
pytest -m unit                 # Unit tests for individual components
pytest -m integration          # Integration tests across components
pytest -m config              # Configuration-related tests  
pytest -m daemon              # Daemon functionality tests
pytest -m patterns            # Pattern detection tests
pytest -m slow                # Long-running tests
pytest -m "not slow"          # Skip slow tests for development

# Combined markers
pytest -m "unit and not slow"  # Fast unit tests only
pytest -m "config or daemon"   # Configuration or daemon tests
```

#### Test Fixtures and Utilities
```python
# Available fixtures (from conftest.py)
def test_example(temp_dir, mock_config, sample_text_content):
    # temp_dir: Temporary directory for test files
    # mock_config: Complete test configuration
    # sample_text_content: Sample content with FLOAT patterns
    pass
```

#### Writing New Tests
```python
# Example test structure
import pytest
from your_module import YourClass

class TestYourClass:
    def setup_method(self):
        """Set up before each test"""
        self.instance = YourClass()
    
    def test_basic_functionality(self, mock_config):
        """Test basic functionality"""
        result = self.instance.process(mock_config)
        assert result['success'] is True
    
    @pytest.mark.slow
    def test_large_file_processing(self):
        """Test that takes longer to run"""
        # Large file processing test
        pass
    
    @pytest.mark.unit
    def test_unit_functionality(self):
        """Unit test for specific component"""
        # Isolated unit test
        pass
```

#### Test Data Management
```bash
# Test data location
tests/data/                     # Static test data files
tests/temp/                     # Temporary test files (auto-created)

# Using test fixtures
def test_with_sample_content(sample_text_content, sample_daily_log_content):
    # Access pre-defined test content
    assert "ctx::" in sample_text_content
    assert "type: log" in sample_daily_log_content
```

#### Continuous Integration Testing
```bash
# Pre-commit testing (fast)
./run_tests.py --fast --parallel

# Full test suite (CI)
./run_tests.py --coverage --parallel

# Quality checks
black --check .                 # Code formatting
flake8 .                       # Linting
mypy --ignore-missing-imports . # Type checking
```

#### Test Coverage Goals
- **Configuration**: 95%+ coverage for config loading, validation, environment handling
- **Daemon Core**: 90%+ coverage for file processing, deduplication, state management  
- **Pattern Detection**: 85%+ coverage for FLOAT pattern recognition
- **Integration**: 80%+ coverage for component interaction testing

#### Performance Testing
```bash
# Memory profiling during tests
pytest --profile-svg tests/test_daemon.py

# Time-based performance testing
pytest --durations=10           # Show 10 slowest tests
pytest --benchmark-only         # Run benchmark tests only (if implemented)
```

#### Test Maintenance
```bash
# Update test dependencies
pip install -r requirements-dev.txt --upgrade

# Clean test artifacts
rm -rf htmlcov/ .coverage .pytest_cache/
rm -rf tests/temp/* tests/data/temp*

# Generate test report
pytest --html=test_report.html --self-contained-html
```

### Git Workflow Best Practices
```bash
# Create feature branch for improvements
git checkout -b feature/improve-pattern-detection

# Keep commits focused and atomic
git add specific_file.py
git commit -m "feat: add enhanced pattern detection for persona annotations

- Implement recognition for [qtb::] and [karen::] patterns
- Add confidence scoring for tripartite classification
- Reduce false positives in conversation detection"

# Rebase before merging to maintain clean history
git rebase main

# Use conventional commit messages
# feat: new feature
# fix: bug fix  
# docs: documentation changes
# test: adding tests
# refactor: code improvements without functionality changes
```

### Performance Monitoring
```bash
# Monitor real-time performance metrics
watch -n 5 'tail -1 ~/float-dropzone/.logs/float_metrics.log | jq .'

# Generate performance report for last 24 hours
python -c "
from performance_monitor import PerformanceMonitor
from pathlib import Path
monitor = PerformanceMonitor(Path('~/float-dropzone'))
print(monitor.get_performance_summary(hours=24))
"

# Check ChromaDB collection sizes
python -c "
import chromadb
client = chromadb.PersistentClient(path='~/github/chroma-data')
for collection in client.list_collections():
    count = collection.count()
    print(f'{collection.name}: {count:,} documents')
"
```

## Architecture Overview

This is a FLOAT (Feed-Log-Offload-Archive-Trunk) knowledge management system that processes files dropped into a dropzone folder and integrates them with an Obsidian vault and ChromaDB vector database.

### Key Components

1. **Streamlined Daemon (`streamlined_float_daemon.py`)**: Main entry point that watches the dropzone folder and orchestrates basic file processing. Simplified to focus on monitoring and delegation.

2. **Enhanced Integration System (`enhanced_integration.py`)**: Central hub for sophisticated content analysis, tripartite routing, and cross-system coordination. Bridges daemon with specialized processing systems.

3. **Enhanced Pattern Detector (`enhanced_pattern_detector.py`)**: Comprehensive FLOAT signal analysis with 40+ pattern types including core signals, extended patterns, persona annotations, and platform integration detection.

4. **Enhanced Comprehensive Context (`enhanced_comprehensive_context_ollama.py`)**: Aggregates daily context from conversations and vault activity, generates conversation .dis files, and provides cross-referencing capabilities. Includes Ollama integration for intelligent summarization.

5. **Daily Log Detection & Processing**: Advanced detection system that distinguishes daily logs from conversations using frontmatter patterns (`type: log`, `uid: log::`, `mood:`, `soundtrack:` fields) and content structure analysis. Provides specialized analysis for actionable items, mood tracking, and productivity signals.

6. **Ollama Float Summarizer (`ollama_enhanced_float_summarizer.py`)**: Handles hierarchical multi-chunk summarization using local Ollama models. Intelligently chunks content based on type (conversation, document, etc.).

7. **Float .dis Generator (`float_dis_template_system.py`)**: Creates rich `.float_dis.md` files with comprehensive YAML frontmatter, enhanced auto-tagging, and Templater.js templates for Obsidian integration.

### Data Flow

1. **File Detection**: Daemon monitors dropzone folder for new files
2. **Basic Processing**: Daemon extracts content/metadata and performs initial analysis
3. **Content Classification (CRITICAL FIRST STEP)**: Enhanced Integration System performs content classification to identify:
   - **Daily Logs**: Via frontmatter patterns (`type: log`, `uid: log::`, etc.) and content structure
   - **Conversations**: Platform-specific exports from Claude.ai, ChatGPT, etc.
   - **General Documents**: All other content types
4. **Specialized Processing Path**: Based on content type:
   - **Daily Logs**: Specialized daily log analysis with mood tracking, actionable items, productivity signals
   - **Conversations**: Platform metadata extraction, speaker analysis, dialogue structure
   - **General Documents**: Standard FLOAT pattern analysis and document structure
5. **Enhanced Integration**: Sophisticated analysis via Enhanced Integration System:
   - **Pattern Analysis**: 40+ FLOAT patterns detected via Enhanced Pattern Detector
   - **Tripartite Classification**: Domain classification (Concept/Framework/Metaphor) with confidence scoring
   - **Signal Density**: Advanced signal analysis with threshold detection
   - **Platform Integration**: Detection of build tools and external service references
6. **Intelligent Routing**: Content routed to appropriate tripartite collections based on analysis
7. **Ollama Summarization**: AI-powered summaries generated (if enabled and configured correctly)
8. **Storage Optimization**: Domain-specific chunking strategies applied
9. **Rich .dis Generation**: Comprehensive `.float_dis.md` files with 30+ metadata fields
   - **Daily Logs**: Enhanced with AI insights, actionable items, mood tracking in `FLOAT.conversations/`
   - **Conversations**: Platform metadata, speaker analysis, topic extraction in `FLOAT.conversations/`
   - **General Documents**: Pattern analysis, tripartite classification, cross-references in dropzone
10. **Cross-Reference**: Vault and collection cross-references generated
11. **Daily Context**: Enhanced daily summaries updated with new content

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

### Daily Log Processing Improvements (Latest)

**Content-Aware Processing:**
- **Fixed daily log misidentification**: Enhanced detection using frontmatter patterns (`type: log`, `uid: log::`, `mood:`, `soundtrack:`)
- **Processing order fix**: Content classification now happens BEFORE conversation detection
- **Specialized daily log analysis**: Mood tracking, actionable item extraction, productivity signals
- **Enhanced .dis generation**: Daily logs now get specialized .dis files in `FLOAT.conversations/` with AI-powered insights

**Configuration Bug Fixes:**
- **Fixed critical Ollama integration bug**: Environment variable handling was incorrectly overriding `enable_ollama` to `False`
- **Proper boolean environment variable handling**: Only overrides when env var is actually set
- **Configuration validation**: Added debug commands for troubleshooting config issues

**Signal-to-Noise Improvements:**
- **Reduced template boilerplate**: Focus on extracting meaningful patterns rather than generic descriptions
- **Enhanced pattern recognition**: 40+ FLOAT patterns detected with confidence scoring
- **Content complexity assessment**: Intelligent chunking based on document type and signal density
- **Cross-reference generation**: Automatic vault linking and temporal context maintenance

**Current State (2025-06-12):**
- **Daemon Status**: Healthy with 2 files processed successfully (100% success rate)
- **Ollama Integration**: Fixed and working correctly with model `llama3.1:8b`
- **ChromaDB**: 51 collections with comprehensive tripartite routing
- **Processing Performance**: Average 81.4 seconds per file with hierarchical AI analysis
- **Daily Log Processing**: Fully functional with specialized templates and AI insights

## documentation

- ObsidianMD dataview documentation @docs/dataview.md
- ObsidianMD templater documentation @docs/templater.md
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

**"AI Summary shows 'None'" - Ollama Integration Issues:**

This critical issue indicates Ollama is not properly enabled or configured. The most common cause is a configuration bug where environment variable logic incorrectly overrides the config file setting.

**Diagnosis:**
```bash
# Check Ollama is running
ollama list
curl http://localhost:11434/api/tags

# Verify FLOAT configuration
python -c "from config import FloatConfig; c=FloatConfig('float-config.json'); print('Ollama enabled:', c.get('enable_ollama'))"

# Check daemon status (if running)
cat ~/float-dropzone/.daemon_status.json | grep -A 10 ollama
```

**Root Cause Fix:**
The issue was in `config.py` where environment variable handling incorrectly overrode `enable_ollama` to `False` even when not set:

```python
# FIXED: Environment variable handling now only overrides when actually set
float_enable_ollama = os.getenv('FLOAT_ENABLE_OLLAMA')
if float_enable_ollama is not None:
    env_overrides['enable_ollama'] = float_enable_ollama.lower() == 'true'
```

**Verification:**
Ensure config file has:
```json
{
  "enable_ollama": true,
  "ollama_url": "http://localhost:11434",
  "ollama_model": "llama3.1:8b"
}
```

**Daily Logs Processed as Conversations:**

FLOAT now properly detects daily logs via comprehensive frontmatter analysis:

```yaml
---
type: log
uid: log::
title: 2025-06-12
mood: "focused"
tags: [daily]
soundtrack: "Artist - Song"
---
```

**Detection criteria:**
- Frontmatter contains `type: log`, `uid: log::`, `mood:`, `soundtrack:` fields
- Filename matches `YYYY-MM-DD.md` pattern
- Content includes daily log section markers (## Brain Boot, ## Body Boot)
- Processing order ensures content classification happens BEFORE conversation detection

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

**Configuration Validation:**
```bash
# Test configuration loading
python -c "from config import FloatConfig; c = FloatConfig(); print(c.validate())"

# Debug specific config values
python -c "from config import FloatConfig; c=FloatConfig('float-config.json'); print('Config:', {k:v for k,v in c.config.items() if 'ollama' in k.lower()})"
```

### Advanced Debugging

**Enable Debug Logging:**
```bash
# Set debug logging level
export FLOAT_LOG_LEVEL=DEBUG

# Start daemon with verbose output
python streamlined_float_daemon.py ~/dropzone --log-level DEBUG

# Monitor logs in real-time
tail -f ~/float-dropzone/.logs/float_daemon.log | jq '.'
```

**Memory and Performance Profiling:**
```bash
# Profile memory usage (install memory_profiler first: pip install memory_profiler)
python -m memory_profiler streamlined_float_daemon.py

# Profile CPU usage with cProfile
python -m cProfile -o profile_output.prof streamlined_float_daemon.py
python -c "import pstats; p = pstats.Stats('profile_output.prof'); p.sort_stats('cumulative').print_stats(20)"

# Monitor system resources
python -c "
import psutil
print(f'Memory usage: {psutil.virtual_memory().percent}%')
print(f'CPU usage: {psutil.cpu_percent()}%')
print(f'Disk usage: {psutil.disk_usage(\"/\").percent}%')
"
```

**ChromaDB Analysis and Debugging:**
```bash
# Analyze ChromaDB performance and storage
python -c "
import chromadb
from pathlib import Path
client = chromadb.PersistentClient(path='~/github/chroma-data')

print('📊 ChromaDB Analysis:')
collections = client.list_collections()
total_docs = 0

for collection in collections:
    count = collection.count()
    total_docs += count
    print(f'  {collection.name}: {count:,} documents')

print(f'\\n📈 Total documents: {total_docs:,}')

# Check disk usage
chroma_path = Path('~/github/chroma-data').expanduser()
if chroma_path.exists():
    size_mb = sum(f.stat().st_size for f in chroma_path.rglob('*') if f.is_file()) / 1024 / 1024
    print(f'💾 ChromaDB disk usage: {size_mb:.1f} MB')
"

# Test ChromaDB query performance
python -c "
import time
import chromadb
client = chromadb.PersistentClient(path='~/github/chroma-data')

try:
    collection = client.get_collection('float_tripartite_v2_concept')
    start = time.time()
    results = collection.query(query_texts=['test query'], n_results=5)
    elapsed = time.time() - start
    print(f'✅ Query performance: {elapsed:.3f}s for {len(results[\"documents\"][0]) if results[\"documents\"] else 0} results')
except Exception as e:
    print(f'❌ ChromaDB query failed: {e}')
"
```

**Dependency and Environment Validation:**
```bash
# Validate all dependencies are correctly installed
python -c "
import sys
print(f'Python version: {sys.version}')

required_modules = [
    'watchdog', 'chromadb', 'pathlib', 'python_magic', 'PyPDF2', 
    'mammoth', 'requests', 'ollama', 'frontmatter'
]

missing = []
for module in required_modules:
    try:
        __import__(module)
        print(f'✅ {module}')
    except ImportError:
        missing.append(module)
        print(f'❌ {module} - MISSING')

if missing:
    print(f'\\n🚨 Install missing: pip install {\" \".join(missing)}')
else:
    print('\\n🎉 All dependencies satisfied!')
"

# Check file permissions for common paths
python -c "
import os
from pathlib import Path

paths_to_check = [
    '~/vault', '~/github/chroma-data', '~/float-dropzone',
    '~/float-dropzone/.logs', '~/vault/FLOAT.conversations'
]

for path_str in paths_to_check:
    path = Path(path_str).expanduser()
    if path.exists():
        readable = os.access(path, os.R_OK)
        writable = os.access(path, os.W_OK)
        print(f'📁 {path}: R:{\"✅\" if readable else \"❌\"} W:{\"✅\" if writable else \"❌\"}')
    else:
        print(f'📁 {path}: ❌ Does not exist')
"
```

**Configuration Deep Dive:**
```bash
# Comprehensive configuration analysis
python -c "
from config import FloatConfig
import json

config = FloatConfig('float-config.json')
print('📋 Current Configuration:')
print(json.dumps(config.config, indent=2, default=str))

print('\\n🔍 Validation Results:')
validations = config.validate()
for key, valid in validations.items():
    status = '✅' if valid else '❌'
    print(f'  {status} {key}: {valid}')

print('\\n🌍 Environment Overrides:')
env_vars = ['FLOAT_VAULT_PATH', 'FLOAT_CHROMA_PATH', 'FLOAT_DROPZONE_PATH', 
           'FLOAT_LOG_DIR', 'FLOAT_ENABLE_OLLAMA', 'OLLAMA_URL']
for var in env_vars:
    value = os.getenv(var)
    if value:
        print(f'  {var}={value}')
"
```

## Memories
- after changes have been made, review the readme.md and claude.md and see if any changes need to be made to reflect the changes
```