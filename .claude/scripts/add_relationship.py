#!/usr/bin/env python3
"""
CLI tool to add relationships between notes in the knowledge graph.

Usage:
    python add_relationship.py <source> <target> <type> <why> [--bidirectional] [--inverse-type TYPE]

Relationship types:
    - prerequisites
    - related_concepts
    - extends
    - extended_by
    - alternatives
    - examples

Example:
    python add_relationship.py "note_a.md" "note_b.md" "extends" "Builds upon concept B"

Bidirectional example:
    python add_relationship.py "note_a.md" "note_b.md" "extends" "Builds upon B" \
        --bidirectional --inverse-type "extended_by"
"""

import sys
import argparse
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

import graph_lib


def main():
    parser = argparse.ArgumentParser(description="Add relationship between notes")
    parser.add_argument("source", help="Source note filename")
    parser.add_argument("target", help="Target note filename")
    parser.add_argument("type", help="Relationship type")
    parser.add_argument("why", help="Explanation of relationship")
    parser.add_argument("--bidirectional", action="store_true", help="Add inverse relationship")
    parser.add_argument("--inverse-type", help="Type for inverse relationship")

    args = parser.parse_args()

    # Validate
    valid_types = ["prerequisites", "related_concepts", "extends", "extended_by", "alternatives", "examples"]
    if args.type not in valid_types:
        print(f"Error: Invalid relationship type '{args.type}'")
        print(f"Valid types: {', '.join(valid_types)}")
        sys.exit(1)

    if args.bidirectional and not args.inverse_type:
        print("Error: --inverse-type required when --bidirectional is used")
        sys.exit(1)

    # Load graph (from .claude/scripts/ go up two levels to repo root)
    graph_path = Path(__file__).parent.parent.parent / "knowledge_graph_full.json"
    graph = graph_lib.load_graph(graph_path)

    # Add relationship
    try:
        added = graph_lib.add_relationship(
            graph,
            source_filename=args.source,
            target_filename=args.target,
            relationship_type=args.type,
            why=args.why,
            bidirectional=args.bidirectional,
            inverse_type=args.inverse_type
        )

        if not added:
            print(f"Relationship already exists: {args.source} --{args.type}--> {args.target}")
            sys.exit(0)

    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Update metadata
    graph_lib.update_metadata(
        graph,
        increment_version=False,  # Don't increment for relationship additions
        update_note_count=False,
        last_updated=__import__('datetime').date.today().isoformat()
    )

    # Save graph
    graph_lib.save_graph(graph, graph_path)

    # Print summary
    print(f"Successfully added relationship:")
    print(f"  {args.source}")
    print(f"    --{args.type}--> {args.target}")
    if args.bidirectional:
        print(f"  {args.target}")
        print(f"    --{args.inverse_type}--> {args.source}")


if __name__ == "__main__":
    main()
