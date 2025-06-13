"""
FLOAT Test Suite
================

Comprehensive test suite for the FLOAT (Feed-Log-Offload-Archive-Trunk) knowledge management system.

Test Categories:
- unit: Unit tests for individual components
- integration: Integration tests across components  
- config: Configuration management tests
- daemon: Core daemon functionality tests
- patterns: Pattern detection and analysis tests
- slow: Long-running tests (marked for optional execution)

Usage:
    # Run all tests
    pytest

    # Run specific test categories
    pytest -m unit
    pytest -m integration
    pytest -m config

    # Run with coverage
    pytest --cov=. --cov-report=html

    # Run in parallel
    pytest -n auto

    # Run specific test file
    pytest tests/test_config.py -v
"""

import os
import sys
from pathlib import Path

# Add the project root to Python path for imports
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Test configuration
TEST_DATA_DIR = Path(__file__).parent / "data"
TEST_TEMP_DIR = Path(__file__).parent / "temp"

# Ensure test directories exist
TEST_DATA_DIR.mkdir(exist_ok=True)
TEST_TEMP_DIR.mkdir(exist_ok=True)

__version__ = "1.0.0"