#!/usr/bin/env python3
"""
CLI tool to add a new note to the knowledge graph.

Usage:
    python add_note.py <filename> <title> <tags> <summary> <batch_name> [relationships_json]

Example:
    python add_note.py "my_note.md" "My Note" "tag1,tag2,tag3" "Brief summary" "Core AI/Agents"

With relationships:
    python add_note.py "my_note.md" "My Note" "tag1,tag2" "Summary" "Core AI/Agents" \
        '{"prerequisites": [{"note": "other.md", "why": "reason"}]}'
"""

import sys
import json
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

import graph_lib


def main():
    if len(sys.argv) < 6:
        print("Usage: python add_note.py <filename> <title> <tags> <summary> <batch_name> [relationships_json]")
        print("\nExample:")
        print('  python add_note.py "my_note.md" "My Note" "tag1,tag2,tag3" "Brief summary" "Core AI/Agents"')
        sys.exit(1)

    filename = sys.argv[1]
    title = sys.argv[2]
    tags = sys.argv[3].split(",")
    summary = sys.argv[4]
    batch_name = sys.argv[5]
    relationships = None

    if len(sys.argv) > 6:
        relationships = json.loads(sys.argv[6])

    # Load graph (from .claude/scripts/ go up two levels to repo root)
    graph_path = Path(__file__).parent.parent.parent / "knowledge_graph_full.json"
    graph = graph_lib.load_graph(graph_path)

    # Check if note already exists
    if graph_lib.find_note(graph["notes"], filename):
        print(f"Error: Note '{filename}' already exists in graph")
        sys.exit(1)

    # Create note entry
    note_entry = graph_lib.create_note_entry(
        filename=filename,
        title=title,
        tags=tags,
        summary=summary,
        relationships=relationships
    )

    # Add note to graph
    graph_lib.add_note(graph, note_entry)

    # Add to batch
    try:
        graph_lib.add_note_to_batch(graph, filename, batch_name=batch_name)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Establish bidirectional relationships if any were provided
    if relationships:
        added = graph_lib.establish_bidirectional_relationships(graph)
        print(f"Established {added} bidirectional relationships")

    # Update metadata
    graph_lib.update_metadata(
        graph,
        increment_version=True,
        update_note_count=True,
        description=f"Added {filename}",
        last_updated=__import__('datetime').date.today().isoformat()
    )

    # Save graph
    graph_lib.save_graph(graph, graph_path)

    # Print summary
    print(f"Successfully added note: {filename}")
    print(f"- Title: {title}")
    print(f"- Tags: {', '.join(tags)}")
    print(f"- Batch: {batch_name}")
    print(f"- Version: {graph['metadata']['version']}")
    print(f"- Total notes: {graph['metadata']['total_notes']}")


if __name__ == "__main__":
    main()
