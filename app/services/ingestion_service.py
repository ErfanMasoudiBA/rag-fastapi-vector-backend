import re
from typing import List, Dict

class IngestionService:
    @staticmethod
    def clean_text(text: str) -> str:
        text = text.strip() # it erases before and after space's text.
        text = re.sub(r"\s+", " ", text) # every sequence of spaces turn into an space
        return text
    @staticmethod
    def chunk_text(text: str, chunk_size: int, chunk_overlap: int) -> List[Dict]: # it gets the cleaned text and turn it into smaller chunks.
        if chunk_overlap >= chunk_size:
            raise ValueError("chunk_overlap must be smaller than chunk_size")
        chunks = []
        start = 0
        index = 0
        text_length = len(text)
        
        while start < text_length:
            end = min(start + chunk_size, text_length)
            chunk = text[start:end]
            chunks.append({
                "index": index,
                "content": chunk,
                "start_char": start,
                "end_char": end,
            })
            
            if end == text_length:
                break
            start = end - chunk_overlap
            index +=1
            
        return chunks
    def process(self, text: str, chunk_size: int, chunk_overlap: int) -> List[Dict]:
        cleaned_text = self.clean_text(text)
        return self.chunk_text(cleaned_text, chunk_size, chunk_overlap)
