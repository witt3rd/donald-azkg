#!/usr/bin/env python3
"""
CLI tool to validate knowledge graph integrity.

This is a convenience wrapper around query_graph.py validate.

Usage:
    python validate_graph.py
"""

import sys
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

import graph_lib


def main():
    # Load graph (from .claude/scripts/ go up two levels to repo root)
    graph_path = Path(__file__).parent.parent.parent / "knowledge_graph_full.json"
    graph = graph_lib.load_graph(graph_path)

    # Validate
    is_valid, errors = graph_lib.validate_graph(graph)

    print("Graph Validation")
    print("=" * 60)

    if is_valid:
        print("[OK] Graph is valid")
        print()
        print("All checks passed:")
        print("  [OK] Metadata counts match actual counts")
        print("  [OK] All batch references point to existing notes")
        print("  [OK] All relationship targets exist")
        print("  [OK] Bidirectional relationships are consistent")
    else:
        print(f"[ERROR] Graph has {len(errors)} error(s):")
        print()
        for i, error in enumerate(errors, 1):
            print(f"{i}. {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
