from openai import OpenAI
from app.core.config import settings
from typing import List
from app.core.ai_client import get_openai_client

class EmbeddingService:
    def __init__(self):
        self.client = get_openai_client()
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