#!/usr/bin/env python3
"""
ChromaDB Cleanup Planning Tool
Identifies cleanup opportunities without triggering numpy errors
"""

import chromadb
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict


def analyze_cleanup_opportunities():
    """Analyze ChromaDB for cleanup opportunities"""
    
    print('🧹 FLOAT ChromaDB Cleanup Analysis')
    print('=' * 50)
    
    try:
        # Connect to ChromaDB
        chroma_path = Path('/Users/evan/github/chroma-data')
        client = chromadb.PersistentClient(path=str(chroma_path))
        
        collections = client.list_collections()
        print(f'📊 Analyzing {len(collections)} collections...\n')
        
        cleanup_opportunities = {
            'duplicate_versions': [],
            'empty_collections': [],
            'oversized_collections': [],
            'redundant_collections': [],
            'old_collections': []
        }
        
        # Analyze each collection
        collection_info = []
        
        for collection in collections:
            try:
                count = collection.count()
                collection_info.append({
                    'name': collection.name,
                    'count': count
                })
                
                # Empty collections
                if count == 0:
                    cleanup_opportunities['empty_collections'].append(collection.name)
                
                # Oversized collections (>20k docs)
                if count > 20000:
                    cleanup_opportunities['oversized_collections'].append((collection.name, count))
                
            except Exception as e:
                print(f"  ⚠️  Error analyzing {collection.name}: {e}")
        
        # Find version duplicates (v1 vs v2)
        v1_collections = [c for c in collection_info if '_v1_' in c['name']]
        v2_collections = [c for c in collection_info if '_v2_' in c['name']]
        
        if v1_collections and v2_collections:
            cleanup_opportunities['duplicate_versions'] = v1_collections
        
        # Find potentially redundant collections
        collection_patterns = defaultdict(list)
        for coll in collection_info:
            # Extract base pattern
            base = coll['name'].replace('_v1', '').replace('_v2', '').replace('_legacy', '')
            collection_patterns[base].append(coll)
        
        for base, colls in collection_patterns.items():
            if len(colls) > 1:
                cleanup_opportunities['redundant_collections'].extend(colls)
        
        # Print cleanup report
        print('🎯 CLEANUP OPPORTUNITIES:\n')
        
        total_reclaimable = 0
        
        # 1. Version duplicates
        if cleanup_opportunities['duplicate_versions']:
            print('📦 OLD VERSION COLLECTIONS (v1 can likely be removed):')
            for coll in cleanup_opportunities['duplicate_versions']:
                print(f"  - {coll['name']}: {coll['count']:,} docs")
                total_reclaimable += coll['count']
        
        # 2. Empty collections
        if cleanup_opportunities['empty_collections']:
            print('\n🗑️  EMPTY COLLECTIONS (safe to remove):')
            for name in cleanup_opportunities['empty_collections']:
                print(f"  - {name}")
        
        # 3. Oversized collections
        if cleanup_opportunities['oversized_collections']:
            print('\n📈 OVERSIZED COLLECTIONS (consider archiving old data):')
            for name, count in cleanup_opportunities['oversized_collections']:
                print(f"  - {name}: {count:,} docs")
                if 'dropzone' in name:
                    print(f"    💡 Dropzone collection - archive processed files >30 days old")
        
        # 4. Specific recommendations
        print('\n💡 SPECIFIC RECOMMENDATIONS:')
        
        print('\n1. DROPZONE CLEANUP:')
        print('   - Archive documents older than 30 days')
        print('   - Remove duplicate float_id entries')
        print('   - Clean up .log, .tmp, .cache files')
        
        print('\n2. TRIPARTITE CLEANUP:')
        print('   - Remove v1 collections if v2 is stable')
        print('   - Consolidate similar collections')
        
        print('\n3. LEGACY CLEANUP:')
        legacy_colls = [c['name'] for c in collection_info if 'legacy' in c['name']]
        if legacy_colls:
            print(f'   - Found {len(legacy_colls)} legacy collections')
            for coll in legacy_colls[:5]:
                print(f'     - {coll}')
        
        # Estimate space savings
        print(f'\n💾 ESTIMATED CLEANUP IMPACT:')
        print(f'   - Documents reclaimable: ~{total_reclaimable:,}')
        print(f'   - Estimated space savings: ~{total_reclaimable * 4000 / 1024 / 1024:.0f} MB')
        
        # Create cleanup script
        print('\n📝 CLEANUP SCRIPT COMMANDS:')
        print('   # Remove empty collections')
        for name in cleanup_opportunities['empty_collections'][:3]:
            print(f'   client.delete_collection("{name}")')
        
        print('\n   # Archive old dropzone data')
        print('   # TODO: Implement date-based archiving for dropzone')
        
        return cleanup_opportunities
        
    except Exception as e:
        print(f'❌ Cleanup Analysis Failed: {e}')
        return None


def create_cleanup_issue():
    """Create GitHub issue for ChromaDB cleanup"""
    
    issue_body = """## Problem
ChromaDB has grown to 5.74 GB with 134,045 documents across 53 collections. Performance is degraded with >1 second query times.

## Cleanup Opportunities Identified

### 1. Dropzone Comprehensive (10,418 docs)
- Archive documents >30 days old
- Remove duplicate float_id entries  
- Clean up temporary file types (.log, .tmp, .cache)
- Split oversized documents (>50KB)

### 2. Version Duplicates
- Remove v1 tripartite collections if v2 is stable
- Clean up legacy collections

### 3. Empty Collections
- Several collections with 0 documents can be safely removed

### 4. Performance Optimization
- Current query time: ~1.1 seconds average
- Target query time: <0.5 seconds
- Consider collection consolidation

## Expected Behavior
- Reduced database size (<2GB target)
- Improved query performance (<0.5s)
- Cleaner collection structure
- Automated cleanup process for future

## Implementation Tasks
- [ ] Create backup of current ChromaDB
- [ ] Implement date-based archiving for dropzone
- [ ] Remove empty collections
- [ ] Consolidate v1/v2 duplicates
- [ ] Clean up temporary file types
- [ ] Add periodic cleanup to daemon
- [ ] Document cleanup procedures

## Priority
Medium - System is functional but performance is degraded

## Philosophy
"Rot vs cannon" - Archive old data rather than keeping everything forever. Let information naturally decay unless explicitly preserved.
"""
    
    print("\n📋 GITHUB ISSUE CONTENT:")
    print("-" * 50)
    print(issue_body)
    print("-" * 50)
    print("\nRun this command to create the issue:")
    print('gh issue create --title "ChromaDB cleanup needed - 5.74GB database causing performance issues" --body "..." --label "enhancement,performance"')


if __name__ == "__main__":
    # Run cleanup analysis
    cleanup_opportunities = analyze_cleanup_opportunities()
    
    # Show how to create GitHub issue
    print("\n")
    create_cleanup_issue()