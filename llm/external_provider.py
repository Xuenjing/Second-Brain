from openai import OpenAI

class ExternalLLMProvider:
    def __init__(self, api_key: str, base_url: str, model_name: str) -> None:
        self.client = OpenAI(api_key=api_key, base_url=base_url, max_retries=0, timeout=30.0)
        self.model_name = model_name

    def generate(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model_name, 
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
        )

        return response.choices[0].message.content