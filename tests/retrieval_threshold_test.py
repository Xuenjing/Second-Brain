from sentence_transformers import util

from database import get_all_knowledge
from retrieval import get_embedding_model

'''
run from project root:
python -m tests.retrieval_threshold_test

this scripts tests similarity thresholds at 0.4, 0.45 and 0.5
with 25 questions against a 200 entry dataset.
0.5 provides cleanest results but completely misses some relevant results,
while 0.4 provides too much noise. 0.45 seems a good sweet spot in this dataset.
'''

def retrieve_with_threshold(query, threshold, top_k=5):
    knowledge = get_all_knowledge()

    if not knowledge:
        return []

    query_embedding = get_embedding_model().encode(query)

    results = []

    for item in knowledge:
        score = util.cos_sim(
            query_embedding,
            item["embedding"]
        )[0][0].item()

        results.append({
            "text": item["text"],
            "source": item["source"],
            "score": score
        })

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    filtered_results = [
        result
        for result in results
        if result["score"] >= threshold
    ]

    return filtered_results[:top_k]


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

thresholds = [0.4, 0.45, 0.5]


for question in questions:
    print("\n" + "=" * 80)
    print(f"QUESTION: {question}")

    for threshold in thresholds:
        print(f"\nThreshold: {threshold}")

        results = retrieve_with_threshold(
            question,
            threshold
        )

        if not results:
            print("No results")
            continue

        for result in results[:3]:
            print(
                f"{result['score']:.3f} | "
                f"{result['text'][:120]}"
            )
        print(f"Results: {len(results)}")
