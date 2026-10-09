import unittest
import tempfile
from pathlib import Path
import numpy as np
import time

import database

'''
run from project root
python -m tests.database_test
'''

class TestDatabase(unittest.TestCase):

    # creates a temporary database before each test
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

        database.DATABASE_PATH = str (Path(self.temp_dir.name) / "test_knowledge.db")

        database.initialize_database()

    # deletes the database after every test
    def tearDown(self):
        self.temp_dir.cleanup()

    # adds knowledge to the fake database
    def test_add_knowledge(self):
        embedding = np.array([0.1, 0.2, 0.3]) # fake embedding for testing

        added = database.add_knowledge(
            "Test knowledge",
            embedding,
            source="test"
        )

        knowledge = database.get_all_knowledge()

        self.assertTrue(added) # did add_knowledge return True?
        self.assertEqual(len(knowledge), 1) # is there exactly one post?
        self.assertEqual(knowledge[0]["text"], "Test knowledge") # does the post contain the added text?

    def test_add_duplicate_knowledge(self):
        embedding = np.array([0.1, 0.2, 0.3])

        first_add = database.add_knowledge(
            "Test knowledge",
            embedding,
            source="test"
        )

        second_add = database.add_knowledge(
            "Test knowledge",
            embedding,
            source="test"
        )

        knowledge = database.get_all_knowledge()

        self.assertTrue(first_add)
        self.assertFalse(second_add)
        self.assertEqual(len(knowledge), 1)

    def test_delete_knowledge(self):
        embedding = np.array([0.1, 0.2, 0.3]) # fake embedding for testing

        added = database.add_knowledge(
            "Test knowledge",
            embedding,
            source="test"
        )

        knowledge = database.get_all_knowledge()
        knowledge_id = knowledge[0]["id"]

        deleted = database.delete_knowledge(knowledge_id)

        knowledge_after_delete = database.get_all_knowledge()

        self.assertTrue(deleted) # true
        self.assertEqual(len(knowledge_after_delete), 0)

    def test_delete_non_existing_knowledge(self):
        deleted = database.delete_knowledge(999)

        self.assertFalse(deleted)

    def test_edit_knowledge(self):

        original_embedding = np.array([0.1, 0.2, 0.3])

        database.add_knowledge(
            "Original knowledge",
            original_embedding,
            source="test"
        )

        knowledge = database.get_all_knowledge()
        knowledge_id = knowledge[0]["id"]

        new_embedding = np.array([0.4, 0.5, 0.6])

        updated = database.edit_knowledge(
            knowledge_id,
            "Updated knowledge",
            new_embedding,
        )

        updated_knowledge = database.get_all_knowledge()

        self.assertTrue(updated) # True
        self.assertEqual(updated_knowledge[0]["text"], "Updated knowledge") # True
        self.assertEqual(updated_knowledge[0]["embedding"], [0.4, 0.5, 0.6])


    def test_search_knowledge(self):
        embedding = np.array([0.1, 0.2, 0.3])

        database.add_knowledge(
            "Python is a programming language",
            embedding,
            source="manual"
        )

        database.add_knowledge(
            "The school opens at 8.00AM",
            embedding,
            source="school.txt"
        )

        results = database.search_knowledge("Python")

        self.assertEqual(len(results), 1) # 1 search result
        self.assertEqual(results[0]["text"], "Python is a programming language")

    def test_get_all_knowledge_sort_order(self):
        embedding = np.array([0.1, 0.2, 0.3])
        database.add_knowledge(
            "First post",
            embedding,
            source="test"
        )

        time.sleep(0.01) # paus for slightly different time stamps

        database.add_knowledge(
            "Second post",
            embedding,
            source="test"
        )

        ascending = database.get_all_knowledge("asc")
        descending = database.get_all_knowledge("desc")

        self.assertEqual(ascending[0]["text"], "First post")
        self.assertEqual(ascending[1]["text"], "Second post")
        self.assertEqual(descending[0]["text"], "Second post")
        self.assertEqual(descending[1]["text"], "First post")




if __name__ == "__main__":
    unittest.main()