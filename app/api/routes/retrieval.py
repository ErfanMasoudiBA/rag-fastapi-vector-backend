from fastapi import APIRouter, HTTPException
from app.schemas.retrieval import RetrievalRequest, RetrievalResponse
from app.services.retrieval_service import retrieval_service

router = APIRouter(prefix="/retrieval", tags=["Retrieval"])

@router.post("/search", response_model=RetrievalResponse)
def retrieve_chunks(request: RetrievalRequest):
    try:
        return retrieval_service.retrieve(
            query=request.query,
            top_k=request.top_k
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Retrieval failed: {str(e)}")