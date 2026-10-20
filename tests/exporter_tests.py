"""
Run from project root:
python -m tests.exporter_tests
"""

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from exporter import export_knowledge_to_json


class TestExporter(unittest.TestCase):

    @patch("exporter.get_all_knowledge")
    def test_export_knowledge_to_json(self, mock_get_all_knowledge):
        """Export knowledge entries to JSON file."""

        mock_get_all_knowledge.return_value = [
            {
                "id": 1,
                "text": "First post",
                "source": "manual",
                "created_at": "2026-10-20T10:00:00"
            },
            {
                "id": 2,
                "text": "Second post",
                "source": "notes.txt",
                "created_at": "2026-10-20T11:00:00"
            }
        ]

        with TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "export.json"

            exported_count = export_knowledge_to_json(file_path)

            with file_path.open("r", encoding="utf-8") as file:
                exported_data = json.load(file)

        self.assertEqual(exported_count, 2)
        self.assertEqual(len(exported_data), 2)

    @patch("exporter.get_all_knowledge")
    def test_exported_json_contains_all_data(self, mock_get_all_knowledge):
        """Export the expected data."""

        mock_get_all_knowledge.return_value = [
            {
                "id": 1,
                "text": "åäö",
                "source": "manual",
                "created_at": "2026-10-20T11:00:00"
            }
        ]

        with TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "export.json"

            export_knowledge_to_json(file_path)

            with file_path.open("r", encoding="utf-8") as file:
                exported_data = json.load(file)

        self.assertEqual(exported_data[0]["id"], 1)
        self.assertEqual(exported_data[0]["text"], "åäö")
        self.assertEqual(exported_data[0]["source"], "manual")
        self.assertEqual(exported_data[0]["created_at"], "2026-10-20T11:00:00")

    @patch("exporter.get_all_knowledge")
    def test_export_empty_knowledge(self, mock_get_all_knowledge):
        """Export an empty JSON list when no knowledge entries exist."""

        mock_get_all_knowledge.return_value = []

        with TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "export.json"

            exported_count = export_knowledge_to_json(file_path)

            with file_path.open("r", encoding="utf-8") as file:
                exported_data = json.load(file)

        self.assertEqual(exported_count, 0)
        self.assertEqual(exported_data, [])

    @patch("exporter.get_all_knowledge")
    def test_export_requests_knowledge_in_ascending_order(self, mock_get_all_knowledge):
        """Request knowledge entries in ascending order."""

        mock_get_all_knowledge.return_value = []

        with TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "export.json"

            export_knowledge_to_json(file_path)

        mock_get_all_knowledge.assert_called_once_with("asc")


if __name__ == "__main__":
    unittest.main()
