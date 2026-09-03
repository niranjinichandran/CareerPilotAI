import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.core.security import get_current_user_optional
from backend.models.user import User
from backend.models.interview import InterviewSessionModel
from backend.schemas.interview import (
    InterviewStartRequest, QuestionItem, AnswerSubmission, AnswerEvaluation, InterviewHistoryResponse
)
from ai.adaptive_interview import adaptive_interview_engine

router = APIRouter(prefix="/api/interview", tags=["Adaptive AI Mock Interview"])

@router.post("/start")
def start_interview_session(
    request: InterviewStartRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_optional)
):
    session_id = None
    if current_user:
        session = InterviewSessionModel(
            user_id=current_user.id,
            target_role=request.target_role,
            difficulty=request.difficulty,
            topics=json.dumps(request.topics),
            weak_skills_json=json.dumps(request.topics),
            history_json="[]",
            overall_score=0.0
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        session_id = session.id

    first_question = adaptive_interview_engine.get_next_question(
        weak_topics=request.topics,
        history=[]
    )

    return {
        "status": "success",
        "session_id": session_id,
        "target_role": request.target_role,
        "question": QuestionItem(
            id=first_question["id"],
            topic=first_question["topic"],
            difficulty=first_question["difficulty"],
            question=first_question["question"],
            key_concepts=first_question["key_concepts"]
        )
    }

@router.post("/answer", response_model=AnswerEvaluation)
def evaluate_answer(
    submission: AnswerSubmission,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_optional)
):
    # Lookup question
    all_qs = []
    for topic, qlist in adaptive_interview_engine.question_bank.items():
        all_qs.extend(qlist)
    
    q_obj = next((q for q in all_qs if q["id"] == submission.question_id), None)
    if not q_obj:
        q_obj = {
            "id": submission.question_id,
            "topic": "General Technical",
            "difficulty": "Intermediate",
            "question": "Explain system trade-offs in your architecture.",
            "key_concepts": ["architecture", "scaling", "trade-offs"],
            "sample_ideal_answer": "Detail problem statement, architecture decisions, and scaling results."
        }

    eval_res = adaptive_interview_engine.evaluate_answer(q_obj, submission.user_answer)
    next_q = adaptive_interview_engine.get_next_question(
        weak_topics=eval_res["missing_concepts"],
        history=[{"question_id": submission.question_id, "score": eval_res["score"], "topic": q_obj["topic"]}]
    )

    next_q_item = QuestionItem(
        id=next_q["id"],
        topic=next_q["topic"],
        difficulty=next_q["difficulty"],
        question=next_q["question"],
        key_concepts=next_q["key_concepts"]
    )

    return AnswerEvaluation(
        score=eval_res["score"],
        feedback=eval_res["feedback"],
        concepts_covered=eval_res["concepts_covered"],
        missing_concepts=eval_res["missing_concepts"],
        strengths=eval_res["strengths"],
        weaknesses=eval_res["weaknesses"],
        sample_ideal_answer=eval_res["sample_ideal_answer"],
        next_question=next_q_item
    )

@router.get("/history")
def get_interview_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_optional)
):
    if not current_user:
        return {"sessions": []}

    sessions = db.query(InterviewSessionModel).filter(InterviewSessionModel.user_id == current_user.id).all()
    history_data = []
    for s in sessions:
        history_data.append({
            "session_id": s.id,
            "target_role": s.target_role,
            "overall_score": s.overall_score,
            "created_at": s.created_at.isoformat()
        })
    return {"sessions": history_data}
