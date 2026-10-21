from sentence_transformers import SentenceTransformer, util
import time

'''
Test sentence embeddings in isolation
A set of questions each get embedded (vectorized) and compared to a fake database
'''

start = time.perf_counter()
# the embeddings model
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

# example posts
knowledge = [
    "The school opens at 8.00AM.",
    "There is a parking lot next to the entrance.",
    "The dining hall opens at 11.00AM."
]

# example questions
questions = [
    "When does school open?",
    "Where can I park?",
    "When does the dining hall open?"
    ]

# embed posts
knowledge_embeddings = model.encode(knowledge)

for question in questions:

    # embed each question
    question_embedding = model.encode(question)

    # compare similarities between question and answer
    similiarities = util.cos_sim(
        question_embedding,
        knowledge_embeddings
    )

    # print
    results = []
    
    for text, score in zip(knowledge, similiarities[0]):
        results.append((text, score.item()))
        # print(score.item(), "-", text)
    results.sort(key=lambda x: x[1], reverse=True) # sort by highest index1 (score)

    print(f"\nQuestion: {question}")

    for text, score in results:
        print(score, "-", text)

end = time.perf_counter()
print(f"Total time: {end-start}")
