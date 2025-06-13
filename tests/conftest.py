"""
Pytest configuration and shared fixtures for FLOAT test suite
"""

import pytest
import tempfile
import json
import shutil
from pathlib import Path
from unittest.mock import Mock, patch


@pytest.fixture(scope="session")
def temp_project_dir():
    """Create a temporary project directory for tests"""
    temp_dir = Path(tempfile.mkdtemp(prefix="float_test_"))
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def temp_dir():
    """Create a temporary directory for individual tests"""
    temp_dir = Path(tempfile.mkdtemp(prefix="float_test_"))
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def mock_config(temp_dir):
    """Create a mock configuration for testing"""
    config = {
        "vault_path": str(temp_dir / "vault"),
        "chroma_data_path": str(temp_dir / "chroma"),
        "dropzone_path": str(temp_dir / "dropzone"),
        "conversation_dis_path": str(temp_dir / "vault" / "FLOAT.conversations"),
        "enable_ollama": False,
        "enable_enhanced_integration": False,
        "auto_update_daily_context": False,
        "max_file_size_mb": 10,
        "chunk_size": 1000,
        "retry_attempts": 2,
        "log_level": "ERROR",
        "enable_performance_monitoring": False,
        "enable_health_checks": False
    }
    
    # Create directories
    for path_key in ["vault_path", "chroma_data_path", "dropzone_path", "conversation_dis_path"]:
        Path(config[path_key]).mkdir(parents=True, exist_ok=True)
    
    return config


@pytest.fixture
def config_file(temp_dir, mock_config):
    """Create a temporary config file"""
    config_file = temp_dir / "test_config.json"
    with open(config_file, 'w') as f:
        json.dump(mock_config, f)
    return config_file


@pytest.fixture
def sample_text_content():
    """Sample text content for testing"""
    return """
    ctx::Meeting preparation for project review
    
    This is a sample document for testing the FLOAT system.
    
    highlight::Key decision point about architecture
    
    Some regular content here with multiple paragraphs.
    The content includes various FLOAT patterns for testing.
    
    signal::Important data point for tracking
    
    float.dispatch(architecture_discussion)
    
    Additional content:
    - Bullet point 1
    - Bullet point 2  
    - Bullet point 3
    
    [sysop::] Technical review notes
    [karen::] Editorial feedback needed
    
    ```python
    def example_function():
        return "test code block"
    ```
    
    expandOn::Further research needed on this topic
    relatesTo::Previous architecture discussions
    """


@pytest.fixture
def sample_daily_log_content():
    """Sample daily log content for testing"""
    return """---
type: log
uid: log::2025-06-12
mood: "focused"
tags: [daily]
created: 2025-06-12T09:00:00
---

## Brain Boot
ctx::Starting the day with clear priorities

## Key Tasks
- Review FLOAT system improvements
- highlight::Configuration bug fix was successful
- Complete testing framework implementation

## Reflection
Good progress on the deduplication system.
The smart routing improvements are working well.

## Notes
signal::Testing framework needs comprehensive coverage
float.dispatch(testing_strategy)

## Body Boot
Physical energy level: high
Focus state: sharp
"""


@pytest.fixture
def sample_conversation_content():
    """Sample conversation content for testing"""
    return """Human: Can you help me understand FLOAT patterns better?

Assistant: Absolutely! FLOAT patterns are key markers in the FLOAT methodology. Let me explain:

ctx::Explaining FLOAT patterns for knowledge management

The core FLOAT patterns include:

1. **Context markers**: ctx::ritual_context
   - Used for temporal anchors and mood tracking
   - Examples: ctx::morning_focus, ctx::evening_reflection

2. **Highlight patterns**: highlight::key_insight
   - Mark important insights or decisions
   - Help with later retrieval and review

3. **Signal patterns**: signal::important_data
   - Track key information and markers
   - Build up signal density for analysis

4. **Dispatch patterns**: float.dispatch(topic)
   - Finalized cognitive exports
   - Never summarized, always preserved

5. **Persona annotations**:
   - [sysop::] - System operator perspectives
   - [karen::] - Editorial conscience and creative director
   - [qtb::] - Queer Techno Bard expressions
   - [lf1m::] - Processing time markers

These patterns help create a neurodivergent symbolic system for narrative-cognitive tracking.

Human: That's helpful! How does signal density work?

Assistant: Great question! Signal density is a key concept in FLOAT analysis.

signal::Signal density measures pattern concentration

Here's how it works:

**Signal Density Calculation:**
- Counts FLOAT patterns per content chunk
- Measures pattern diversity and frequency
- Calculates percentage of content with signals

**Thresholds for Content Value:**
- **Ultra-high value**: >5% density + 10+ total signals
- **High value**: >3% density + 5+ total signals  
- **Medium value**: >1% density + 3+ total signals
- **Low value**: <1% density

**Impact on Processing:**
- High signal density → Smaller chunks for precision
- Low signal density → Larger chunks for efficiency
- Ultra-high content → Special preservation handling

float.dispatch(signal_density_explanation)

The system uses this to optimize storage and retrieval in ChromaDB collections.

Human: Interesting! What about the tripartite routing system?

Assistant: The tripartite routing system is one of FLOAT's most sophisticated features!

highlight::Tripartite routing enables domain-specific optimization

**Three Specialized Collections:**

1. **Concept Domain** (float_tripartite_v2_concept)
   - Abstract ideas, theories, mental models
   - Precision-optimized chunking: 600/1200 chars
   - Best for: Philosophical discussions, theoretical frameworks

2. **Framework Domain** (float_tripartite_v2_framework) 
   - Structured methodologies, processes, systems
   - Structure-optimized chunking: 900/1800 chars
   - Best for: Technical documentation, workflows

3. **Metaphor Domain** (float_tripartite_v2_metaphor)
   - Analogies, stories, creative expressions
   - Resonance-optimized chunking: 800/1600 chars
   - Best for: Creative writing, explanatory analogies

**Routing Logic:**
- Content analysis determines domain fit
- Confidence scores guide routing decisions
- Multi-domain content gets stored in multiple collections
- Special patterns (dispatch, rfc) get dual routing

ctx::This enables optimized retrieval for different cognitive needs

The system learns from usage patterns to improve routing accuracy over time."""


@pytest.fixture
def mock_chromadb_client():
    """Mock ChromaDB client for testing"""
    mock_client = Mock()
    mock_collection = Mock()
    
    # Configure collection methods
    mock_collection.add.return_value = None
    mock_collection.query.return_value = {
        'ids': [['test_id_1', 'test_id_2']],
        'documents': [['Test document 1', 'Test document 2']],
        'metadatas': [[{'source': 'test'}, {'source': 'test'}]],
        'distances': [[0.1, 0.2]]
    }
    mock_collection.get.return_value = {
        'ids': ['test_id_1'],
        'documents': ['Test document'],
        'metadatas': [{'source': 'test'}]
    }
    
    # Configure client methods
    mock_client.get_or_create_collection.return_value = mock_collection
    mock_client.create_collection.return_value = mock_collection
    mock_client.get_collection.return_value = mock_collection
    mock_client.list_collections.return_value = [{'name': 'test_collection'}]
    
    return mock_client


@pytest.fixture
def mock_ollama_client():
    """Mock Ollama client for testing"""
    mock_client = Mock()
    mock_client.generate.return_value = {
        'response': 'This is a test summary generated by the mock Ollama client.',
        'done': True
    }
    return mock_client


@pytest.fixture
def sample_file_content():
    """Sample file content for testing file processing"""
    return {
        'text': 'This is sample file content for testing.',
        'markdown': '# Test Document\n\nThis is a **test** document with *markdown* formatting.',
        'conversation': '''Human: Hello, can you help me with something?\n\nAssistant: Of course! I'd be happy to help you. What do you need assistance with?''',
        'daily_log': '''---\ntype: log\nuid: log::2025-06-12\n---\n\n## Brain Boot\nStarting the day with focus.\n\n## Tasks\n- Complete testing\n- Review code'''
    }


@pytest.fixture
def mock_float_daemon(mock_config, mock_chromadb_client):
    """Mock FLOAT daemon for testing"""
    with patch('streamlined_float_daemon.ChromaClient', return_value=mock_chromadb_client), \
         patch('logging_config.setup_logging') as mock_logging, \
         patch('error_recovery.FileProcessingRecovery') as mock_recovery, \
         patch('performance_monitor.PerformanceMonitor') as mock_perf, \
         patch('health_monitor.HealthMonitor') as mock_health:
        
        mock_logging.return_value = Mock()
        
        from streamlined_float_daemon import StreamlinedFloatDaemon
        daemon = StreamlinedFloatDaemon(
            dropzone_path=mock_config['dropzone_path'],
            config_path=None
        )
        # Override config with mock
        daemon.config.config = mock_config
        return daemon


@pytest.fixture
def mock_all_imports():
    """Mock all external imports for daemon testing"""
    with patch('logging_config.setup_logging') as mock_logging, \
         patch('error_recovery.FileProcessingRecovery') as mock_recovery, \
         patch('performance_monitor.PerformanceMonitor') as mock_perf, \
         patch('health_monitor.HealthMonitor') as mock_health, \
         patch('enhanced_integration.EnhancedSystemIntegration') as mock_integration:
        
        mock_logging.return_value = Mock()
        yield {
            'logging': mock_logging,
            'recovery': mock_recovery,
            'performance': mock_perf,
            'health': mock_health,
            'integration': mock_integration
        }