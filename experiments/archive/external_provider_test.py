"""
run from project root:
python -m experiments.external_provider_test
"""

import os
import time

from dotenv import load_dotenv

from llm.external_provider import ExternalLLMProvider

from openai import InternalServerError, RateLimitError


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if api_key is None:
    raise ValueError("GEMINI_API_KEY is missing from .env")

provider = ExternalLLMProvider(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    model_name="gemini-3.8-flash",
)

prompts = [
    "What is 2+2? Answer with only the number.",
    "Svara på svenska: Vad heter Sveriges huvudstad?",
    """
Use only the context below to answer the question.

CONTEXT:
The Atlas meeting room has capacity for 60 people.

QUESTION:
How many people can fit in the Atlas meeting room?
"""
]

for prompt in prompts:
    start = time.perf_counter()
    print("\nPROMPT:")
    print(prompt)

    try:
        answer = provider.generate(prompt)
        print("\nANSWER:")
        print(answer)
    except InternalServerError as error:
        print(f"External model unavailable: {error}")
    except RateLimitError as error:
        print(f"API quota exceeded: {error}")
    
    elapsed_time = time.perf_counter() - start
    print(f"elapsed time: {elapsed_time:.3f} seconds")
        

