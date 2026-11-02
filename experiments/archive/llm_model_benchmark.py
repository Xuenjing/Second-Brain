import time

from llm.local_provider import LocalLLMProvider
from retrieval import retrieve_knowledge

'''
run from project root
python -m tests.llm_model_benchmark
'''

# Heavy, light and intermediate models
models = [
    "Qwen/Qwen3-0.6B",
    "Qwen/Qwen3-1.7B",
    "Qwen/Qwen3-4B-Instruct-2507"
]

questions = [
    "När öppnar receptionen?",
    "Vad ska göras vid brandlarm?",
    "Vilka är Sveriges tre största städer i ordning?",
    "Hur många personer rymmer Atlas respektive Orion?",
    "Vilken parkering är störst?",
    "Vad krävs för ett externt möte i Orion?",
    "När måste specialkost meddelas?",
    "Vad gör man om man tappar sitt passerkort?"
]

def create_prompt(question):
    results = retrieve_knowledge(question)

    if not results:
        return None

    context = "\n\n".join(result["text"] for result in results)

    return f"""
/no_think

Use only the information in the context below to answer the question.

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
    """

for model in models:
    print("\n" + "=" *80)
    print(f"MODEL: {model}")
    start_load = time.perf_counter()
    provider = LocalLLMProvider(model)
    load_time = time.perf_counter() - start_load
    print(f"Model load time: {load_time:.2f} seconds")

    for question in questions:
        print("\n" + "-" * 60)
        print(f"QUESTION: {question}")

        prompt = create_prompt(question)

        if prompt is None:
            print("No retrieval results.")
            continue

        start_generation = time.perf_counter()
        answer = provider.generate(prompt)
        generation_time = time.perf_counter() - start_generation

        print(f"ANSWER: {answer}")
        print(f"Generation time: {generation_time:.2f} seconds")