from pathlib import Path

from retrieval import create_embedding
from database import add_knowledge
from imports.document_parser import extract_docx_chunks

def import_docx_to_database(file_path: str) -> int:
    """Import a DOCX document to the database.

    Args:
        file_path: Path to the DOCX file.

    Returns:
        The number of new chunks added to the database.
    """

    chunks = extract_docx_chunks(file_path)

    added_count = 0
    source = Path(file_path).name

    for chunk in chunks:
        embedding = create_embedding(chunk)

        if add_knowledge(chunk, embedding, source=source):
            added_count += 1

    return added_count