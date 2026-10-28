"""
Production RAG evaluation.

Run from project root:

python -m experiments.rag_production_evaluation

Purpose:
Evaluate the current production RAG pipeline using:

- Production retrieval:
  paraphrase-multilingual-MiniLM-L12-v2
  similarity threshold = 0.45
  top_k = 5

- Production local LLM:
  Qwen/Qwen3-1.7B

The evaluation focuses on:
- paraphrased questions
- similar entities
- negation
- lunch/dinner distinction
- complete opening-hour answers
- questions that cannot be answered from the knowledge base
"""

from time import perf_counter

from llm.local_provider import LocalLLMProvider
from retrieval import retrieve_knowledge


TEST_CASES = [
    # ---------------------------------------------------------
    # Negation
    # ---------------------------------------------------------
    {
        "category": "negation",
        "question": "Har Niklas ett telefonnummer?",
        "should_answer": True,
        "expected_retrieval": "Niklas har inget telefonnummer",
        "expected_answer": ["inget telefonnummer"],
    },

    # Same fact, more paraphrased wording.
    {
        "category": "paraphrase + negation",
        "question": "Finns det något telefonnummer till Niklas?",
        "should_answer": True,
        "expected_retrieval": "Niklas har inget telefonnummer",
        "expected_answer": ["inget telefonnummer"],
    },

    # ---------------------------------------------------------
    # Similar entities
    # ---------------------------------------------------------
    {
        "category": "similar entities",
        "question": "Vilket internnummer har IT-support för avdelning 9?",
        "should_answer": True,
        "expected_retrieval": (
            "IT-support för avdelning 9 nås via internnummer 1209"
        ),
        "expected_answer": ["1209"],
    },

    {
        "category": "similar entities + paraphrase",
        "question": "Hur når jag supporten på avdelning 5?",
        "should_answer": True,
        "expected_retrieval": (
            "IT-support för avdelning 5 nås via internnummer 1205"
        ),
        "expected_answer": ["1205"],
    },

    # ---------------------------------------------------------
    # Opening hours
    # ---------------------------------------------------------
    {
        "category": "opening hours",
        "question": "När är Reception 17 öppen?",
        "should_answer": True,
        "expected_retrieval": (
            "Reception 17 öppnar klockan 9:00 och "
            "stänger klockan 18:00"
        ),
        "expected_answer": ["9:00", "18:00"],
    },

    {
        "category": "opening hours + entity distinction",
        "question": "Vilka öppettider har Reception 12?",
        "should_answer": True,
        "expected_retrieval": (
            "Reception 12 öppnar klockan 7:00 och "
            "stänger klockan 16:00"
        ),
        "expected_answer": ["7:00", "16:00"],
    },

    # ---------------------------------------------------------
    # Paraphrased meal questions
    # ---------------------------------------------------------
    {
        "category": "paraphrase",
        "question": "När kan man äta lunch i Matsal 18?",
        "should_answer": True,
        "expected_retrieval": (
            "Matsal 18 serverar lunch mellan klockan "
            "10:30 och 13:30"
        ),
        "expected_answer": ["10:30", "13:30"],
    },

    {
        "category": "paraphrase",
        "question": "Mellan vilka tider serveras lunchen i Matsal 1?",
        "should_answer": True,
        "expected_retrieval": (
            "Matsal 1 serverar lunch mellan klockan "
            "11:30 och 14:30"
        ),
        "expected_answer": ["11:30", "14:30"],
    },

    # ---------------------------------------------------------
    # Known difficult Huvudmatsalen case
    # ---------------------------------------------------------
    {
        "category": "known retrieval weakness",
        "question": "Vilka är Huvudmatsalens öppettider för lunch?",
        "should_answer": True,
        "expected_retrieval": (
            "Huvudmatsalen öppnar för lunch klockan 11:00"
        ),
        "expected_answer": ["11:00", "14:00"],
    },

    # Different wording of the same fact.
    {
        "category": "known retrieval weakness + paraphrase",
        "question": "När kan jag äta lunch i Huvudmatsalen?",
        "should_answer": True,
        "expected_retrieval": (
            "Huvudmatsalen öppnar för lunch klockan 11:00"
        ),
        "expected_answer": ["11:00", "14:00"],
    },

    # ---------------------------------------------------------
    # Unsupported questions
    # ---------------------------------------------------------
    {
        "category": "meal mismatch",
        "question": "När serverar Matsal 18 middag?",
        "should_answer": False,
        "expected_retrieval": None,
        "expected_answer": None,
    },

    {
        "category": "meal mismatch",
        "question": "När öppnar Huvudmatsalen för middag?",
        "should_answer": False,
        "expected_retrieval": None,
        "expected_answer": None,
    },

    {
        "category": "missing entity",
        "question": "Har Johan ett telefonnummer?",
        "should_answer": False,
        "expected_retrieval": None,
        "expected_answer": None,
    },

    {
        "category": "missing property",
        "question": "Vad är telefonnumret till Reception 5?",
        "should_answer": False,
        "expected_retrieval": None,
        "expected_answer": None,
    },

    # ---------------------------------------------------------
    # Other paraphrases
    # ---------------------------------------------------------
    {
        "category": "location paraphrase",
        "question": "Vilken byggnad ligger Besöksparkering 7 vid?",
        "should_answer": True,
        "expected_retrieval": (
            "Besöksparkering 7 finns vid byggnad B"
        ),
        "expected_answer": ["byggnad B"],
    },
]


NO_INFORMATION_PHRASES = [
    "inte tillräcklig information",
    "inte tillräckligt med information",
    "ingen information",
    "inget information",
    "saknas information",
    "informationen saknas",
    "kan inte besvaras",
    "det finns inte information",
    "inte något telefonnummer angivet",
]


def build_prompt(context: str, question: str) -> str:
    """Build a prompt matching the production RAG behaviour."""

    return f"""
Use only the information in the context below to answer the question.

Rules:
- If the context contains information about the correct entity but not the requested fact, say that there is not enough information.
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
{question}

ANSWER:
"""


def evaluate_retrieval(test: dict, results: list[dict]) -> bool | None:
    """Evaluate whether expected knowledge was retrieved.

    Returns:
        True if expected knowledge was retrieved.
        False if expected knowledge was not retrieved.
        None for tests where retrieval itself is not evaluated.
    """

    expected = test["expected_retrieval"]

    if expected is None:
        return None

    retrieved_texts = [
        result["text"].lower()
        for result in results
    ]

    return any(
        expected.lower() in text
        for text in retrieved_texts
    )


def evaluate_generation(test: dict, answer: str) -> bool:
    """Evaluate generated answer against expected behaviour."""

    answer_lower = answer.lower()

    if test["should_answer"]:
        return all(
            expected.lower() in answer_lower
            for expected in test["expected_answer"]
        )

    return any(
        phrase in answer_lower
        for phrase in NO_INFORMATION_PHRASES
    )


def run_evaluation() -> None:
    """Run production RAG evaluation."""

    print()
    print("#" * 72)
    print("PRODUCTION RAG EVALUATION")
    print("Retrieval: MiniLM / threshold 0.45 / top_k 5")
    print("LLM: Qwen3-1.7B")
    print("#" * 72)

    llm = LocalLLMProvider("Qwen/Qwen3-1.7B")

    retrieval_pass_count = 0
    retrieval_test_count = 0
    generation_pass_count = 0

    failures = []

    total_start = perf_counter()

    for index, test in enumerate(TEST_CASES, start=1):
        print()
        print("=" * 72)
        print(
            f"{index}/{len(TEST_CASES)} "
            f"[{test['category']}]"
        )
        print("Question:", test["question"])
        print("Should answer:", test["should_answer"])
        print("-" * 72)

        # -----------------------------------------------------
        # Retrieval
        # -----------------------------------------------------

        retrieval_start = perf_counter()

        results = retrieve_knowledge(
            test["question"]
        )

        retrieval_time = perf_counter() - retrieval_start

        print()
        print("Retrieved:")

        if results:
            for rank, result in enumerate(results, start=1):
                print(
                    f"{rank}. "
                    f"score={result['score']:.3f} | "
                    f"source={result['source']}"
                )
                print(result["text"])
        else:
            print("No results.")

        retrieval_pass = evaluate_retrieval(
            test,
            results
        )

        if retrieval_pass is not None:
            retrieval_test_count += 1

            if retrieval_pass:
                retrieval_pass_count += 1

        # -----------------------------------------------------
        # Generation
        # -----------------------------------------------------

        context = "\n".join(
            result["text"]
            for result in results
        )

        if results:
            prompt = build_prompt(
                context,
                test["question"]
            )

            generation_start = perf_counter()

            answer = llm.generate(prompt)

            generation_time = (
                perf_counter() - generation_start
            )

        else:
            answer = (
                "Det finns inte tillräcklig information "
                "i kunskapsbasen."
            )

            generation_time = 0.0

        generation_pass = evaluate_generation(
            test,
            answer
        )

        if generation_pass:
            generation_pass_count += 1

        # -----------------------------------------------------
        # Output
        # -----------------------------------------------------

        print()
        print("Answer:")
        print(answer)

        print()
        print(
            "Retrieval result:",
            (
                "N/A"
                if retrieval_pass is None
                else "PASS"
                if retrieval_pass
                else "FAIL"
            )
        )

        print(
            "Generation result:",
            "PASS" if generation_pass else "FAIL"
        )

        print(
            f"Retrieval time: {retrieval_time:.3f}s"
        )

        print(
            f"Generation time: {generation_time:.3f}s"
        )

        if retrieval_pass is False or not generation_pass:
            failures.append({
                "question": test["question"],
                "category": test["category"],
                "retrieval_pass": retrieval_pass,
                "generation_pass": generation_pass,
                "answer": answer,
            })

    total_time = perf_counter() - total_start

    # ---------------------------------------------------------
    # Summary
    # ---------------------------------------------------------

    print()
    print("#" * 72)
    print("SUMMARY")
    print("#" * 72)

    print(
        "Retrieval:",
        f"{retrieval_pass_count}/{retrieval_test_count} PASS"
    )

    print(
        "Generation:",
        f"{generation_pass_count}/{len(TEST_CASES)} PASS"
    )

    print(
        f"Total evaluation time: {total_time:.2f}s"
    )

    print()

    if failures:
        print("FAILURES")
        print("-" * 72)

        for failure in failures:
            print(
                f"[{failure['category']}] "
                f"{failure['question']}"
            )

            print(
                "Retrieval:",
                failure["retrieval_pass"]
            )

            print(
                "Generation:",
                failure["generation_pass"]
            )

            print(
                "Answer:",
                failure["answer"]
            )

            print()

    else:
        print("All evaluation cases passed.")


if __name__ == "__main__":
    run_evaluation()