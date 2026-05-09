from fastapi import APIRouter, HTTPException

from app.schemas.document import DocumentIndexRequest, DocumentIndexResponse
from app.services.document_indexing_service import DocumentIndexingService

router = APIRouter(prefix="/documents", tags=["documents"])

document_indexing_service = DocumentIndexingService()


@router.post("/index", response_model=DocumentIndexResponse)
def index_document(request: DocumentIndexRequest):
    try:
        result = document_indexing_service.index_document(
            text=request.text,
            metadata=request.metadata,
            chunk_size=request.chunk_size,
            chunk_overlap=request.chunk_overlap,
        )

        return DocumentIndexResponse(
            message="Document indexed successfully",
            total_chunks=result["total_chunks"],
            total_vectors=result["total_vectors"],
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
