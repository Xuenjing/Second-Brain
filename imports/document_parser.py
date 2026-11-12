from pathlib import Path
from zipfile import BadZipFile

from docx import Document
from docx.table import Table
from docx.text.paragraph import Paragraph


def extract_docx_chunks(file_path: str) -> list[str]:
    """Extract text from a docx file (paragraphs and tables).
    Paragraphs become individual chunks.
    Tables become one multi-line chunk.

    Args:
        file_path: File path to the docx file.

    Returns:
        A list of chunks.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file is not a valid docx document.
    """

    path = Path(file_path)

    # Safeguards.
    if not path.exists():
        raise FileNotFoundError(
            "document_parser.file_not_found"
        )
    if path.suffix.lower() != ".docx":
        raise ValueError(
            "document_parser.invalid_file_type"
        )

    try:
        document = Document(path)
    except BadZipFile as error:
        raise ValueError(
            "document_parser.invalid_document"
        ) from error

    chunks = []

    # Read paragraphs and tables in document order.
    for block in document.iter_inner_content():
        if isinstance(block, Paragraph):
            text = block.text.strip()

            if text:
                chunks.append(text)

        elif isinstance(block, Table):
            table_rows = []

            for row in block.rows:
                cells = [
                    cell.text.strip()
                    for cell in row.cells
                ]

                if any(cells):
                    table_rows.append(" | ".join(cells))

            if table_rows:
                table_text = "\n".join(table_rows)
                chunks.append(table_text)

    return chunks


def split_docx_text(text: str) -> list[str]:
    """Split reviewed DOCX text at paragraph and table boundaries."""
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    chunks = [
        chunk.strip()
        for chunk in text.split("\f")
        if chunk.strip()
    ]

    return chunks


def read_docx_for_preview(file_path: str) -> str:
    """Read DOCX text for review without saving it.

    Args:
        file_path: Path to the DOCX file.

    Returns:
        Extracted text with form-feed characters separating paragraphs
        and tables.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the document is invalid or contains no text.
    """
    chunks = extract_docx_chunks(file_path)

    if not chunks:
        raise ValueError("document_parser.no_text")

    return "\n\f\n".join(chunks)