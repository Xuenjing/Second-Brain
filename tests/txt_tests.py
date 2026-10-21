"""
Run from project root:
python -m tests.txt_tests
"""

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from imports.text_importer import import_txt_to_database
from imports.text_parser import extract_txt_chunks


class testTxtParser(unittest.TestCase):

    def test_extract_txt_chunks(self):
        """Extract paragraphs from a valid TXT file."""

        with TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "test.txt"

            file_path.write_text(
                "First paragraph.\n\nSecond paragraph.", 
                encoding="utf-8")

            chunks = extract_txt_chunks(file_path)
        
        self.assertEqual(chunks, ["First paragraph.", "Second paragraph."])

    def test_missing_txt_file_raises_error(self):
        """Raise FileNotFoundError when the TXT file does not exist."""

        with TemporaryDirectory() as temp_file:
            file_path = Path(temp_file) / "missing.txt"

            with self.assertRaises(FileNotFoundError):
                extract_txt_chunks(file_path)

    def test_wrong_file_extension_raises_error(self):
        """Raise ValueError when the file is not a TXT file."""

        with TemporaryDirectory() as temp_file:
            file_path = Path(temp_file) / "wrong_file.pdf"

            file_path.write_text(
                "This is not a TXT file.",
                encoding="utf-8"
            )

            with self.assertRaises(ValueError):
                extract_txt_chunks(file_path)

    def test_empty_txt_file_raises_error(self):
        """Raise ValueError when the TXT file is empty."""

        with TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "empty.txt"
            file_path.write_text("", encoding="utf-8")

            with self.assertRaises(ValueError):
                extract_txt_chunks(file_path)

    def test_invalid_utf8_raises_error(self):
        """Raise ValueError when a TXT file is not a valid UTF-8."""

        with TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "invalid_utf8.txt"
            
            # Writes raw bytes which is invalid UTF-8.
            file_path.write_bytes(b"\xff\xfe\xfa")

            with self.assertRaises(ValueError):
                extract_txt_chunks(file_path)

    @patch("imports.text_importer.add_knowledge")
    @patch("imports.text_importer.create_embedding")
    @patch("imports.text_importer.extract_txt_chunks")
    def test_import_txt_to_database(
        self,
        mock_extract_chunks,
        mock_create_embedding,
        mock_add_knowledge
    ):
        """Import all extracted TXT chunks into the database."""

        mock_extract_chunks.return_value = [
            "First paragraph.",
            "Second paragraph."
        ]

        mock_create_embedding.return_value = [0.1, 0.2, 0.3]

        mock_add_knowledge.return_value = True

        added_count = import_txt_to_database("test.txt")

        self.assertEqual(added_count, 2)
        self.assertEqual(mock_create_embedding.call_count, 2)
        self.assertEqual(mock_add_knowledge.call_count, 2)

    @patch("imports.text_importer.add_knowledge")
    @patch("imports.text_importer.create_embedding")
    @patch("imports.text_importer.extract_txt_chunks")
    def test_import_txt_counts_only_added_chunks(
            self,
            mock_extract_chunks,
            mock_create_embedding,
            mock_add_knowledge
    ):
        """Count only TXT chunks that were added."""

        mock_extract_chunks.return_value = [
            "First paragraph.",
            "Second paragraph.",
            "Third paragraph."
        ]

        mock_create_embedding.return_value = [0.1, 0.2, 0.3]

        mock_add_knowledge.side_effect = [
            True,
            False,
            True
        ]

        added_count = import_txt_to_database("test.txt")

        self.assertEqual(added_count, 2)

    @patch("imports.text_importer.add_knowledge")
    @patch("imports.text_importer.create_embedding")
    @patch("imports.text_importer.extract_txt_chunks")
    def test_import_txt_uses_filename_as_source(
        self,
        mock_extract_chunks,
        mock_create_embedding,
        mock_add_knowledge
    ):
        """Use the TXT filename as the knowledge source."""

        mock_extract_chunks.return_value = [
            "First paragraph."
        ]

        mock_create_embedding.return_value = [0.1, 0.2, 0.3]

        mock_add_knowledge.return_value = True

        import_txt_to_database("test.txt")

        mock_add_knowledge.assert_called_once_with(
            "First paragraph.",
             [0.1, 0.2, 0.3],
             source="test.txt")


if __name__ == "__main__":
    unittest.main()

# parser happy path
# saknad fil
# fel filtyp
# tom fil
# ogiltig UTF-8
# importer lägger till alla chunks
# importer räknar bara faktiskt nya poster
# importer använder rätt filnamn som source