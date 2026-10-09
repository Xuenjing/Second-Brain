"""
Tests the retrieval benchmarks between MiniLM and E5-Small

Run from project root:

python -m tests.retrieval_model_benchmark
"""

import time
from sentence_transformers import SentenceTransformer, util
from database import get_all_knowledge

# the E5-small model requires a query prefix and different embeddings
models = [
    {
        "name": "MiniLM",
        "model_name": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        "query_prefix": "",
        "passage_prefix": ""
    },
    {
        "name": "E5-small",
        "model_name": "intfloat/multilingual-e5-small",
        "query_prefix": "query: ",
        "passage_prefix": "passage: "
    }
]

questions = [
    "När öppnar receptionen?",
    "Hur många platser finns på besöksparkeringen?",
    "Hur många platser finns på personalparkeringen?",
    "Var finns cykelparkeringen?",
    "Vilket nummer har central IT?",
    "När är central IT bemannad?",
    "Var ligger Orion och hur många personer rymmer rummet?",
    "Har Orion videokonferens och hur många skärmar finns?",
    "Var ligger Atlas och hur långt i förväg måste det bokas?",
    "När öppnar huvudmatsalen?",
    "Hur många sittplatser finns i huvudmatsalen?",
    "Var ligger HR-avdelningen?",
    "När har HR drop-in?",
    "Vad ska göras vid brandövning?",
    "Vad måste besökare bära?",
    "Vad gör man om man tappar sitt passerkort?",
    "Vad krävs för ett externt möte i Orion?",
    "Vad ska göras vid brandlarm?",
    "Vilka är Sveriges tre största städer i ordning?",
    "Hur får man ett tillfälligt passerkort?",
    "Hur reserverar man en laptop?",
    "När måste specialkost meddelas?",
    "Hur många personer rymmer Atlas respektive Orion?",
    "Vilken parkering är störst?",
    "Vilken byggnad innehåller både matsal och HR?"
]

def create_passage_embeddings(model, knowledge, passage_prefix):
    """
    Create new embeddings for all knowledge entries using
    the model currently being benchmarked.
    """
    
    texts = [passage_prefix + item["text"] for item in knowledge]
    return model.encode(texts)

def retrieve_with_model(question, model, knowledge, passage_embeddings, query_prefix, top_k=5):
    """
    Retrieve the top_k most similar knowledge entries
    using the current embedding model.
    """

    query_embedding = model.encode(query_prefix + question) # query prefix being empty for Mini-LM
    scores = util.cos_sim(query_embedding, passage_embeddings)[0]

    results = []

    for index, score in enumerate(scores):
        results.append({
            "text": knowledge[index]["text"],
            "source": knowledge[index]["source"],
            "score": score.item()
        })

    results.sort(key=lambda result: result["score"], reverse=True) # sort by highest first

    return results[:top_k] # top 5

def run_benchmark():
    '''
    Retrieve database, load the models and have them create their own embeddings for the questions and answers,
    then print the top_k, sim scores and processing times
    '''
    knowledge = get_all_knowledge()

    if not knowledge:
        print("No knowledge entries.")
        return

    print(f"Knowledge entries: {len(knowledge)}")

    for model_info in models:
        print("\n" + "=" * 80)
        print(f"MODEL: {model_info['name']}")
        print(f"Hugging Face model: {model_info['model_name']}")

        # measure loading time
        load_start = time.perf_counter()
        model = SentenceTransformer(model_info["model_name"])
        load_time = time.perf_counter() - load_start

        print(f"Model load time: {load_time:.2f} seconds")

        # each model must create its own embeddings
        embedding_start = time.perf_counter()
        passage_embeddings = create_passage_embeddings(model, knowledge, model_info["passage_prefix"])
        embedding_time = time.perf_counter() - embedding_start

        print(
            f"Embedding {len(knowledge)} passages: "
            f"{embedding_time:.2f} seconds"
        )

        retrieval_times = []

        for question in questions:
            start = time.perf_counter()
            results = retrieve_with_model(question, model, knowledge, passage_embeddings, model_info["query_prefix"])
            retrieval_time = time.perf_counter() - start
            retrieval_times.append(retrieval_time)

            print("\n" + "-" * 80)
            print(f"QUESTION: {question}")
            print(f"Retrieval time: "
                  f"{retrieval_time:.2f} seconds")

            # print only top 5 results for comparison
            for rank, result in enumerate(results[:5], start=1):
                print(f"{rank}. "
                      f"{result['score']:.2f} | "
                      f"{result['text'][:140]}")

        average_time = (sum(retrieval_times) / len(retrieval_times))

        print("\n" + "=" * 80)
        print(f"SUMMARY FOR{model_info['name']}")
        print(f"Model load time: {load_time:.2f} seconds")
        print(f"Passage embedding time: "
                f"{embedding_time:.2f} seconds")

        print(f"Average retrieval time: "
                f"{average_time:.2f} seconds")


if __name__ == "__main__":
    run_benchmark()