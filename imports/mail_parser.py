"""Extract the subject and plain text from an EML or MSG file."""

from email import policy
from email.parser import BytesParser
from pathlib import Path

import extract_msg


def extract_mail_chunks(file_path: str) -> list[str]:
    """Extract the subject and plain text from an EML file.

    Args:
        file_path: File path to the EML or MSG file.

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

    extension = path.suffix.lower()

    if extension == ".eml":
        subject, text = read_eml(path)
    elif extension == ".msg":
        subject, text = read_msg(path)
    else:
        raise ValueError("File must be an EML or MSG file.")

    if not text.strip():
        raise ValueError("The email text is empty.")

    # Include the subject with the email text.
    text = text.strip()
    subject = subject.strip()

    if subject:
        text = f"Ämne: {subject}\n\n{text}"

    return [text]


def read_eml(path: Path) -> tuple[str, str]:
    """Read the subject and plain text from an EML file.

    Args:
        path: Path to the EML file.

    Returns:
        The subject and email text.

    Raises:
        ValueError: If the file cannot be read or decoded,
            or has no plain text body.
    """
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
        text = body.get_content()
    except (UnicodeError, LookupError) as error:
        raise ValueError(
            "The email text could not be decoded."
        ) from error

    subject = str(message.get("Subject", ""))

    return subject, text


def read_msg(path: Path) -> tuple[str, str]:
    """Read the subject and text from an MSG file.

    Args:
        path: Path to the MSG file.

    Returns:
        The subject and email text.

    Raises:
        ValueError: If the MSG file cannot be read.
    """
    try:
        # Close the file automatically after reading.
        with extract_msg.openMsg(str(path)) as message:
            subject = message.subject or ""
            text = message.body or ""
    except Exception as error:
        raise ValueError(
            "The MSG file could not be read."
        ) from error

    return subject, text