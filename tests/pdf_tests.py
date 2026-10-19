"""
Run from project root:
python -m tests.pdf_tests
"""

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import MagicMock, patch

from pypdf.errors import PdfReadError

from imports.pdf_importer import import_pdf_to_database
from imports.pdf_parser import extract_pdf_chunks, looks_like_table


class TestPdfParser(unittest.TestCase):

    def test_looks_like_table(self):
        text = (
            "Room       Capacity\n"
            "Atlas      60\n"
            "Orion      12"
        )

        self.assertTrue(looks_like_table(text))
    
    def test_looks_like_table_returns_false(self):
        text = "This is a normal paragraph without spacing."

        self.assertFalse(looks_like_table(text))

    @patch("imports.pdf_parser.PdfReader")
    def test_extract_pdf_chunks(self, mock_pdf_reader):
        """Extract chunks from a mocked PDF page."""

        # Extract a fake PDF file and control what extract_text returns.
        mock_page = MagicMock()
        mock_page.extract_text.return_value = (
            "First paragraph.\n\nSecond paragraph."
        )

        # Create a fake PDF reader containing the mocked page.
        mock_reader = MagicMock()
        mock_reader.pages = [mock_page]

        # Make PdfReader return our fake reader instead of opening the file.
        mock_pdf_reader.return_value = mock_reader

        # Create a temporary .pdf file so file validation passes.
        with TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "test.pdf"
            file_path.touch()

            chunks = extract_pdf_chunks(file_path)

        self.assertEqual(
            chunks,
            ["First paragraph.", "Second paragraph."]
        )

    @patch("imports.pdf_parser.PdfReader")
    def test_extract_pdf_chunks_from_multiple_pages(self, mock_pdf_reader):
        """Extract chunks from multiple PDF pages."""

        first_page = MagicMock()
        first_page.extract_text.return_value = "First page paragraph."
        second_page = MagicMock()
        second_page.extract_text.return_value = "Second page paragraph."

        mock_reader = MagicMock()
        mock_reader.pages = [first_page, second_page]

        mock_pdf_reader.return_value = mock_reader

        with TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "test.pdf"
            file_path.touch()

            chunks = extract_pdf_chunks(file_path)

        self.assertEqual(
            chunks,
            ["First page paragraph.", "Second page paragraph."]
        )

    @patch("imports.pdf_parser.PdfReader")
    def test_empty_pdf_page_is_ignored(self, mock_pdf_reader):
        """Ignore PDF pages that contain no extractable text."""

        empty_page = MagicMock()
        empty_page.extract_text.return_value = ""

        mock_reader = MagicMock()
        mock_reader.pages = [empty_page]

        mock_pdf_reader.return_value = mock_reader

        with TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "test.pdf"
            file_path.touch()

            chunks = extract_pdf_chunks(file_path)

        self.assertEqual(chunks, [])

    def test_missing_pdf_file_raises_error(self):
        """Raise FileNotFoundError when the PDF file does not exist."""

        with TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "missing.pdf"

            with self.assertRaises(FileNotFoundError):
                extract_pdf_chunks(file_path)

    def test_wrong_file_extension_raises_error(self):
        """Raise ValueError when the file is not a .PDF file."""

        with TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "test.txt"
            file_path.write_text("This is not a PDF file.")

            with self.assertRaises(ValueError):
                extract_pdf_chunks(file_path)

    def test_invalid_pdf_raises_error(self):
        """Raise PdfReadError when this file is not a valid PDF file."""

        with TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "test.pdf"
            file_path.write_text("This is an invalid PDF file.")

            with self.assertRaises(PdfReadError):
                extract_pdf_chunks(file_path)

    @patch("imports.pdf_parser.PdfReader")
    def test_table_page_is_kept_as_single_chunk(self, mock_pdf_reader):
        """Keep table-like PDF text together as a single chunk."""

        mock_page = MagicMock()
        mock_page.extract_text.return_value = (
            "Room       Capacity\n\n"
            "Atlas      60\n\n"
            "Orion      12"
        )

        mock_reader = MagicMock()
        mock_reader.pages = [mock_page]

        mock_pdf_reader.return_value = mock_reader

        with TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "test.pdf"
            file_path.touch()
            chunks = extract_pdf_chunks(file_path)

        self.assertEqual(
            chunks,
            [
            "Room       Capacity\n\n"
            "Atlas      60\n\n"
            "Orion      12"                
            ]
        )

    @patch("imports.pdf_importer.add_knowledge")
    @patch("imports.pdf_importer.create_embedding")
    @patch("imports.pdf_importer.extract_pdf_chunks")
    def test_import_pdf_to_database(
        self,
        mock_extract_chunks,
        mock_create_embedding,
        mock_add_knowledge
    ):
        """Import all extracted PDF chunks into the database."""

        mock_extract_chunks.return_value = [
            "First paragraph.",
            "Second paragraph."
        ]

        mock_create_embedding.return_value = [0.1, 0.2, 0.3]

        mock_add_knowledge.return_value = True

        added_count = import_pdf_to_database("documents/test.pdf")

        self.assertEqual(added_count, 2)
        self.assertEqual(mock_create_embedding.call_count, 2)
        self.assertEqual(mock_add_knowledge.call_count, 2)

    @patch("imports.pdf_importer.add_knowledge")
    @patch("imports.pdf_importer.create_embedding")
    @patch("imports.pdf_importer.extract_pdf_chunks")
    def test_import_pdf_counts_only_added_entries(
        self,
        mock_extract_chunks,
        mock_create_embedding,
        mock_add_knowledge
    ):
        """Count only PDF chunks that are successfully added."""

        mock_extract_chunks.return_value = [
            "First paragraph.",
            "Second paragraph.",
            "Third paragraph."
        ]

        mock_create_embedding.return_value = [0.1, 0.2, 0.3]

        mock_add_knowledge.side_effect = [True, False, True]

        added_count = import_pdf_to_database("documents/test.pdf")

        self.assertEqual(added_count, 2)

    @patch("imports.pdf_importer.add_knowledge")
    @patch("imports.pdf_importer.create_embedding")
    @patch("imports.pdf_importer.extract_pdf_chunks")
    def test_import_pdf_uses_filename_as_source(
        self,
        mock_extract_chunks,
        mock_create_embedding,
        mock_add_knowledge
    ):
        """Use the PDF filename as the knowledge source."""

        mock_extract_chunks.return_value = ["First paragraph."]
        mock_create_embedding.return_value = [0.1, 0.2, 0.3]
        mock_add_knowledge.return_value = True

        import_pdf_to_database("documents/test.pdf")

        mock_add_knowledge.assert_called_once_with(
            "First paragraph.",
            [0.1, 0.2, 0.3],
            source="test.pdf"
        )

    @patch("imports.pdf_importer.add_knowledge")
    @patch("imports.pdf_importer.create_embedding")
    @patch("imports.pdf_importer.extract_pdf_chunks")
    def test_import_pdf_with_empty_chunks_list(
        self,
        mock_extract_chunks,
        mock_create_embedding,
        mock_add_knowledge
    ):
        """Do nothing when the PDF contains no extractable chunks."""

        mock_extract_chunks.return_value = []
        added_count = import_pdf_to_database("documents/test.pdf")

        self.assertEqual(added_count, 0)
        mock_create_embedding.assert_not_called()
        mock_add_knowledge.assert_not_called()

if __name__ == "__main__":
    unittest.main()