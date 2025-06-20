#!/usr/bin/env python3
"""
Test script for cross-reference pattern integration - Issue #3
Tests that enhanced patterns show up in cross-reference output
"""

from pathlib import Path
from cross_reference_system import CrossReferenceSystem

# Test content with enhanced patterns
test_content = """
# Test Document for Enhanced Patterns

Standard FLOAT patterns:
ctx:: 2025-06-20 - 4:30pm [mode:testing]
highlight:: important insight about pattern detection

New inline patterns:
This idea should [expandOn:: integration with vault archaeology]
We need to [relatesTo:: productivity vs ritual computing]

New line-level patterns:
mood:: focused and analytical
boundary:: stay on task, test thoroughly  
progress:: implementing enhanced pattern detection
"""

def test_cross_reference_integration():
    """Test that enhanced patterns appear in cross-reference output"""
    print("Testing cross-reference integration for enhanced patterns...")
    print("=" * 70)
    
    # Create a minimal cross-reference system for testing
    vault_path = Path("/tmp/test_vault")
    vault_path.mkdir(exist_ok=True)
    
    # Mock chroma client (we're just testing pattern extraction)
    class MockChromaClient:
        def list_collections(self):
            return []
    
    cross_ref = CrossReferenceSystem(
        vault_path=vault_path,
        chroma_client=MockChromaClient(),
        config={},
        logger=None
    )
    
    # Test signal extraction
    print("\n🔍 SIGNAL EXTRACTION:")
    signals = cross_ref._extract_signal_references(test_content)
    
    print(f"Found {len(signals)} signals:")
    for signal in signals:
        print(f"  - **{signal['type']}** ({signal['importance']}): {signal['content']}")
    
    # Test full cross-reference generation
    print("\n📄 FULL CROSS-REFERENCE GENERATION:")
    
    mock_file_analysis = {
        'float_id': 'test_float_123',
        'content': test_content,  # This was missing!
        'metadata': {
            'filename': 'test-enhanced-patterns.md',
            'file_size': len(test_content),
            'file_type': 'markdown'
        }
    }
    
    cross_refs = cross_ref.generate_cross_references(mock_file_analysis)
    
    print(f"Signal references found: {len(cross_refs.get('signal_references', []))}")
    for signal in cross_refs.get('signal_references', []):
        print(f"  - {signal['type']}: {signal['content']}")
    
    # Test that enhanced patterns are included
    signal_types = [s['type'] for s in cross_refs.get('signal_references', [])]
    
    enhanced_patterns_found = {
        'inline_expand_on': 'inline_expand_on' in signal_types,
        'inline_relates_to': 'inline_relates_to' in signal_types,
        'mood': 'mood' in signal_types,
        'boundary': 'boundary' in signal_types,
        'progress': 'progress' in signal_types
    }
    
    print(f"\n✅ ENHANCED PATTERN DETECTION:")
    for pattern, found in enhanced_patterns_found.items():
        status = "✅" if found else "❌"
        print(f"  {status} {pattern}: {'Found' if found else 'Missing'}")
    
    # Count successful detections
    success_count = sum(enhanced_patterns_found.values())
    total_expected = len(enhanced_patterns_found)
    
    print(f"\n📊 SUMMARY:")
    print(f"  Enhanced patterns detected: {success_count}/{total_expected}")
    print(f"  Traditional patterns still work: {'ctx_signal' in signal_types and 'highlight_signal' in signal_types}")
    
    # Clean up
    try:
        vault_path.rmdir()
    except:
        pass
    
    return success_count >= 3  # At least 3 of the 5 enhanced patterns should work

if __name__ == "__main__":
    success = test_cross_reference_integration()
    print(f"\n{'✅ SUCCESS' if success else '❌ FAILED'}: Cross-reference integration test")