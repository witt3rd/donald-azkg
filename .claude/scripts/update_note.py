#!/usr/bin/env python3
"""
CLI tool to update a note's metadata in the knowledge graph.

Usage:
    python update_note.py <filename> [--title TITLE] [--tags TAG1,TAG2,...] [--summary SUMMARY]

Examples:
    # Update title only
    python update_note.py "agents.md" --title "AI Agents: Autonomous Intelligence Systems"

    # Update tags only
    python update_note.py "agents.md" --tags "ai,agents,llm,architecture"

    # Update multiple fields
    python update_note.py "agents.md" \
        --title "AI Agents" \
        --tags "ai,agents" \
        --summary "Brief summary of AI agents"
"""

import sys
import json
from pathlib import Path
from datetime import date

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

import graph_lib


def main():
    if len(sys.argv) < 2:
        print("Usage: python update_note.py <filename> [--title TITLE] [--tags TAG1,TAG2,...] [--summary SUMMARY]")
        print("\nExamples:")
        print('  python update_note.py "agents.md" --title "AI Agents: Autonomous Intelligence Systems"')
        print('  python update_note.py "agents.md" --tags "ai,agents,llm"')
        print('  python update_note.py "agents.md" --summary "Brief summary"')
        sys.exit(1)

    filename = sys.argv[1]

    # Parse optional arguments
    updates = {}
    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == '--title' and i + 1 < len(sys.argv):
            updates['title'] = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == '--tags' and i + 1 < len(sys.argv):
            updates['tags'] = [t.strip() for t in sys.argv[i + 1].split(',')]
            i += 2
        elif sys.argv[i] == '--summary' and i + 1 < len(sys.argv):
            updates['summary'] = sys.argv[i + 1]
            i += 2
        else:
            print(f"Error: Unknown argument '{sys.argv[i]}'")
            sys.exit(1)

    if not updates:
        print("Error: At least one update field (--title, --tags, --summary) is required")
        sys.exit(1)

    # Load graph
    graph_path = Path(__file__).parent.parent.parent / "knowledge_graph_full.json"
    graph = graph_lib.load_graph(graph_path)

    # Find note
    note = graph_lib.find_note(graph["notes"], filename)
    if not note:
        print(f"Error: Note '{filename}' not found in graph")
        sys.exit(1)

    # Store old values for reporting
    old_values = {}
    if 'title' in updates:
        old_values['title'] = note['title']
    if 'tags' in updates:
        old_values['tags'] = note['tags'].copy()
    if 'summary' in updates:
        old_values['summary'] = note['summary']

    # Apply updates
    for key, value in updates.items():
        note[key] = value

    # Update graph metadata
    changes_description = f"Updated {filename}: {', '.join(updates.keys())}"
    graph_lib.update_metadata(
        graph,
        increment_version=False,  # Minor update, just increment decimal
        update_note_count=False,
        description=changes_description,
        last_updated=date.today().isoformat()
    )

    # Increment version by 0.1 (minor update)
    current_version = float(graph['metadata']['version'])
    graph['metadata']['version'] = f"{current_version + 0.1:.1f}"

    # Save graph
    graph_lib.save_graph(graph, graph_path)

    # Print summary
    print(f"Successfully updated note: {filename}")
    print(f"Version: {current_version} -> {graph['metadata']['version']}")
    print()

    for key in updates:
        if key in old_values:
            print(f"{key.capitalize()}:")
            print(f"  Old: {old_values[key]}")
            print(f"  New: {updates[key]}")
        else:
            print(f"{key.capitalize()}: {updates[key]}")


if __name__ == "__main__":
    main()
