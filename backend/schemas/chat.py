from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class ChatQueryRequest(BaseModel):
    query: str
    target_role: Optional[str] = "AI Engineer"

class Citation(BaseModel):
    topic: str
    category: str

class ChatQueryResponse(BaseModel):
    answer: str
    citations: List[Citation]
    retrieved_context: str
    has_relevant_context: bool
