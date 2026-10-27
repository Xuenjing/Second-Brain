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
        raise FileNotFoundError("The selected backup file does not exist.")

    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)

    except json.JSONDecodeError as error:
        raise ValueError("The selected file is not a valid JSON") from error

    if not isinstance(data, list):
        raise ValueError("The backup file must contain a list of knwoledge entries.")

    validated_entries = []

    for item in data:
        if not isinstance(item, dict):
            raise ValueError("Each knowledge entry must be a JSON object.")

        required_fields = {
            "text",
            "source",
            "created_at"
        }

        if not required_fields.issubset(item):
            raise ValueError("One or more knowledge entries missing required fields")

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