#!/usr/bin/env python3
"""
Debug why boundary:: pattern isn't being detected in real content
"""

import re

# Extract the actual line from the file
test_line = "- boundary:: let it drift"
full_context = """
## break for real real 
- ctx:: 2025-06-18 - 4:22pm 

- boundary:: let it drift
	- it's in the logs
"""

print("Debugging boundary:: pattern detection...")
print("=" * 50)
print(f"Test line: '{test_line}'")
print(f"Full context:\n{full_context}")

# Test different regex patterns
patterns = {
    'original': r'^boundary::\s*(.+)$',
    'with_indent': r'^\s*boundary::\s*(.+)$', 
    'with_bullet': r'^\s*-\s*boundary::\s*(.+)$',
    'anywhere': r'boundary::\s*([^\n]+)',
}

for name, pattern in patterns.items():
    matches = re.findall(pattern, full_context, re.MULTILINE | re.IGNORECASE)
    print(f"{name:15}: {len(matches)} matches - {matches}")

print("\n" + "=" * 50)
print("Testing enhanced pattern detector...")

from enhanced_pattern_detector import EnhancedFloatPatternDetector

detector = EnhancedFloatPatternDetector()
analysis = detector.extract_comprehensive_patterns(full_context)

extended_patterns = analysis.get('extended_float_patterns', {})
boundary_data = extended_patterns.get('line_boundary', {})
print(f"line_boundary detection: {boundary_data}")

generic_data = extended_patterns.get('line_generic', {})
print(f"line_generic detection: {generic_data}")