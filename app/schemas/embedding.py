from pydantic import BaseModel, Field
from typing import List

class EmbeddingRequest(BaseModel):
    # when a client send a request, it must have this structure
    # ... means it is mandatory to be filled
    text: List[str] = Field(..., min_length=1, description="List of text chunks to embed")

# this is the structure of each item in output
class EmbeddingItemResponse(BaseModel):
    # the number of each chunk in input list
    index: int
    text: str
    EmbeddingResponse: int

# this is the schema of the last endpoint
class EmbeddingResponse(BaseModel):
    model: str
    total_embeddings: int
    items: List[EmbeddingItemResponse]