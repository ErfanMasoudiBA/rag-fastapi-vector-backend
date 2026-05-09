from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class DocumentIndexRequest(BaseModel):
    text: str = Field(..., min_length=1)
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)

    chunk_size: int = Field(default=500, gt=0)
    chunk_overlap: int = Field(default=50, ge=0)


class DocumentIndexResponse(BaseModel):
    message: str
    total_chunks: int
    total_vectors: int
