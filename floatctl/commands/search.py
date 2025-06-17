"""
Enhanced search commands with FloatQL support

Provides both basic text search and advanced FloatQL pattern search.
"""

import click
import json
from typing import List, Dict, Any
from floatctl.floatql.parser import FloatQLParser
from floatctl.floatql.translator import QueryTranslator


def search_with_floatql(lf1m, query: str, collections: List[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Enhanced search that detects and processes FloatQL syntax
    
    Falls back to basic search if no FloatQL patterns detected.
    """
    parser = FloatQLParser()
    
    # Check if this is a FloatQL query
    if parser.is_floatql_query(query):
        return _execute_floatql_search(lf1m, parser, query, collections, limit)
    else:
        # Basic text search
        return lf1m.search_collections(query, collections, limit)


def _execute_floatql_search(lf1m, parser: FloatQLParser, query: str, collections: List[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
    """Execute FloatQL-aware search"""
    
    # Parse the query
    parsed = parser.parse(query)
    
    # Get suggested collections if none specified
    if collections is None:
        collections = parser.get_suggested_collections(parsed)
    
    # Create query translator
    translator = QueryTranslator(lf1m.chroma_data_path)
    chroma_query = translator.translate_to_chroma_query(parsed)
    
    # Execute search with metadata filters
    results = []
    
    try:
        import chromadb
        client = chromadb.PersistentClient(path=lf1m.chroma_data_path)
        
        for collection_name in collections:
            try:
                collection = client.get_collection(collection_name)
                
                # Build query parameters
                query_params = {
                    'query_texts': chroma_query['query_texts'],
                    'n_results': limit
                }
                
                # Add metadata filters if present
                if chroma_query['where']:
                    query_params['where'] = chroma_query['where']
                
                # Execute query
                search_results = collection.query(**query_params)
                
                # Format results
                for i, doc in enumerate(search_results['documents'][0]):
                    results.append({
                        'collection': collection_name,
                        'document': doc,
                        'metadata': search_results['metadatas'][0][i] if search_results['metadatas'][0] else {},
                        'distance': search_results['distances'][0][i] if search_results['distances'][0] else None,
                        'id': search_results['ids'][0][i] if search_results['ids'][0] else None,
                        'floatql_match': _analyze_floatql_match(doc, parsed)
                    })
                    
            except Exception as e:
                lf1m.logger.warning(f"Error searching collection {collection_name}: {e}")
                continue
        
        # Sort by FloatQL relevance, then by distance
        results.sort(key=lambda x: (
            -x['floatql_match']['score'],  # Higher FloatQL scores first
            x['distance'] or float('inf')   # Then by similarity distance
        ))
        
        return results[:limit]
        
    except Exception as e:
        lf1m.logger.error(f"FloatQL search error: {e}")
        # Fallback to basic search
        basic_query = parser.extract_search_terms(parsed)
        return lf1m.search_collections(basic_query, collections, limit)


def _analyze_floatql_match(document: str, parsed: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze how well a document matches FloatQL patterns"""
    score = 0
    matches = []
    
    # Score FLOAT pattern matches
    for pattern in parsed['float_patterns']:
        if f"{pattern}::" in document:
            score += 10
            matches.append(f"float:{pattern}")
    
    # Score persona pattern matches
    for pattern in parsed['persona_patterns']:
        if f"[{pattern}::]" in document:
            score += 8
            matches.append(f"persona:{pattern}")
    
    # Score bridge ID matches
    for bridge_id in parsed['bridge_ids']:
        if bridge_id in document:
            score += 15  # Bridge matches are very important
            matches.append(f"bridge:{bridge_id}")
    
    # Score text term matches
    for term in parsed['text_terms']:
        if term.lower() in document.lower():
            score += 1
            matches.append(f"text:{term}")
    
    return {
        'score': score,
        'matches': matches,
        'total_patterns': len(parsed['float_patterns'] + parsed['persona_patterns'] + parsed['bridge_ids'])
    }


@click.command()
@click.argument('query')
@click.option('--collections', '-c', help='Comma-separated list of collections to search')
@click.option('--limit', '-l', default=10, help='Maximum number of results')
@click.option('--floatql-only', is_flag=True, help='Force FloatQL parsing even for simple queries')
@click.option('--explain', is_flag=True, help='Show how the query was parsed and executed')
@click.pass_context
def query(ctx, query, collections, limit, floatql_only, explain):
    """Advanced search with FloatQL pattern support
    
    Supports FLOAT :: notation patterns:
    
    \b
    Basic patterns:
      ctx::meeting           - Context markers
      highlight::important   - Highlighted content  
      signal::key           - Signal markers
    
    \b
    Persona annotations:
      [sysop::]             - System operator notes
      [karen::]             - Editorial conscience  
      [qtb::]               - Queer Techno Bard
    
    \b
    Temporal filters:
      created:today         - Created today
      modified:yesterday    - Modified yesterday  
      date:2025-06-13      - Specific date
    
    \b  
    Bridge references:
      bridge::CB-20250611-1510-N1CK  - Specific bridge
    
    \b
    Type filters:
      type:log              - Daily logs
      type:conversation     - Conversations
    
    \b
    Examples:
      floatctl query "ctx::meeting nick::"
      floatctl query "[karen::] boundaries as care"  
      floatctl query "bridge::CB-20250611-1510-N1CK --follow"
      floatctl query "redux:: created:today"
    """
    from floatctl.core.lf1m import LF1M
    
    try:
        lf1m = LF1M(config_path=ctx.obj.get('config_path'))
        
        # Parse collections list
        collection_list = None
        if collections:
            collection_list = [c.strip() for c in collections.split(',')]
        
        click.echo(f"Searching for: '{query}'")
        
        # Show parsing if explain mode
        if explain or floatql_only:
            parser = FloatQLParser()
            parsed = parser.parse(query)
            click.echo(f"\nParsed query:")
            click.echo(f"  Text terms: {parsed['text_terms']}")
            click.echo(f"  FLOAT patterns: {parsed['float_patterns']}")
            click.echo(f"  Persona patterns: {parsed['persona_patterns']}")
            click.echo(f"  Temporal filters: {parsed['temporal_filters']}")
            click.echo(f"  Type filters: {parsed['type_filters']}")
            click.echo(f"  Bridge IDs: {parsed['bridge_ids']}")
            if collection_list is None:
                suggested = parser.get_suggested_collections(parsed)
                click.echo(f"  Suggested collections: {suggested}")
            click.echo()
        
        # Execute search
        if floatql_only or FloatQLParser().is_floatql_query(query):
            results = search_with_floatql(lf1m, query, collection_list, limit)
        else:
            results = lf1m.search_collections(query, collection_list, limit)
        
        # Display results
        _display_query_results(results, explain)
        
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        if ctx.obj.get('verbose'):
            import traceback
            traceback.print_exc()


def _display_query_results(results: List[Dict[str, Any]], show_details: bool = False):
    """Display query results with FloatQL match information"""
    if not results:
        click.echo("No results found.")
        return
    
    click.echo(f"Found {len(results)} results:")
    
    for i, result in enumerate(results, 1):
        click.echo(f"\n{i}. Collection: {result['collection']}")
        
        # Show FloatQL match information if available
        if 'floatql_match' in result and show_details:
            match_info = result['floatql_match']
            click.echo(f"   FloatQL Score: {match_info['score']}")
            if match_info['matches']:
                click.echo(f"   Matches: {', '.join(match_info['matches'])}")
        
        if show_details:
            click.echo(f"   ID: {result.get('id', 'N/A')}")
            click.echo(f"   Distance: {result.get('distance', 'N/A')}")
            if result.get('metadata'):
                # Show key metadata fields
                metadata = result['metadata']
                if 'float_id' in metadata:
                    click.echo(f"   Float ID: {metadata['float_id']}")
                if 'conversation_date' in metadata:
                    click.echo(f"   Date: {metadata['conversation_date']}")
                if 'content_type' in metadata:
                    click.echo(f"   Type: {metadata['content_type']}")
        
        # Show content preview
        content = result['document']
        first_line = content.split('\n')[0] if content else "No content"
        if len(first_line) > 100:
            first_line = first_line[:97] + "..."
        click.echo(f"   {first_line}")


if __name__ == '__main__':
    query()