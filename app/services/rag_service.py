from app.services.embedding_service import EmbeddingService
from app.services.vector_store_service import VectorStoreService
from app.services.llm_service import LLMService


class RAGService:
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.vector_store_service = VectorStoreService()
        self.llm_service = LLMService()

    def build_prompt(self, question: str, contexts: list) -> str:
        context_text = "\n\n".join(
            [
                f"Context {idx + 1}:\n{item.text}"
                for idx, item in enumerate(contexts)
            ]
        )

        prompt = (
            "Answer the question using only the context below.\n\n"
            f"Question:\n{question}\n\n"
            f"Context:\n{context_text}\n\n"
            "If the answer is not contained in the context, say that you could not find it."
        )
        return prompt

    def answer_question(self, question: str, top_k: int = 3) -> dict:
        query_embedding_result = self.embedding_service.generate_embeddings([question])

        if not query_embedding_result:
            raise ValueError("Failed to generate query embedding")

        query_embedding = query_embedding_result[0]["vector"]

        contexts = self.vector_store_service.search_similar(
            query_embedding=query_embedding,
            top_k=top_k,
        )

        if not contexts:
            return {
                "question": question,
                "answer": "I could not find the answer in the provided documents.",
                "contexts": [],
            }

        prompt = self.build_prompt(question, contexts)
        answer = self.llm_service.generate_answer(prompt)

        return {
            "question": question,
            "answer": answer,
            "contexts": contexts,
        }
