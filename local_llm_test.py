'''
Local LLM candidate:
Qwen/Qwen3-4B-Instruct-2507
8gb disk size

License:
Model: Apache 2.0
Transformers: Apache 2.0

Status: testing purposes

Necessary libraries: pip install transformers torch
transformers: loading the models
torch: performing the computations

results:
Time spent loading the module and generating a single-sentence response was on current hardware:
loading model: 16.91
generating a response: 23.48
'''

if __name__ == "__main__":
    
    from transformers import pipeline
    import time

    start_loading = time.perf_counter()
    # generate text with specific model
    generator = pipeline(
        "text-generation",
        "Qwen/Qwen3-4B-Instruct-2507"
    )
    end_loading = time.perf_counter()
    loading_model = end_loading - start_loading

    # test
    messages = [
        {
        "role": "user",
        "content": "Explain python in one sentence."
        }
    ]

    # time the operation of generating a response
    start = time.perf_counter()
    # send to generator
    result = generator(
        messages,
        max_new_tokens = 50, # ceiling for how long the reply will be
        do_sample=False # less random replies
    )
    end = time.perf_counter()
    generating_response = end-start

    # pick the assistant's response
    # First dictionary in list -> list with chat messages -> last message (assistant) -> content
    answer = result[0]["generated_text"][-1]["content"]
    print(answer)
    print(f"Time spent loading model: {loading_model}")
    print(f"Time spent generating a response: {generating_response}")

