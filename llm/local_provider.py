from copy import deepcopy

from transformers import pipeline

from performance import measure_time


class LocalLLMProvider:
    """Create a class container for a local model which can then be queried
    with generate(prompt) without the calling code needing to know about pipeline(),
    the model or result parsing.
    """
    
    @measure_time
    def __init__(self, model_name: str) -> None:
        """Initialize a local language model.
        
        Args:
            model_name: Name of the model to load.
        """
        self.model_name = model_name

        self.generator = pipeline(
            "text-generation",
            model=self.model_name
        )

        # Create a copy of the original settings of the model.
        self.generation_config = deepcopy(self.generator.model.generation_config)

        # Limit response length.
        self.generation_config.max_new_tokens = 200
        
        # Deterministic answers
        self.generation_config.do_sample = False

        # Standard settings -> not used while do_sample = False, but prevents error messages.
        self.generation_config.temperature = 1.0
        self.generation_config.top_p = 1.0
        self.generation_config.top_k = 50


    @measure_time
    def generate(self, prompt: str, system_prompt: str | None = None, max_new_tokens: int | None = None) -> str:
        """Generate an answer based on provided prompt using the local language model.

        System messages defines behaviours of the assistant.
        The user message is defined by the prompt.
        Messages are then converted to a format expected by the language model,
        with thinking_mode disabled, and then generated into a response using model settings.

        Args:
            prompt: Prompt to send to the language model.
            system_prompt: Optional system instructions for the task.
            max_new_tokens: Optional output token limit for this call.

        Returns:
            Generated assistant response.
        """
        
        # Use the default chat instructions unless custom ones are provided.
        if system_prompt is None:
            system_prompt = (
                "Always answer in the same language as the user's QUESTION. "
                "Use the language of the QUESTION, not the language used "
                "in the instructions or context."
            )

        messages = [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": prompt
            }
        ]

        # Format the text message to what Qwen expects.
        formatted_prompt = self.generator.tokenizer.apply_chat_template(
            messages,
            # Let pipeline handle tokenization.
            tokenize=False,
            # Mark the assistent's turn to answer
            add_generation_prompt=True,
            # Disable Qwen thinking mode.
            enable_thinking=False
        )

        # Apply task-specific settings without changing the chat defaults.
        generation_config = deepcopy(self.generation_config)

        if max_new_tokens is not None:
            generation_config.max_new_tokens = max_new_tokens

        # Generate text using configuration settings.
        result = self.generator(
            formatted_prompt,
            generation_config=generation_config,
            clean_up_tokenization_spaces=False
        )

        # Pipeline returns original prompt followed by generated text.
        generated_text = result[0]["generated_text"]
        # Remove the prompt and keep only the assistant's answer.
        answer = generated_text[len(formatted_prompt):].strip()

        return answer