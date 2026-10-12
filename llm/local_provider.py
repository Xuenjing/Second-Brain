from copy import deepcopy
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

        # creates a copy of the original settings of the model
        self.generation_config = deepcopy(self.generator.model.generation_config)

        self.generation_config.max_new_tokens = 100 # limits response length
        self.generation_config.do_sample = False # deterministic answers

        # standard settings -> not used while do_sample = False, but prevents error messages
        self.generation_config.temperature = 1.0
        self.generation_config.top_p = 1.0
        self.generation_config.top_k = 50


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
            generation_config=self.generation_config,
            clean_up_tokenization_spaces=False
        )

        # first dictionary in list -> full generated text containing prompt and answer
        generated_text = result[0]["generated_text"]
        # remove the prompt and keep only the answer
        answer = generated_text[len(formatted_prompt):].strip()

        return answer
