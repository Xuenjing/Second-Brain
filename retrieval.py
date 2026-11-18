from typing import Any

import numpy as np
import re

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
def retrieve_knowledge(
    query: str,
    top_k: int = 5,
    similarity_threshold: float = 0.82,
) -> dict[str, list[dict]]:
    """Retrieve and group knowledge entries by relevance.

    Entries are ranked by semantic similarity with a bonus
    for matching word-number identifiers, such as "Matsal 18".

    Args:
        query: Question used to search the knowledge database.
        top_k: Maximum number of entries used for answer generation.
        similarity_threshold: Minimum semantic score for relevant entries.

    Returns:
        A dictionary containing three lists:
        used_sources: Relevant entries selected for answer generation.
        additional_sources: Relevant entries beyond the Top-K limit.
        less_relevant_sources: Entries below the similarity threshold.
    """

    # Ranking bonus for matching word-number identifiers.
    identifier_boost = 0.20

    knowledge = get_all_knowledge()

    if not knowledge:
        return {
            "used_sources": [],
            "additional_sources": [],
            "less_relevant_sources": [],
        }

    from sentence_transformers import util

    query_embedding = create_query_embedding(query)

    # Extract identifiers once from the query.
    query_identifiers = extract_numeric_phrases(query)

    results = []

    for item in knowledge:

        # Pure semantic similarity from E5.
        semantic_score = util.cos_sim(
            query_embedding,
            item["embedding"],
        )[0][0].item()

        # Extract identifiers from the stored knowledge.
        item_identifiers = extract_numeric_phrases(
            item["text"]
        )

        identifier_match = bool(
            query_identifiers
            and query_identifiers.intersection(
                item_identifiers
            )
        )

        # Start with the semantic score.
        hybrid_score = semantic_score

        # Boost ranking if an exact identifier matches.
        if identifier_match:
            hybrid_score += identifier_boost

        results.append({
            "id": item["id"],
            "text": item["text"],
            "source": item["source"],
            "score": hybrid_score,
            "semantic_score": semantic_score,
            "identifier_match": identifier_match,
            "created_at": item["created_at"]
        })

    ranked_results = rank_results(results)
    used_sources, additional_sources, less_relevant_sources = (
        split_retrieval_results(
            ranked_results,
            similarity_threshold,
            top_k
        )
    )
    

    # Print retrievals in terminal.
    for result in used_sources:
        print(
            f"Semantic score: {result['semantic_score']:.3f} | "
            f"Hybrid score: {result['score']:.3f} | "
            f"Identifier match: {result['identifier_match']} | "
            f"Source: {result['source']} | "
            f"Text: {result['text']}"
        )

    return {
        "used_sources": used_sources,
        "additional_sources": additional_sources,
        "less_relevant_sources": less_relevant_sources,
    }


def create_embedding(text: str) -> np.ndarray:
    """Create an embedding vector for stored knowledge.

    Text is prefixed with "passage: " before encoding.

    Args:
        text: Text to embed.
    
    Returns:
        A NumPy array containing the generated embedding.
    """

    return get_embedding_model().encode(f"passage: {text}")


def create_query_embedding(query: str) -> np.ndarray:
    """Create an embedding for a search query.
    
    The query is prefixed with "query: " before encoding.

    Args:
        query: Search query to embed.
    
    Returns:
        A NumPy array containing the generated query embedding.
    """
    return get_embedding_model().encode(f"query: {query}")


def extract_numeric_phrases(text: str) -> set[str]:
    """Extract word-number identifier phrases from text.
    
    Args:
        text: Text to search for numeric tokens.

    Returns:
        A set containing the word-number phrase found in the text.
    """

    text = text.lower()
    matches = re.findall(
        r"\b([a-zåäö]+)\s+(?:nummer\s+)?(\d+)\b",
        text
    )
    
    return {
        f"{word} {number}"
        for word, number in matches
    }



def rank_results(results: list[dict]) -> list[dict]:
    """Rank retrieval results by hybrid score.
    
    Args:
        results: Retrieval results containing semantic and hybrid scores.

    Returns:
        Results sorted by hybrid score in descending order.
    """

    return sorted(
        results,
        key=lambda result: result["score"], reverse=True
    )


def split_retrieval_results(
        ranked_results: list[dict],
        similarity_threshold: float,
        top_k: int,
) -> tuple[list[dict], list[dict], list[dict]]:
    """Split ranked results into relevance levels.
    
    Args:
        ranked_results: Retrieval results sorted by hybrid score.
        similarity_threshold: Minimum semantic score for relevant results.
        top_k: Maximum number of results used for generation.
    
    Returns:
        A tuple containing used sources, additional relevant sources, and less relevant sources.
    """ 

    relevant_results = [
        result 
        for result in ranked_results
        if result["semantic_score"] >= similarity_threshold
    ]

    less_relevant_results = [
        result
        for result in ranked_results
        if result["semantic_score"] < similarity_threshold
    ]

    used_sources = relevant_results[:top_k]
    additional_sources = relevant_results[top_k:]

    return (
        used_sources,
        additional_sources,
        less_relevant_results
    )


def filter_and_rank_results(
    results: list[dict], 
    similarity_threshold: float, 
    top_k: int,
) -> list[dict]:
    """Filter by semantic similarity and rank by hybrid score.

    Args:
        results: Retrieval results containing semantic and hybrid scores.
        similarity_threshold: Minimum semantic score required for inclusion.
        top_k: The maximum number of results to return.

    Returns:
        Results above the threshold, ranked by hybrid score.
    """

    ranked_results = rank_results(results)

    used_sources, _, _ = split_retrieval_results(
        ranked_results,
        similarity_threshold,
        top_k
    )
    
    return used_sources


# Run a manual retrieval check when executing this module directly.
if __name__ == "__main__":
    results = retrieve_knowledge("When does school open?")

    for group_name, entries in results.items():
        print(f"\n{group_name}: {len(entries)} entries")

        for entry in entries:
            print(entry)