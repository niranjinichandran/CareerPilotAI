from fastapi import APIRouter
from backend.schemas.chat import ChatQueryRequest, ChatQueryResponse, Citation
from backend.ai.rag_pipeline import rag_pipeline

router = APIRouter(prefix="/api/chat", tags=["RAG Career Assistant"])

@router.post("/query", response_model=ChatQueryResponse)
def query_rag_assistant(request: ChatQueryRequest):
    res = rag_pipeline.answer_question(request.query)
    citations = [Citation(topic=c["topic"], category=c["category"]) for c in res["citations"]]

    return ChatQueryResponse(
        answer=res["answer"],
        citations=citations,
        retrieved_context=res["retrieved_context"],
        has_relevant_context=res["has_relevant_context"]
    )
