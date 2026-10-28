"""
Run from project root:
python -m tests.system_tests
"""

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import numpy as np

from database import(
    initialize_database,
    add_knowledge,
    get_all_knowledge,
    get_knowledge_by_id,
    edit_knowledge,
    delete_knowledge
)
from retrieval import create_embedding, retrieve_knowledge


class TestKnowledgeFlow(unittest.TestCase):

    def test_add_edit_delete_knowledge(self):
        """Test the main knowledge database functions."""

        with TemporaryDirectory() as temp_dir:
            database_path = Path(temp_dir) / "test_knowledge.db"

            with patch("database.DATABASE_PATH", str(database_path)):
                
                # Initializing
                initialize_database()

                # Added.
                original_embedding = np.array([0.1, 0.2, 0.3])
                added = add_knowledge(
                    "Original test knowledge",
                    original_embedding,
                    source="system test"
                )

                self.assertTrue(added)

                entries = get_all_knowledge()

                self.assertEqual(len(entries), 1)

                knowledge_id = entries[0]["id"]
                entry = get_knowledge_by_id(knowledge_id)

                self.assertIsNotNone(entry)
                self.assertEqual(entry["text"], "Original test knowledge")
                self.assertEqual(entry["source"], "system test")


                # Updated. 
                new_embedding = np.array([0.4, 0.5, 0.6])
                updated = edit_knowledge(
                    knowledge_id,
                    "Updated test knowledge",
                    new_embedding
                )

                self.assertTrue(updated)

                updated_entry = get_knowledge_by_id(knowledge_id)

                self.assertEqual(updated_entry["text"], "Updated test knowledge")

                # Deleted.
                deleted = delete_knowledge(knowledge_id)

                self.assertTrue(deleted)

                deleted_entry = get_knowledge_by_id(knowledge_id)

                self.assertIsNone(deleted_entry)


    def test_retrieval_finds_relevant_knowledge(self):
        """Stored knowledge can be retrieved from a language query."""

        with TemporaryDirectory() as temp_dir:
            database_path = Path(temp_dir) / "test_knowledge.db"

            with patch("database.DATABASE_PATH", str(database_path)):
                initialize_database()

                lunch_text = ("Huvudmatsalen serverar lunch mellan kl 11:00 och 14:00")
                lunch_embedding = create_embedding(lunch_text) 
                gym_text = ("Gymet stänger kl 20:00")
                gym_embedding = create_embedding(gym_text)

                add_knowledge(lunch_text, lunch_embedding, source="system_test")
                add_knowledge(gym_text, gym_embedding, source="system_test")

                results = retrieve_knowledge("När serverar Huvudmatsalen lunch?")

                self.assertGreater(len(results), 0)
                self.assertEqual(results[0]["text"], lunch_text)


    def test_retrieval_finds_updated_knowledge(self):
        """Edited knowledge can be retrieved using its updated content."""

        with TemporaryDirectory() as temp_dir:
            database_path = Path(temp_dir) / "test_knowledge.db"

            with patch("database.DATABASE_PATH", str(database_path)):
                initialize_database()

                original_text = ("Huvudmatsalen serverar lunch mellan kl 11:00 och 14:00")
                original_embedding = create_embedding(original_text)
                add_knowledge(
                    original_text,
                    original_embedding,
                    source="system_test"
                )
                entries = get_all_knowledge()
                knowledge_id = entries[0]["id"]

                # Verify that the original knowledge can be retrieved
                original_results = retrieve_knowledge("När serverar huvudmatsalen lunch?")

                self.assertGreater(len(original_results), 0)
                self.assertEqual(original_results[0]["text"], original_text)

                # Update both text and embedding.
                updated_text = "Huvudmatsalen serverar middag mellan 17:00 och 20:00"
                updated_embedding = create_embedding(updated_text)
                updated = edit_knowledge(
                    knowledge_id,
                    updated_text,
                    updated_embedding
                )

                self.assertTrue(updated)

                # Verify that retrieval finds the updated knowledge.
                updated_results = retrieve_knowledge("När serverar huvudmatsalen middag?")

                self.assertGreater(len(updated_results), 0)
                self.assertEqual(updated_results[0]["text"], updated_text)



if __name__ == "__main__":
    unittest.main()