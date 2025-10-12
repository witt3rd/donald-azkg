#!/usr/bin/env python3
"""
Rename a note and update all references throughout the knowledge base.

Usage:
    python rename_note.py <old_filename> <new_filename>

Examples:
    python rename_note.py mcp_sdk python_mcp_sdk
    python rename_note.py agents.md ai_agents.md
"""

import sys
import json
import re
from pathlib import Path
from datetime import datetime
from typing import List, Tuple
import graph_lib


def normalize_filename(filename: str) -> str:
    """Ensure filename has .md extension."""
    if not filename.endswith('.md'):
        filename += '.md'
    return filename


def create_backup(graph_path: Path) -> Path:
    """Create timestamped backup of knowledge graph."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = graph_path.parent / f"knowledge_graph_backup_{timestamp}.json"

    with open(graph_path, 'r', encoding='utf-8') as src:
        with open(backup_path, 'w', encoding='utf-8') as dst:
            dst.write(src.read())

    return backup_path


def update_graph_references(graph: dict, old_filename: str, new_filename: str) -> int:
    """
    Update all references to old_filename in the knowledge graph.

    Returns:
        Number of references updated
    """
    count = 0

    # Update in batches
    for batch in graph["batches"]:
        if old_filename in batch["notes"]:
            batch["notes"] = [new_filename if n == old_filename else n for n in batch["notes"]]
            count += 1

    # Update note entry itself
    for note in graph["notes"]:
        if note["filename"] == old_filename:
            note["filename"] = new_filename
            count += 1

        # Update relationships that reference the old filename
        for rel_type, relationships in note["relationships"].items():
            for rel in relationships:
                if rel["note"] == old_filename:
                    rel["note"] = new_filename
                    count += 1

    return count


def update_markdown_wikilinks(repo_path: Path, old_name: str, new_name: str) -> List[Tuple[Path, int]]:
    """
    Update all wikilinks [[old_name]] -> [[new_name]] in markdown files.

    Args:
        repo_path: Path to repository root
        old_name: Old filename without .md extension
        new_name: New filename without .md extension

    Returns:
        List of (file_path, replacement_count) tuples
    """
    updates = []

    # Pattern to match [[old_name]] wikilinks
    pattern = re.compile(r'\[\[' + re.escape(old_name) + r'\]\]')
    replacement = f'[[{new_name}]]'

    # Find all markdown files
    for md_file in repo_path.glob("*.md"):
        # Skip the renamed file itself
        if md_file.name == f"{new_name}.md":
            continue

        try:
            content = md_file.read_text(encoding='utf-8')
            new_content, count = pattern.subn(replacement, content)

            if count > 0:
                md_file.write_text(new_content, encoding='utf-8')
                updates.append((md_file, count))
        except Exception as e:
            print(f"Warning: Failed to update {md_file}: {e}", file=sys.stderr)

    return updates


def main():
    if len(sys.argv) != 3:
        print("Usage: python rename_note.py <old_filename> <new_filename>")
        print("\nExamples:")
        print("  python rename_note.py mcp_sdk python_mcp_sdk")
        print("  python rename_note.py agents.md ai_agents.md")
        sys.exit(1)

    old_filename = normalize_filename(sys.argv[1])
    new_filename = normalize_filename(sys.argv[2])

    # Get repository root (2 levels up from script location)
    repo_path = Path(__file__).parent.parent.parent
    graph_path = repo_path / "knowledge_graph_full.json"
    old_file_path = repo_path / old_filename
    new_file_path = repo_path / new_filename

    print(f"\n{'='*60}")
    print(f"Renaming Note: {old_filename} → {new_filename}")
    print(f"{'='*60}\n")

    # Validation
    if not old_file_path.exists():
        print(f"❌ Error: File does not exist: {old_filename}")
        sys.exit(1)

    if new_file_path.exists():
        print(f"❌ Error: Target filename already exists: {new_filename}")
        sys.exit(1)

    if not graph_path.exists():
        print(f"❌ Error: Knowledge graph not found: {graph_path}")
        sys.exit(1)

    # Create backup
    print("📦 Creating backup of knowledge graph...")
    backup_path = create_backup(graph_path)
    print(f"   ✓ Backup created: {backup_path.name}\n")

    # Step 1: Rename physical file
    print("📝 Renaming physical file...")
    try:
        old_file_path.rename(new_file_path)
        print(f"   ✓ Renamed: {old_filename} → {new_filename}\n")
    except Exception as e:
        print(f"   ❌ Failed to rename file: {e}")
        sys.exit(1)

    # Step 2: Update knowledge graph
    print("🔗 Updating knowledge graph references...")
    try:
        graph = graph_lib.load_graph(graph_path)
        graph_updates = update_graph_references(graph, old_filename, new_filename)

        # Update metadata
        graph_lib.update_metadata(
            graph,
            increment_version=False,  # Don't increment for rename
            update_note_count=False,  # Note count unchanged
            last_updated=datetime.now().strftime("%Y-%m-%d")
        )

        graph_lib.save_graph(graph, graph_path)
        print(f"   ✓ Updated {graph_updates} references in knowledge graph\n")
    except Exception as e:
        print(f"   ❌ Failed to update knowledge graph: {e}")
        print(f"   ⚠️  Reverting file rename...")
        new_file_path.rename(old_file_path)
        sys.exit(1)

    # Step 3: Update wikilinks in markdown files
    print("📄 Updating wikilinks in markdown files...")
    old_name_no_ext = old_filename.replace('.md', '')
    new_name_no_ext = new_filename.replace('.md', '')

    try:
        wikilink_updates = update_markdown_wikilinks(repo_path, old_name_no_ext, new_name_no_ext)

        if wikilink_updates:
            print(f"   ✓ Updated wikilinks in {len(wikilink_updates)} files:")
            for file_path, count in wikilink_updates:
                print(f"      - {file_path.name}: {count} reference(s)")
        else:
            print("   ℹ️  No wikilinks found to update")
        print()
    except Exception as e:
        print(f"   ⚠️  Warning: Failed to update some wikilinks: {e}\n")

    # Validate graph integrity
    print("✅ Validating knowledge graph integrity...")
    is_valid, errors = graph_lib.validate_graph(graph)

    if is_valid:
        print("   ✓ Graph validation passed\n")
    else:
        print("   ⚠️  Validation warnings:")
        for error in errors[:5]:  # Show first 5 errors
            print(f"      - {error}")
        if len(errors) > 5:
            print(f"      ... and {len(errors) - 5} more")
        print()

    # Summary
    print(f"{'='*60}")
    print("✅ Rename Complete!")
    print(f"{'='*60}\n")
    print(f"📋 Summary:")
    print(f"   • File renamed: {old_filename} → {new_filename}")
    print(f"   • Knowledge graph references updated: {graph_updates}")
    print(f"   • Markdown files with wikilink updates: {len(wikilink_updates)}")
    print(f"   • Backup created: {backup_path.name}")
    print()
    print("💡 Next steps:")
    print("   • Review changes with git diff")
    print("   • Update any MOC files that reference this note")
    print("   • Consider updating note title if needed")
    print()


if __name__ == "__main__":
    main()
