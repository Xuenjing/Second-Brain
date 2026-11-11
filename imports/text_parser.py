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
        raise FileNotFoundError(
            "text_parser.file_not_found"
        )
    if path.suffix.lower() != ".txt":
        raise ValueError(
            "text_parser.invalid_file_type"
        )

    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as error:
        raise ValueError(
            "text_parser.invalid_encoding"
        ) from error
    except OSError as error:
        raise ValueError(
            "text_parser.read_failed"
        ) from error

    if not text.strip():
        raise ValueError(
            "text_parser.empty_file"
        )

    chunks = [
        chunk.strip()
        for chunk in text.split("\n\n")
        if chunk.strip()
    ]

    return chunks
