from pathlib import Path


def extract_txt_chunks(file_path: str) -> list[str]:
    """Extract text chunks from a UTF-8 txt file.
    
    Text is split into chunks based on paragraphs.
    
        Args:
            file_path: File path to the text file.

        Returns:
            A list of text chunks.

        Raises:
            FileNotFoundError: If file does not exist.
            ValueError: If the file is not a text file,
                cannot be read as UTF-8, or is empty.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    if path.suffix.lower() != ".txt":
        raise ValueError("File must be a txt file.")

    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeEncodeError as error:
        raise ValueError("The file could not be read as UTF-8") from error
    except OSError as error:
        raise ValueError("The file could not be read.") from error

    chunks = [
        chunk.strip()
        for chunk in text.split("\n\n")
        if chunk.strip()
    ]

    return chunks
