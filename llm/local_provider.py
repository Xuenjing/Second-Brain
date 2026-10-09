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

        # format the text message to what Qwen expects
        formatted_prompt = self.generator.tokenizer.apply_chat_template(
            messages,
            tokenize = False, # return the formatted text (not the token ID)
            add_generation_prompt = True, # mark the assistent's turn to answer
            enable_thinking = False # remove thinking mode without specifically adding it to the message
        )

        result = self.generator(
            formatted_prompt,
            max_new_tokens = 100,
            do_sample = False
        )

        # first dictionary in list -> full generated text containing prompt and answer
        generated_text = result[0]["generated_text"]
        # remove the prompt and keep only the answer
        answer = generated_text[len(formatted_prompt):].strip()

        # NOT NEEDED WITH FORMATTED PROMPT: FEEL FREE TO REMOVE
        # strip away /think from answer if disabling thinking mode
        # if "</think>" in answer:
        #     answer = answer.split("</think>", 1)[1].strip()

        return answer
