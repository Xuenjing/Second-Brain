"""
Run from project root:
python -m tests.docx_tests
"""

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from docx import Document

from imports.document_importer import import_docx_to_database
from imports.document_parser import extract_docx_chunks


class TestDocxParser(unittest.TestCase):
    """Test DOCX parsing and import functionality."""

    def setUp(self) -> None:
        self.temp_dir = TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_extract_paragraphs(self) -> None:
        file_path = self.temp_path / "test.docx"

        document = Document()
        document.add_paragraph("First paragraph")
        document.add_paragraph("Second paragraph")
        document.save(file_path)

        chunks = extract_docx_chunks(str(file_path))

        self.assertEqual(chunks, ["First paragraph", "Second paragraph"])

    def test_extract_table(self) -> None:
        file_path = self.temp_path / "test.docx"

        document = Document()

        table = document.add_table(rows=3, cols=2)
        table.cell(0, 0).text = "Room"
        table.cell(0, 1).text = "Capacity"
        table.cell(1, 0).text = "Atlas"
        table.cell(1, 1).text = "60"
        table.cell(2, 0).text = "Orion"
        table.cell(2, 1).text = "12"

        document.save(file_path)

        chunks = extract_docx_chunks(str(file_path))

        self.assertEqual(
            chunks, 
            [
                "Room | Capacity\n"
                "Atlas | 60\n"
                "Orion | 12"
            ],
        )

    def test_extract_paragraphs_and_tables(self) -> None:
        file_path = self.temp_path / "test.docx"

        document = Document()
        document.add_paragraph("First paragraph")
        document.add_paragraph("Second paragraph")

        table = document.add_table(rows=3, cols=2)
        table.cell(0, 0).text = "Room"
        table.cell(0, 1).text = "Capacity"
        table.cell(1, 0).text = "Atlas"
        table.cell(1, 1).text = "60"
        table.cell(2, 0).text = "Orion"
        table.cell(2, 1).text = "12"

        document.save(file_path)

        chunks = extract_docx_chunks(str(file_path))

        self.assertEqual(
            chunks,
            [
                "First paragraph",
                "Second paragraph",
                "Room | Capacity\nAtlas | 60\nOrion | 12",
            ],
        )

    def test_empty_paragraphs_are_ignored(self) -> None:
        file_path = self.temp_path / "test.docx"
        
        document = Document()
        document.add_paragraph("First paragraph")
        document.add_paragraph("")
        document.add_paragraph("  ")
        document.add_paragraph("Second paragraph")

        document.save(file_path)

        chunks = extract_docx_chunks(str(file_path))

        self.assertEqual(chunks, ["First paragraph", "Second paragraph"])

    def test_missing_file_raises_error(self) -> None:
        file_path = self.temp_path / "test.docx"

        with self.assertRaises(FileNotFoundError):
            extract_docx_chunks(str(file_path))

    def test_wrong_file_extension_raises_error(self) -> None:
        file_path = self.temp_path / "test.txt"
        file_path.write_text("Not a DOCX file.", encoding="utf-8")

        with self.assertRaises(ValueError):
            extract_docx_chunks(str(file_path))

    def test_invalid_docx_raises_error(self) -> None:
        file_path = self.temp_path / "test.docx"
        file_path.write_text("This is not a real DOCX file.", encoding="utf-8")

        with self.assertRaises(ValueError):
            extract_docx_chunks(str(file_path))

    @patch("imports.document_importer.add_knowledge")
    @patch("imports.document_importer.create_embedding")
    @patch("imports.document_importer.extract_docx_chunks")
    def test_import_docx_to_database(self, 
        mock_extract, 
        mock_embeddings, 
        mock_add_knowledge
    ) -> None:
        mock_extract.return_value = ["First paragraph", "Second paragraph"]
        mock_embeddings.return_value = [0.1, 0.2, 0.3]
        mock_add_knowledge.return_value = True

        added_count = import_docx_to_database("test.docx")
        self.assertEqual(added_count, 2)

    @patch("imports.document_importer.add_knowledge")
    @patch("imports.document_importer.create_embedding")
    @patch("imports.document_importer.extract_docx_chunks")
    def test_import_docx_counts_only_added_entries(
        self,
        mock_extract,
        mock_embeddings,
        mock_add_knowledge
    ) -> None:
        mock_extract.return_value = [
            "First paragraph", 
            "Second paragraph", 
            "Third paragraph"
        ]

        mock_embeddings.return_value = [0.1, 0.2, 0.3]

        mock_add_knowledge.side_effect = [
            True,
            False,
            True
        ]

        added_count = import_docx_to_database("test.docx")

        self.assertEqual(added_count, 2)

    @patch("imports.document_importer.add_knowledge")
    @patch("imports.document_importer.create_embedding")
    @patch("imports.document_importer.extract_docx_chunks")
    def test_import_docx_uses_filename_as_source(
        self,
        mock_extract,
        mock_embeddings,
        mock_add_knowledge
    ) -> None:
        mock_extract.return_value = ["First paragraph"]
        mock_embeddings.return_value = [0.1, 0.2, 0.3]
        mock_add_knowledge.return_value = True

        import_docx_to_database("documents/test.docx")

        mock_add_knowledge.assert_called_once_with(
            "First paragraph", 
            [0.1, 0.2, 0.3], 
            source="test.docx"
        )

    @patch("imports.document_importer.add_knowledge")
    @patch("imports.document_importer.create_embedding")
    @patch("imports.document_importer.extract_docx_chunks")
    def test_import_docx_creates_embeddings_for_each_chunk(
        self,
        mock_extract,
        mock_embedding,
        mock_add_knowledge
    ) -> None:
        mock_extract.return_value = [
            "First paragraph",
            "Second paragraph",
            "Third paragraph"
        ]
        mock_embedding.return_value = [0.1, 0.2, 0.3]
        mock_add_knowledge.return_value = True

        import_docx_to_database("test.docx")

        self.assertEqual(mock_embedding.call_count, 3)
        mock_embedding.assert_any_call("First paragraph")
        mock_embedding.assert_any_call("Second paragraph")
        mock_embedding.assert_any_call("Third paragraph")

    @patch("imports.document_importer.add_knowledge")
    @patch("imports.document_importer.create_embedding")
    @patch("imports.document_importer.extract_docx_chunks")
    def test_import_docx_with_empty_chunks_list(
        self,
        mock_extract,
        mock_embedding,
        mock_add_knowledge
    ) -> None:

        mock_extract.return_value = []

        added_count = import_docx_to_database("test.docx")

        self.assertEqual(added_count, 0)
        mock_embedding.assert_not_called()
        mock_add_knowledge.assert_not_called()


if __name__ == "__main__":
    unittest.main()