from pathlib import Path
from zipfile import BadZipFile

from docx import Document


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

    # Extract regular paragraphs into chunks.
    for paragraph in document.paragraphs:
        text = paragraph.text.strip()
        if text:
            chunks.append(text)

    # Extract each table into one chunk.
    for table in document.tables:
        table_rows = []

        for row in table.rows:
            cells = []

            for cell in row.cells:
                text = cell.text.strip()

                if text:
                    cells.append(text)

            if cells:
                table_rows.append(" | ".join(cells))

        if table_rows:
            table_text = "\n".join(table_rows)
            chunks.append(table_text)

    return chunks