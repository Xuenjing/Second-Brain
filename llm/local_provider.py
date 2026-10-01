from transformers import pipeline
from performance import measure_time

class LocalLLMProvider:
    '''
    Creates a class container for a local model which can then be queried
    with generate(prompt) without the calling code needing to know about pipeline(),
    the model or result parsing
    '''
    
    @measure_time
    def __init__(self, model_name):
        self.model_name = model_name

        self.generator = pipeline(
            "text-generation",
            model = self.model_name
        )

    @measure_time
    def generate(self, prompt):
        messages = [
            {
                "role": "user",
                "content": prompt
            }
        ]

        result = self.generator(
            messages,
            max_new_tokens = 50,
            do_sample = False
        )

        # First dictionary in list -> list with chat messages -> last message (assistant) -> content
        answer = result[0]["generated_text"][-1]["content"]

        return answer
