from app.core.ai_client import get_openai_client
from app.core.config import settings


class LLMService:
    def __init__(self):
        self.client = get_openai_client()
        self.model = settings.GENERATION_MODEL

    def generate_answer(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful RAG assistant. "
                        "Answer only based on the provided context. "
                        "If the answer is not in the context, say: "
                        "'I could not find the answer in the provided documents.'"
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0.2,
        )

        return response.choices[0].message.content.strip()
