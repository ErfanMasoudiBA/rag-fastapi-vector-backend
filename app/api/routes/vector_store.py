from fastapi import APIRouter, HTTPException

from app.schemas.vector_store import (
    StoreVectorsRequest,
    StoreVectorsResponse,
    SearchVectorsRequest,
    SearchVectorsResponse,
)

from app.services.vector_store_service import VectorStoreService

router = APIRouter(prefix="/vector", tags=["Vector Store"])
vector_service = VectorStoreService()

@router.post("/add", response_model=StoreVectorsResponse)
def add_vectors(payload: StoreVectorsRequest):
    try:
        total = vector_service.add_embeddings(payload.items)
        return StoreVectorsResponse(
            message="Vectors stored successfully",
            total_stored=total,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/search", response_model=SearchVectorsResponse)
def search_vectors(payload: SearchVectorsRequest):
    try:
        results = vector_service.search_similar(
            query_embedding=payload.query_embedding,
            top_k=payload.top_k,
        )
        return SearchVectorsResponse(
            query_dimension=len(payload.query_embedding),
            top_k=payload.top_k,
            results=results,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))