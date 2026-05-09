from typing import List, Dict, Any
from pydantic import BaseModel, Field


class RAGAnswerRequest(BaseModel):
    question: str = Field(..., min_length=1)
    top_k: int = Field(default=3, gt=0, le=10)


class RetrievedContext(BaseModel):
    text: str
    distance: float
    metadata: Dict[str, Any]


class RAGAnswerResponse(BaseModel):
    question: str
    answer: str
    contexts: List[RetrievedContext]
