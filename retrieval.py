from sentence_transformers import SentenceTransformer, util
from database import get_all_knowledge
from performance import measure_time
import numpy as np

model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

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
    
    query_embedding = model.encode(query)
    results = []
    for item in knowledge:
        # extracts the similarity score and converts the tensor value into a Python float
        score = util.cos_sim(query_embedding, item["embedding"])[0][0].item() 

        results.append({
            "text": item["text"],
            "source": item["source"],
            "score": score
        })

    results.sort(key=lambda x: x["score"], reverse=True) # sort results by highest sim score first
    filtered_results = [result for result in results if result["score"] >= similarity_threshold ] # only results > threshold

    return filtered_results[:top_k]

def create_embedding(text: str) -> np.ndarray:
    '''
    Helper function that creates an ambedding vector for a text string.
    Returns a numpy array containing the generated embeddings.
    '''
    return model.encode(text)

# testing purposes
if __name__ == "__main__":
    results = retrieve_knowledge("When does school open?")

    for result in results:
        print(result)