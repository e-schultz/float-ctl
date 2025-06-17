# floatctl Usage Examples

## Real Usage Scenarios Tested

### File Processing
```bash
# Process a single file through FLOAT pipeline
$ echo "Test content with ctx::testing patterns and float.dispatch({test: true})" > /tmp/test.md
$ floatctl process /tmp/test.md

Processing file: test.md
✓ Processed - Float ID: 1901878be5ba
```

### Collections Overview
```bash
$ floatctl collections

=== ChromaDB Collections ===
float_tripartite_v2_concept: 9,273 documents
float_tripartite_v2_framework: 18,019 documents  
float_tripartite_v2_metaphor: 18,789 documents
float_dispatch_bay: 2,246 documents
float_echoCopy: 752 documents
...
Total documents: 119,354
```

### Basic Search
```bash
$ floatctl search "redux patterns" --limit 3

Searching for: 'redux patterns'
Found 3 results:

1. Collection: float_tripartite_v2_concept
   ```javascript
   
2. Collection: float_tripartite_v2_concept  
   ```javascript
   
3. Collection: float_tripartite_v2_concept
   ```javascript
```

### FloatQL Pattern Search
```bash
$ floatctl query "ctx::meeting" --explain

Searching for: 'ctx::meeting'

Parsed query:
  Text terms: ['meeting']
  FLOAT patterns: ['ctx']
  Persona patterns: []
  Temporal filters: {}
  Type filters: []
  Bridge IDs: []
  Suggested collections: ['float_tripartite_v2_framework', 'float_tripartite_v2_concept', 'float_tripartite_v2_metaphor']

No results found.
```

### Persona Annotation Search
```bash
$ floatctl query "[karen::]" --explain

Searching for: '[karen::]'

Parsed query:
  Text terms: []
  FLOAT patterns: []
  Persona patterns: ['karen']
  Temporal filters: {}
  Type filters: []  
  Bridge IDs: []
  Suggested collections: ['float_tripartite_v2_framework', 'float_tripartite_v2_metaphor', 'float_tripartite_v2_concept']

No results found.
```

### Daemon Status
```bash
$ floatctl daemon status

=== lf1m Daemon Status ===
Status: unknown
```

## Workflow Examples

### Daily Processing Workflow
```bash
# 1. Check what collections we have
floatctl collections

# 2. Process new conversation exports
floatctl process ~/Downloads/claude-conversation-export.md

# 3. Search for specific patterns
floatctl query "ctx::planning" --limit 5

# 4. Find persona-specific content
floatctl query "[sysop::] technical decisions"
```

### Research Workflow  
```bash
# 1. Find all Redux-related content
floatctl search "redux event-sourcing" --limit 10

# 2. Use pattern search for FLOAT signals
floatctl query "highlight::architecture"

# 3. Find bridge references
floatctl query "bridge::CB-20250611"
```

## FloatQL Pattern Reference

### FLOAT Methodology Patterns
```bash
floatctl query "ctx::ritual"          # Context markers
floatctl query "highlight::insight"   # Important highlights  
floatctl query "signal::pattern"      # Key signals
floatctl query "expandOn::concept"    # Follow-up areas
```

### Persona System
```bash
floatctl query "[sysop::]"           # System operator perspective
floatctl query "[karen::]"           # Editorial conscience
floatctl query "[qtb::]"             # Queer Techno Bard
floatctl query "[lf1m::]"            # Processing time markers
```

### Temporal Queries
```bash
floatctl query "created:today"       # Today's content
floatctl query "modified:yesterday"  # Recently modified
floatctl query "date:2025-06-13"     # Specific date
```

### Content Type Filtering
```bash
floatctl query "type:log"            # Daily logs only
floatctl query "type:conversation"   # Conversations only
```

### Bridge Operations (Planned)
```bash
# These will work when bridge commands are implemented
floatctl query "bridge::CB-20250611-1510-N1CK"
floatctl bridge restore CB-20250611-1510-N1CK
floatctl bridge list --date today
```

## Command Options

### Process Command
```bash
floatctl process FILE_OR_FOLDER [OPTIONS]

Options:
  -r, --recursive      Process folders recursively
  -o, --output FORMAT  Output format: json, summary, detailed
```

### Search Command  
```bash
floatctl search QUERY [OPTIONS]

Options:
  -c, --collections LIST  Comma-separated collection names
  -l, --limit NUMBER      Maximum results (default: 10)
  -o, --output FORMAT     Output format: json, summary, detailed
```

### Query Command (FloatQL)
```bash
floatctl query FLOATQL_QUERY [OPTIONS]

Options:
  -c, --collections LIST  Comma-separated collection names
  -l, --limit NUMBER      Maximum results (default: 10)
  --floatql-only          Force FloatQL parsing
  --explain               Show query parsing details
```

## Next Steps

The MVP is working! Key next implementations:

1. **Bridge Operations**: Full `bridge::` reference handling
2. **Daemon Control**: Start/stop daemon from CLI  
3. **Reprocess Commands**: Re-run dropzone contents
4. **Enhanced Output**: Better result formatting and export options