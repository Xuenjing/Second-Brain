import json
from pathlib import Path

from database import get_all_knowledge


def export_knowledge_to_json(file_path: str) -> int:
    """Export the entire database as a JSON file.

        Args:
            file_path: Destination path for the JSON file.
        
        Returns:
            Number of exported knowledge entries.
    """

    knowledge = get_all_knowledge("asc")

    export_data = []

    for item in knowledge:
        export_data.append({
            "id": item["id"],
            "text": item["text"],
            "source": item["source"],
            "created_at": item["created_at"]
        })

    path = Path(file_path)

    with path.open("w", encoding="utf-8") as file:
        json.dump(
            export_data,
            file,
            ensure_ascii=False,
            indent=4
        )

    return len(export_data)


# Testing purposes.
if __name__ == "__main__":
    n=export_knowledge_to_json("test_export.json")
    print(f"Antal poster sparade: {n}")

