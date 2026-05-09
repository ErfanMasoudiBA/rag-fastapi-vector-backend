from app.services.embedding_service import EmbeddingService
from app.services.vector_store_service import VectorStoreService
from app.schemas.vector_store import SearchResultItem


class RetrievalService:
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.vector_store_service = VectorStoreService()

    def retrieve(self, query: str, top_k: int = 3) -> dict:
        embedding_items = self.embedding_service.generate_embeddings([query])

        if not embedding_items:
            return {
                "query": query,
                "query_dimension": 0,
                "top_k": top_k,
                "results": []
            }

        query_embedding = embedding_items[0]["vector"]
        query_dimension = embedding_items[0]["embedding_dimension"]

        results = self.vector_store_service.search_similar(
            query_embedding=query_embedding,
            top_k=top_k
        )

        return {
            "query": query,
            "query_dimension": query_dimension,
            "top_k": top_k,
            "results": results
        }
