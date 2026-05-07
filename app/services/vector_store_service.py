import json
import os # for working with files
from typing import List, Dict, Any

# the vector search library that we use
import faiss
import numpy as np

from app.schemas.vector_store import VectorItem, SearchResultItem

class VectorStoreService:
    def __init__(self):
        # filepaths that we keep on the disk
        # FAISS and metadata files
        self.index_path = "data/vector.index"
        self.metadata_path = "data/vector_metadata.json"
        
        os.makedirs("data", exist_ok=True)
        
        # for each vectors stored in FAISS, keep both text and its metadata related to it in a parallel list
        self.index = None
        self.metadata_store: List[Dict[str, Any]] = []
        
        # at fist when service is made, it must check that the file is already been there or not, to load or start empty
        self._load_or_initialize()
        
    # responsible for recovery and persistence
    def _load_or_initialize(self):
        if os.path.exists(self.index_path) and os.path.exists(self.metadata_path):
            # load the disk
            self.index = faiss.read_index(self.index_path)
            # read the metadata
            with open(self.metadata_path, "r", encoding="utf-8") as f:
                self.metadata_store = json.load(f)
        else:
            self.index = None
            self.metadata_store = []
        # the number of fiass items and metadata store items must be equal
    
    def _save(self):
        # store the index
        if self.index is not None:
            faiss.write_index(self.index, self.index_path)
        # store the metadata
        with open(self.metadata_path, "w", encoding="utf-8") as f:
            json.dump(self.metadata_store, f, ensure_ascii=False, indent=2)
    # insertion and indexing
    def add_embeddings(self, items: List[VectorItem]) -> int:
        # if the input empty, then do nothing
        if not items:
            return 0
        # just took the embeddings from vectoritem's list
        vectors = np.array([item.embedding for item in items], dtype="float32")
        # float32 is the standard of faiss
        
        if vectors.ndim != 2:
            raise ValueError("Embeddings must be a 2D array")
        # faiss expect that the data look like : (number_of_vectors, dimension)
        
        dimension = vectors.shape[1]
        
        if self.index is None:
            self.index = faiss.IndexFlatL2(dimension)
            # IndexFlatL2 is the simplest type of data in faiss
            # it is based on l2 distance
            # no compression , no approximate search, but it is brute-force and fast
        
        if self.index.d != dimension:
            raise ValueError(
                f"Embedding dimension mismatch. "
                f"Expected {self.index.d}, got {dimension}"
            )
        # add the vectors into the index so faiss have them for search
        self.index.add(vectors)
        
        # we have to know each vector belongs to which text
        # faiss will just keep the vectors
        for item in items:
            self.metadata_store.append(
                {
                    "text": item.text,
                    "metadata": item.metadata,
                }
            )
        
        self._save()
        return len(items)
    
    # it gets the query embedding and finds the closest chunks
    def search_similar(self, query_embedding: List[float], top_k: int = 3) -> List[SearchResultItem]:
        if self.index is None or self.index.ntotal == 0:
            return []
        
        query_vector = np.array([query_embedding], dtype="float32")
        
        # checking the length of the embedding query with the length of the index
        if query_vector.shape[1] != self.index.d:
            raise ValueError(
                f"Query embedding dimension mismatch. "
                f"Expected {self.index.d}, got {query_vector.shape[1]}"
            )
            
        # faiss return two things:
        distances, indices = self.index.search(query_vector, top_k)
        
        # make an empty list for the final results
        results: List[SearchResultItem] = []
        
        # we have just one query so it keep looking
        for distance, idx in zip(distances[0], indices[0]):
            # sometime faiss gives -1 for empty spaces, so we pass by them
            if idx == -1:
                continue
            stored_item = self.metadata_store[idx]
            
            results.append(
                SearchResultItem(
                    text=stored_item["text"],
                    distance=float(distance),
                    metadata=stored_item["metadata"],
                )
            )
        return results

