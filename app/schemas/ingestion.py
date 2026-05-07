from pydantic import BaseModel, Field
from typing import List

class IngestionRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Raw input text to ingest")
    chunk_size: int = Field(500, gt=0, le=2000, description="Chunk size in characters")
    # gt means it must be bigger than zero
    # le means less that 2000
    chunk_overlap: int = Field(50, gt=0, le=500, description="Overlap between chunks")
    # it helps that some part pf the last chunk repeated at the next one

class ChunkResponse(BaseModel):
    index: int
    content: str
    start_char: int
    end_char: int

class IngestionResponse(BaseModel):
    total_chunks: int
    chunks: List[ChunkResponse]