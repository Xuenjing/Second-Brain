from pathlib import Path

from retrieval import create_embedding
from database import add_knowledge
from imports.pdf_parser import extract_pdf_chunks


def import_pdf_to_database(file_path: str) -> int:
    """Import a PDF document to the database.

    Args:
        file_path: Path to the PDF file.

    Returns:
        The number of new chunks added to the database.
    """ 

    chunks = extract_pdf_chunks(file_path)

    added_count = 0
    source = Path(file_path).name

    for chunk in chunks:
        embedding = create_embedding(chunk)

        if add_knowledge(chunk, embedding, source=source):
            added_count += 1

    return added_count