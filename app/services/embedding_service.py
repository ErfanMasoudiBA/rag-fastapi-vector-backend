from openai import OpenAI
from app.core.config import settings
from typing import List

class EmbeddingService:
    def __init__(self):
        self.client = OpenAI(base_url=settings.BASE_URL, api_key=settings.OPENAI_API_KEY)
        self.model = settings.EMBEDDING_MODEL
        
    def generate_embeddings(self, texts: List[str]) -> list[dict]:
        response= self.client.embeddings.create(
            model=self.model,
            input=texts
        )

        results = []
        for idx, item in enumerate(response.data):
            vector = item.embedding
            results.append({
                "index": idx,
                "text": texts[idx],
                "vector": vector,
                "embedding_dimension": len(vector)
            })
        return results