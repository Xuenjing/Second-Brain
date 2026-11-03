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
        
        self.assertEqual(
            results,
            {
                "used_sources": [],
                "additional_sources": [],
                "less_relevant_sources": [],
            }
        )


    def test_results_are_sorted_by_similarity(self):
        '''
        Test similarity sorting by faking embedding and get_all_knowledge
        '''

        results = [
            {
                "text": "Medium match",
                "source": "test",
                "score": 0.7,
                "semantic_score": 0.7
            },
            {
                "text": "Best match",
                "source": "test",
                "score": 0.9,
                "semantic_score": 0.9
            }
        ]

        ranked_results = retrieval.filter_and_rank_results(results, similarity_threshold=0.45, top_k=5)

        self.assertEqual(ranked_results[0]["text"], "Best match")
        self.assertEqual(ranked_results[1]["text"], "Medium match")


    def test_results_below_threshold_are_filtered(self):
        '''
        Test that all similarity scores below the threshold are filtered out
        '''

        results = [
            {
                "text": "Relevant",
                "source": "test",
                "score": 0.8,
                "semantic_score": 0.8
            },
            {
                "text": "Irrelevant",
                "source": "test",
                "score": 0.3,
                "semantic_score": 0.3
            }
        ]

        filtered_results = retrieval.filter_and_rank_results(results, similarity_threshold=0.45, top_k=5)

        self.assertEqual(len(filtered_results), 1)
        self.assertEqual(filtered_results[0]["text"], "Relevant")


    def test_retrieve_returns_max_top_k_results(self):
        '''
        Return top_k (=5) entries
        '''
        results = [
            {"text": "Post 1", "source": "test", "score": 0.99, "semantic_score": 0.99},
            {"text": "Post 2", "source": "test", "score": 0.98, "semantic_score": 0.98},
            {"text": "Post 3", "source": "test", "score": 0.97, "semantic_score": 0.97},
            {"text": "Post 4", "source": "test", "score": 0.96, "semantic_score": 0.96},
            {"text": "Post 5", "source": "test", "score": 0.95, "semantic_score": 0.95},
            {"text": "Post 6", "source": "test", "score": 0.94, "semantic_score": 0.94},
        ]

        ranked_results = retrieval.filter_and_rank_results(results, similarity_threshold=0.45, top_k=5)

        self.assertEqual(len(ranked_results), 5) # only 5 should be returned if top_k = 5
        
        # lowest-ranked result should not be included because top_k = 5
        self.assertNotIn("Post 6", [result["text"] for result in ranked_results])


    def test_results_are_filtered_by_semantic_score_but_ranked_by_hybrid_score(self):
        """Verify that results are filtered by semantic score, but ranked by hybrid score."""
        results = [
            {"score": 1.05, "semantic_score": 0.85},
            {"score": 0.9, "semantic_score": 0.9},
            {"score": 1.10, "semantic_score": 0.4},
        ] 

        ranked_results = retrieval.filter_and_rank_results(results, similarity_threshold=0.82, top_k=5)

        self.assertEqual(len(ranked_results), 2)
        self.assertEqual(ranked_results[0]["score"], 1.05)
        self.assertEqual(ranked_results[1]["score"], 0.90)


    def test_split_retrieval_results(self):
        """ Verify that results are split into three different dictionaries."""
        results = [
            {"text": "Best", "score": 0.95, "semantic_score": 0.95},
            {"text": "Second", "score": 0.90, "semantic_score": 0.90},
            {"text": "Extra", "score": 0.85, "semantic_score": 0.85},
            {"text": "Below threshold", "score": 0.70, "semantic_score": 0.70},
        ]

        ranked_results = retrieval.rank_results(results)

        used_sources, additional_sources, less_relevant_sources = (
            retrieval.split_retrieval_results(
                ranked_results,
                similarity_threshold=0.82,
                top_k=2,
            )
        )

        self.assertEqual(len(used_sources), 2)
        self.assertEqual(used_sources[0]["text"], "Best")
        self.assertEqual(used_sources[1]["text"], "Second")

        self.assertEqual(len(additional_sources), 1)
        self.assertEqual(additional_sources[0]["text"], "Extra")

        self.assertEqual(len(less_relevant_sources), 1)
        self.assertEqual(
            less_relevant_sources[0]["text"],
            "Below threshold",
        )


if __name__ == "__main__":
    unittest.main()
