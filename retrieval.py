from typing import Any

import numpy as np

from database import get_all_knowledge
from performance import measure_time


_embedding_model: Any = None


def get_embedding_model() -> Any:
    """Get embedding model, loading it if necessary."""

    global _embedding_model

    if _embedding_model is None:
        from sentence_transformers import SentenceTransformer

        _embedding_model = SentenceTransformer(
            "intfloat/multilingual-e5-small"
        )

    return _embedding_model


@measure_time
def retrieve_knowledge(query: str) -> list[dict]:
    """Retrieve knowledge entries similar to a query.

    Query is embedded and compared to knowledge embeddings
    using cosine similarity. Results below threshold are removed, 
    and the highest ranked results are returned.

    Args:
        query: A query used to search the knowledge database.

    Returns:
        A list of matching knowledge entries with similarity scores.
    """

    # Maximum number of posts that can be returned.
    top_k = 5

    # Minimum score required for a result.
    similarity_threshold = 0.82

    knowledge = get_all_knowledge()

    if not knowledge:
        return []
    
    from sentence_transformers import util

    query_embedding = create_query_embedding(query)
    results = []
    for item in knowledge:

        # Convert the tensor value into a Python float.
        score = util.cos_sim(
            query_embedding, 
            item["embedding"],
        )[0][0].item() 

        results.append({
            "id": item["id"],
            "text": item["text"],
            "source": item["source"],
            "score": score,
            "created_at": item["created_at"]
        })

    ranked_results = filter_and_rank_results(
        results,
        similarity_threshold,
        top_k,
    )

    # Print retrievals in terminal
    for result in ranked_results:
        print(
            f"Score: {result['score']:.3f} | "
            f"Source: {result['source']} | "
            f"Text: {result['text']}"
        )

    return ranked_results


def create_embedding(text: str) -> np.ndarray:
    """Create an embedding vector for stored knowledge.

    Text is prefixed by "passage:" by the E5 model.

    Args:
        text: Text to embed.
    
    Returns:
        A NumPy array containing the generated embedding.
    """

    return get_embedding_model().encode(f"passage: {text}")


def create_query_embedding(query: str) -> np.ndarray:
    """Create an embedding for a search query.
    
    The query is prefixed with "query by the E5 model.

    Args:
        query: Search query to embed.
    
    Returns:
        A NumPy array containing the generated query embedding.
    """
    return get_embedding_model().encode(f"query: {query}")


def filter_and_rank_results(
    results: list[dict], 
    similarity_threshold: float, 
    top_k: int,
) -> list[dict]:
    """Filter and rank retrieval results by similarity score.

    Args:
        results: Retrieval results containing similarity scores.
        similarity_threshold: Minimum score required for inclusion.
        top_k: The maximum number of results to return.

    Returns:
        Results above the threshold, sorted by descending similarity scores.
    """

    results.sort(key=lambda result: result["score"], reverse=True)
    filtered_results = [
        result
        for result in results
        if result["score"] >= similarity_threshold
    ]

    return filtered_results[:top_k]


# testing purposes
if __name__ == "__main__":
    results = retrieve_knowledge("When does school open?")

    for result in results:
        print(result)