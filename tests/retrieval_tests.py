import unittest
from unittest.mock import patch

import retrieval

'''
run from project root
python -m tests.retrieval_tests
'''

class TestRetrieval(unittest.TestCase):
    
    @patch("retrieval.get_all_knowledge") # use a fake version of get_all_knowledge
    
    def test_retrieve_empty_knowledge(self, mock_get_all_knowledge):
        '''
        Test empty retrieval by faking an empty list within get_all_knowledge
        '''

        # mocked/faked version returns an empty list
        mock_get_all_knowledge.return_value  = []

        # real function sees that the list is empty
        results = retrieval.retrieve_knowledge("Test question")
        
        self.assertEqual(results, []) # True if empty list

    @patch("retrieval.model.encode") # use mocked embedding
    @patch("retrieval.get_all_knowledge")
    def test_results_are_sorted_by_similarity(self, mock_get_all_knowledge, mock_encode):
        '''
        Test similarity sorting by faking embedding and get_all_knowledge
        '''

        mock_get_all_knowledge.return_value = [
            {
                "text": "Medium match",
                "source": "test",
                "embedding": [0.8, 0.6]
            },
            {
                "text": "Best match",
                "source": "test",
                "embedding": [1.0, 0.0]
            }
        ]

        mock_encode.return_value = [1.0, 0.0] # fake

        results = retrieval.retrieve_knowledge("Test question")

        self.assertEqual(results[0]["text"], "Best match")
        self.assertEqual(results[1]["text"], "Medium match")

    @patch("retrieval.model.encode")
    @patch("retrieval.get_all_knowledge")
    def test_results_below_threshold_are_filtered(self, mock_get_all_knowledge, mock_encode):
        '''
        Test that all similarity scores below the threshold are filtered out
        '''

        mock_get_all_knowledge.return_value = [
            {
                "text": "Relevant",
                "source": "test",
                "embedding": [1.0, 0.0] # should be kept
            },
            {
                "text": "Irrelevant",
                "source": "test",
                "embedding": [0.0, 1.0] # should be filtered out
            }
        ]

        mock_encode.return_value = [1.0, 0.0]
        results = retrieval.retrieve_knowledge("Test question")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["text"], "Relevant")

    @patch("retrieval.model.encode")
    @patch("retrieval.get_all_knowledge")
    def test_retrieve_returns_max_top_k_results(self, mock_get_all_knowledge, mock_encode):
        '''
        Return top_k (=5) entries
        '''
        mock_get_all_knowledge.return_value = [
            {"text": "Post 1", "source": "test", "embedding": [1.0, 0.0]},
            {"text": "Post 2", "source": "test", "embedding": [0.99, 0.1]},
            {"text": "Post 3", "source": "test", "embedding": [0.98, 0.2]},
            {"text": "Post 4", "source": "test", "embedding": [0.97, 0.25]},
            {"text": "Post 5", "source": "test", "embedding": [0.96, 0.3]},
            {"text": "Post 6", "source": "test", "embedding": [0.95, 0.31]},            
        ]

        mock_encode.return_value = [1.0, 0.0]

        results = retrieval.retrieve_knowledge("Test question")

        self.assertEqual(len(results), 5) # only 5 should be returned if top_k = 5
        
        # lowest-ranked result should not be included because top_k = 5
        self.assertNotIn("Post 6", [result["text"] for result in results]) 


if __name__ == "__main__":
    unittest.main()
