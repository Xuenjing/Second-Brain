"""Extract the subject and plain text from an EML or MSG file."""

from email import policy
from email.parser import BytesParser
from pathlib import Path
from html.parser import HTMLParser

import re
import extract_msg

class MailHTMLParser(HTMLParser):
    """Extract readable text from an HTML email."""

    BLOCK_TAGS = {
        "address", "article", "blockquote", "div", "dl",
        "dt", "dd", "footer", "h1", "h2", "h3", "h4",
        "h5", "h6", "header", "hr", "li", "ol", "p",
        "pre", "section", "table", "tr", "ul"
    }

    IGNORED_TAGS = {"head", "script", "style"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.ignored_depth = 0

    def handle_starttag(self, tag: str, attrs: list) -> None:
        if tag in self.IGNORED_TAGS:
            self.ignored_depth += 1

        if self.ignored_depth:
            return

        if tag == "br" or tag in self.BLOCK_TAGS:
            self.parts.append("\n")
        elif tag in {"td", "th"}:
            self.parts.append(" ")

    def handle_endtag(self, tag: str) -> None:
        if tag in self.IGNORED_TAGS:
            self.ignored_depth = max(0, self.ignored_depth - 1)
            return

        if self.ignored_depth:
            return

        if tag in self.BLOCK_TAGS:
            self.parts.append("\n")
        elif tag in {"td", "th"}:
            self.parts.append(" ")

    def handle_data(self, data: str) -> None:
        if not self.ignored_depth:
            # HTML source formatting should not create extra line breaks.
            self.parts.append(re.sub(r"\s+", " ", data))


def html_to_text(html: str) -> str:
    """Convert HTML to plain text while retaining paragraph breaks."""
    parser = MailHTMLParser()
    parser.feed(html)
    parser.close()

    text = "".join(parser.parts)

    # Normalize spaces within lines and limit consecutive line breaks.
    lines = [
        re.sub(r"[^\S\n]+", " ", line).strip()
        for line in text.split("\n")
    ]

    return re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip()

def extract_mail_chunks(file_path: str) -> list[str]:
    """Extract the subject and plain text from an EML or MSG file.

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
    """Read the subject and body from an EML file.

    Prefer plain text and convert HTML when plain text is unavailable.
    Attachments are ignored.

    Args:
        path: Path to the EML file.

    Returns:
        The subject and email text.

    Raises:
        ValueError: If the file cannot be read or decoded,
            or has no supported email body.
    """
    try:
        with path.open("rb") as file:
            message = BytesParser(policy=policy.default).parse(file)
    except OSError as error:
        raise ValueError("The file could not be read.") from error

    # Prefer plain text, fall back to HTML, and ignore attachments.
    body = message.get_body(preferencelist=("plain", "html"))

    if body is None:
        raise ValueError("No plain text or HTML was found in the email.")

    try:
        text = body.get_content()
    except (UnicodeError, LookupError) as error:
        raise ValueError(
            "The email text could not be decoded."
        ) from error

    if body.get_content_type() == "text/html":
        text = html_to_text(text)

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