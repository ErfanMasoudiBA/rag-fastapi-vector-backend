from typing import Dict, Any
import uuid

from app.services.ingestion_service import IngestionService
from app.services.embedding_service import EmbeddingService
from app.services.vector_store_service import VectorStoreService
from app.schemas.vector_store import VectorItem


class DocumentIndexingService:
    def __init__(self):
        self.ingestion_service = IngestionService()
        self.embedding_service = EmbeddingService()
        self.vector_store_service = VectorStoreService()

    def index_document(
        self,
        text: str,
        metadata: Dict[str, Any] | None = None,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
    ) -> Dict[str, Any]:
        metadata = metadata or {}

        document_id = str(uuid.uuid4())

        # 1. Clean + Chunk using your existing IngestionService
        chunks = self.ingestion_service.process(
            text=text,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

        if not chunks:
            return {
                "document_id": document_id,
                "total_chunks": 0,
                "total_vectors": 0,
            }

        # chunks shape:
        # [
        #   {
        #       "index": 0,
        #       "content": "...",
        #       "start_char": 0,
        #       "end_char": 500
        #   }
        # ]

        chunk_texts = [chunk["content"] for chunk in chunks]

        # 2. Embed chunks using your existing EmbeddingService
        embedding_results = self.embedding_service.generate_embeddings(chunk_texts)

        # embedding_results shape:
        # [
        #   {
        #       "index": 0,
        #       "text": "...",
        #       "vector": [...],
        #       "embedding_dimension": 1536
        #   }
        # ]

        # 3. Convert embeddings into VectorItem objects
        vector_items = []

        for embedding_item in embedding_results:
            chunk_index = embedding_item["index"]
            related_chunk = chunks[chunk_index]

            enriched_metadata = {
                **metadata,
                "document_id": document_id,
                "chunk_index": related_chunk["index"],
                "start_char": related_chunk["start_char"],
                "end_char": related_chunk["end_char"],
                "embedding_dimension": embedding_item["embedding_dimension"],
            }

            vector_items.append(
                VectorItem(
                    text=embedding_item["text"],
                    embedding=embedding_item["vector"],
                    metadata=enriched_metadata,
                )
            )

        # 4. Store vectors in FAISS using your existing VectorStoreService
        total_vectors = self.vector_store_service.add_embeddings(vector_items)

        return {
            "document_id": document_id,
            "total_chunks": len(chunks),
            "total_vectors": total_vectors,
        }
