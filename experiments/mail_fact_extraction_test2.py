"""Manually evaluate fact extraction from a sample email."""

from imports.mail_fact_extractor import extract_mail_facts
from llm.local_provider import LocalLLMProvider


def main() -> None:
    """Run fact extraction and print the suggested facts."""
    email_text = """
Från den 1 januari 2027 ska frågor om säkerhetsklassning
av utvecklingsmiljöer gå via Maria Lind.
"""

    # Use the same model as the application.
    llm = LocalLLMProvider("Qwen/Qwen3-1.7B")

    try:
        facts = extract_mail_facts(email_text, llm)
    except ValueError as error:
        print(f"Fact extraction failed: {error}")
        return

    print("\nSUGGESTED FACTS:")

    if not facts:
        print("No facts were suggested.")

    for index, fact in enumerate(facts, start=1):
        print(f"{index}. {fact}")


if __name__ == "__main__":
    main()