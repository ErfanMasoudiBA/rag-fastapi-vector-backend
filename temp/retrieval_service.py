from app.schemas.retrieval import RetrievalResponse, RetrievedChunk
from app.services.embedding_service import EmbeddingService
from app.services.vector_store_service import VectorStoreService

embedding_service = EmbeddingService()


class RetrievalService:
    def retrieve(self, query: str, top_k: int = 3) -> RetrievalResponse:
        if not query or not query.strip():
            raise ValueError("Query cannot be empty")

        cleaned_query = query.strip()

        embedding_results = embedding_service.generate_embeddings([cleaned_query])

        if not embedding_results:
            raise ValueError("Failed to generate query embedding")

        query_vector = embedding_results[0]["vector"]

        search_results = VectorStoreService.search_similar(
            query_embedding=query_vector,
            top_k=top_k
        )

        results = [
            RetrievedChunk(
                text=item.text,
                metadata=item.metadata,
                distance=item.distance
            )
            for item in search_results
        ]

        return RetrievalResponse(
            query=cleaned_query,
            results=results
        )


retrieval_service = RetrievalService()