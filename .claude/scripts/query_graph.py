#!/usr/bin/env python3
"""
CLI tool to query the knowledge graph.

Usage:
    python query_graph.py <command> [args]

Commands:
    stats               - Show graph statistics
    note <filename>     - Show information about a note
    batch <name>        - Show information about a batch
    validate            - Validate graph integrity
    metadata            - Show graph metadata

Examples:
    python query_graph.py stats
    python query_graph.py note "agents.md"
    python query_graph.py batch "Core AI/Agents"
    python query_graph.py validate
    python query_graph.py metadata
"""

import sys
import json
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

import graph_lib


def print_stats(graph):
    """Print graph statistics."""
    stats = graph_lib.get_statistics(graph)

    print("Graph Statistics")
    print("=" * 60)
    print(f"Total notes: {stats['total_notes']}")
    print(f"Total batches: {stats['total_batches']}")
    print()
    print("Relationship counts:")
    for rel_type, count in stats['relationship_counts'].items():
        print(f"  {rel_type}: {count}")
    print()
    print(f"Unique tags: {len(stats['tags_distribution'])}")
    print("Top 10 tags:")
    sorted_tags = sorted(stats['tags_distribution'].items(), key=lambda x: x[1], reverse=True)[:10]
    for tag, count in sorted_tags:
        print(f"  {tag}: {count}")


def print_note(graph, filename):
    """Print information about a specific note."""
    note = graph_lib.find_note(graph["notes"], filename)
    if not note:
        print(f"Error: Note '{filename}' not found")
        sys.exit(1)

    print(f"Note: {note['filename']}")
    print("=" * 60)
    print(f"Title: {note['title']}")
    print(f"Tags: {', '.join(note['tags'])}")
    print(f"Summary: {note['summary']}")
    print()
    print("Relationships:")
    for rel_type, relationships in note['relationships'].items():
        if relationships:
            print(f"  {rel_type}: {len(relationships)}")
            for rel in relationships:
                # Use ASCII-safe output to avoid Unicode encoding issues on Windows
                why_text = rel['why'].encode('ascii', errors='replace').decode('ascii')
                print(f"    - {rel['note']}: {why_text}")


def print_batch(graph, batch_name):
    """Print information about a specific batch."""
    batch = graph_lib.find_batch(graph["batches"], batch_name=batch_name)
    if not batch:
        print(f"Error: Batch '{batch_name}' not found")
        sys.exit(1)

    print(f"Batch {batch['batch_number']}: {batch['name']}")
    print("=" * 60)
    print(f"Total notes: {len(batch['notes'])}")
    print()
    print("Notes:")
    for note_filename in batch['notes']:
        note = graph_lib.find_note(graph["notes"], note_filename)
        if note:
            print(f"  - {note_filename}: {note['title']}")
        else:
            print(f"  - {note_filename}: [NOT FOUND IN GRAPH]")


def print_validate(graph):
    """Validate and print validation results."""
    is_valid, errors = graph_lib.validate_graph(graph)

    print("Graph Validation")
    print("=" * 60)

    if is_valid:
        print("[OK] Graph is valid")
    else:
        print(f"[ERROR] Graph has {len(errors)} error(s):")
        print()
        for i, error in enumerate(errors, 1):
            print(f"{i}. {error}")
        sys.exit(1)


def print_metadata(graph):
    """Print graph metadata."""
    metadata = graph["metadata"]

    print("Graph Metadata")
    print("=" * 60)
    for key, value in metadata.items():
        print(f"{key}: {value}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python query_graph.py <command> [args]")
        print("\nCommands:")
        print("  stats               - Show graph statistics")
        print("  note <filename>     - Show information about a note")
        print("  batch <name>        - Show information about a batch")
        print("  validate            - Validate graph integrity")
        print("  metadata            - Show graph metadata")
        sys.exit(1)

    command = sys.argv[1]

    # Load graph (from .claude/scripts/ go up two levels to repo root)
    graph_path = Path(__file__).parent.parent.parent / "knowledge_graph_full.json"
    graph = graph_lib.load_graph(graph_path)

    if command == "stats":
        print_stats(graph)
    elif command == "note":
        if len(sys.argv) < 3:
            print("Error: note command requires filename argument")
            sys.exit(1)
        print_note(graph, sys.argv[2])
    elif command == "batch":
        if len(sys.argv) < 3:
            print("Error: batch command requires batch name argument")
            sys.exit(1)
        print_batch(graph, sys.argv[2])
    elif command == "validate":
        print_validate(graph)
    elif command == "metadata":
        print_metadata(graph)
    else:
        print(f"Error: Unknown command '{command}'")
        sys.exit(1)


if __name__ == "__main__":
    main()
