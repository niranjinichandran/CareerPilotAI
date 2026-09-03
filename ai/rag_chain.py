from backend.ai.rag_pipeline import rag_pipeline

class RAGCareerAssistant:
    def answer_query(self, query: str):
        return rag_pipeline.answer_question(query)

__all__ = ["RAGCareerAssistant", "rag_pipeline"]
