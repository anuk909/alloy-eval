import os

from alloy_eval.models import AlloyPred
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()


class OpenAIClient:
    def __init__(self, model: str, temperature: float):
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY", ""),
        )
        self.model = model
        self.temperature = temperature

    def query(self, prompt: str) -> str | None:
        """Query OpenAI API with structured response."""
        try:
            response = self.client.beta.chat.completions.parse(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert in formal methods and the Alloy specification language. Complete the Alloy predicate implementation in one line.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=self.temperature,
                max_tokens=512,
                response_format=AlloyPred,
            )
            return response.choices[0].message.parsed.content
        except Exception as e:
            print(f"Error querying OpenAI API: {e}")
            return None
