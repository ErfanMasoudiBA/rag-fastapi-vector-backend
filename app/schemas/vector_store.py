from pydantic import BaseModel, Field
from typing import List, Dict, Any

# each items that it goes to our store must have this structure
class VectorItem(BaseModel):
    # min_length =1 means that the text couldn't be empty
    text: str = Field(..., min_length=1, description="Original chunk text")
    embedding: List[float] = Field(..., min_length=1, description="Embedding vector")
    # metadata is for additional data like doc_id, chunk_index, source, filename, page_number and etc.
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Optional metadata")
    
# when user called /add/vector , the body must be in this structure
class StoreVectorsRequest(BaseModel):
    # items is a list of the VectorItem 's objects -> text, embedding, metadata
    items: List[VectorItem] = Field(..., min_length=1, description="List of vectors to store")

# this is a report of an ingestion operation
class StoreVectorsResponse(BaseModel):
    message: str
    total_stored: int

# the system doesn't get the text, but actually it gets the embedding of it
class SearchVectorsRequest(BaseModel):
    query_embedding: List[float] = Field(..., min_length=1, description="Query embedding vector")
    # default top_k is 3, min is 1 and max is 20
    top_k: int = Field(3, ge=1, le=20, description= "Number of similar results to retrieve")
    
# this class said that, i think this chunk might be related to your query
class SearchResultItem(BaseModel):
    text: str
    # distance, the more closer it gets, it is better!
    distance : float
    metadata: Dict[str, Any] = Field(default_factory=dict)

# it has the complete output of the retrieval operation
class SearchVectorsResponse(BaseModel):
    # when we embedding a text, it becomes into some numbers, we call the number of these numbers: dimension
    # The number of components or length of the embedding vector associated with the query
    query_dimension: int
    top_k: int
    results: List[SearchResultItem]
    
