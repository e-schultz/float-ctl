#!/usr/bin/env python3
"""
Test script to verify our deduplication fixes for issues #1 and #2
"""

import re
from pathlib import Path

# Test content with duplicate dates and conversation links
test_content = """
# Test Document

Date references that should be deduplicated:
2025-06-19 was a good day
2025-06-20 is today
2025-06-19 appears again
2025-06-20 also appears again

Conversation links with artifacts:
- [Claude.AI](https://claude.ai/chat/5a0e9b31-ed68-44d8-ab66-d8a23b77186c\n\t-)
- [ChatGPT](https://chatgpt.com/c/67f73d06-9d04-8010-b080-8969145881e2\n\t-)
- [Claude.AI](https://claude.ai/chat/5a0e9b31-ed68-44d8-ab66-d8a23b77186c)

Collection names that should NOT match as conversation IDs:
conversations_active
conversations_legacy_v1
conversation_analysis
conversation_chunks
"""

def test_temporal_links_deduplication():
    """Test the fixed temporal links deduplication"""
    print("Testing temporal links deduplication...")
    
    # Simulate the fixed _find_temporal_links method
    date_pattern = re.compile(r'\b(\d{4}-\d{2}-\d{2})\b')
    
    # OLD WAY (creates duplicates)
    old_dates = date_pattern.findall(test_content)
    old_temporal_links = []
    for date in old_dates:
        old_temporal_links.append({
            'type': 'date_reference',
            'date': date,
            'target': f"FLOAT.logs/{date}.md"
        })
    
    # NEW WAY (deduplicated)
    new_dates = set(date_pattern.findall(test_content))
    new_temporal_links = []
    for date in sorted(new_dates):
        new_temporal_links.append({
            'type': 'date_reference',
            'date': date,
            'target': f"FLOAT.logs/{date}.md"
        })
    
    print(f"Old method found {len(old_temporal_links)} temporal links:")
    for link in old_temporal_links:
        print(f"  - [[{link['target']}]] ({link['date']})")
    
    print(f"\nNew method found {len(new_temporal_links)} temporal links:")
    for link in new_temporal_links:
        print(f"  - [[{link['target']}]] ({link['date']})")
    
    print(f"\nReduction: {len(old_temporal_links) - len(new_temporal_links)} duplicate links removed\n")

def test_conversation_links_cleaning():
    """Test the fixed conversation links cleaning"""
    print("Testing conversation links cleaning...")
    
    url_pattern = re.compile(r'https?://[^\s<>"]+')
    conversation_id_pattern = re.compile(r'conversation[_-]([a-f0-9]{8,})', re.IGNORECASE)
    
    # Extract URLs and clean them
    urls = url_pattern.findall(test_content)
    clean_links = []
    seen_urls = set()
    
    for url in urls:
        # Clean URL of any whitespace/newline artifacts
        clean_url = url.strip().replace('\n', '').replace('\t', '').replace(' ', '')
        
        if clean_url in seen_urls:
            continue
            
        if any(platform in clean_url for platform in ['claude.ai', 'chatgpt.com', 'chat.openai.com']):
            # Determine platform and generate better title
            if 'claude.ai' in clean_url:
                platform = 'claude_ai'
                title = 'Claude.AI Conversation'
            elif 'chatgpt.com' in clean_url:
                platform = 'chatgpt'
                title = 'ChatGPT Conversation'
            else:
                platform = 'unknown'
                title = 'AI Conversation'
            
            # Extract conversation ID from URL for better titles
            conv_id_match = re.search(r'/chat/([a-zA-Z0-9-]+)', clean_url)
            if conv_id_match:
                conv_id = conv_id_match.group(1)[:8]  # First 8 chars
                title += f" ({conv_id})"
            
            clean_links.append({
                'type': 'conversation_url',
                'url': clean_url,
                'platform': platform,
                'title': title
            })
            seen_urls.add(clean_url)
    
    print("Original URLs found:")
    for url in urls:
        print(f"  {url}")
    
    print("\nCleaned conversation links:")
    for link in clean_links:
        print(f"  - [{link['title']}]({link['url']})")
    
    # Test conversation ID pattern (should not match collection names)
    conv_ids = conversation_id_pattern.findall(test_content)
    print(f"\nConversation IDs found: {conv_ids}")
    print("(Should be empty - collection names should not match)\n")

if __name__ == "__main__":
    test_temporal_links_deduplication()
    test_conversation_links_cleaning()
    print("✅ Deduplication tests completed!")