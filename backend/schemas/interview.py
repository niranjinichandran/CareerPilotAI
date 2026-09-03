from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class InterviewStartRequest(BaseModel):
    target_role: str = "AI Engineer"
    difficulty: str = "Intermediate"
    topics: List[str] = ["Python", "Machine Learning", "LLM", "RAG"]

class QuestionItem(BaseModel):
    id: str
    topic: str
    difficulty: str
    question: str
    key_concepts: List[str]

class AnswerSubmission(BaseModel):
    question_id: str
    user_answer: str

class AnswerEvaluation(BaseModel):
    score: float
    feedback: str
    concepts_covered: List[str]
    missing_concepts: List[str]
    strengths: List[str]
    weaknesses: List[str]
    sample_ideal_answer: str
    next_question: Optional[QuestionItem] = None

class InterviewHistoryResponse(BaseModel):
    session_id: int
    target_role: str
    overall_score: float
    history: List[Dict[str, Any]]
    repeated_weak_topics: List[str]
