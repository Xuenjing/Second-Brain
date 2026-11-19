"""
Two-stage RAG grounding experiment.

Run from project root:

python -m experiments.rag_two_stage_grounding_evaluation

Purpose:
Test whether a separate answerability check improves RAG grounding.

Pipeline:
1. Retrieve production Top-5 context.
2. Ask Qwen whether the requested fact is explicitly supported by the context.
3. If NOT_SUPPORTED, return the standard "not enough information" answer.
4. If SUPPORTED, generate the answer using the current grounding prompt.

This experiment does not modify production code.
"""

from time import perf_counter

from llm.local_provider import LocalLLMProvider
from retrieval import retrieve_knowledge
from experiments.archive.rag_production_evaluation import (
    TEST_CASES,
    evaluate_retrieval,
    evaluate_generation,
)


NO_INFORMATION_ANSWER = (
    "Det finns inte tillräcklig information i kunskapsbasen."
)


def build_support_system_prompt() -> str:
    """Build instructions for the answerability check."""

    return """
Decide whether the context explicitly contains the exact information needed
to answer the question.

Return exactly one label:

SUPPORTED
or
NOT_SUPPORTED

Rules:
- SUPPORTED means the context explicitly contains the requested fact.
- NOT_SUPPORTED means the context does not explicitly contain the requested fact.
- Related information is not enough.
- Information about a different property, event, category, person, entity,
  or time period does not count as support.
- Do not infer missing information.
- Do not answer the question itself.
""".strip()


def build_support_prompt(context: str, question: str) -> str:
    """Build the user prompt for the support check."""

    return f"""
CONTEXT:
{context}

QUESTION:
{question}

LABEL:
""".strip()


def build_answer_system_prompt() -> str:
    """Build the best-performing grounding prompt from the earlier experiment."""

    return """
Use only the information in the provided context to answer the question.

Rules:
- Do not substitute information about a different property, event, or category for the one asked about. If the context only provides a related but different fact, treat the requested information as missing.
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
""".strip()


def build_answer_prompt(context: str, question: str) -> str:
    """Build the user prompt for answer generation."""

    return f"""
CONTEXT:
{context}

QUESTION:
{question}
""".strip()


def parse_support_label(raw_label: str) -> bool | None:
    """Convert model output into True/False support status."""

    label = raw_label.strip().upper()

    if label.startswith("NOT_SUPPORTED"):
        return False

    if label.startswith("SUPPORTED"):
        return True

    return None


def run_evaluation() -> None:
    """Run the two-stage grounding evaluation."""

    print()
    print("#" * 72)
    print("TWO-STAGE RAG GROUNDING EVALUATION")
    print("Retrieval: current production Top-5")
    print("LLM: Qwen3-1.7B")
    print("Stage 1: SUPPORTED / NOT_SUPPORTED")
    print("Stage 2: answer generation only when supported")
    print("#" * 72)

    llm = LocalLLMProvider("Qwen/Qwen3-1.7B")

    support_system_prompt = build_support_system_prompt()
    answer_system_prompt = build_answer_system_prompt()

    retrieval_pass_count = 0
    retrieval_test_count = 0

    support_pass_count = 0
    support_test_count = 0

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
        print("Expected support:", test["should_answer"])
        print("-" * 72)

        # -----------------------------------------------------
        # Retrieval
        # -----------------------------------------------------

        retrieval_start = perf_counter()

        results = retrieve_knowledge(
            test["question"]
        )

        retrieval_time = perf_counter() - retrieval_start

        retrieval_pass = evaluate_retrieval(
            test,
            results,
        )

        if retrieval_pass is not None:
            retrieval_test_count += 1

            if retrieval_pass:
                retrieval_pass_count += 1

        print()
        print("Retrieved:")

        if results:
            for rank, result in enumerate(results, start=1):
                print(
                    f"{rank}. "
                    f"semantic={result['semantic_score']:.3f} | "
                    f"hybrid={result['score']:.3f} | "
                    f"identifier={result['identifier_match']}"
                )
                print(result["text"])
        else:
            print("No results.")

        # -----------------------------------------------------
        # Stage 1: answerability / support check
        # -----------------------------------------------------

        support_raw = ""
        support_status = False
        support_time = 0.0

        if results:
            context = "\n".join(
                result["text"]
                for result in results
            )

            support_prompt = build_support_prompt(
                context,
                test["question"],
            )

            support_start = perf_counter()

            support_raw = llm.generate(
                support_prompt,
                system_prompt=support_system_prompt,
                max_new_tokens=20,
            )

            support_time = perf_counter() - support_start

            parsed_support = parse_support_label(
                support_raw
            )

            support_status = (
                parsed_support
                if parsed_support is not None
                else False
            )
        else:
            context = ""
            support_raw = "NOT_SUPPORTED (no retrieval results)"
            support_status = False

        expected_support = test["should_answer"]
        support_pass = support_status == expected_support

        support_test_count += 1

        if support_pass:
            support_pass_count += 1

        # -----------------------------------------------------
        # Stage 2: answer generation
        # -----------------------------------------------------

        generation_time = 0.0

        if support_status and results:

            answer_prompt = build_answer_prompt(
                context,
                test["question"],
            )

            generation_start = perf_counter()

            answer = llm.generate(
                answer_prompt,
                system_prompt=answer_system_prompt,
            )

            generation_time = (
                perf_counter() - generation_start
            )

        else:
            answer = NO_INFORMATION_ANSWER

        generation_pass = evaluate_generation(
            test,
            answer,
        )

        if generation_pass:
            generation_pass_count += 1

        # -----------------------------------------------------
        # Output
        # -----------------------------------------------------

        print()
        print("Support check:")
        print("Raw:", support_raw)
        print("Parsed:", support_status)
        print(
            "Support result:",
            "PASS" if support_pass else "FAIL",
        )

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
            ),
        )

        print(
            "Generation result:",
            "PASS" if generation_pass else "FAIL",
        )

        print(
            f"Retrieval time: {retrieval_time:.3f}s"
        )

        print(
            f"Support-check time: {support_time:.3f}s"
        )

        print(
            f"Generation time: {generation_time:.3f}s"
        )

        if (
            retrieval_pass is False
            or not support_pass
            or not generation_pass
        ):
            failures.append({
                "question": test["question"],
                "category": test["category"],
                "retrieval_pass": retrieval_pass,
                "expected_support": expected_support,
                "support_raw": support_raw,
                "support_status": support_status,
                "support_pass": support_pass,
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
        f"{retrieval_pass_count}/{retrieval_test_count} PASS",
    )

    print(
        "Support check:",
        f"{support_pass_count}/{support_test_count} PASS",
    )

    print(
        "Generation:",
        f"{generation_pass_count}/{len(TEST_CASES)} PASS",
    )

    print(
        f"Total evaluation time: {total_time:.2f}s"
    )

    print()

    if failures:
        print("FAILURES")
        print("-" * 72)

        for failure in failures:

            retrieval_result = (
                "N/A"
                if failure["retrieval_pass"] is None
                else failure["retrieval_pass"]
            )

            print(
                f"[{failure['category']}] "
                f"{failure['question']}"
            )

            print(
                "Retrieval:",
                retrieval_result,
            )

            print(
                "Expected support:",
                failure["expected_support"],
            )

            print(
                "Support raw:",
                failure["support_raw"],
            )

            print(
                "Support parsed:",
                failure["support_status"],
            )

            print(
                "Support:",
                failure["support_pass"],
            )

            print(
                "Generation:",
                failure["generation_pass"],
            )

            print(
                "Answer:",
                failure["answer"],
            )

            print()

    else:
        print("All evaluation cases passed.")


if __name__ == "__main__":
    run_evaluation()
