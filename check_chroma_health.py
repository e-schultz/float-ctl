#!/usr/bin/env python3
"""
ChromaDB Health Check for FLOAT System
Comprehensive health assessment after heavy usage
"""

import chromadb
from pathlib import Path
import time
import sys


def check_chroma_health():
    """Comprehensive ChromaDB health check"""
    
    print('🔍 FLOAT ChromaDB Health Check')
    print('=' * 50)
    
    try:
        # Check ChromaDB path
        chroma_path = Path('/Users/evan/github/chroma-data')
        print(f'📁 ChromaDB Path: {chroma_path}')
        print(f'📁 Path exists: {chroma_path.exists()}')
        
        if not chroma_path.exists():
            print('❌ ChromaDB directory not found!')
            return False
        
        # Calculate disk usage
        total_size = sum(f.stat().st_size for f in chroma_path.rglob('*') if f.is_file())
        size_mb = total_size / 1024 / 1024
        size_gb = size_mb / 1024
        
        print(f'💾 Disk usage: {size_mb:.1f} MB ({size_gb:.2f} GB)')
        
        # Count files
        file_count = len([f for f in chroma_path.rglob('*') if f.is_file()])
        dir_count = len([d for d in chroma_path.rglob('*') if d.is_dir()])
        print(f'📄 Total files: {file_count:,}')
        print(f'📁 Total directories: {dir_count:,}')
        
        print()
        
        # Connect to ChromaDB
        print('🔌 Connecting to ChromaDB...')
        start_time = time.time()
        client = chromadb.PersistentClient(path=str(chroma_path))
        connect_time = time.time() - start_time
        print(f'⚡ Connection time: {connect_time:.3f}s')
        
        # List collections
        collections = client.list_collections()
        print(f'📊 Total collections: {len(collections)}')
        
        if len(collections) == 0:
            print('⚠️  No collections found - database may be empty')
            return True
        
        print()
        print('📋 COLLECTION ANALYSIS:')
        
        total_docs = 0
        collection_data = []
        slow_collections = []
        
        # Analyze each collection
        for collection in collections:
            try:
                print(f'  🔍 Analyzing {collection.name}...', end=' ')
                
                start_time = time.time()
                count = collection.count()
                count_time = time.time() - start_time
                
                # Test a simple query for responsiveness
                start_time = time.time()
                try:
                    collection.query(query_texts=['test'], n_results=1)
                    query_time = time.time() - start_time
                except:
                    query_time = -1  # Query failed
                
                total_docs += count
                collection_data.append({
                    'name': collection.name,
                    'count': count,
                    'count_time': count_time,
                    'query_time': query_time
                })
                
                # Track slow collections
                if count_time > 0.5 or query_time > 0.5:
                    slow_collections.append(collection.name)
                
                print(f'{count:,} docs ({count_time:.3f}s count, {query_time:.3f}s query)')
                
            except Exception as e:
                print(f'❌ Error: {e}')
                collection_data.append({
                    'name': collection.name,
                    'count': 0,
                    'count_time': -1,
                    'query_time': -1,
                    'error': str(e)
                })
        
        # Sort by document count
        collection_data.sort(key=lambda x: x['count'], reverse=True)
        
        print()
        print('📈 COLLECTION SUMMARY (Top 10):')
        for i, data in enumerate(collection_data[:10]):
            if 'error' in data:
                print(f'  {i+1:2d}. ❌ {data["name"]:<35} ERROR: {data["error"]}')
            else:
                count_str = f'{data["count"]:,}'
                times = f'({data["count_time"]:.2f}s/{data["query_time"]:.2f}s)'
                print(f'  {i+1:2d}. 📚 {data["name"]:<35} {count_str:>8} docs {times}')
        
        print()
        print('🏥 HEALTH ASSESSMENT:')
        print(f'  📊 Total documents: {total_docs:,}')
        print(f'  📁 Total collections: {len(collections)}')
        print(f'  💾 Database size: {size_mb:.1f} MB')
        
        if collection_data:
            avg_count_time = sum(d['count_time'] for d in collection_data if d['count_time'] > 0) / len([d for d in collection_data if d['count_time'] > 0])
            avg_query_time = sum(d['query_time'] for d in collection_data if d['query_time'] > 0) / len([d for d in collection_data if d['query_time'] > 0])
            
            print(f'  ⚡ Avg count time: {avg_count_time:.3f}s')
            print(f'  ⚡ Avg query time: {avg_query_time:.3f}s')
        
        # Health status determination
        errors = [d for d in collection_data if 'error' in d]
        
        if len(errors) > 0:
            status = '❌ UNHEALTHY'
            message = f'{len(errors)} collections have errors'
        elif len(slow_collections) > len(collections) * 0.3:  # >30% slow
            status = '⚠️  DEGRADED'
            message = f'{len(slow_collections)} collections are slow'
        elif size_gb > 2:  # >2GB
            status = '⚠️  LARGE'
            message = f'Database is large ({size_gb:.1f} GB) - consider cleanup'
        elif total_docs > 50000:
            status = '✅ HEALTHY (HIGH VOLUME)'
            message = f'Performing well with {total_docs:,} documents'
        else:
            status = '✅ HEALTHY'
            message = f'All systems normal with {total_docs:,} documents'
        
        print(f'  🎯 Status: {status}')
        print(f'  💬 Message: {message}')
        
        # Recommendations
        print()
        print('💡 RECOMMENDATIONS:')
        
        if size_gb > 1:
            print('  🧹 Consider cleaning up old/unused collections')
        
        if len(slow_collections) > 0:
            print(f'  ⚡ {len(slow_collections)} collections are slow - consider optimization')
        
        if total_docs > 100000:
            print('  📊 High document count - monitor performance regularly')
        
        if len(errors) > 0:
            print('  🔧 Fix collection errors before continuing')
            for error_data in errors:
                print(f'     - {error_data["name"]}: {error_data["error"]}')
        
        print()
        print('✅ Health check complete!')
        
        return len(errors) == 0  # Healthy if no errors
        
    except Exception as e:
        print(f'❌ Health Check Failed: {e}')
        print()
        print('Possible issues:')
        print('  - ChromaDB not installed or accessible')
        print('  - Database corruption')
        print('  - Permission problems')
        print('  - Path configuration incorrect')
        return False


if __name__ == "__main__":
    success = check_chroma_health()
    sys.exit(0 if success else 1)