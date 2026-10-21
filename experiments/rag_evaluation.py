'''
RAG evaluation experiment.

Run from project root:

python -m experiments.rag_evaluation

Previous experiment:
- Compared MiniLM and multilingual-e5-small for retrieval.
- E5 retrieved the expected knowledge in all positive test cases.
- MiniLM missed one paraphrased Huvudmatsalen query.

Current experiment:
- Keep E5 retrieval unchanged.
- Compare Qwen3-1.7B and Qwen3-4B generation quality.
'''

from database import get_all_knowledge
from llm.local_provider import LocalLLMProvider
from sentence_transformers import SentenceTransformer, util


TEST_CASES = [
    {
        "question": "Har Natalie ett telefonnummer?",
        "should_answer": True,
        "expected_retrieval": "Natalie har ett telefonnummer",
        "expected_answer": ["telefonnummer"]
    },
    {
        "question": "Har Niklas ett telefonnummer?",
        "should_answer": True,
        "expected_retrieval": "Niklas har inget telefonnummer",
        "expected_answer": ["inget telefonnummer"]
    },
    {
        "question": "Har Johan ett telefonnummer?",
        "should_answer": False,
        "expected_retrieval": None,
        "expected_answer": None
    },
    {
        "question": "När öppnar Huvudmatsalen för lunch?",
        "should_answer": True,
        "expected_retrieval": (
            "Huvudmatsalen öppnar för lunch klockan 11:00"
        ),
        "expected_answer": ["11:00"]
    },
    {
        "question": "När stänger Huvudmatsalen?",
        "should_answer": True,
        "expected_retrieval": (
            "Huvudmatsalen öppnar för lunch klockan 11:00"
        ),
        "expected_answer": ["14:00"]
    },
    {
        "question": "När öppnar Huvudmatsalen för middag?",
        "should_answer": False,
        "expected_retrieval": None,
        "expected_answer": None
    },
    {
        "question": "Vilka är Huvudmatsalens öppettider för lunch?",
        "should_answer": True,
        "expected_retrieval": (
            "Huvudmatsalen öppnar för lunch klockan 11:00"
        ),
        "expected_answer": ["11:00", "14:00"]
    },
    {
        "question": "När öppnar Reception 17?",
        "should_answer": True,
        "expected_retrieval": (
            "Reception 17 öppnar klockan 9:00 och "
            "stänger klockan 18:00"
        ),
        "expected_answer": ["9:00"]
    },
    {
        "question": "När stänger Reception 12?",
        "should_answer": True,
        "expected_retrieval": (
            "Reception 12 öppnar klockan 7:00 och "
            "stänger klockan 16:00"
        ),
        "expected_answer": ["16:00"]
    },
    {
        "question": "Vilka öppettider har Reception 5?",
        "should_answer": True,
        "expected_retrieval": (
            "Reception 5 öppnar klockan 9:00 och "
            "stänger klockan 18:00"
        ),
        "expected_answer": ["9:00", "18:00"]
    },
    {
        "question": "När öppnar Huvudreceptionen på vardagar?",
        "should_answer": True,
        "expected_retrieval": (
            "Huvudreceptionen öppnar klockan 07:30 på vardagar"
        ),
        "expected_answer": ["07:30"]
    },
    {
        "question": "När serverar Matsal 18 lunch?",
        "should_answer": True,
        "expected_retrieval": (
            "Matsal 18 serverar lunch mellan klockan "
            "10:30 och 13:30"
        ),
        "expected_answer": ["10:30", "13:30"]
    },
    {
        "question": "Vilka lunchtider har Matsal 1?",
        "should_answer": True,
        "expected_retrieval": (
            "Matsal 1 serverar lunch mellan klockan "
            "11:30 och 14:30"
        ),
        "expected_answer": ["11:30", "14:30"]
    },
    {
        "question": "Vilket internnummer har IT-support för avdelning 9?",
        "should_answer": True,
        "expected_retrieval": (
            "IT-support för avdelning 9 nås via internnummer 1209"
        ),
        "expected_answer": ["1209"]
    },
    {
        "question": "Vilket internnummer har IT-support för avdelning 5?",
        "should_answer": True,
        "expected_retrieval": (
            "IT-support för avdelning 5 nås via internnummer 1205"
        ),
        "expected_answer": ["1205"]
    },
    {
        "question": "Var finns Besöksparkering 7?",
        "should_answer": True,
        "expected_retrieval": (
            "Besöksparkering 7 finns vid byggnad B"
        ),
        "expected_answer": ["byggnad B"]
    },
    {
        "question": "När serverar Matsal 18 middag?",
        "should_answer": False,
        "expected_retrieval": None,
        "expected_answer": None
    }
]


# Retrieval is fixed to E5 for this experiment.
# Previous evaluation compared E5 against MiniLM.
EMBEDDING_MODEL = {
    "name": "E5",
    "model_name": "intfloat/multilingual-e5-small",
    "use_e5_prefix": True
}


LLM_MODELS = [
    {
        "name": "Qwen3-1.7B",
        "model_name": "Qwen/Qwen3-1.7B"
    },
    {
        "name": "Qwen3-4B",
        "model_name": "Qwen/Qwen3-4B"
    }
]


def retrieve_with_model(
    query: str,
    knowledge: list[dict],
    model: SentenceTransformer,
    use_e5_prefix: bool,
    top_k: int = 5,
) -> list[dict]:
    """Retrieve knowledge using the selected embedding model.

    Args:
        query: User question.
        knowledge: Knowledge entries from the database.
        model: SentenceTransformer model used for embeddings.
        use_e5_prefix: Whether E5 query/passage prefixes should be used.
        top_k: Maximum number of results to return.

    Returns:
        Ranked retrieval results.
    """

    if use_e5_prefix:
        query_text = f"query: {query}"
    else:
        query_text = query

    query_embedding = model.encode(query_text)

    results = []

    for item in knowledge:
        if use_e5_prefix:
            knowledge_text = f"passage: {item['text']}"
        else:
            knowledge_text = item["text"]

        knowledge_embedding = model.encode(knowledge_text)

        score = util.cos_sim(
            query_embedding,
            knowledge_embedding,
        )[0][0].item()

        results.append({
            "id": item["id"],
            "text": item["text"],
            "source": item["source"],
            "score": score,
            "created_at": item["created_at"]
        })

    results.sort(
        key=lambda result: result["score"],
        reverse=True
    )

    return results[:top_k]


def run_evaluation() -> None:
    """Compare generation quality between local LLM models."""

    knowledge = get_all_knowledge()

    print()
    print("#" * 70)
    print("EMBEDDING MODEL:", EMBEDDING_MODEL["name"])
    print("#" * 70)

    embedding_model = SentenceTransformer(
        EMBEDDING_MODEL["model_name"]
    )

    for llm_config in LLM_MODELS:
        print()
        print("*" * 70)
        print("LLM MODEL:", llm_config["name"])
        print("*" * 70)

        llm = LocalLLMProvider(
            llm_config["model_name"]
        )

        generation_pass_count = 0
        retrieval_pass_count = 0
        retrieval_test_count = 0

        for test in TEST_CASES:
            print("=" * 60)
            print("Question:", test["question"])
            print("Should answer:", test["should_answer"])

            results = retrieve_with_model(
                test["question"],
                knowledge,
                embedding_model,
                EMBEDDING_MODEL["use_e5_prefix"]
            )

            print("\nRetrieved:")

            for index, result in enumerate(results, start=1):
                print(
                    f"{index}. "
                    f"score={result['score']:.3f} | "
                    f"source={result['source']}"
                )
                print(result["text"])
                print()

            if results:
                context = "\n".join(
                    result["text"]
                    for result in results
                )

                prompt = f"""
Use only the information in the context below to answer the question.

Rules:
- Before answering, verify that the context explicitly states BOTH:
  1. the same entity mentioned in the question, and
  2. the same requested property, event, meal, time, or fact.
- A statement about lunch does not answer a question about dinner.
- A statement about one person does not answer a question about another person, even if their names are similar.
- Never change a fact from the context to match the wording of the question.
- If either the entity or the requested fact does not match exactly, say that there is not enough information in the knowledge base.
- Pay close attention to negation such as "not", "no", "does not", "inte", "inget" and "har inte".
- If the context explicitly states that something is not true, do not answer that it is true.
- Base the answer on the complete relevant statement, not only on matching words.
- Identify the statement in the context that refers to the same person or entity as the question.
- Answer strictly according to that statement.
- Do not infer information about one person or entity from information about another.
- The context may contain information that is related to the topic but does not answer the question.
- If the context does not explicitly contain the information needed to answer the question, respond that there is not enough information in the knowledge base.
- Answer in the same language as the question.
- Do not make up information.

CONTEXT:
{context}

QUESTION:
{test["question"]}

ANSWER:
"""

                answer = llm.generate(prompt)

            else:
                answer = (
                    "Det finns inte tillräcklig information "
                    "i kunskapsbasen."
                )

            print("LLM answer:")
            print(answer)
            print()

            # Evaluate generation.
            if test["should_answer"]:
                expected_answers = test["expected_answer"]

                generation_pass = all(
                    expected.lower() in answer.lower()
                    for expected in expected_answers
                )

            else:
                answer_lower = answer.lower()

                no_information_phrases = [
                    "inte tillräcklig information",
                    "inte tillräckligt med information",
                    "ingen information",
                    "inget information",
                    "inte information",
                    "saknas information"
                ]

                generation_pass = any(
                    phrase in answer_lower
                    for phrase in no_information_phrases
                )

            if generation_pass:
                generation_pass_count += 1

            print(
                "Generation result:",
                "PASS" if generation_pass else "FAIL"
            )

            # Evaluate retrieval.
            if test["expected_retrieval"] is not None:
                retrieval_test_count += 1

                retrieved_texts = [
                    result["text"].lower()
                    for result in results
                ]

                retrieval_pass = any(
                    test["expected_retrieval"].lower() in text
                    for text in retrieved_texts
                )

                if retrieval_pass:
                    retrieval_pass_count += 1

                print(
                    "Retrieval result:",
                    "PASS" if retrieval_pass else "FAIL"
                )

            else:
                print("Retrieval result: N/A")

            print()

        print()
        print("-" * 70)
        print("SUMMARY:", llm_config["name"])
        print(
            "Generation:",
            f"{generation_pass_count}/{len(TEST_CASES)} PASS"
        )
        print(
            "Retrieval:",
            f"{retrieval_pass_count}/{retrieval_test_count} PASS"
        )
        print("-" * 70)


if __name__ == "__main__":
    run_evaluation()