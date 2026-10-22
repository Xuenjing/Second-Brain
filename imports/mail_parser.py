"""Extract text from saved email files."""

from email import policy
from email.parser import BytesParser
from pathlib import Path


def extract_mail_chunks(file_path: str) -> list[str]:
    """Extract the subject and plain text from an EML file.

    Args:
        file_path: File path to the EML file.

    Returns:
        A list containing the email text.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file type is unsupported, the email
            cannot be read, or is empty.
    """
    path = Path(file_path)

    if not path.is_file():
        raise FileNotFoundError(f"File not found: {path}")

    if path.suffix.lower() != ".eml":
        raise ValueError("File must be an EML file.")

    try:
        with path.open("rb") as file:
            message = BytesParser(policy=policy.default).parse(file)
    except OSError as error:
        raise ValueError("The file could not be read.") from error

    # Get the plain text body and ignore attachments.
    body = message.get_body(preferencelist=("plain",))

    if body is None:
        raise ValueError("No plain text was found in the email.")

    try:
        text = body.get_content().strip()
    except (UnicodeError, LookupError) as error:
        raise ValueError("The email text could not be decoded.") from error

    if not text:
        raise ValueError("The email text is empty.")

    # Include the subject with the email text.
    subject = str(message.get("Subject", "")).strip()

    if subject:
        text = f"Ämne: {subject}\n\n{text}"

    return [text]