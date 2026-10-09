from sentence_transformers import SentenceTransformer, util
from database import get_all_knowledge
from performance import measure_time

model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

@measure_time
def retrieve_knowledge(query):
    '''
    Get the knowledge.db
    embed the query
    Make a cosine similarity between the query and each post in the db
    return only top_k results if they also exceed the similarity_threshold
    '''
    top_k = 5 # how many posts should be returned
    similarity_threshold = 0.45 # to not return irrelevant posts

    knowledge = get_all_knowledge()

    if not knowledge:
        return []
    
    query_embedding = model.encode(query)
    results = []
    for item in knowledge:
        # [0][0] > similarity score. item() turns the tensor value into a python float instead
        score = util.cos_sim(query_embedding, item["embedding"])[0][0].item() 

        results.append({
            "text": item["text"],
            "source": item["source"],
            "score": score
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    filtered_results = [result for result in results if result["score"] >= similarity_threshold ]

    return filtered_results[:top_k]

def create_embedding(text):
    '''
    Helper function to create embeddings for text
    '''
    return model.encode(text)

if __name__ == "__main__":
    results = retrieve_knowledge("When does school open?")

    for result in results:
        print(result)