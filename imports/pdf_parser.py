from pathlib import Path

from pypdf import PdfReader


def looks_like_table(text: str) -> bool:
    """Check whether extracted PDF text looks like a table.
    
    A line is table-like if it contains at least 3 white spaces.
    The text is considered table-like if at least 2 lines contain
    3 white spaces.

    Args:
        text: Text extracted from a PDF file.

    Returns:
        True if the text appears to contain a table, otherwise False.
    
    """

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    table_like_lines = [
        line
        for line in lines
        if "   " in line
    ]

    return len(table_like_lines) >= 2


def split_pdf_text(text: str) -> list[str]:
    """Split PDF text while keeping table-like pages together."""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    chunks = []

    for page_text in text.split("\f"):
        if not page_text.strip():
            continue

        if looks_like_table(page_text):
            chunks.append(page_text.strip())
        else:
            page_chunks = [
                chunk.strip()
                for chunk in page_text.split("\n\n")
                if chunk.strip()
            ]
            chunks.extend(page_chunks)

    return chunks


def extract_pdf_chunks(file_path: str) -> list[str]:
    """Extract text chunks from a PDF document.

    Text is extracted page by page and split into paragraph-based chunks.

    Args:
        file_path: Path to the PDF file.

    Returns:
        A list of extracted text chunks.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            "pdf_parser.file_not_found"
        )
    if path.suffix.lower() != ".pdf":
        raise ValueError(
            "pdf_parser.invalid_file_type"
        )
    
    reader = PdfReader(path)

    chunks = []

    for page in reader.pages:
        text = page.extract_text(extraction_mode="layout")

        if not text:
            continue

        if looks_like_table(text):
            chunks.append(text.strip())

        else:
            page_chunks = [
                chunk.strip() 
                for chunk in text.split("\n\n") 
                if chunk.strip()
            ]
        
            chunks.extend(page_chunks)

    return chunks


def read_pdf_for_preview(file_path: str) -> str:
    """Extract PDF text for review without saving it.

    Args:
        file_path: Path to the PDF file.

    Returns:
        Extracted text with form-feed characters marking page boundaries.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file type is invalid or no text is found.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError("pdf_parser.file_not_found")

    if path.suffix.lower() != ".pdf":
        raise ValueError("pdf_parser.invalid_file_type")

    reader = PdfReader(path)
    pages = []

    for page in reader.pages:
        text = page.extract_text(extraction_mode="layout")

        if text and text.strip():
            pages.append(text.strip())

    if not pages:
        raise ValueError("pdf_parser.no_text")

    return "\n\f\n".join(pages)