import json
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.core.security import get_current_user_optional
from backend.models.user import User
from backend.models.skill import AnalysisResultModel
from backend.models.interview import InterviewSessionModel

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard Summary"])

@router.get("/summary")
def get_dashboard_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_optional)
):
    if current_user:
        latest_analysis = (
            db.query(AnalysisResultModel)
            .filter(AnalysisResultModel.user_id == current_user.id)
            .order_by(AnalysisResultModel.id.desc())
            .first()
        )
        latest_interview = (
            db.query(InterviewSessionModel)
            .filter(InterviewSessionModel.user_id == current_user.id)
            .order_by(InterviewSessionModel.id.desc())
            .first()
        )
        
        match_score = latest_analysis.match_score if latest_analysis else 72.0
        matched_skills = json.loads(latest_analysis.matched_skills_json) if latest_analysis else ["Python", "FastAPI", "SQL", "Git", "Docker"]
        missing_skills = json.loads(latest_analysis.missing_skills_json) if latest_analysis else ["RAG", "LangChain", "Prompt Engineering", "ChromaDB"]
        interview_score = latest_interview.overall_score if latest_interview else 78.0
        user_name = current_user.full_name
        target_role = current_user.target_role or "AI Engineer"
    else:
        match_score = 72.0
        matched_skills = ["Python", "FastAPI", "SQL", "Git", "Docker"]
        missing_skills = ["RAG", "LangChain", "Prompt Engineering", "ChromaDB"]
        interview_score = 78.0
        user_name = "Guest Candidate"
        target_role = "AI Engineer"

    high_priority = missing_skills[:2] if missing_skills else ["RAG", "Prompt Engineering"]

    return {
        "status": "success",
        "user_name": user_name,
        "target_role": target_role,
        "resume_match_score": match_score,
        "skills_matched_count": len(matched_skills),
        "skills_missing_count": len(missing_skills),
        "learning_progress_pct": 65.0,
        "interview_score": interview_score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "high_priority_skills": high_priority,
        "next_recommended_action": f"Master '{high_priority[0]}' by completing the recommended AI Knowledge Assistant project."
    }
