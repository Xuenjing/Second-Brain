from database import get_all_knowledge
from performance import measure_time
import numpy as np



_embedding_model = None

def get_embedding_model():
    '''
    Get embedding model, loading it if necessary
    '''
    global _embedding_model
    if _embedding_model is None:
        from sentence_transformers import SentenceTransformer
        _embedding_model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
    return _embedding_model

# model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

@measure_time
def retrieve_knowledge(query: str) -> list[dict]:
    '''
    Retrieve knowledge entries similar to query.
    Query is embedded and compared to knowledge embeddings through cosine similarity.
    Results below threshold are removed, 
    and up to top_k results are returned sorted by highest sim score.
    '''
    top_k = 5 # how many posts should be returned
    similarity_threshold = 0.45 # to not return irrelevant posts

    knowledge = get_all_knowledge()

    if not knowledge:
        return []
    
    from sentence_transformers import util

    query_embedding = get_embedding_model().encode(query)
    results = []
    for item in knowledge:
        # extracts the similarity score and converts the tensor value into a Python float
        score = util.cos_sim(query_embedding, item["embedding"])[0][0].item() 

        results.append({
            "text": item["text"],
            "source": item["source"],
            "score": score
        })

    return filter_and_rank_results(results, similarity_threshold, top_k)

def create_embedding(text: str) -> np.ndarray:
    '''
    Helper function that creates an embedding vector for a text string.
    Returns a numpy array containing the generated embeddings.
    '''
    return get_embedding_model().encode(text)

def filter_and_rank_results(results: list[dict], similarity_threshold: float, top_k: int) -> list[dict]:
    '''
    Sort retrieval results by similarity score,
    filter out results below the threshold, 
    and return the top_k results
    '''
    results.sort(key=lambda result: result["score"], reverse=True)
    filtered_results=[result for result in results if result["score"] >= similarity_threshold]
    return filtered_results[:top_k]

# testing purposes
if __name__ == "__main__":
    results = retrieve_knowledge("When does school open?")

    for result in results:
        print(result)