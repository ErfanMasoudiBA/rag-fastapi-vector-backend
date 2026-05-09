from fastapi import APIRouter
from app.schemas.retrieval import RetrievalRequest, RetrievalResponse
from app.services.retrieval_service import RetrievalService

router = APIRouter(prefix="/retrieval", tags=["Retrieval"])

retrieval_service = RetrievalService()


@router.post("/search", response_model=RetrievalResponse)
def retrieve(request: RetrievalRequest):
    return retrieval_service.retrieve(
        query=request.query,
        top_k=request.top_k
    )
