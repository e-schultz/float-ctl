#!/usr/bin/env python3
"""
Test script for enhanced pattern detection - Issue #3
Tests inline [expandOn:: xyz] and line-level key:: value patterns
"""

from enhanced_pattern_detector import EnhancedFloatPatternDetector

# Test content with the new patterns from real usage
test_content = """
# Test Document

Standard patterns (should still work):
ctx:: 2025-06-20 - 4:30pm [mode:break time]
expandOn:: some future topic

Inline patterns (new - Issue #3):
This is an idea that is going to [expandOn:: the problem with blogs]
We should [relatesTo:: productivity vs ritual computing]
Need to [connectTo:: vault archaeology patterns]
This reminds me of [rememberWhen:: the first FLOAT experiments]
Generic inline [customKey:: some value here]

Line-level patterns (new - Issue #3):
mood:: focused and energetic
soundtrack:: Artist - Song Name Here  
bodyCheck:: unlock knees and check feet
impact:: significant workflow improvement
boundary:: let it drift, trust the system
progress:: fixed duplicate links successfully
completed:: issues #1 and #2 resolved
issue:: working on pattern detection enhancement
customPattern:: this should be caught by line_generic

Some more content with mixed patterns:
- [expandOn:: cross-reference integration]
- progress:: 75% done with implementation
- boundary:: don't chase every rabbit hole
"""

def test_new_patterns():
    """Test the new inline and line-level patterns"""
    detector = EnhancedFloatPatternDetector()
    
    print("Testing enhanced pattern detection (Issue #3)...")
    print("=" * 60)
    
    # Test inline patterns
    print("\n🔍 INLINE PATTERNS:")
    inline_patterns = [
        'inline_expand_on', 'inline_relates_to', 'inline_connect_to', 
        'inline_remember_when', 'inline_generic'
    ]
    
    for pattern_name in inline_patterns:
        if pattern_name in detector.patterns:
            matches = detector.patterns[pattern_name].findall(test_content)
            print(f"  {pattern_name}: {len(matches)} matches")
            for match in matches:
                if isinstance(match, tuple):
                    print(f"    - Key: '{match[0]}' Value: '{match[1]}'")
                else:
                    print(f"    - '{match}'")
    
    # Test line-level patterns  
    print("\n🔍 LINE-LEVEL PATTERNS:")
    line_patterns = [
        'line_mood', 'line_soundtrack', 'line_body_check', 'line_impact',
        'line_boundary', 'line_progress', 'line_completed', 'line_issue',
        'line_generic'
    ]
    
    for pattern_name in line_patterns:
        if pattern_name in detector.patterns:
            matches = detector.patterns[pattern_name].findall(test_content)
            print(f"  {pattern_name}: {len(matches)} matches")
            for match in matches:
                if isinstance(match, tuple):
                    print(f"    - Key: '{match[0]}' Value: '{match[1]}'")
                else:
                    print(f"    - '{match}'")
    
    # Test full analysis
    print("\n🧠 FULL ANALYSIS:")
    analysis = detector.extract_comprehensive_patterns(test_content)
    
    extended_patterns = analysis.get('extended_float_patterns', {})
    new_pattern_count = 0
    
    for pattern_name in inline_patterns + line_patterns:
        if pattern_name in extended_patterns:
            pattern_data = extended_patterns[pattern_name]
            count = pattern_data.get('count', 0)
            if count > 0:
                new_pattern_count += count
                print(f"  ✅ {pattern_name}: {count} matches")
                for match in pattern_data.get('matches', []):
                    print(f"     - {match}")
    
    print(f"\n📊 SUMMARY:")
    print(f"  Total new patterns detected: {new_pattern_count}")
    print(f"  Inline patterns: {sum(1 for p in inline_patterns if p in extended_patterns and extended_patterns[p]['count'] > 0)}")
    print(f"  Line-level patterns: {sum(1 for p in line_patterns if p in extended_patterns and extended_patterns[p]['count'] > 0)}")
    
    # Verify existing patterns still work
    print(f"\n✅ BACKWARD COMPATIBILITY:")
    core_patterns = analysis.get('core_float_patterns', {})
    ctx_count = core_patterns.get('ctx_markers', {}).get('count', 0)
    expand_count = extended_patterns.get('expand_on', {}).get('count', 0)
    
    print(f"  Standard ctx:: patterns: {ctx_count}")
    print(f"  Standard expandOn:: patterns: {expand_count}")
    
    return new_pattern_count > 0

if __name__ == "__main__":
    success = test_new_patterns()
    print(f"\n{'✅ SUCCESS' if success else '❌ FAILED'}: Enhanced pattern detection test")