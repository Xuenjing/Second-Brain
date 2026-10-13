from pathlib import Path
from docx import Document
from zipfile import BadZipFile

def extract_docx_chunks(file_path: str) -> list[str]:
    '''
    Extract text from a docx file (paragraphs and tables).
    Paragraphs become individual chunks.
    Tables become one multi-line chunk.
    '''

    path = Path(file_path)

    # safeguards
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    if path.suffix.lower() != ".docx":
        raise ValueError(f"File must be a docx file")

    try: 
        document = Document(path)
    except BadZipFile as error:
        raise ValueError(f"The file is not a valid docx document.") from error

    chunks = []

    # extract regular paragraphs into chunks
    for paragraph in document.paragraphs:
        text = paragraph.text.strip()
        if text:
            chunks.append(text)

    # extract tables into one chunks
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