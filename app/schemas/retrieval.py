from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class RetrievalRequest(BaseModel):
    query: str = Field(..., min_length=1, description="User query text")
    top_k: int = Field(3, ge=1, le=20, description="Number of similar chunks to retrieve")
    
class RetrievedChunk(BaseModel):
    text: str
    metadata: Optional[Dict[str, Any]] = None
    distance: float
    
class RetrievalResponse(BaseModel):
    query: str
    results: List[RetrievedChunk]