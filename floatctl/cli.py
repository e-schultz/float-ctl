"""
floatctl - FLOAT command-line interface

Main CLI entry point using Click framework.
Exposes lf1m daemon functionality as CLI commands.
"""

import click
import json
import sys
from pathlib import Path
from typing import List, Optional

from floatctl.core.lf1m import LF1M


@click.group()
@click.option('--config', '-c', help='Path to config file')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
@click.pass_context
def cli(ctx, config, verbose):
    """FLOAT command-line interface
    
    floatctl exposes the lf1m daemon's processing pipeline for direct CLI use.
    Process files, search collections, and manage the daemon.
    """
    # Store config in context
    ctx.ensure_object(dict)
    ctx.obj['config_path'] = config
    ctx.obj['verbose'] = verbose


@cli.command()
@click.argument('target', type=click.Path(exists=True))
@click.option('--recursive', '-r', is_flag=True, help='Process folders recursively')
@click.option('--output', '-o', help='Output format: json, summary, detailed', default='summary')
@click.pass_context
def process(ctx, target, recursive, output):
    """Process file or folder through FLOAT pipeline
    
    TARGET can be a file or folder path.
    
    Examples:
      floatctl process ./chat-export.md
      floatctl process ./exports/ --recursive
    """
    target_path = Path(target)
    
    try:
        # Initialize LF1M
        lf1m = LF1M(config_path=ctx.obj.get('config_path'))
        
        if target_path.is_file():
            click.echo(f"Processing file: {target_path.name}")
            result = lf1m.process_file(target_path)
            _display_process_result(result, output)
            
        elif target_path.is_dir():
            click.echo(f"Processing folder: {target_path.name} (recursive: {recursive})")
            results = lf1m.process_folder(target_path, recursive=recursive)
            _display_process_results(results, output)
            
        else:
            click.echo(f"Error: {target} is neither a file nor a directory", err=True)
            sys.exit(1)
            
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        if ctx.obj.get('verbose'):
            import traceback
            traceback.print_exc()
        sys.exit(1)


@cli.command()
@click.argument('query')
@click.option('--collections', '-c', help='Comma-separated list of collections to search')
@click.option('--limit', '-l', default=10, help='Maximum number of results')
@click.option('--output', '-o', help='Output format: json, summary, detailed', default='summary')
@click.pass_context
def search(ctx, query, collections, limit, output):
    """Search across FLOAT collections
    
    Basic text search across ChromaDB collections.
    
    Examples:
      floatctl search "boundaries as care"
      floatctl search "redux" --collections float_tripartite_v2_concept
      floatctl search "meeting notes" --limit 5
    """
    try:
        lf1m = LF1M(config_path=ctx.obj.get('config_path'))
        
        # Parse collections list
        collection_list = None
        if collections:
            collection_list = [c.strip() for c in collections.split(',')]
        
        click.echo(f"Searching for: '{query}'")
        if collection_list:
            click.echo(f"Collections: {', '.join(collection_list)}")
        
        results = lf1m.search_collections(query, collection_list, limit)
        _display_search_results(results, output)
        
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        if ctx.obj.get('verbose'):
            import traceback
            traceback.print_exc()
        sys.exit(1)


# Import and add the enhanced query command
from floatctl.commands.search import query as query_command
cli.add_command(query_command)


@cli.group()
def daemon():
    """Daemon control commands"""
    pass


@daemon.command()
@click.pass_context
def status(ctx):
    """Show daemon status and processing statistics"""
    try:
        lf1m = LF1M(config_path=ctx.obj.get('config_path'))
        status_info = lf1m.get_daemon_status()
        
        click.echo("=== lf1m Daemon Status ===")
        click.echo(f"Status: {status_info.get('status', 'unknown')}")
        
        if 'message' in status_info:
            click.echo(f"Message: {status_info['message']}")
        
        if 'processed_files' in status_info:
            click.echo(f"Files processed: {status_info['processed_files']}")
        
        if 'last_activity' in status_info:
            click.echo(f"Last activity: {status_info['last_activity']}")
            
        if ctx.obj.get('verbose') and status_info.get('status') != 'stopped':
            click.echo("\n=== Raw Status ===")
            click.echo(json.dumps(status_info, indent=2))
            
    except Exception as e:
        click.echo(f"Error getting daemon status: {e}", err=True)
        sys.exit(1)


@daemon.command()
@click.pass_context
def start(ctx):
    """Start the lf1m daemon (placeholder)"""
    click.echo("Daemon start functionality coming soon...")
    click.echo("For now, run: python streamlined_float_daemon.py <dropzone_path>")


@daemon.command()
@click.pass_context  
def stop(ctx):
    """Stop the lf1m daemon (placeholder)"""
    click.echo("Daemon stop functionality coming soon...")
    click.echo("For now, use Ctrl+C to stop the daemon process")


@cli.command()
@click.pass_context
def collections(ctx):
    """List ChromaDB collections and document counts"""
    try:
        lf1m = LF1M(config_path=ctx.obj.get('config_path'))
        collections_info = lf1m.list_collections()
        
        click.echo("=== ChromaDB Collections ===")
        total_docs = 0
        
        for collection in collections_info:
            count = collection['count']
            total_docs += count
            click.echo(f"{collection['name']}: {count:,} documents")
        
        click.echo(f"\nTotal documents: {total_docs:,}")
        
    except Exception as e:
        click.echo(f"Error listing collections: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option('--dropzone-only', is_flag=True, help='Only reprocess dropzone folder')
@click.pass_context
def reprocess(ctx, dropzone_only):
    """Reprocess files in dropzone or vault (placeholder)"""
    click.echo("Reprocess functionality coming soon...")
    if dropzone_only:
        click.echo("Will reprocess dropzone folder when implemented")
    else:
        click.echo("Will reprocess specified paths when implemented")


def _display_process_result(result: dict, output_format: str):
    """Display single file processing result"""
    if output_format == 'json':
        click.echo(json.dumps(result, indent=2))
    elif output_format == 'detailed':
        click.echo(f"Success: {result.get('success', False)}")
        if result.get('success'):
            click.echo(f"Float ID: {result.get('float_id', 'N/A')}")
            click.echo(f"DIS file: {result.get('dis_file', 'N/A')}")
            if 'storage_result' in result:
                storage = result['storage_result']
                click.echo(f"Stored in: {storage.get('collection', 'N/A')}")
                click.echo(f"Chunks: {storage.get('chunk_count', 0)}")
        else:
            click.echo(f"Error: {result.get('error', 'Unknown error')}")
    else:  # summary
        if result.get('success'):
            click.echo(f"✓ Processed - Float ID: {result.get('float_id', 'N/A')}")
        else:
            click.echo(f"✗ Failed - {result.get('error', 'Unknown error')}")


def _display_process_results(results: List[dict], output_format: str):
    """Display multiple file processing results"""
    if output_format == 'json':
        click.echo(json.dumps(results, indent=2))
        return
    
    successful = sum(1 for r in results if r.get('success'))
    total = len(results)
    
    click.echo(f"\nProcessed {successful}/{total} files successfully")
    
    if output_format == 'detailed':
        for result in results:
            click.echo(f"\n{result.get('file_path', 'Unknown file')}:")
            _display_process_result(result, 'detailed')
    else:  # summary
        failed = [r for r in results if not r.get('success')]
        if failed:
            click.echo("\nFailed files:")
            for result in failed:
                click.echo(f"  ✗ {Path(result.get('file_path', 'Unknown')).name}: {result.get('error', 'Unknown error')}")


def _display_search_results(results: List[dict], output_format: str):
    """Display search results"""
    if output_format == 'json':
        click.echo(json.dumps(results, indent=2))
        return
    
    if not results:
        click.echo("No results found.")
        return
    
    click.echo(f"\nFound {len(results)} results:")
    
    for i, result in enumerate(results, 1):
        click.echo(f"\n{i}. Collection: {result['collection']}")
        
        if output_format == 'detailed':
            click.echo(f"   ID: {result.get('id', 'N/A')}")
            click.echo(f"   Distance: {result.get('distance', 'N/A')}")
            if result.get('metadata'):
                click.echo(f"   Metadata: {json.dumps(result['metadata'], indent=6)}")
            click.echo(f"   Content: {result['document'][:200]}...")
        else:  # summary
            # Extract title or first line of content
            content = result['document']
            first_line = content.split('\n')[0] if content else "No content"
            if len(first_line) > 80:
                first_line = first_line[:77] + "..."
            click.echo(f"   {first_line}")


if __name__ == '__main__':
    cli()