'''
BENCHMARK MED TVÅ OLIKA QWEN-MODELLER

Qwen 4B:
~47–84 s generation

Qwen 0.6B:
~6–21 s generation
oftast ~6–16 s

Retrieval:
~0.03–0.08 s

Svarskvalitet:
mycket liten märkbar försämring i detta test

Top_k = 5 och threshold 0.5 verkar vara sweet spot för just detta test.
'''

import time

from sentence_transformers import SentenceTransformer, util
from llm.local_provider import LocalLLMProvider


model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")


knowledge = []

# Reception
for i in range(1, 21):
    knowledge.append(
        f"Reception {i} öppnar klockan {7 + (i % 3)}:00 och stänger klockan {16 + (i % 3)}:00."
    )

# Parking
for i in range(1, 21):
    knowledge.append(
        f"Besöksparkering {i} finns vid byggnad {chr(64 + ((i - 1) % 6) + 1)}."
    )

# IT
for i in range(1, 21):
    knowledge.append(
        f"IT-support för avdelning {i} nås via internnummer {1200 + i}."
    )

# Meeting rooms
for i in range(1, 21):
    knowledge.append(
        f"Mötesrum {i} måste bokas minst {i % 5 + 1} timmar i förväg."
    )

# Dining
for i in range(1, 21):
    knowledge.append(
        f"Matsal {i} serverar lunch mellan klockan {10 + (i % 2)}:30 och {13 + (i % 2)}:30."
    )

# Security
for i in range(1, 21):
    knowledge.append(
        f"Besökare till säkerhetszon {i} måste bära besöksbricka och ledsagas av personal."
    )

# Departments
for i in range(1, 21):
    knowledge.append(
        f"Avdelning {i} ligger på våning {i % 5 + 1} i byggnad {chr(65 + ((i - 1) % 5))}."
    )

# Special posts with known answers
knowledge.extend([
    "Huvudreceptionen öppnar klockan 07:30 på vardagar.",
    "Besöksparkeringen vid huvudentrén har 25 platser.",
    "Central IT-support nås via internnummer 1234.",
    "Mötesrum Orion ligger på våning 3 i byggnad C.",
    "Huvudmatsalen öppnar för lunch klockan 11:00.",
    "Besökare måste alltid bära en synlig besöksbricka.",
    "HR-avdelningen ligger på våning 2 i byggnad B.",
    "Brandövning genomförs första måndagen varje månad.",
    "Receptionen kan utfärda tillfälliga passerkort.",
    "Cykelparkering finns på den östra sidan av byggnad A."
])

test_cases = [
    {
        "question": "När öppnar huvudreceptionen?",
        "expected": "Huvudreceptionen öppnar klockan 07:30 på vardagar."
    },
    {
        "question": "Hur många platser finns på besöksparkeringen vid huvudentrén?",
        "expected": "Besöksparkeringen vid huvudentrén har 25 platser."
    },
    {
        "question": "Hur kontaktar jag central IT-support?",
        "expected": "Central IT-support nås via internnummer 1234."
    },
    {
        "question": "Var ligger mötesrum Orion?",
        "expected": "Mötesrum Orion ligger på våning 3 i byggnad C."
    },
    {
        "question": "När öppnar huvudmatsalen för lunch?",
        "expected": "Huvudmatsalen öppnar för lunch klockan 11:00."
    },
    {
        "question": "Vad måste besökare bära?",
        "expected": "Besökare måste alltid bära en synlig besöksbricka."
    },
    {
        "question": "Var ligger HR-avdelningen?",
        "expected": "HR-avdelningen ligger på våning 2 i byggnad B."
    },
    {
        "question": "När genomförs brandövningen?",
        "expected": "Brandövning genomförs första måndagen varje månad."
    },
    {
        "question": "Var kan jag få ett tillfälligt passerkort?",
        "expected": "Receptionen kan utfärda tillfälliga passerkort."
    },
    {
        "question": "Var finns cykelparkeringen?",
        "expected": "Cykelparkering finns på den östra sidan av byggnad A."
    }
]

knowledge_embeddings = model.encode(knowledge)



top_k = 5
similarity_threshold = 0.5

correct = 0

print("Knowledge entries:", len(knowledge))

# mer avancerad modell
# llm = LocalLLMProvider("Qwen/Qwen3-4B-Instruct-2507")

# enklare modell
llm = LocalLLMProvider("Qwen/Qwen3-0.6B")

for test_case in test_cases:
    question = test_case["question"]
    expected = test_case["expected"]

    # -------------------------
    # Retrieval
    # -------------------------

    retrieval_start = time.perf_counter()

    question_embedding = model.encode(question)

    similarities = util.cos_sim(
        question_embedding,
        knowledge_embeddings
    )[0]

    results = []

    for text, score in zip(knowledge, similarities):
        score = score.item()

        if score >= similarity_threshold:
            results.append({
                "text": text,
                "score": score
            })

    results.sort(
        key=lambda result: result["score"],
        reverse=True
    )

    results = results[:top_k]

    retrieval_end = time.perf_counter()

    # -------------------------
    # Check retrieval result
    # -------------------------

    found_expected = any(
        result["text"] == expected
        for result in results
    )

    if found_expected:
        correct += 1

    # -------------------------
    # Build context for LLM
    # -------------------------

    context = "\n".join(
        result["text"]
        for result in results
    )

    prompt = f"""
/no_think

Use only the information in the context below to answer the question.

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""

    # -------------------------
    # LLM generation
    # -------------------------

    generation_start = time.perf_counter()

    answer = llm.generate(prompt)

    generation_end = time.perf_counter()

    # -------------------------
    # Output
    # -------------------------

    print("\nQUESTION:")
    print(question)

    print("\nEXPECTED:")
    print(expected)

    print("\nRETRIEVED:")

    for result in results:
        print(
            f'{result["score"]:.3f} - '
            f'{result["text"]}'
        )

    print("\nCorrect result found:", found_expected)

    print(
        f"Retrieval time: "
        f"{retrieval_end - retrieval_start:.4f} seconds"
    )

    print("\nLLM ANSWER:")
    print(answer)

    print(
        f"Generation time: "
        f"{generation_end - generation_start:.3f} seconds"
    )

print("\nSUMMARY")
print(f"Correct: {correct}/{len(test_cases)}")