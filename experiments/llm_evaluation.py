"""
Compare local LLM models using the production RAG retrieval pipeline.

The experiment separates:
1. Retrieval quality
2. LLM generation quality
3. End-to-end RAG quality

Run from project root:

python -m experiments.llm_evaluation
"""

import gc
from time import perf_counter

from llm.local_provider import LocalLLMProvider
from retrieval import retrieve_knowledge


TEST_CASES = [
    {
        "question": "Har Natalie ett telefonnummer?",
        "should_answer": True,
        "expected_retrieval": "Natalie har ett telefonnummer",
        "expected_entity": "Natalie",
        "expected_answer": ["har ett telefonnummer"]
    },
    {
        "question": "Har Niklas ett telefonnummer?",
        "should_answer": True,
        "expected_retrieval": "Niklas har inget telefonnummer",
        "expected_entity": "Niklas",
        "expected_answer": ["inget telefonnummer"]
    },
    {
        "question": "Har Johan ett telefonnummer?",
        "should_answer": False,
        "expected_retrieval": None,
        "expected_entity": None,
        "expected_answer": None
    },
    {
        "question": "När öppnar Huvudmatsalen för lunch?",
        "should_answer": True,
        "expected_retrieval": (
            "Huvudmatsalen öppnar för lunch klockan 11:00"
        ),
        "expected_entity": "Huvudmatsalen",
        "expected_answer": ["11:00"]
    },
    {
        "question": "När stänger Huvudmatsalen?",
        "should_answer": True,
        "expected_retrieval": (
            "Huvudmatsalen öppnar för lunch klockan 11:00"
        ),
        "expected_entity": "Huvudmatsalen",
        "expected_answer": ["14:00"]
    },
    {
        "question": "När öppnar Huvudmatsalen för middag?",
        "should_answer": False,
        "expected_retrieval": None,
        "expected_entity": None,
        "expected_answer": None
    },
    {
        "question": "Vilka är Huvudmatsalens öppettider för lunch?",
        "should_answer": True,
        "expected_retrieval": (
            "Huvudmatsalen öppnar för lunch klockan 11:00"
        ),
        "expected_entity": "Huvudmatsalen",
        "expected_answer": ["11:00", "14:00"]
    },
    {
        "question": "När öppnar Reception 17?",
        "should_answer": True,
        "expected_retrieval": (
            "Reception 17 öppnar klockan 9:00 "
            "och stänger klockan 18:00"
        ),
        "expected_entity": "Reception 17",
        "expected_answer": ["9:00"]
    },
    {
        "question": "När stänger Reception 12?",
        "should_answer": True,
        "expected_retrieval": (
            "Reception 12 öppnar klockan 7:00 "
            "och stänger klockan 16:00"
        ),
        "expected_entity": "Reception 12",
        "expected_answer": ["16:00"]
    },
    {
        "question": "Vilka öppettider har Reception 5?",
        "should_answer": True,
        "expected_retrieval": (
            "Reception 5 öppnar klockan 9:00 "
            "och stänger klockan 18:00"
        ),
        "expected_entity": "Reception 5",
        "expected_answer": ["9:00", "18:00"]
    },
    {
        "question": "När öppnar Huvudreceptionen på vardagar?",
        "should_answer": True,
        "expected_retrieval": (
            "Huvudreceptionen öppnar klockan 07:30 på vardagar"
        ),
        "expected_entity": "Huvudreceptionen",
        "expected_answer": ["07:30"]
    },
    {
        "question": "När serverar Matsal 18 lunch?",
        "should_answer": True,
        "expected_retrieval": (
            "Matsal 18 serverar lunch mellan "
            "klockan 10:30 och 13:30"
        ),
        "expected_entity": "Matsal 18",
        "expected_answer": ["10:30", "13:30"]
    },
    {
        "question": "Vilka lunchtider har Matsal 1?",
        "should_answer": True,
        "expected_retrieval": (
            "Matsal 1 serverar lunch mellan "
            "klockan 11:30 och 14:30"
        ),
        "expected_entity": "Matsal 1",
        "expected_answer": ["11:30", "14:30"]
    },
    {
        "question": "Vilket internnummer har IT-support för avdelning 9?",
        "should_answer": True,
        "expected_retrieval": (
            "IT-support för avdelning 9 nås via internnummer 1209"
        ),
        "expected_entity": "avdelning 9",
        "expected_answer": ["1209"]
    },
    {
        "question": "Vilket internnummer har IT-support för avdelning 5?",
        "should_answer": True,
        "expected_retrieval": (
            "IT-support för avdelning 5 nås via internnummer 1205"
        ),
        "expected_entity": "avdelning 5",
        "expected_answer": ["1205"]
    },
    {
        "question": "Var finns Besöksparkering 7?",
        "should_answer": True,
        "expected_retrieval": (
            "Besöksparkering 7 finns vid byggnad B"
        ),
        "expected_entity": "Besöksparkering 7",
        "expected_answer": ["byggnad B"]
    },
    {
        "question": "När serverar Matsal 18 middag?",
        "should_answer": False,
        "expected_retrieval": None,
        "expected_entity": None,
        "expected_answer": None
    }
]


LLM_MODELS = [
    {
        "name": "Qwen3-1.7B",
        "model_name": "Qwen/Qwen3-1.7B"
    },
    {
        "name": "Qwen2.5-3B-Instruct",
        "model_name": "Qwen/Qwen2.5-3B-Instruct"
    }
]


NO_INFORMATION_PHRASES = [
    "inte tillräcklig information",
    "inte tillräckligt med information",
    "ingen information",
    "inget information",
    "saknas information",
    "informationen saknas",
    "framgår inte"
]


def create_prompt(
    question: str,
    context: str,
) -> str:
    """Create the same grounding prompt for every model."""

    return f"""
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
{question}

ANSWER:
"""


def evaluate_retrieval(
    test: dict,
    results: list[dict],
) -> bool | None:
    """Check whether retrieval found the required knowledge.

    Returns:
        True if expected knowledge was found.
        False if expected knowledge was not found.
        None if the test intentionally has no expected knowledge.
    """

    expected_retrieval = test["expected_retrieval"]

    if expected_retrieval is None:
        return None

    retrieved_texts = [
        result["text"].lower()
        for result in results
    ]

    return any(
        expected_retrieval.lower() in text
        for text in retrieved_texts
    )


def evaluate_answer(
    test: dict,
    answer: str,
) -> bool:
    """Evaluate an answer when sufficient context was available."""

    answer_lower = answer.lower()

    if not test["should_answer"]:
        return any(
            phrase in answer_lower
            for phrase in NO_INFORMATION_PHRASES
        )

    entity_correct = (
        test["expected_entity"].lower()
        in answer_lower
    )

    facts_correct = all(
        expected.lower() in answer_lower
        for expected in test["expected_answer"]
    )

    return entity_correct and facts_correct


def prepare_retrievals() -> dict[str, list[dict]]:
    """Run production retrieval once for each question."""

    retrievals = {}

    print()
    print("#" * 70)
    print("PREPARING PRODUCTION MINILM RETRIEVAL")
    print("top_k = 5")
    print("similarity_threshold = 0.45")
    print("#" * 70)

    for test in TEST_CASES:
        question = test["question"]

        print()
        print("Question:", question)

        retrievals[question] = retrieve_knowledge(question)

    return retrievals


def run_evaluation() -> None:
    """Compare local LLM quality and performance."""

    retrievals = prepare_retrievals()

    # Retrieval is identical for every LLM, so calculate
    # its overall result once.
    positive_retrieval_tests = 0
    retrieval_pass_count = 0

    for test in TEST_CASES:
        if test["expected_retrieval"] is None:
            continue

        positive_retrieval_tests += 1

        results = retrievals[test["question"]]

        if evaluate_retrieval(test, results):
            retrieval_pass_count += 1

    print()
    print("-" * 70)
    print("RETRIEVAL SUMMARY")
    print(
        "Positive retrieval cases:",
        f"{retrieval_pass_count}/{positive_retrieval_tests} PASS"
    )
    print("-" * 70)

    for llm_config in LLM_MODELS:
        print()
        print("*" * 70)
        print("LLM MODEL:", llm_config["name"])
        print("*" * 70)

        load_start = perf_counter()

        llm = LocalLLMProvider(
            llm_config["model_name"]
        )

        load_time = perf_counter() - load_start

        llm_pass_count = 0
        llm_test_count = 0

        end_to_end_pass_count = 0

        skipped_generation_count = 0

        generation_times = []

        for test in TEST_CASES:
            question = test["question"]
            results = retrievals[question]

            retrieval_result = evaluate_retrieval(
                test,
                results
            )

            print()
            print("=" * 70)
            print("Question:", question)
            print("Should answer:", test["should_answer"])

            print("\nRetrieved:")

            for index, result in enumerate(
                results,
                start=1
            ):
                print(
                    f"{index}. "
                    f"score={result['score']:.3f} | "
                    f"source={result['source']}"
                )
                print(result["text"])
                print()

            if retrieval_result is True:
                print("Retrieval result: PASS")
            elif retrieval_result is False:
                print("Retrieval result: FAIL")
            else:
                print("Retrieval result: N/A")

            if results:
                context = "\n".join(
                    result["text"]
                    for result in results
                )

                prompt = create_prompt(
                    question,
                    context
                )

                generation_start = perf_counter()

                answer = llm.generate(prompt)

                generation_time = (
                    perf_counter()
                    - generation_start
                )

                generation_times.append(
                    generation_time
                )

            else:
                answer = (
                    "Det finns inte tillräcklig information "
                    "i kunskapsbasen."
                )

                generation_time = 0.0

            print()
            print("LLM answer:")
            print(answer)

            print()
            print(
                f"Generation time: "
                f"{generation_time:.3f} seconds"
            )

            # Positive question where retrieval failed:
            # the LLM cannot fairly be judged on information
            # it never received.
            if (
                test["should_answer"]
                and retrieval_result is False
            ):
                generation_result = None
                skipped_generation_count += 1

                print("Generation result: SKIP")

            else:
                generation_result = evaluate_answer(
                    test,
                    answer
                )

                llm_test_count += 1

                if generation_result:
                    llm_pass_count += 1

                print(
                    "Generation result:",
                    (
                        "PASS"
                        if generation_result
                        else "FAIL"
                    )
                )

            # End-to-end evaluation represents what the actual
            # user experiences from the complete RAG system.
            if test["should_answer"]:
                end_to_end_pass = (
                    retrieval_result is True
                    and generation_result is True
                )
            else:
                end_to_end_pass = (
                    generation_result is True
                )

            if end_to_end_pass:
                end_to_end_pass_count += 1

            print(
                "End-to-end result:",
                (
                    "PASS"
                    if end_to_end_pass
                    else "FAIL"
                )
            )

        if generation_times:
            total_generation_time = sum(
                generation_times
            )

            average_generation_time = (
                total_generation_time
                / len(generation_times)
            )
        else:
            total_generation_time = 0.0
            average_generation_time = 0.0

        print()
        print("-" * 70)
        print("SUMMARY:", llm_config["name"])

        print(
            "LLM quality:",
            f"{llm_pass_count}/{llm_test_count} PASS"
        )

        print(
            "Generation tests skipped:",
            skipped_generation_count
        )

        print(
            "End-to-end RAG:",
            f"{end_to_end_pass_count}/{len(TEST_CASES)} PASS"
        )

        print(
            f"Average generation time: "
            f"{average_generation_time:.3f} seconds"
        )

        print(
            f"Total generation time: "
            f"{total_generation_time:.3f} seconds"
        )

        print(
            f"Model load time: "
            f"{load_time:.3f} seconds"
        )

        print("-" * 70)

        del llm
        gc.collect()


if __name__ == "__main__":
    run_evaluation()