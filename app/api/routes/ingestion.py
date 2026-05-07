from fastapi import APIRouter
from app.schemas.ingestion import IngestionRequest, IngestionResponse
from app.services.ingestion_service import IngestionService

router = APIRouter(prefix="/ingestion", tags=["ingestion"])
service = IngestionService()

@router.post("/chunk", response_model=IngestionResponse)
def chunk_text(request: IngestionRequest):
    chunks = service.process(
        text=request.text,
        chunk_size=request.chunk_size,
        chunk_overlap=request.chunk_overlap
    )
    return IngestionResponse(
        total_chunks=len(chunks),
        chunks=chunks,
    )