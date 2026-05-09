from fastapi import APIRouter, HTTPException

from app.schemas.rag import RAGAnswerRequest, RAGAnswerResponse, RetrievedContext
from app.services.rag_service import RAGService

router = APIRouter(prefix="/rag", tags=["rag"])

rag_service = RAGService()


@router.post("/answer", response_model=RAGAnswerResponse)
def generate_rag_answer(request: RAGAnswerRequest):
    try:
        result = rag_service.answer_question(
            question=request.question,
            top_k=request.top_k,
        )

        return RAGAnswerResponse(
            question=result["question"],
            answer=result["answer"],
            contexts=[
                RetrievedContext(
                    text=item.text,
                    distance=item.distance,
                    metadata=item.metadata,
                )
                for item in result["contexts"]
            ],
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
