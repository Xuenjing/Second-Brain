"""
E5 similarity threshold evaluation.

Run from project root:

python -m experiments.e5_threshold_evaluation

Purpose:
Evaluate which similarity threshold is appropriate for the current
E5-based production retrieval.

The experiment uses the existing knowledge database and compares:

- positive questions where a known knowledge entry should be retrieved
- unrelated negative questions where nothing should be retrieved
- hard negative questions where related information exists, but does
  not actually answer the question

No knowledge is added, edited or deleted.
"""

from sentence_transformers import util

from database import get_all_knowledge
from retrieval import create_query_embedding


TOP_K = 5

THRESHOLDS = [
    0.45,
    0.75,
    0.80,
    0.82,
    0.85,
    0.88,
    0.90,
]


# ---------------------------------------------------------
# Positive cases
#
# The expected knowledge should be present within Top-5.
# ---------------------------------------------------------

POSITIVE_CASES = [
    {
        "category": "negation",
        "question": "Har Niklas ett telefonnummer?",
        "expected": "Niklas har inget telefonnummer",
    },
    {
        "category": "paraphrase + negation",
        "question": "Finns det något telefonnummer till Niklas?",
        "expected": "Niklas har inget telefonnummer",
    },
    {
        "category": "similar entities",
        "question": "Vilket internnummer har IT-support för avdelning 9?",
        "expected": (
            "IT-support för avdelning 9 nås via internnummer 1209"
        ),
    },
    {
        "category": "similar entities + paraphrase",
        "question": "Hur når jag supporten på avdelning 5?",
        "expected": (
            "IT-support för avdelning 5 nås via internnummer 1205"
        ),
    },
    {
        "category": "opening hours",
        "question": "När är Reception 17 öppen?",
        "expected": (
            "Reception 17 öppnar klockan 9:00 och "
            "stänger klockan 18:00"
        ),
    },
    {
        "category": "opening hours + entity distinction",
        "question": "Vilka öppettider har Reception 12?",
        "expected": (
            "Reception 12 öppnar klockan 7:00 och "
            "stänger klockan 16:00"
        ),
    },
    {
        "category": "paraphrase",
        "question": "När kan man äta lunch i Matsal 18?",
        "expected": (
            "Matsal 18 serverar lunch mellan klockan "
            "10:30 och 13:30"
        ),
    },
    {
        "category": "paraphrase",
        "question": "Mellan vilka tider serveras lunchen i Matsal 1?",
        "expected": (
            "Matsal 1 serverar lunch mellan klockan "
            "11:30 och 14:30"
        ),
    },
    {
        "category": "known MiniLM weakness",
        "question": "Vilka är Huvudmatsalens öppettider för lunch?",
        "expected": (
            "Huvudmatsalen öppnar för lunch klockan 11:00"
        ),
    },
    {
        "category": "known MiniLM weakness + paraphrase",
        "question": "När kan jag äta lunch i Huvudmatsalen?",
        "expected": (
            "Huvudmatsalen öppnar för lunch klockan 11:00"
        ),
    },
    {
        "category": "location paraphrase",
        "question": "Vilken byggnad ligger Besöksparkering 7 vid?",
        "expected": (
            "Besöksparkering 7 finns vid byggnad B"
        ),
    },
]


# ---------------------------------------------------------
# Unrelated negatives
#
# Ideally no knowledge should pass the similarity threshold.
# ---------------------------------------------------------

UNRELATED_NEGATIVE_CASES = [
    {
        "question": "Finns det en swimmingpool?",
    },
    {
        "question": "När går tåget till Göteborg?",
    },
    {
        "question": "Var finns tandläkaren?",
    },
    {
        "question": "Vilket lösenord har wifi-nätverket?",
    },
    {
        "question": "Finns det en frisör i byggnaden?",
    },
]


# ---------------------------------------------------------
# Hard negatives
#
# Related knowledge exists, but it does not answer the requested fact.
#
# These are important because a similarity threshold may NOT be able
# to distinguish them from genuinely relevant information.
# ---------------------------------------------------------

HARD_NEGATIVE_CASES = [
    {
        "category": "meal mismatch",
        "question": "När serverar Matsal 18 middag?",
    },
    {
        "category": "meal mismatch",
        "question": "När öppnar Huvudmatsalen för middag?",
    },
    {
        "category": "missing entity",
        "question": "Har Johan ett telefonnummer?",
    },
    {
        "category": "missing property",
        "question": "Vad är telefonnumret till Reception 5?",
    },
]


# ---------------------------------------------------------
# Retrieval
# ---------------------------------------------------------

def get_ranked_results(
    query: str,
    knowledge: list[dict],
) -> list[dict]:
    """Calculate raw E5 similarity scores for a query.

    No threshold is applied here. This allows the same raw retrieval
    results to be evaluated against several different thresholds.

    Args:
        query: Search query to evaluate.
        knowledge: Knowledge entries containing stored E5 embeddings.

    Returns:
        All knowledge entries sorted by descending similarity score.
    """

    query_embedding = create_query_embedding(query)

    results = []

    for item in knowledge:
        score = util.cos_sim(
            query_embedding,
            item["embedding"],
        )[0][0].item()

        results.append({
            "text": item["text"],
            "source": item["source"],
            "score": score,
        })

    results.sort(
        key=lambda result: result["score"],
        reverse=True,
    )

    return results


def apply_threshold(
    results: list[dict],
    threshold: float,
) -> list[dict]:
    """Apply a similarity threshold and Top-K limit."""

    filtered = [
        result
        for result in results
        if result["score"] >= threshold
    ]

    return filtered[:TOP_K]


def expected_is_retrieved(
    results: list[dict],
    expected: str,
) -> bool:
    """Check whether expected knowledge appears in retrieved results."""

    return any(
        expected.lower() in result["text"].lower()
        for result in results
    )


# ---------------------------------------------------------
# Diagnostics
# ---------------------------------------------------------

def print_positive_diagnostics(
    knowledge: list[dict],
) -> None:
    """Print raw retrieval scores for all positive questions."""

    print()
    print("#" * 72)
    print("POSITIVE CASES - RAW E5 SCORES")
    print("#" * 72)

    for test in POSITIVE_CASES:
        results = get_ranked_results(
            test["question"],
            knowledge,
        )

        expected_rank = None
        expected_score = None

        for rank, result in enumerate(results, start=1):
            if test["expected"].lower() in result["text"].lower():
                expected_rank = rank
                expected_score = result["score"]
                break

        print()
        print(
            f"[{test['category']}] "
            f"{test['question']}"
        )

        if expected_rank is None:
            print("Expected knowledge: NOT FOUND")
        else:
            print(
                f"Expected knowledge: "
                f"rank={expected_rank} | "
                f"score={expected_score:.3f}"
            )

        print("Top 5 raw results:")

        for rank, result in enumerate(
            results[:TOP_K],
            start=1,
        ):
            print(
                f"  {rank}. "
                f"score={result['score']:.3f} | "
                f"{result['text']}"
            )


def print_negative_diagnostics(
    knowledge: list[dict],
) -> None:
    """Print highest raw scores for negative questions."""

    print()
    print("#" * 72)
    print("NEGATIVE CASES - RAW E5 SCORES")
    print("#" * 72)

    all_negative_cases = []

    for test in UNRELATED_NEGATIVE_CASES:
        all_negative_cases.append({
            "category": "unrelated",
            "question": test["question"],
        })

    all_negative_cases.extend(HARD_NEGATIVE_CASES)

    for test in all_negative_cases:
        results = get_ranked_results(
            test["question"],
            knowledge,
        )

        print()
        print(
            f"[{test['category']}] "
            f"{test['question']}"
        )

        print("Top 5 raw results:")

        for rank, result in enumerate(
            results[:TOP_K],
            start=1,
        ):
            print(
                f"  {rank}. "
                f"score={result['score']:.3f} | "
                f"{result['text']}"
            )


# ---------------------------------------------------------
# Threshold comparison
# ---------------------------------------------------------

def evaluate_threshold(
    knowledge: list[dict],
    threshold: float,
) -> dict:
    """Evaluate one threshold against all test cases."""

    positive_passes = 0

    unrelated_negative_passes = 0
    hard_negative_passes = 0

    for test in POSITIVE_CASES:
        raw_results = get_ranked_results(
            test["question"],
            knowledge,
        )

        results = apply_threshold(
            raw_results,
            threshold,
        )

        if expected_is_retrieved(
            results,
            test["expected"],
        ):
            positive_passes += 1

    for test in UNRELATED_NEGATIVE_CASES:
        raw_results = get_ranked_results(
            test["question"],
            knowledge,
        )

        results = apply_threshold(
            raw_results,
            threshold,
        )

        # Correct behaviour for these questions means that
        # nothing survives the threshold.
        if not results:
            unrelated_negative_passes += 1

    for test in HARD_NEGATIVE_CASES:
        raw_results = get_ranked_results(
            test["question"],
            knowledge,
        )

        results = apply_threshold(
            raw_results,
            threshold,
        )

        # Again, for threshold evaluation alone, a pass means
        # that no result survives.
        #
        # We expect these cases to be difficult because related
        # information may have a very high semantic similarity.
        if not results:
            hard_negative_passes += 1

    return {
        "threshold": threshold,
        "positive": positive_passes,
        "unrelated_negative": unrelated_negative_passes,
        "hard_negative": hard_negative_passes,
    }


def print_threshold_comparison(
    knowledge: list[dict],
) -> None:
    """Compare all configured thresholds."""

    print()
    print("#" * 72)
    print("THRESHOLD COMPARISON")
    print("#" * 72)

    print()
    print(
        f"{'Threshold':<12}"
        f"{'Positive':<16}"
        f"{'Unrelated neg.':<20}"
        f"{'Hard neg.':<16}"
    )

    print("-" * 64)

    for threshold in THRESHOLDS:
        result = evaluate_threshold(
            knowledge,
            threshold,
        )

        print(
            f"{threshold:<12.2f}"
            f"{result['positive']}/{len(POSITIVE_CASES):<13}"
            f"{result['unrelated_negative']}/"
            f"{len(UNRELATED_NEGATIVE_CASES):<18}"
            f"{result['hard_negative']}/"
            f"{len(HARD_NEGATIVE_CASES):<13}"
        )


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def run_evaluation() -> None:
    """Run the complete E5 threshold evaluation."""

    knowledge = get_all_knowledge()

    print()
    print("#" * 72)
    print("E5 SIMILARITY THRESHOLD EVALUATION")
    print("#" * 72)

    print(
        f"Knowledge entries: {len(knowledge)}"
    )

    print(
        "Embedding model: "
        "intfloat/multilingual-e5-small"
    )

    print(
        f"Positive cases: "
        f"{len(POSITIVE_CASES)}"
    )

    print(
        f"Unrelated negative cases: "
        f"{len(UNRELATED_NEGATIVE_CASES)}"
    )

    print(
        f"Hard negative cases: "
        f"{len(HARD_NEGATIVE_CASES)}"
    )

    if not knowledge:
        print()
        print(
            "Knowledge database is empty. "
            "Import E5-embedded knowledge before running this experiment."
        )
        return

    print_positive_diagnostics(
        knowledge
    )

    print_negative_diagnostics(
        knowledge
    )

    print_threshold_comparison(
        knowledge
    )


if __name__ == "__main__":
    run_evaluation()