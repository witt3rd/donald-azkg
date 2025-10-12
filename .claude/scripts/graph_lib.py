"""
Core library for knowledge graph operations.

This module provides generic functions for working with knowledge graph JSON files
in the Zettelkasten format. All functions are designed to be graph-agnostic and
work with any knowledge graph instance following the standard structure.

Graph structure:
{
  "metadata": {
    "version": "X.0",
    "total_notes": N,
    "forward_pass_batches_complete": M,
    "backward_pass_complete": bool,
    ...
  },
  "batches": [
    {
      "batch_number": N,
      "name": "Batch Name",
      "notes": ["note1.md", "note2.md", ...]
    }
  ],
  "notes": [
    {
      "filename": "note.md",
      "title": "Note Title",
      "tags": ["tag1", "tag2"],
      "summary": "Brief summary",
      "relationships": {
        "prerequisites": [{"note": "other.md", "why": "reason"}],
        "related_concepts": [...],
        "extends": [...],
        "extended_by": [...],
        "alternatives": [...],
        "examples": [...]
      }
    }
  ]
}
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple


def load_graph(graph_path: str | Path) -> Dict:
    """Load knowledge graph from JSON file."""
    with open(graph_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_graph(graph: Dict, graph_path: str | Path) -> None:
    """Save knowledge graph to JSON file."""
    with open(graph_path, 'w', encoding='utf-8') as f:
        json.dump(graph, f, indent=2, ensure_ascii=False)


def find_note(notes_list: List[Dict], filename: str) -> Optional[Dict]:
    """Find a note by filename in the notes list."""
    for note in notes_list:
        if note["filename"] == filename:
            return note
    return None


def find_batch(batches: List[Dict], batch_name: str = None, batch_number: int = None) -> Optional[Dict]:
    """Find a batch by name or number."""
    for batch in batches:
        if batch_name and batch["name"] == batch_name:
            return batch
        if batch_number is not None and batch["batch_number"] == batch_number:
            return batch
    return None


def add_note_to_batch(graph: Dict, filename: str, batch_name: str = None, batch_number: int = None) -> bool:
    """
    Add a note filename to a batch.

    Args:
        graph: The knowledge graph
        filename: Note filename to add
        batch_name: Target batch name (either this or batch_number required)
        batch_number: Target batch number (either this or batch_name required)

    Returns:
        True if added, False if already exists in batch
    """
    batch = find_batch(graph["batches"], batch_name, batch_number)
    if not batch:
        raise ValueError(f"Batch not found: {batch_name or batch_number}")

    if filename not in batch["notes"]:
        batch["notes"].append(filename)
        return True
    return False


def create_note_entry(
    filename: str,
    title: str,
    tags: List[str],
    summary: str,
    relationships: Dict[str, List[Dict[str, str]]] = None
) -> Dict:
    """
    Create a new note entry with the standard structure.

    Args:
        filename: Note filename (e.g., "my_note.md")
        title: Human-readable title
        tags: List of tags
        summary: Brief summary of the note
        relationships: Optional relationships dict with structure:
            {
              "prerequisites": [{"note": "file.md", "why": "reason"}],
              "related_concepts": [...],
              "extends": [...],
              "extended_by": [...],
              "alternatives": [...],
              "examples": [...]
            }

    Returns:
        Complete note entry dict
    """
    if relationships is None:
        relationships = {
            "prerequisites": [],
            "related_concepts": [],
            "extends": [],
            "extended_by": [],
            "alternatives": [],
            "examples": []
        }

    return {
        "filename": filename,
        "title": title,
        "tags": tags,
        "summary": summary,
        "relationships": relationships
    }


def add_note(graph: Dict, note_entry: Dict) -> bool:
    """
    Add a note entry to the graph.

    Args:
        graph: The knowledge graph
        note_entry: Complete note entry (use create_note_entry to create)

    Returns:
        True if added, False if note already exists
    """
    if find_note(graph["notes"], note_entry["filename"]):
        return False

    graph["notes"].append(note_entry)
    return True


def remove_note(graph: Dict, filename: str) -> bool:
    """
    Remove a note from the graph and clean up all references.

    Args:
        graph: The knowledge graph
        filename: Note filename to remove

    Returns:
        True if removed, False if not found
    """
    # Remove from notes list
    note = find_note(graph["notes"], filename)
    if not note:
        return False

    graph["notes"].remove(note)

    # Remove from all batches
    for batch in graph["batches"]:
        if filename in batch["notes"]:
            batch["notes"].remove(filename)

    # Remove all references from other notes
    for other_note in graph["notes"]:
        for rel_type in other_note["relationships"].values():
            other_note["relationships"][rel_type] = [
                r for r in rel_type if r["note"] != filename
            ]

    return True


def add_relationship(
    graph: Dict,
    source_filename: str,
    target_filename: str,
    relationship_type: str,
    why: str,
    bidirectional: bool = False,
    inverse_type: str = None
) -> bool:
    """
    Add a relationship between two notes.

    Args:
        graph: The knowledge graph
        source_filename: Source note filename
        target_filename: Target note filename
        relationship_type: Type of relationship (prerequisites, related_concepts, extends, etc.)
        why: Explanation of why this relationship exists
        bidirectional: If True, add inverse relationship
        inverse_type: Type for inverse relationship (required if bidirectional=True)

    Returns:
        True if added, False if relationship already exists
    """
    source = find_note(graph["notes"], source_filename)
    if not source:
        raise ValueError(f"Source note not found: {source_filename}")

    target = find_note(graph["notes"], target_filename)
    if not target:
        raise ValueError(f"Target note not found: {target_filename}")

    # Check if relationship already exists
    existing = [r for r in source["relationships"][relationship_type] if r["note"] == target_filename]
    if existing:
        return False

    # Add forward relationship
    source["relationships"][relationship_type].append({
        "note": target_filename,
        "why": why
    })

    # Add inverse relationship if requested
    if bidirectional:
        if not inverse_type:
            raise ValueError("inverse_type required when bidirectional=True")

        existing_inverse = [r for r in target["relationships"][inverse_type] if r["note"] == source_filename]
        if not existing_inverse:
            target["relationships"][inverse_type].append({
                "note": source_filename,
                "why": why
            })

    return True


def establish_bidirectional_relationships(graph: Dict) -> int:
    """
    Establish all bidirectional relationships in the graph.

    For example:
    - If A extends B, ensure B has extended_by A
    - If A has example B, ensure B has extended_by A

    Returns:
        Number of relationships added
    """
    added = 0

    # Mapping of forward -> inverse relationship types
    inverse_map = {
        "extends": "extended_by",
        "examples": "extended_by"  # Examples are also extended_by
    }

    for note in graph["notes"]:
        for forward_type, inverse_type in inverse_map.items():
            for rel in note["relationships"][forward_type]:
                target = find_note(graph["notes"], rel["note"])
                if target:
                    # Check if inverse exists
                    existing = [r for r in target["relationships"][inverse_type] if r["note"] == note["filename"]]
                    if not existing:
                        target["relationships"][inverse_type].append({
                            "note": note["filename"],
                            "why": rel["why"]
                        })
                        added += 1

    return added


def update_metadata(
    graph: Dict,
    increment_version: bool = True,
    update_note_count: bool = True,
    description: str = None,
    **kwargs
) -> None:
    """
    Update graph metadata.

    Args:
        graph: The knowledge graph
        increment_version: If True, increment version number
        update_note_count: If True, update total_notes count
        description: Optional description for this update
        **kwargs: Additional metadata fields to update
    """
    metadata = graph["metadata"]

    if increment_version:
        version_parts = metadata["version"].split(".")
        major = int(version_parts[0])
        metadata["version"] = f"{major + 1}.0"

    if update_note_count:
        metadata["total_notes"] = len(graph["notes"])

    if description:
        metadata["description"] = description

    # Update any additional fields
    for key, value in kwargs.items():
        metadata[key] = value


def validate_graph(graph: Dict) -> Tuple[bool, List[str]]:
    """
    Validate graph integrity.

    Checks:
    - All notes in batches exist in notes list
    - All relationship targets exist
    - Bidirectional relationships are consistent
    - Metadata counts match actual counts

    Returns:
        (is_valid, list_of_errors)
    """
    errors = []

    # Check metadata counts
    actual_count = len(graph["notes"])
    declared_count = graph["metadata"]["total_notes"]
    if actual_count != declared_count:
        errors.append(f"Metadata total_notes ({declared_count}) doesn't match actual count ({actual_count})")

    # Build set of all note filenames
    note_filenames = {note["filename"] for note in graph["notes"]}

    # Check batch references
    for batch in graph["batches"]:
        for filename in batch["notes"]:
            if filename not in note_filenames:
                errors.append(f"Batch '{batch['name']}' references non-existent note: {filename}")

    # Check relationship targets
    for note in graph["notes"]:
        for rel_type, relationships in note["relationships"].items():
            for rel in relationships:
                target = rel["note"]
                if target not in note_filenames:
                    errors.append(f"Note '{note['filename']}' has {rel_type} relationship to non-existent note: {target}")

    # Check bidirectional consistency
    for note in graph["notes"]:
        # Check extends -> extended_by
        for rel in note["relationships"]["extends"]:
            target = find_note(graph["notes"], rel["note"])
            if target:
                inverse = [r for r in target["relationships"]["extended_by"] if r["note"] == note["filename"]]
                if not inverse:
                    errors.append(f"Note '{note['filename']}' extends '{rel['note']}' but inverse not found")

    return (len(errors) == 0, errors)


def get_statistics(graph: Dict) -> Dict:
    """
    Get statistics about the graph.

    Returns:
        Dict with statistics like:
        - total_notes
        - total_batches
        - relationship_counts (by type)
        - tags_distribution
        - etc.
    """
    stats = {
        "total_notes": len(graph["notes"]),
        "total_batches": len(graph["batches"]),
        "relationship_counts": {
            "prerequisites": 0,
            "related_concepts": 0,
            "extends": 0,
            "extended_by": 0,
            "alternatives": 0,
            "examples": 0
        },
        "tags_distribution": {}
    }

    for note in graph["notes"]:
        # Count relationships
        for rel_type, rels in note["relationships"].items():
            stats["relationship_counts"][rel_type] += len(rels)

        # Count tags
        for tag in note["tags"]:
            stats["tags_distribution"][tag] = stats["tags_distribution"].get(tag, 0) + 1

    return stats
