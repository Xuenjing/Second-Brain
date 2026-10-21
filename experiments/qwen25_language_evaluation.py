"""
Evaluate whether a Swedish grounding prompt improves Qwen2.5-3B
language consistency without reducing answer quality.

The experiment compares:
1. Current English grounding prompt
2. Equivalent Swedish grounding prompt

Production MiniLM retrieval is used for both prompt variants.

Run from project root:

python -m experiments.qwen25_language_evaluation
"""

from time import perf_counter

from llm.local_provider import LocalLLMProvider
from retrieval import retrieve_knowledge


MODEL_NAME = "Qwen/Qwen2.5-3B-Instruct"


TEST_CASES = [
    # Negative / grounding cases where Qwen2.5 previously
    # answered correctly in meaning, but in English.
    {
        "question": "Har Johan ett telefonnummer?",
        "should_answer": False,
        "expected_entity": None,
        "expected_answer": None
    },
    {
        "question": "När öppnar Huvudmatsalen för middag?",
        "should_answer": False,
        "expected_entity": None,
        "expected_answer": None
    },
    {
        "question": "När serverar Matsal 18 middag?",
        "should_answer": False,
        "expected_entity": None,
        "expected_answer": None
    },

    # Positive control cases.
    {
        "question": "Har Natalie ett telefonnummer?",
        "should_answer": True,
        "expected_entity": "Natalie",
        "expected_answer": ["telefonnummer"]
    },
    {
        "question": "Har Niklas ett telefonnummer?",
        "should_answer": True,
        "expected_entity": "Niklas",
        "expected_answer": ["inget telefonnummer"]
    },
    {
        "question": "När öppnar Huvudmatsalen för lunch?",
        "should_answer": True,
        "expected_entity": "Huvudmatsalen",
        "expected_answer": ["11:00"]
    },
    {
        "question": "Vilka öppettider har Reception 5?",
        "should_answer": True,
        "expected_entity": "Reception 5",
        "expected_answer": ["9:00", "18:00"]
    },
    {
        "question": "Var finns Besöksparkering 7?",
        "should_answer": True,
        "expected_entity": "Besöksparkering 7",
        "expected_answer": ["byggnad B"]
    }
]


SWEDISH_NO_INFORMATION_PHRASES = [
    "inte tillräcklig information",
    "inte tillräckligt med information",
    "ingen information",
    "inget information",
    "saknas information",
    "informationen saknas",
    "framgår inte"
]


ENGLISH_NO_INFORMATION_PHRASES = [
    "not enough information",
    "insufficient information",
    "no information",
    "information is missing"
]


def create_english_prompt(
    question: str,
    context: str
) -> str:
    """Create the current English grounding prompt."""

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


def create_swedish_prompt(
    question: str,
    context: str
) -> str:
    """Create an equivalent grounding prompt written in Swedish."""

    return f"""
Använd endast informationen i kontexten nedan för att besvara frågan.

Regler:
- Innan du svarar, kontrollera att kontexten uttryckligen innehåller BÅDE:
  1. samma person eller entitet som nämns i frågan, och
  2. samma egenskap, händelse, måltid, tid eller fakta som efterfrågas.
- Information om lunch besvarar inte en fråga om middag.
- Information om en person besvarar inte en fråga om en annan person,
  även om deras namn liknar varandra.
- Ändra aldrig fakta från kontexten för att passa formuleringen i frågan.
- Om antingen entiteten eller den efterfrågade informationen saknas,
  svara att det inte finns tillräckligt med information i kunskapsbasen.
- Var särskilt uppmärksam på negationer som "inte", "inget",
  "ingen" och "har inte".
- Om kontexten uttryckligen säger att något inte är sant,
  får du inte svara att det är sant.
- Basera svaret på hela det relevanta påståendet,
  inte bara på ord som råkar matcha frågan.
- Identifiera det påstående i kontexten som handlar om samma person
  eller entitet som frågan.
- Svara strikt utifrån detta påstående.
- Dra inte slutsatser om en person eller entitet utifrån information
  om någon annan.
- Kontexten kan innehålla information som är relaterad till ämnet
  men som ändå inte besvarar frågan.
- Om kontexten inte uttryckligen innehåller informationen som behövs
  för att besvara frågan, svara att det inte finns tillräckligt med
  information i kunskapsbasen.
- Svara alltid på samma språk som frågan.
- Hitta inte på information.

KONTEXT:
{context}

FRÅGA:
{question}

SVAR:
"""


PROMPT_VARIANTS = [
    {
        "name": "Current English prompt",
        "function": create_english_prompt
    },
    {
        "name": "Swedish prompt",
        "function": create_swedish_prompt
    }
]


def evaluate_semantic_result(
    test: dict,
    answer: str
) -> bool:
    """Evaluate whether the answer is semantically correct."""

    answer_lower = answer.lower()

    if test["should_answer"]:
        entity_correct = (
            test["expected_entity"].lower()
            in answer_lower
        )

        facts_correct = all(
            expected.lower() in answer_lower
            for expected in test["expected_answer"]
        )

        return entity_correct and facts_correct

    # For negative cases, both Swedish and English refusal
    # phrases count as semantically correct.
    all_no_information_phrases = (
        SWEDISH_NO_INFORMATION_PHRASES
        + ENGLISH_NO_INFORMATION_PHRASES
    )

    return any(
        phrase in answer_lower
        for phrase in all_no_information_phrases
    )


def evaluate_swedish_fallback(
    test: dict,
    answer: str
) -> bool | None:
    """Check whether negative answers use Swedish fallback wording.

    Positive cases return None because this experiment specifically
    targets the known English fallback problem.
    """

    if test["should_answer"]:
        return None

    answer_lower = answer.lower()

    has_swedish_fallback = any(
        phrase in answer_lower
        for phrase in SWEDISH_NO_INFORMATION_PHRASES
    )

    has_english_fallback = any(
        phrase in answer_lower
        for phrase in ENGLISH_NO_INFORMATION_PHRASES
    )

    return (
        has_swedish_fallback
        and not has_english_fallback
    )


def prepare_retrievals() -> dict[str, list[dict]]:
    """Run production retrieval once per question."""

    retrievals = {}

    print()
    print("#" * 70)
    print("PREPARING PRODUCTION MINILM RETRIEVAL")
    print("#" * 70)

    for test in TEST_CASES:
        question = test["question"]

        print()
        print("Question:", question)

        retrievals[question] = retrieve_knowledge(
            question
        )

    return retrievals


def run_evaluation() -> None:
    """Compare Qwen2.5 behaviour using two prompt languages."""

    retrievals = prepare_retrievals()

    print()
    print("#" * 70)
    print("LOADING MODEL")
    print(MODEL_NAME)
    print("#" * 70)

    load_start = perf_counter()

    llm = LocalLLMProvider(
        MODEL_NAME
    )

    load_time = perf_counter() - load_start

    print(
        f"Model load time: "
        f"{load_time:.3f} seconds"
    )

    for prompt_variant in PROMPT_VARIANTS:
        print()
        print("*" * 70)
        print(
            "PROMPT:",
            prompt_variant["name"]
        )
        print("*" * 70)

        semantic_pass_count = 0

        negative_language_pass_count = 0
        negative_language_test_count = 0

        positive_pass_count = 0
        positive_test_count = 0

        generation_times = []

        for test in TEST_CASES:
            question = test["question"]
            results = retrievals[question]

            print()
            print("=" * 70)
            print("Question:", question)
            print(
                "Should answer:",
                test["should_answer"]
            )

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

            context = "\n".join(
                result["text"]
                for result in results
            )

            prompt = prompt_variant["function"](
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

            semantic_result = (
                evaluate_semantic_result(
                    test,
                    answer
                )
            )

            if semantic_result:
                semantic_pass_count += 1

            language_result = (
                evaluate_swedish_fallback(
                    test,
                    answer
                )
            )

            if test["should_answer"]:
                positive_test_count += 1

                if semantic_result:
                    positive_pass_count += 1

            else:
                negative_language_test_count += 1

                if language_result:
                    negative_language_pass_count += 1

            print("LLM answer:")
            print(answer)

            print()
            print(
                "Semantic result:",
                (
                    "PASS"
                    if semantic_result
                    else "FAIL"
                )
            )

            if language_result is None:
                print(
                    "Swedish fallback:",
                    "N/A"
                )
            else:
                print(
                    "Swedish fallback:",
                    (
                        "PASS"
                        if language_result
                        else "FAIL"
                    )
                )

            print(
                f"Generation time: "
                f"{generation_time:.3f} seconds"
            )

        total_generation_time = sum(
            generation_times
        )

        average_generation_time = (
            total_generation_time
            / len(generation_times)
        )

        print()
        print("-" * 70)
        print(
            "SUMMARY:",
            prompt_variant["name"]
        )

        print(
            "Semantic quality:",
            f"{semantic_pass_count}/"
            f"{len(TEST_CASES)} PASS"
        )

        print(
            "Positive control cases:",
            f"{positive_pass_count}/"
            f"{positive_test_count} PASS"
        )

        print(
            "Swedish fallback cases:",
            f"{negative_language_pass_count}/"
            f"{negative_language_test_count} PASS"
        )

        print(
            f"Average generation time: "
            f"{average_generation_time:.3f} seconds"
        )

        print("-" * 70)


if __name__ == "__main__":
    run_evaluation()