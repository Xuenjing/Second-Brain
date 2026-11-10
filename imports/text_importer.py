from pathlib import Path

from database import add_knowledge
from imports.text_parser import extract_txt_chunks
from retrieval import create_embedding

def read_txt_for_preview(file_path: str) -> str:
    """Read a UTF-8 text file for review without saving it.

    Args:
        file_path: Local path to the text file.

    Returns:
        Original text with line breaks preserved.

    Raises:
        OSError: If the file cannot be read.
        ValueError: If the encoding is unsupported or the file is empty.
    """
    path = Path(file_path)

    try:
        # Accept UTF-8 files both with and without a byte-order mark.
        text = path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError as error:
        raise ValueError(
            "document_import.invalid_encoding"
        ) from error

    if not text.strip():
        raise ValueError("document_import.empty_file")

    return text

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