import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.core.security import get_current_user_optional
from backend.models.user import User
from backend.models.resume import JobDescriptionModel
from backend.schemas.job import JobAnalysisRequest, JobAnalysisResponse, NormalizedSkill
from ai.resume_parser import ResumeParser

router = APIRouter(prefix="/api/jobs", tags=["Job Description Analyzer"])

# Equivalent skills normalization dictionary
SKILL_NORMALIZATION_MAP = {
    "ml": "Machine Learning",
    "genai": "Generative AI",
    "llm": "Large Language Models",
    "llms": "Large Language Models",
    "js": "JavaScript",
    "ts": "TypeScript",
    "py": "Python",
    "nlp": "Natural Language Processing",
    "cv": "Computer Vision",
    "dl": "Deep Learning",
    "rag": "Retrieval-Augmented Generation",
    "db": "Database",
    "sql": "SQL",
    "k8s": "Kubernetes"
}

@router.post("/analyze", response_model=JobAnalysisResponse)
def analyze_job_description(
    request: JobAnalysisRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_optional)
):
    parser = ResumeParser()
    extracted_skills = parser.extract_skills(request.jd_text)

    normalized_skills = []
    for skill in extracted_skills:
        skill_lower = skill.lower()
        norm = SKILL_NORMALIZATION_MAP.get(skill_lower, skill)
        normalized_skills.append(NormalizedSkill(
            original=skill,
            normalized=norm,
            category="Technical Skill"
        ))

    # Basic responsibility extraction
    lines = [line.strip() for line in request.jd_text.split("\n") if len(line.strip()) > 15]
    responsibilities = [l for l in lines if any(w in l.lower() for w in ["build", "develop", "design", "manage", "lead", "implement", "responsible"])][:4]
    if not responsibilities:
        responsibilities = lines[:3]

    if current_user:
        jd_record = JobDescriptionModel(
            user_id=current_user.id,
            title=request.target_role or "Target Role",
            raw_text=request.jd_text,
            extracted_skills=json.dumps(extracted_skills),
            normalized_skills=json.dumps([n.normalized for n in normalized_skills]),
            responsibilities=json.dumps(responsibilities)
        )
        db.add(jd_record)
        db.commit()

    return JobAnalysisResponse(
        title=request.target_role or "AI Engineer",
        extracted_skills=extracted_skills,
        normalized_skills=normalized_skills,
        responsibilities=responsibilities,
        experience_req="1-3 years"
    )
