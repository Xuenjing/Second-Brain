from pathlib import Path

from database import add_knowledge
from imports.text_parser import extract_txt_chunks
from retrieval import create_embedding


def import_txt_to_database(file_path: str) -> int:
    """Import a TXT file to database.
    
        Args:
            file_path: Path to the text file.

        Results:
            The number of chunks added to the database.
    """

    chunks = extract_txt_chunks(file_path)

    added_count = 0
    source = Path(file_path).name

    for chunk in chunks:
        embedding = create_embedding(chunk)

        if add_knowledge(
            chunk,
            embedding,
            source=source
        ):
            added_count += 1

    return added_count