"""Import saved email files into the knowledge database."""

from pathlib import Path

from database import add_knowledge
from imports.mail_parser import extract_mail_chunks
from retrieval import create_embedding


def import_mail_to_database(file_path: str) -> int:
    """Import an EML file to database.
    
    Args:
        file_path: Path to the EML file.

    Returns:
        The number of chunks added to the database.
    """

    chunks = extract_mail_chunks(file_path)

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