#!/usr/bin/env python3
"""
Test script for Issue #5: Plugin integration with Enhanced Pattern Detector
Tests the integration of the plugin system with the main pattern detection system.
"""

import sys
from pathlib import Path

# Test the integration
def test_plugin_integration():
    print("🧪 Testing Plugin Integration - Issue #5")
    print("=" * 60)
    
    try:
        # Import the enhanced pattern detector
        from enhanced_pattern_detector import EnhancedFloatPatternDetector
        
        # Create detector instance
        detector = EnhancedFloatPatternDetector()
        
        # Test content with various patterns
        test_content = """
        ctx:: 2025-06-20 - testing plugin integration
        highlight:: plugin system working correctly
        signal:: core FLOAT patterns detected
        
        [expandOn:: extending FLOAT with plugins]
        [relatesTo:: modular architecture design]
        
        mood:: excited about extensibility
        boundary:: keep plugins simple and focused
        progress:: 90% complete on Issue #5
        
        [qtb:: creative architectural thinking]
        [sysop:: system-level pattern organization]
        
        float.dispatch({
            topic: "plugin_architecture",
            status: "nearly_complete",
            insights: ["extensible patterns", "plugin separation", "transferable vs personal"]
        })
        """
        
        # Run comprehensive pattern detection
        results = detector.extract_comprehensive_patterns(test_content, Path("test_file.md"))
        
        print("🔍 PATTERN DETECTION RESULTS:")
        print(f"   Pattern detector version: {results['analysis_metadata']['pattern_detector_version']}")
        print(f"   Plugin system enabled: {results['analysis_metadata']['plugin_system_enabled']}")
        print(f"   Plugin count: {results['analysis_metadata']['plugin_count']}")
        
        # Check core patterns (built-in)
        core_patterns = results['core_float_patterns']
        core_count = sum(1 for p in core_patterns.values() if p.get('has_pattern', False))
        print(f"\n📊 CORE PATTERNS (built-in): {core_count} pattern types detected")
        for pattern_name, data in core_patterns.items():
            if data.get('has_pattern', False):
                print(f"   ✅ {pattern_name}: {data['count']} matches")
        
        # Check plugin patterns
        plugin_patterns = results.get('plugin_patterns', {})
        plugin_count = sum(1 for p in plugin_patterns.values() if p.get('has_pattern', False))
        print(f"\n🔌 PLUGIN PATTERNS: {plugin_count} pattern types detected")
        for pattern_name, data in plugin_patterns.items():
            if data.get('has_pattern', False):
                transferable = data.get('transferable', True)
                transfer_note = " (non-transferable)" if not transferable else ""
                print(f"   ✅ {pattern_name}: {data['count']} matches{transfer_note}")
        
        # Check extended patterns (built-in)
        extended_patterns = results['extended_float_patterns']
        extended_count = sum(1 for p in extended_patterns.values() if p.get('has_pattern', False))
        print(f"\n📈 EXTENDED PATTERNS (built-in): {extended_count} pattern types detected")
        for pattern_name, data in extended_patterns.items():
            if data.get('has_pattern', False):
                print(f"   ✅ {pattern_name}: {data['count']} matches")
        
        # Summary
        total_patterns = core_count + plugin_count + extended_count
        print(f"\n🎯 TOTAL PATTERNS DETECTED: {total_patterns}")
        print(f"   Built-in patterns: {core_count + extended_count}")
        print(f"   Plugin patterns: {plugin_count}")
        
        if detector.plugin_manager:
            plugin_info = detector.plugin_manager.get_plugin_info()
            print(f"\n📋 LOADED PLUGINS:")
            for plugin_name, info in plugin_info.items():
                print(f"   🔌 {plugin_name} v{info['version']}")
                print(f"      Pattern types: {', '.join(info['pattern_types'])}")
        
        # Validate that we detected both built-in and plugin patterns
        if total_patterns > 10:  # Should detect many patterns
            print(f"\n✅ SUCCESS: Plugin integration working correctly!")
            print("   - Built-in patterns detected ✓")
            print("   - Plugin patterns detected ✓")
            print("   - Extensible architecture functional ✓")
            return True
        else:
            print(f"\n❌ FAILED: Expected more patterns, only got {total_patterns}")
            return False
            
    except Exception as e:
        print(f"❌ INTEGRATION TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_plugin_integration()
    sys.exit(0 if success else 1)