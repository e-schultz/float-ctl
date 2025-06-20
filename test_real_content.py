#!/usr/bin/env python3
"""
Test enhanced patterns with real content from operations dropzone
"""

from pathlib import Path
from enhanced_pattern_detector import EnhancedFloatPatternDetector

def test_with_real_content():
    """Test enhanced patterns with real dropzone content"""
    print("Testing enhanced patterns with real content from operations dropzone...")
    print("=" * 75)
    
    # Read a real file from operations dropzone
    dropzone_path = Path("/Users/evan/projects/float-workspace/operations/float-dropzone")
    daily_log = dropzone_path / "2025-06-18.md"
    
    if not daily_log.exists():
        print("❌ Real content file not found, using test content instead")
        return False
    
    with open(daily_log, 'r', encoding='utf-8') as f:
        real_content = f.read()
    
    print(f"📄 Analyzing: {daily_log.name}")
    print(f"📏 Content length: {len(real_content):,} characters")
    
    detector = EnhancedFloatPatternDetector()
    analysis = detector.extract_comprehensive_patterns(real_content)
    
    # Check for enhanced patterns
    extended_patterns = analysis.get('extended_float_patterns', {})
    
    print(f"\n🔍 ENHANCED PATTERNS FOUND:")
    enhanced_found = 0
    for pattern_name in ['inline_expand_on', 'inline_relates_to', 'line_mood', 
                        'line_soundtrack', 'line_body_check', 'line_boundary',
                        'line_progress', 'line_issue', 'line_generic']:
        
        if pattern_name in extended_patterns:
            pattern_data = extended_patterns[pattern_name]
            count = pattern_data.get('count', 0)
            if count > 0:
                enhanced_found += count
                print(f"  ✅ {pattern_name}: {count} matches")
                for match in pattern_data.get('matches', [])[:3]:  # Show first 3
                    if isinstance(match, tuple):
                        print(f"     - {match[0]}: {match[1]}")
                    else:
                        print(f"     - {match}")
                if len(pattern_data.get('matches', [])) > 3:
                    print(f"     ... and {len(pattern_data.get('matches', [])) - 3} more")
    
    # Check traditional patterns still work
    core_patterns = analysis.get('core_float_patterns', {})
    ctx_count = core_patterns.get('ctx_markers', {}).get('count', 0)
    
    traditional_patterns = extended_patterns.get('expand_on', {}).get('count', 0)
    
    print(f"\n📊 SUMMARY:")
    print(f"  Enhanced patterns found: {enhanced_found}")
    print(f"  Traditional ctx:: patterns: {ctx_count}")
    print(f"  Traditional expandOn:: patterns: {traditional_patterns}")
    print(f"  Total pattern density: {analysis.get('signal_analysis', {}).get('signal_density', 0):.2%}")
    
    return enhanced_found > 0

if __name__ == "__main__":
    success = test_with_real_content()
    print(f"\n{'✅ SUCCESS' if success else '❌ FAILED'}: Real content pattern detection test")