from fastapi import APIRouter
from app.schemas.embedding import EmbeddingRequest, EmbeddingResponse, EmbeddingItemResponse
from app.services.embedding_service import EmbeddingService

router = APIRouter(prefix="/embedding", tags=["embedding"])

service = EmbeddingService()


@router.post("/generate", response_model=EmbeddingResponse)
def generate_embedding(request: EmbeddingRequest):
    results = service.generate_embeddings(request.text)

    items = [
        EmbeddingItemResponse(
            index=item["index"],
            text=item["text"],
            vector=item["vector"],
            embedding_dimension=item["embedding_dimension"]
        )
        for item in results
    ]

    return EmbeddingResponse(
        model=service.model,
        total_embeddings=len(items),
        items=items
    )
