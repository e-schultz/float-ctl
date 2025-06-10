#!/bin/bash

# Bootstrap script for conversation → artifact pipeline exploration
# Based on Claude Code session 2025-06-09

PROJECT_NAME="conversation-artifact-pipeline"
PROJECT_DIR="$HOME/projects/$PROJECT_NAME"

echo "🚀 Bootstrapping $PROJECT_NAME..."

# Create project structure
mkdir -p "$PROJECT_DIR"/{docs,src,examples,experiments}
cd "$PROJECT_DIR"

# Initialize git
git init
echo "# Conversation → Artifact Pipeline Exploration

Exploring the architecture patterns discovered in Claude Code session where conversation threads become control planes for live systems.

## Key Concepts
- Bidirectional sync between chat and running infrastructure
- Conversation as source code, artifacts as compiled output
- Personal knowledge systems as queryable infrastructure
- One-shot prompts to bypass context constraints

## Session Origin
Started from debugging FLOAT daemon, discovered we're already doing distributed cognition across human/AI/system boundaries.

" > README.md

# Create basic structure files
cat > docs/session-capture.md << 'EOF'
# Session Capture Methods

## Manual Approaches
- Copy/paste full conversation
- Screenshot key moments
- Export highlights to external tools

## Programmatic Ideas
- Browser extension for Claude chat export
- Readwise integration for conversation highlights
- FLOAT dropzone processing of chat exports

## Integration Points
- Obsidian vault for conversation indexing
- ChromaDB for semantic search across sessions
- Artifact generation from conversation AST
EOF

cat > src/conversation-ast-parser.md << 'EOF'
# Conversation AST Parser Concepts

Ideas for parsing natural language conversation into executable structures:

## Pattern Recognition
- Intent detection: "build X" vs "debug Y" vs "explore Z"
- Artifact boundaries: when conversation becomes code
- Context preservation: maintaining state across tool calls

## AST Structures
- ConversationNode: captures dialogue context
- ArtifactNode: represents generated code/systems
- SyncNode: bidirectional state updates
- BootstrapNode: project initialization patterns

## Implementation Approaches
- LLM-based parsing of conversation semantics
- Pattern matching on tool call sequences
- State machine for conversation → artifact transitions
EOF

cat > experiments/README.md << 'EOF'
# Experiments Directory

Space for exploring conversation → artifact pipeline concepts:

## Planned Experiments
1. Chat export → structured data parsing
2. One-shot artifact generation prompts
3. Bidirectional sync simulation
4. Context compression techniques
5. Personal knowledge system queries

## Session References
- Original discovery session in float-log
- Nick/Rangle demonstration of Readwise → artifact pipeline
- FLOAT system integration patterns
EOF

# Copy the exploration file from float-log
cp "/Users/evan/github/float-log/conversation_artifact_pipeline_exploration.md" docs/

# Initial commit
git add .
git commit -m "Initial bootstrap: conversation → artifact pipeline exploration

Based on Claude Code session discovering bidirectional sync between 
chat threads and running infrastructure. 

Key insight: We're already doing distributed cognition across 
human/AI/system boundaries - now let's make it intentional.

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"

echo "✅ Project bootstrapped at: $PROJECT_DIR"
echo "📁 Structure created with docs, experiments, and session capture"
echo "🎯 Next: Copy full session content to docs/full-session-capture.md"
echo "🚀 Then: cd $PROJECT_DIR && explore!"