#!/usr/bin/env python3
"""
Test the enhanced integration with the fixed configuration
"""

from pathlib import Path
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from config import FloatConfig

print("=== TESTING ENHANCED INTEGRATION WITH FIXED CONFIG ===")

# Create a simple test daily log content
test_content = """---
created: 2025-06-11T09:37:22
uid: log::20250611093722
title: 2025-06-11
type: log
status: active
week: 2025-W24
quarter: 2025-Q2
mood: "excited"
soundtrack: ""
tags:
  - daily
  - y2025/q2/w24
---

## Brain Boot

ctx:: 2025-06-11 7:15am [mood::excited]

Starting the day with some organization and Claude conversation analysis.

## Body Boot

Need to shower and get groceries.

## Key Discussion Points

Had a great meeting about AI safety and enterprise opportunities.

ctx:: important collaboration potential identified

## EOD Summary

Productive day with good insights and actionable follow-ups.
"""

# Test the enhanced integration
try:
    from enhanced_integration import EnhancedSystemIntegration
    from config import FloatConfig
    
    # Mock daemon with fixed config
    class MockDaemon:
        def __init__(self):
            self.config = FloatConfig("/Users/evan/github/float-log/float-config.json")
            self.vault_path = Path("/Users/evan/Documents/FLOAT.SHACK")
            
        class MockLogger:
            def info(self, msg): print(f"INFO: {msg}")
            def warning(self, msg): print(f"WARNING: {msg}")
            def error(self, msg): print(f"ERROR: {msg}")
            
        logger = MockLogger()
        
        # Mock components to avoid full initialization
        components = {
            'context': None,
            'summarizer': None,
            'dis_generator': None
        }
    
    daemon = MockDaemon()
    print(f"Daemon config enable_ollama: {daemon.config.get('enable_ollama')}")
    
    # Initialize enhanced integration
    integration = EnhancedSystemIntegration(daemon)
    
    print(f"Enhanced integration ollama_enabled: {integration.ollama_enabled}")
    print(f"Enhanced integration ollama_summarizer: {integration.ollama_summarizer}")
    
    if integration.ollama_enabled and integration.ollama_summarizer:
        print("✅ Ollama is enabled and initialized!")
        print(f"Ollama URL: {integration.ollama_summarizer.ollama_url}")
        print(f"Ollama model: {integration.ollama_summarizer.model}")
        
        # Test the daily log analysis
        print("\n=== TESTING DAILY LOG ANALYSIS ===")
        
        # Extract frontmatter
        frontmatter_data = integration._extract_daily_log_frontmatter(test_content)
        print(f"Extracted frontmatter: {frontmatter_data}")
        
        # Test Ollama daily log analysis directly
        ollama_result = integration._generate_ollama_daily_log_analysis(test_content, frontmatter_data)
        print(f"Ollama analysis result: {ollama_result}")
        print(f"Summary: {ollama_result.get('summary', 'NO SUMMARY')}")
        
    else:
        print("❌ Ollama is not properly enabled")
        
except Exception as e:
    print(f"Error during test: {e}")
    import traceback
    traceback.print_exc()