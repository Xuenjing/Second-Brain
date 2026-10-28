"""
Large-scale retrieval experiment.

Run from project root:

python -m experiments.large_scale_retrieval_test

Purpose:
Test how the production retrieval pipeline behaves with a larger and
more varied knowledge base.

The experiment:

1. Creates a temporary SQLite database.
2. Generates exactly 1000 synthetic knowledge entries.
3. Creates real MiniLM embeddings for all entries.
4. Stores the entries in the temporary database.
5. Runs a controlled set of retrieval questions.
6. Measures:
   - Top-1 accuracy
   - Top-5 hit rate
   - Average retrieval time
   - Slowest retrieval time
   - Database setup time

The real knowledge.db is never modified.
"""

import re

from sentence_transformers import util


from pathlib import Path
from tempfile import TemporaryDirectory
from time import perf_counter
from unittest.mock import patch

from database import (
    initialize_database,
    add_knowledge,
    get_all_knowledge,
)

from retrieval import (
    get_embedding_model
)


# ---------------------------------------------------------
# Dataset generation
# ---------------------------------------------------------

def person_text(index: int) -> str:
    department = (index % 25) + 1
    phone = 5000 + index

    return (
        f"Medarbetare {index} har telefonnummer {phone} "
        f"och arbetar på avdelning {department}."
    )


def room_text(index: int) -> str:
    buildings = ["A", "B", "C", "D", "E"]
    building = buildings[index % len(buildings)]

    floor = (index % 5) + 1
    capacity = 4 + (index % 20)

    return (
        f"Mötesrum {index} finns i byggnad {building} "
        f"på våning {floor} och har plats för "
        f"{capacity} personer."
    )


def reception_text(index: int) -> str:
    opening_hour = 7 + (index % 3)
    closing_hour = 16 + (index % 3)

    return (
        f"Reception {index} öppnar klockan "
        f"{opening_hour:02d}:00 och stänger klockan "
        f"{closing_hour:02d}:00."
    )


def dining_text(index: int) -> str:
    start_hour = 10 + (index % 2)
    start_minute = 30 if index % 3 == 0 else 00

    end_hour = 13 + (index % 2)
    end_minute = 30 if index % 4 == 0 else 00

    return (
        f"Matsal {index} serverar lunch mellan klockan "
        f"{start_hour:02d}:{start_minute:02d} och "
        f"{end_hour:02d}:{end_minute:02d}."
    )


def it_support_text(index: int) -> str:
    extension = 1200 + index

    return (
        f"IT-support för avdelning {index} nås via "
        f"internnummer {extension}."
    )


def policy_text(index: int) -> str:
    area = (index % 20) + 1

    return (
        f"Policy {index} kräver att besökare bär synlig "
        f"besöksbricka i område {area}."
    )


def project_text(index: int) -> str:
    day = (index % 27) + 1
    room = (index % 100) + 1

    return (
        f"Projekt {index} har nästa avstämningsmöte "
        f"den {day} november i Mötesrum {room}."
    )


def parking_text(index: int) -> str:
    buildings = ["A", "B", "C", "D", "E"]
    building = buildings[index % len(buildings)]

    return (
        f"Besöksparkering {index} finns vid byggnad "
        f"{building}."
    )


def generate_dataset() -> list[dict]:
    """Generate a large synthetic knowledge dataset."""

    entries = []

    # 150 people
    for index in range(1, 151):
        entries.append({
            "text": person_text(index),
            "source": "synthetic_people",
        })

    # 150 meeting rooms
    for index in range(1, 151):
        entries.append({
            "text": room_text(index),
            "source": "synthetic_rooms",
        })

    # 125 receptions
    for index in range(1, 126):
        entries.append({
            "text": reception_text(index),
            "source": "synthetic_receptions",
        })

    # 125 dining halls
    for index in range(1, 126):
        entries.append({
            "text": dining_text(index),
            "source": "synthetic_dining",
        })

    # 125 IT support entries
    for index in range(1, 126):
        entries.append({
            "text": it_support_text(index),
            "source": "synthetic_it",
        })

    # 125 policies
    for index in range(1, 126):
        entries.append({
            "text": policy_text(index),
            "source": "synthetic_policies",
        })

    # 100 projects
    for index in range(1, 101):
        entries.append({
            "text": project_text(index),
            "source": "synthetic_projects",
        })

    # 100 parking entries
    for index in range(1, 101):
        entries.append({
            "text": parking_text(index),
            "source": "synthetic_parking",
        })

    # -----------------------------------------------------
    # Semantic control entries
    # -----------------------------------------------------

    semantic_control_entries = [
        "Cykelverkstaden ligger bredvid den norra entrén.",
        "Företagshälsovården finns på bottenvåningen i byggnad D.",
        "Cafeterian serverar frukost fram till klockan 09:30.",
        "Besökare måste registrera sig i receptionen innan de går vidare.",
        "Lånecyklar kan hämtas vid transportcentralen.",
        "Postrummet tar emot interna paket fram till klockan 15:00.",
        "Tysta arbetsplatser finns på bibliotekets övre våning.",
        "Förlorade passerkort ska rapporteras till säkerhetsavdelningen.",
        "Videokonferensutrustning kan lånas från servicedisken.",
        "Kontorsmaterial beställs genom den interna inköpsportalen.",
        "Duschar för cykelpendlare finns bredvid omklädningsrummen.",
        "Gästnätverket kräver en tillfällig kod från receptionen.",
    ]

    for text in semantic_control_entries:
        entries.append({
            "text": text,
            "source": "synthetic_semantic_control",
        })

    return entries


# ---------------------------------------------------------
# Evaluation questions
# ---------------------------------------------------------

TEST_CASES = [
    # People
    {
        "category": "people",
        "question": "Vilket telefonnummer har Medarbetare 17?",
        "expected_text": person_text(17),
    },
    {
        "category": "people",
        "question": "Hur når jag Medarbetare 83 på telefon?",
        "expected_text": person_text(83),
    },
    {
        "category": "people",
        "question": "Vilket nummer har Medarbetare 149?",
        "expected_text": person_text(149),
    },

    # Rooms
    {
        "category": "rooms",
        "question": "Var ligger Mötesrum 12?",
        "expected_text": room_text(12),
    },
    {
        "category": "rooms",
        "question": "Hur många personer får plats i Mötesrum 84?",
        "expected_text": room_text(84),
    },
    {
        "category": "rooms",
        "question": "Vilken byggnad finns Mötesrum 143 i?",
        "expected_text": room_text(143),
    },

    # Receptions
    {
        "category": "receptions",
        "question": "När öppnar Reception 9?",
        "expected_text": reception_text(9),
    },
    {
        "category": "receptions",
        "question": "Vilka öppettider har Reception 64?",
        "expected_text": reception_text(64),
    },
    {
        "category": "receptions",
        "question": "När stänger Reception 117?",
        "expected_text": reception_text(117),
    },

    # Dining
    {
        "category": "dining",
        "question": "När serveras lunch i Matsal 8?",
        "expected_text": dining_text(8),
    },
    {
        "category": "dining",
        "question": "När kan jag äta lunch i Matsal 48?",
        "expected_text": dining_text(48),
    },
    {
        "category": "dining",
        "question": "Vilka lunchtider har Matsal 119?",
        "expected_text": dining_text(119),
    },

    # IT
    {
        "category": "it",
        "question": "Vilket internnummer har IT-support för avdelning 7?",
        "expected_text": it_support_text(7),
    },
    {
        "category": "it",
        "question": "Hur når jag supporten på avdelning 71?",
        "expected_text": it_support_text(71),
    },
    {
        "category": "it",
        "question": "Vad har IT-support för avdelning 124 för internnummer?",
        "expected_text": it_support_text(124),
    },

    # Policies
    {
        "category": "policies",
        "question": "Vad säger Policy 14 om besöksbrickor?",
        "expected_text": policy_text(14),
    },
    {
        "category": "policies",
        "question": "Vilka regler gäller enligt Policy 76?",
        "expected_text": policy_text(76),
    },
    {
        "category": "policies",
        "question": "Vad kräver Policy 121 av besökare?",
        "expected_text": policy_text(121),
    },

    # Projects
    {
        "category": "projects",
        "question": "När har Projekt 11 sitt nästa avstämningsmöte?",
        "expected_text": project_text(11),
    },
    {
        "category": "projects",
        "question": "Var hålls nästa möte för Projekt 57?",
        "expected_text": project_text(57),
    },
    {
        "category": "projects",
        "question": "Vilket mötesrum ska Projekt 96 använda?",
        "expected_text": project_text(96),
    },

    # Parking
    {
        "category": "parking",
        "question": "Var finns Besöksparkering 4?",
        "expected_text": parking_text(4),
    },
    {
        "category": "parking",
        "question": "Vilken byggnad ligger Besöksparkering 46 vid?",
        "expected_text": parking_text(46),
    },
    {
        "category": "parking",
        "question": "Var hittar jag Besöksparkering 99?",
        "expected_text": parking_text(99),
    },

    # ---------------------------------------------------------
    # Semantic retrieval without numeric identifiers
    # ---------------------------------------------------------

    {
        "category": "semantic control",
        "question": "Var hittar jag cykelverkstaden?",
        "expected_text": (
            "Cykelverkstaden ligger bredvid den norra entrén."
        ),
    },
    {
        "category": "semantic control",
        "question": "Var finns företagshälsovården?",
        "expected_text": (
            "Företagshälsovården finns på bottenvåningen "
            "i byggnad D."
        ),
    },
    {
        "category": "semantic control",
        "question": "Hur länge går det att få frukost i cafeterian?",
        "expected_text": (
            "Cafeterian serverar frukost fram till klockan 09:30."
        ),
    },
    {
        "category": "semantic control",
        "question": "Vad behöver en besökare göra innan den går in?",
        "expected_text": (
            "Besökare måste registrera sig i receptionen "
            "innan de går vidare."
        ),
    },
    {
        "category": "semantic control",
        "question": "Var kan jag hämta en lånecykel?",
        "expected_text": (
            "Lånecyklar kan hämtas vid transportcentralen."
        ),
    },
    {
        "category": "semantic control",
        "question": "När slutar postrummet ta emot interna paket?",
        "expected_text": (
            "Postrummet tar emot interna paket fram till "
            "klockan 15:00."
        ),
    },
    {
        "category": "semantic control",
        "question": "Var kan jag arbeta ostört?",
        "expected_text": (
            "Tysta arbetsplatser finns på bibliotekets övre våning."
        ),
    },
    {
        "category": "semantic control",
        "question": "Vad gör jag om jag tappar bort mitt passerkort?",
        "expected_text": (
            "Förlorade passerkort ska rapporteras till "
            "säkerhetsavdelningen."
        ),
    },

    # ---------------------------------------------------------
    # Identifier paraphrases not recognized by current regex
    # ---------------------------------------------------------

    {
        "category": "identifier paraphrase",
        "question": "Hur når jag IT på den sjunde avdelningen?",
        "expected_text": it_support_text(7),
    },
    {
        "category": "identifier paraphrase",
        "question": "Vilka öppettider har reception nummer 64?",
        "expected_text": reception_text(64),
    },
    {
        "category": "identifier paraphrase",
        "question": "Hur många får plats i mötesrum nummer 84?",
        "expected_text": room_text(84),
    },
    {
        "category": "identifier paraphrase",
        "question": "Vad står det i policy nummer 14?",
        "expected_text": policy_text(14),
    },

]


# ---------------------------------------------------------
# Database setup
# ---------------------------------------------------------

def populate_database(entries: list[dict]) -> float:
    """
    Create embeddings and store all generated entries.

    Embeddings are created in one batch because this experiment focuses
    on retrieval behaviour rather than measuring individual import speed.

    Returns:
        Total setup time in seconds.
    """

    start = perf_counter()

    texts = [
        entry["text"]
        for entry in entries
    ]

    model = get_embedding_model()

    print(f"Creating embeddings for {len(entries)} entries...")

    embeddings = model.encode(
        texts,
        batch_size=32,
        show_progress_bar=True,
    )

    print("Saving entries to temporary database...")

    for entry, embedding in zip(entries, embeddings):
        add_knowledge(
            entry["text"],
            embedding,
            source=entry["source"],
        )

    return perf_counter() - start


# ---------------------------------------------------------
# Evaluation
# ---------------------------------------------------------

IDENTIFIER_PATTERNS = [
    r"\bmötesrum(?:\s+nummer)?\s+\d+\b",
    r"\breception(?:\s+nummer)?\s+\d+\b",
    r"\bmatsal(?:\s+nummer)?\s+\d+\b",
    r"\bpolicy(?:\s+nummer)?\s+\d+\b",
    r"\bavdelning(?:\s+nummer)?\s+\d+\b",
    r"\bmedarbetare(?:\s+nummer)?\s+\d+\b",
    r"\bbesöksparkering(?:\s+nummer)?\s+\d+\b",
    r"\bprojekt(?:\s+nummer)?\s+\d+\b",
]

def normalize_identifier(identifier: str) -> str:
    return identifier.replace(" nummer ", " ")

def extract_identifiers(text: str) -> set[str]:
    """Extract important named numeric identifiers from text."""

    text = text.lower()

    identifiers = set()

    for pattern in IDENTIFIER_PATTERNS:
        matches = re.findall(pattern, text)

        for match in matches:
            identifiers.add(
                normalize_identifier(match)
            )

    return identifiers


def retrieve_hybrid(
    query: str,
    top_k: int = 5,
    threshold: float = 0.45,
    identifier_boost: float = 0.20,
) -> list[dict]:
    """
    Retrieve knowledge using semantic similarity plus an exact
    identifier-match bonus.
    """

    knowledge = get_all_knowledge()

    if not knowledge:
        return []

    model = get_embedding_model()

    query_embedding = model.encode(query)

    query_identifiers = extract_identifiers(query)

    results = []

    for item in knowledge:
        semantic_score = util.cos_sim(
            query_embedding,
            item["embedding"],
        )[0][0].item()

        item_identifiers = extract_identifiers(
            item["text"]
        )

        identifier_match = bool(
            query_identifiers
            and query_identifiers.intersection(
                item_identifiers
            )
        )

        hybrid_score = semantic_score

        if identifier_match:
            hybrid_score += identifier_boost

        results.append({
            "id": item["id"],
            "text": item["text"],
            "source": item["source"],
            "semantic_score": semantic_score,
            "identifier_match": identifier_match,
            "score": hybrid_score,
            "created_at": item["created_at"],
        })

    results.sort(
        key=lambda result: result["score"],
        reverse=True,
    )

    filtered_results = [
        result
        for result in results
        if result["semantic_score"] >= threshold
    ]

    return filtered_results[:top_k]

def run_retrieval_evaluation() -> None:
    """Run all retrieval questions and print metrics."""

    top_1_passes = 0
    top_5_passes = 0

    retrieval_times = []

    failures = []

    print()
    print("#" * 72)
    print("RUNNING RETRIEVAL EVALUATION")
    print("#" * 72)

    for index, test in enumerate(TEST_CASES, start=1):

        start = perf_counter()

        # retrieve_knowledge currently prints its own debug information.
        # Suppress that output here so this experiment remains readable.
        results = retrieve_hybrid(
            test["question"]
        )

        retrieval_time = perf_counter() - start
        retrieval_times.append(retrieval_time)

        top_1_correct = (
            len(results) > 0
            and results[0]["text"] == test["expected_text"]
        )

        top_5_correct = any(
            result["text"] == test["expected_text"]
            for result in results
        )

        if top_1_correct:
            top_1_passes += 1

        if top_5_correct:
            top_5_passes += 1

        expected_rank = None
        expected_score = None

        for rank, result in enumerate(results, start=1):
            if result["text"] == test["expected_text"]:
                expected_rank = rank
                expected_score = result["score"]
                break

        print()
        print(
            f"{index:02d}/{len(TEST_CASES)} "
            f"[{test['category']}]"
        )
        print("Question:", test["question"])

        if expected_rank is not None:
            print(
                f"Expected result: rank {expected_rank} "
                f"| score={expected_score:.3f}"
            )
        else:
            print("Expected result: NOT RETRIEVED")

        print(
            "Top-1:",
            "PASS" if top_1_correct else "FAIL"
        )

        print(
            "Top-5:",
            "PASS" if top_5_correct else "FAIL"
        )

        print(
            f"Time: {retrieval_time:.4f}s"
        )

        if not top_5_correct:
            failures.append({
                "question": test["question"],
                "category": test["category"],
                "expected": test["expected_text"],
                "results": results,
            })

    # -----------------------------------------------------
    # Summary
    # -----------------------------------------------------

    average_time = (
        sum(retrieval_times)
        / len(retrieval_times)
    )

    slowest_time = max(retrieval_times)
    fastest_time = min(retrieval_times)

    total_tests = len(TEST_CASES)

    print()
    print("#" * 72)
    print("RETRIEVAL SUMMARY")
    print("#" * 72)

    print(
        f"Top-1 accuracy: "
        f"{top_1_passes}/{total_tests} "
        f"({top_1_passes / total_tests:.1%})"
    )

    print(
        f"Top-5 hit rate: "
        f"{top_5_passes}/{total_tests} "
        f"({top_5_passes / total_tests:.1%})"
    )

    print(
        f"Average retrieval time: "
        f"{average_time:.4f}s"
    )

    print(
        f"Fastest retrieval: "
        f"{fastest_time:.4f}s"
    )

    print(
        f"Slowest retrieval: "
        f"{slowest_time:.4f}s"
    )

    print()

    if failures:
        print("TOP-5 FAILURES")
        print("-" * 72)

        for failure in failures:
            print()
            print(
                f"[{failure['category']}] "
                f"{failure['question']}"
            )

            print(
                "Expected:",
                failure["expected"]
            )

            print("Retrieved:")

            if failure["results"]:
                for rank, result in enumerate(
                    failure["results"],
                    start=1,
                ):
                    print(
                        f"  {rank}. "
                        f"semantic={result['semantic_score']:.3f} | "
                        f"hybrid={result['score']:.3f} | "
                        f"identifier={result['identifier_match']} | "
                        f"{result['text']}"
                    )
            else:
                print("  No results.")

    else:
        print(
            "All expected entries appeared "
            "within the top 5."
        )


# ---------------------------------------------------------
# Main experiment
# ---------------------------------------------------------

def run_experiment() -> None:
    """Create temporary data and run the large-scale experiment."""

    dataset = generate_dataset()

    print()
    print("#" * 72)
    print("LARGE-SCALE RETRIEVAL TEST")
    print("#" * 72)
    print(f"Generated entries: {len(dataset)}")
    print(f"Evaluation questions: {len(TEST_CASES)}")
    print(
        "Embedding model: "
        "paraphrase-multilingual-MiniLM-L12-v2"
    )
    print("Production threshold: 0.45")
    print("Production top_k: 5")

    with TemporaryDirectory() as temp_dir:

        database_path = (
            Path(temp_dir)
            / "large_scale_test.db"
        )

        with patch(
            "database.DATABASE_PATH",
            str(database_path)
        ):
            initialize_database()

            setup_time = populate_database(
                dataset
            )

            stored_entries = get_all_knowledge()

            print()
            print(
                f"Stored entries: "
                f"{len(stored_entries)}"
            )

            print(
                f"Database setup time: "
                f"{setup_time:.2f}s"
            )

            run_retrieval_evaluation()

    print()
    print(
        "Temporary database deleted. "
        "The production knowledge.db was not modified."
    )


if __name__ == "__main__":
    run_experiment()