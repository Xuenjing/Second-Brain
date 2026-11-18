import json
from pathlib import Path

from retrieval import create_embedding
from database import add_knowledge


def load_knowledge_from_json(file_path: str) -> list[dict]:
    """Load and verify knowledge entries from a JSON backup file.

    Args:
        file_path: Path to the JSON backup file.
    
    Returns:
        A list of validated knowledge entries.
    
    Raises:
        FileNotFoundError: If the selected file does not exist.
        ValueError: If the file is not a valid JSON file or has an invalid structure.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            "json_importer.file_not_found"
        )

    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)

    except json.JSONDecodeError as error:
        raise ValueError(
            "json_importer.invalid_json"
        ) from error

    if not isinstance(data, list):
        raise ValueError(
            "json_importer.invalid_root"
        )

    validated_entries = []

    for item in data:
        if not isinstance(item, dict):
            raise ValueError(
                "json_importer.invalid_entry"
            )

        required_fields = {
            "text",
            "source",
            "created_at"
        }

        if not required_fields.issubset(item):
            raise ValueError(
                "json_importer.missing_fields"
            )

        # Validate field types before importing any entries.
        if not all(
            isinstance(item[field], str)
            for field in required_fields
        ):
            raise ValueError(
                "json_importer.invalid_entry"
            )

        # Reject empty text, including whitespace-only values.
        if not item["text"].strip():
            raise ValueError(
                "json_importer.invalid_entry"
            )

        validated_entries.append({
            "text": item["text"],
            "source": item["source"],
            "created_at": item["created_at"]
        })

    return validated_entries


def import_knowledge_from_json_file(file_path: str) -> tuple[int, int]:
    """Import knowledge entries from a JSON backup file.

    Args:
        file_path: Path to the JSON backup file.

    Returns:
        Tuple containing: number of imported entries and skipped duplicate entries
    """

    entries = load_knowledge_from_json(file_path)

    imported_count = 0
    skipped_count = 0

    for item in entries:
        embedding = create_embedding(item["text"])

        added = add_knowledge(
            item["text"],
            embedding,
            source=item["source"]
        )

        if added:
            imported_count += 1
        else:
            skipped_count += 1

    return imported_count, skipped_count