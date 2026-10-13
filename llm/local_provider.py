import torch

from copy import deepcopy
from transformers import pipeline, StoppingCriteria, StoppingCriteriaList
from performance import measure_time

class CancelGenerationCriteria(StoppingCriteria):
    """Stop generation when cancellation is requested."""

    def __init__(self, cancel_event):
        self.cancel_event = cancel_event

    def __call__(self, input_ids, scores, **kwargs):
        return torch.full(
            (input_ids.shape[0], 1),
            self.cancel_event.is_set(),
            dtype=torch.bool,
            device=input_ids.device
        )

class LocalLLMProvider:
    '''
    Creates a class container for a local model which can then be queried
    with generate(prompt) without the calling code needing to know about pipeline(),
    the model or result parsing
    '''
    
    @measure_time
    def __init__(self, model_name: str) -> None:
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
    def generate(self, prompt: str, cancel_event=None) -> str:
        '''
        Generates an answer based on provided prompt using the local language model.
        System messages defines behaviours of the assistant.
        The user message is defined by the prompt.
        Messages are then converted to a format expected by the language model,
        with thinking_mode disabled, and then generated into a response using model settings.
        
        '''
        messages = [
            {
                "role": "system",
                "content": (
                    "Always answer in the same language as the user's QUESTION. "
                    "Use the language of the QUESTION, not the language used in the instructions or context."
                    )
            },
            {
                "role": "user",
                "content": prompt
            }
        ]

        # format the text message to what Qwen expects
        formatted_prompt = self.generator.tokenizer.apply_chat_template(
            messages,
            tokenize = False, # keep results as text and let pipeline handle tokenization
            add_generation_prompt = True, # mark the assistent's turn to answer
            enable_thinking = False # disable thinking mode without specifically adding it to the message
        )

        result = self.generator(
            formatted_prompt,
            generation_config=self.generation_config,
            clean_up_tokenization_spaces=False,
            stopping_criteria=StoppingCriteriaList([
                CancelGenerationCriteria(cancel_event)
            ]) if cancel_event is not None else None
        )

        # Do not return partial text if generation was cancelled.
        if cancel_event is not None and cancel_event.is_set():
            return ""

        # Pipeline returns the original prompt followed by generated text.
        generated_text = result[0]["generated_text"]

        # remove the prompt and keep only the assistant's answer
        answer = generated_text[len(formatted_prompt):].strip()

        return answer
