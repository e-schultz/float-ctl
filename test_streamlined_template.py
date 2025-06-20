#!/usr/bin/env python3
"""
Test script to compare verbose vs streamlined template output - Issue #4
"""

from float_dis_template_system import FloatDisGenerator
from streamlined_dis_template import StreamlinedFloatDisGenerator

# Mock data for testing
mock_file_metadata = {
    'filename': '2025-06-20-test-document.md',
    'relative_path': '2025-06-20-test-document.md',
    'extension': '.md',
    'size_bytes': 15430,
    'mime_type': 'text/plain',
    'file_type': 'Markdown document',
    'created_at': '2025-06-20T10:30:00',
    'modified_at': '2025-06-20T11:45:00'
}

mock_chroma_metadata = {
    'collection_name': 'float_tripartite_v2_concept',
    'chunk_count': 5,
    'total_chunks': 5,
    'chunk_ids': ['test_chunk_0', 'test_chunk_1', 'test_chunk_2'],
    'embedding_model': 'default',
    'storage_path': '/chroma/data',
    'chunking_strategy': 'content_aware'
}

mock_content_analysis = {
    'summary': 'A comprehensive test document demonstrating FLOAT pattern detection with various inline and line-level patterns for enhanced workflow tracking.',
    'word_count': 1847,
    'line_count': 89,
    'content_type': 'Markdown document',
    'detected_patterns': ['ctx::', 'boundary::', 'expandOn::'],
    'language': 'en',
    'encoding': 'utf-8',
    'has_ctx_markers': True,
    'has_highlights': True,
    'signal_density': 0.08
}

mock_enhanced_patterns = {
    'core_float_patterns': {
        'ctx_markers': {'count': 3, 'matches': ['test context 1', 'test context 2']},
        'highlight_markers': {'count': 2, 'matches': ['important insight']},
        'signal_markers': {'count': 1, 'matches': ['key signal']}
    },
    'extended_float_patterns': {
        'inline_expand_on': {'count': 2, 'matches': ['future research', 'integration options']},
        'inline_relates_to': {'count': 1, 'matches': ['productivity patterns']},
        'line_boundary': {'count': 1, 'matches': ['stay focused, test thoroughly']},
        'line_progress': {'count': 2, 'matches': ['75% complete', 'templates streamlined']},
        'line_mood': {'count': 1, 'matches': ['productive and focused']}
    },
    'signal_analysis': {
        'signal_density': 0.08,
        'total_patterns': 10
    }
}

def test_template_comparison():
    """Compare verbose vs streamlined template output."""
    print("Testing Template Streamlining (Issue #4)")
    print("=" * 60)
    
    float_id = "test_float_20250620_abc123"
    
    # Generate with original verbose template
    print("🏗️  ORIGINAL VERBOSE TEMPLATE:")
    verbose_generator = FloatDisGenerator()
    verbose_output = verbose_generator.generate_float_dis(
        mock_file_metadata, mock_chroma_metadata, mock_content_analysis, float_id
    )
    
    verbose_lines = len(verbose_output.split('\n'))
    verbose_chars = len(verbose_output)
    print(f"  Lines: {verbose_lines}")
    print(f"  Characters: {verbose_chars:,}")
    print(f"  Size: {verbose_chars / 1024:.1f} KB")
    
    # Generate with streamlined template
    print(f"\n🏠 STREAMLINED TEMPLATE:")
    streamlined_generator = StreamlinedFloatDisGenerator()
    streamlined_output = streamlined_generator.generate_float_dis(
        mock_file_metadata, mock_chroma_metadata, mock_content_analysis, 
        float_id, mock_enhanced_patterns
    )
    
    streamlined_lines = len(streamlined_output.split('\n'))
    streamlined_chars = len(streamlined_output)
    print(f"  Lines: {streamlined_lines}")
    print(f"  Characters: {streamlined_chars:,}")
    print(f"  Size: {streamlined_chars / 1024:.1f} KB")
    
    # Calculate reduction
    line_reduction = ((verbose_lines - streamlined_lines) / verbose_lines) * 100
    char_reduction = ((verbose_chars - streamlined_chars) / verbose_chars) * 100
    
    print(f"\n📊 REDUCTION ACHIEVED:")
    print(f"  Lines reduced: {line_reduction:.1f}% ({verbose_lines} → {streamlined_lines})")
    print(f"  Characters reduced: {char_reduction:.1f}% ({verbose_chars:,} → {streamlined_chars:,})")
    print(f"  File size reduced: {char_reduction:.1f}%")
    
    # Show sample output
    print(f"\n📄 STREAMLINED OUTPUT SAMPLE:")
    print("-" * 40)
    sample_lines = streamlined_output.split('\n')[:25]  # First 25 lines
    for i, line in enumerate(sample_lines, 1):
        print(f"{i:2d}: {line}")
    print("...")
    
    # Validate key information is preserved
    print(f"\n✅ VALIDATION:")
    has_float_id = float_id in streamlined_output
    has_filename = mock_file_metadata['filename'] in streamlined_output
    has_pattern_info = 'FLOAT Patterns' in streamlined_output
    has_templater = 'Templater' in streamlined_output
    
    print(f"  Float ID preserved: {'✅' if has_float_id else '❌'}")
    print(f"  Filename preserved: {'✅' if has_filename else '❌'}")
    print(f"  Pattern info included: {'✅' if has_pattern_info else '❌'}")
    print(f"  Templater integration: {'✅' if has_templater else '❌'}")
    
    success_criteria = [
        line_reduction > 50,  # At least 50% line reduction
        char_reduction > 40,  # At least 40% character reduction  
        has_float_id,         # Key metadata preserved
        has_filename,         # File info preserved
        has_pattern_info      # Pattern detection preserved
    ]
    
    success = all(success_criteria)
    
    print(f"\n{'✅ SUCCESS' if success else '❌ FAILED'}: Template streamlining test")
    print(f"Philosophy: {'Shacks not cathedrals' if success else 'Still too cathedral-like'}")
    
    return success

if __name__ == "__main__":
    test_template_comparison()