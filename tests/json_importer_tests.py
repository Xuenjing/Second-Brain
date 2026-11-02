"""
Run from project root:
python -m tests.json_importer_tests
"""

"""
IMPORT
- giltig backup läses korrekt
- ogiltig JSON ger ValueError
- fel struktur ger ValueError
- dubletter hoppas över
- saknade poster importeras
- embeddings skapas för importerade poster

- gammalt id återanvänds inte
"""

import json
import unittest
from unittest.mock import patch
from pathlib import Path
from tempfile import TemporaryDirectory

from json_importer import load_knowledge_from_json, import_knowledge_from_json_file


class TestImporter(unittest.TestCase):

    def test_load_valid_backup(self):
        """Load a valid JSON backup."""

        with TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "import.json"
            

            data = [
                {
                    "id": 1,
                    "text": "Test knowledge",
                    "source": "manual",
                    "created_at": "2026-10-27T10:00:00"
                }
            ]

            with file_path.open("w", encoding="utf-8") as file:
                json.dump(data, file)

            entries = load_knowledge_from_json(file_path)

            self.assertEqual(len(entries), 1)
            self.assertEqual(entries[0]["text"], "Test knowledge")
            self.assertEqual(entries[0]["source"], "manual")
            self.assertEqual(entries[0]["created_at"], "2026-10-27T10:00:00")


    def test_invalid_import_gives_valueerror(self):
        """Load an invalid JSON file gives ValueError."""

        with TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "invalid.json"

            with file_path.open("w", encoding="utf-8") as file:
                file.write("Invalid JSON")

            with self.assertRaises(ValueError):
                load_knowledge_from_json(file_path)

            
    def test_invalid_structure_gives_valueerror(self):
        """Load a JSON file with invalid structure gives ValueError."""

        with TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "invalid_structure.json"

            data = {                
                    "id": 1,
                    "text": "Test knowledge",
                    "source": "manual",
                    "created_at": "2026-10-27T10:00:00"
            }

            with file_path.open("w", encoding="utf-8") as file:
                json.dump(data, file)

            with self.assertRaises(ValueError):
                load_knowledge_from_json(file_path)
            

    @patch("json_importer.create_embedding")
    @patch("json_importer.add_knowledge")
    def test_skip_doubles(self, mock_add_knowledge, mock_create_embedding):
        """Duplicate knowledge entries are counted as skipped."""

        mock_create_embedding.return_value = [0.1, 0.2, 0.3]

        # First entry added, second duplicate.
        mock_add_knowledge.side_effect = [True, False]

        with TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "skip_doubles.json"

            data = [
                {                
                    "id": 1,
                    "text": "Test knowledge",
                    "source": "manual",
                    "created_at": "2026-10-27T10:00:00"
            },
            {
                    "id": 2,
                    "text": "Test knowledge",
                    "source": "manual",
                    "created_at": "2026-10-27T10:00:00"
            }
            ]

            with file_path.open("w", encoding="utf-8") as file:
                json.dump(data, file)

            imported_count, skipped_count = import_knowledge_from_json_file(file_path)

            self.assertEqual(imported_count, 1)
            self.assertEqual(skipped_count, 1)


    @patch("json_importer.create_embedding")
    @patch("json_importer.add_knowledge")
    def test_missing_entries_are_imported(self, mock_add_knowledge, mock_create_embedding):
        """A missing knowledge entry is imported."""

        mock_create_embedding.return_value = [0.1, 0.2, 0.3]
        mock_add_knowledge.returnv_vaule = True

        with TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "missing_entry.json"

            data = [
                {
                    "id": 1,
                    "text": "Missing knowledge",
                    "source": "manual",
                    "created_at": "2026-10-27T10:00:00"
                }
            ]

            with file_path.open("w", encoding="utf-8") as file:
                json.dump(data, file)

            imported_count, skipped_count = import_knowledge_from_json_file(file_path)

            self.assertEqual(imported_count, 1)
            self.assertEqual(skipped_count, 0)
            
            mock_create_embedding.assert_called_once_with("Missing knowledge")
            mock_add_knowledge.assert_called_once_with("Missing knowledge", [0.1, 0.2, 0.3], source="manual")


    @patch("json_importer.create_embedding")
    @patch("json_importer.add_knowledge")
    def test_previous_id_not_reused(self, mock_add_knowledge, mock_create_embedding):
        """The ID stored in the backup is not reused during import."""

        mock_create_embedding.return_value = [0.1, 0.2, 0.3]
        mock_add_knowledge.return_value = True

        with TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "old_id.json"

            data = [
                {
                    "id": 999,
                    "text": "Test knowledge",
                    "source": "manual",
                    "created_at": "2026-10-27T10:00:00"
                }
            ]

            with file_path.open("w", encoding="utf-8") as file:
                json.dump(data, file)

            import_knowledge_from_json_file(file_path)

            mock_add_knowledge.assert_called_once_with("Test knowledge", [0.1, 0.2, 0.3], source="manual")

if __name__ == "__main__":
    unittest.main()