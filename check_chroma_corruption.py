#!/usr/bin/env python3
"""
ChromaDB Corruption and Data Integrity Check
Specifically checks for corrupted data and analyzes bloated collections
"""

import chromadb
from pathlib import Path
import time
import json
import random
from collections import defaultdict


def check_collection_integrity(collection, sample_size=100):
    """Check a collection for data corruption issues"""
    
    issues = {
        'empty_documents': 0,
        'missing_ids': 0,
        'duplicate_ids': set(),
        'malformed_metadata': 0,
        'oversized_documents': 0,
        'null_embeddings': 0,
        'query_failures': 0,
        'total_checked': 0
    }
    
    try:
        # Get total count
        total_count = collection.count()
        
        # For large collections, sample random documents
        if total_count > sample_size:
            print(f"    Sampling {sample_size} of {total_count:,} documents...")
            
            # Try to get a random sample
            try:
                # Get all documents (limited sample)
                results = collection.get(
                    limit=min(sample_size * 2, 1000),  # Get more than needed for random sampling
                    include=['documents', 'metadatas', 'embeddings']
                )
                
                # Random sample from results
                if results['ids']:
                    sample_indices = random.sample(
                        range(len(results['ids'])), 
                        min(sample_size, len(results['ids']))
                    )
                else:
                    sample_indices = []
                    
            except Exception as e:
                print(f"    ⚠️  Failed to get sample: {e}")
                issues['query_failures'] += 1
                return issues
        else:
            # Get all documents for small collections
            try:
                results = collection.get(include=['documents', 'metadatas', 'embeddings'])
                sample_indices = range(len(results['ids']))
            except Exception as e:
                print(f"    ⚠️  Failed to get documents: {e}")
                issues['query_failures'] += 1
                return issues
        
        # Check sampled documents
        seen_ids = set()
        
        for idx in sample_indices:
            issues['total_checked'] += 1
            
            try:
                doc_id = results['ids'][idx] if idx < len(results['ids']) else None
                document = results['documents'][idx] if idx < len(results['documents']) else None
                metadata = results['metadatas'][idx] if idx < len(results['metadatas']) else None
                embedding = results['embeddings'][idx] if results['embeddings'] and idx < len(results['embeddings']) else None
                
                # Check for missing IDs
                if not doc_id:
                    issues['missing_ids'] += 1
                    continue
                
                # Check for duplicate IDs
                if doc_id in seen_ids:
                    issues['duplicate_ids'].add(doc_id)
                seen_ids.add(doc_id)
                
                # Check for empty documents
                if not document or (isinstance(document, str) and len(document.strip()) == 0):
                    issues['empty_documents'] += 1
                
                # Check for oversized documents
                if document and isinstance(document, str) and len(document) > 100000:  # 100KB
                    issues['oversized_documents'] += 1
                
                # Check for malformed metadata
                if metadata:
                    try:
                        # Try to serialize metadata to check if it's valid
                        json.dumps(metadata)
                    except:
                        issues['malformed_metadata'] += 1
                
                # Check for null embeddings (if included)
                if embedding is not None and all(v == 0 for v in embedding):
                    issues['null_embeddings'] += 1
                    
            except Exception as e:
                print(f"    ⚠️  Error checking document {idx}: {e}")
                issues['query_failures'] += 1
        
        # Test query functionality
        try:
            test_results = collection.query(
                query_texts=["test query"],
                n_results=1
            )
            if not test_results or not test_results.get('ids'):
                issues['query_failures'] += 1
        except Exception as e:
            print(f"    ⚠️  Query test failed: {e}")
            issues['query_failures'] += 1
        
    except Exception as e:
        print(f"    ❌ Collection check failed: {e}")
        issues['query_failures'] += 999  # Major failure
    
    return issues


def analyze_dropzone_comprehensive(client):
    """Detailed analysis of the dropzone comprehensive collection"""
    
    print("\n🔍 ANALYZING DROPZONE COMPREHENSIVE COLLECTION")
    print("=" * 50)
    
    try:
        collection = client.get_collection("float_dropzone_comprehensive")
        
        # Get basic stats
        count = collection.count()
        print(f"📊 Total documents: {count:,}")
        
        # Sample documents to analyze patterns
        print("\n📋 Document Analysis (sampling 500 documents)...")
        
        sample_results = collection.get(
            limit=500,
            include=['documents', 'metadatas']
        )
        
        # Analyze document sizes
        doc_sizes = []
        metadata_stats = defaultdict(int)
        file_types = defaultdict(int)
        float_ids = defaultdict(int)
        
        for i, (doc_id, doc, metadata) in enumerate(zip(
            sample_results['ids'], 
            sample_results['documents'], 
            sample_results['metadatas']
        )):
            if doc:
                doc_sizes.append(len(doc))
            
            if metadata:
                # Track file types
                if 'filename' in metadata:
                    ext = Path(metadata['filename']).suffix
                    file_types[ext] += 1
                
                # Track float_id patterns (potential duplicates)
                if 'float_id' in metadata:
                    float_ids[metadata['float_id']] += 1
                
                # Track metadata keys
                for key in metadata.keys():
                    metadata_stats[key] += 1
        
        # Document size analysis
        if doc_sizes:
            avg_size = sum(doc_sizes) / len(doc_sizes)
            max_size = max(doc_sizes)
            min_size = min(doc_sizes)
            
            print(f"\n📏 Document Size Analysis:")
            print(f"  Average: {avg_size:,.0f} chars")
            print(f"  Largest: {max_size:,} chars")
            print(f"  Smallest: {min_size:,} chars")
            
            # Find bloated documents
            bloated = [s for s in doc_sizes if s > 50000]  # >50KB
            if bloated:
                print(f"  ⚠️  Bloated documents (>50KB): {len(bloated)} ({len(bloated)/len(doc_sizes)*100:.1f}%)")
        
        # File type distribution
        print(f"\n📁 File Type Distribution:")
        for ext, count in sorted(file_types.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"  {ext or 'no extension':15} {count:4d} files")
        
        # Check for duplicate float_ids
        duplicates = {fid: cnt for fid, cnt in float_ids.items() if cnt > 1}
        if duplicates:
            print(f"\n⚠️  DUPLICATE FLOAT IDs FOUND:")
            for fid, cnt in sorted(duplicates.items(), key=lambda x: x[1], reverse=True)[:10]:
                print(f"  {fid}: {cnt} occurrences")
        
        # Metadata consistency
        print(f"\n🏷️  Metadata Fields (from sample):")
        for field, count in sorted(metadata_stats.items(), key=lambda x: x[1], reverse=True):
            consistency = (count / len(sample_results['ids'])) * 100
            print(f"  {field:20} {consistency:5.1f}% consistency")
        
        # Check for potential cleanup opportunities
        print(f"\n🧹 CLEANUP OPPORTUNITIES:")
        
        # Old data check (if timestamps available)
        old_count = 0
        for metadata in sample_results['metadatas']:
            if metadata and 'created_at' in metadata:
                try:
                    # Check if older than 30 days
                    from datetime import datetime, timedelta
                    created = datetime.fromisoformat(metadata['created_at'].replace('Z', '+00:00'))
                    if created < datetime.now(created.tzinfo) - timedelta(days=30):
                        old_count += 1
                except:
                    pass
        
        if old_count > 0:
            old_pct = (old_count / len(sample_results['ids'])) * 100
            estimated_old = int(count * old_pct / 100)
            print(f"  📅 Documents >30 days old: ~{estimated_old:,} ({old_pct:.1f}% of total)")
        
        # File type cleanup potential
        cleanable_types = ['.log', '.tmp', '.cache', '.bak']
        cleanable_count = sum(file_types.get(ext, 0) for ext in cleanable_types)
        if cleanable_count > 0:
            print(f"  🗑️  Potentially cleanable files: {cleanable_count} (logs, temp, cache, backups)")
        
        # Bloated documents
        if doc_sizes and any(s > 50000 for s in doc_sizes):
            bloat_pct = (len([s for s in doc_sizes if s > 50000]) / len(doc_sizes)) * 100
            estimated_bloated = int(count * bloat_pct / 100)
            print(f"  📈 Bloated documents (>50KB): ~{estimated_bloated:,} ({bloat_pct:.1f}% of total)")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to analyze dropzone comprehensive: {e}")
        return False


def main():
    """Main corruption check"""
    
    print('🔍 FLOAT ChromaDB Corruption & Integrity Check')
    print('=' * 50)
    
    try:
        # Connect to ChromaDB
        chroma_path = Path('/Users/evan/github/chroma-data')
        client = chromadb.PersistentClient(path=str(chroma_path))
        
        # Get all collections
        collections = client.list_collections()
        print(f'📊 Checking {len(collections)} collections for corruption...\n')
        
        # Track overall issues
        corrupted_collections = []
        
        # Priority collections to check thoroughly
        priority_collections = [
            'float_dropzone_comprehensive',
            'float_tripartite_v2_framework',
            'float_tripartite_v2_metaphor',
            'float_tripartite_v2_concept'
        ]
        
        # Check each collection
        for collection in collections:
            collection_name = collection.name
            is_priority = collection_name in priority_collections
            
            if is_priority:
                print(f'🔍 Checking {collection_name} (PRIORITY - thorough check)...')
                sample_size = 500  # Larger sample for priority collections
            else:
                print(f'🔍 Checking {collection_name}...')
                sample_size = 50   # Smaller sample for others
            
            issues = check_collection_integrity(collection, sample_size)
            
            # Report issues
            has_issues = False
            issue_report = []
            
            if issues['empty_documents'] > 0:
                issue_report.append(f"empty docs: {issues['empty_documents']}")
                has_issues = True
            
            if issues['duplicate_ids']:
                issue_report.append(f"duplicate IDs: {len(issues['duplicate_ids'])}")
                has_issues = True
            
            if issues['malformed_metadata'] > 0:
                issue_report.append(f"bad metadata: {issues['malformed_metadata']}")
                has_issues = True
            
            if issues['oversized_documents'] > 0:
                issue_report.append(f"oversized: {issues['oversized_documents']}")
                has_issues = True
            
            if issues['query_failures'] > 0:
                issue_report.append(f"query failures: {issues['query_failures']}")
                has_issues = True
            
            if has_issues:
                print(f"  ⚠️  Issues found: {', '.join(issue_report)}")
                print(f"     (checked {issues['total_checked']} documents)")
                corrupted_collections.append((collection_name, issues))
            else:
                print(f"  ✅ No issues found (checked {issues['total_checked']} documents)")
        
        # Detailed dropzone analysis
        analyze_dropzone_comprehensive(client)
        
        # Summary
        print("\n" + "=" * 50)
        print("📊 CORRUPTION CHECK SUMMARY:")
        
        if corrupted_collections:
            print(f"\n⚠️  Collections with issues: {len(corrupted_collections)}")
            for name, issues in corrupted_collections:
                print(f"\n  {name}:")
                if issues['empty_documents'] > 0:
                    print(f"    - {issues['empty_documents']} empty documents")
                if issues['duplicate_ids']:
                    print(f"    - {len(issues['duplicate_ids'])} duplicate IDs")
                if issues['malformed_metadata'] > 0:
                    print(f"    - {issues['malformed_metadata']} malformed metadata entries")
                if issues['oversized_documents'] > 0:
                    print(f"    - {issues['oversized_documents']} oversized documents")
        else:
            print("\n✅ No corruption detected in any collection!")
        
        print("\n💡 RECOMMENDATIONS:")
        print("  1. Clean up dropzone comprehensive - it's quite bloated")
        print("  2. Remove duplicate entries where found")
        print("  3. Consider archiving old data (>30 days)")
        print("  4. Split oversized documents into smaller chunks")
        print("  5. Clean up temporary file types (.log, .tmp, etc.)")
        
    except Exception as e:
        print(f'❌ Corruption Check Failed: {e}')
        return False


if __name__ == "__main__":
    main()