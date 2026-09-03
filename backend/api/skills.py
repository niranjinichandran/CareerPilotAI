import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.core.security import get_current_user_optional
from backend.models.user import User
from backend.models.skill import AnalysisResultModel
from backend.schemas.skills import GapAnalysisRequest, GapAnalysisResponse, ScoreBreakdown, SkillRecommendation
from ai.skill_gap_engine import SkillGapEngine
from ai.explainable_engine import explainable_engine
from ai.skill_graph import skill_graph

router = APIRouter(prefix="/api/skills", tags=["Skill Gap & Explainable AI"])

@router.post("/gap-analysis", response_model=GapAnalysisResponse)
def analyze_skill_gap(
    request: GapAnalysisRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_optional)
):
    engine = SkillGapEngine()
    resume_data = {
        "skills": request.resume_skills,
        "experience_years": request.experience_years or 1.0,
        "has_certifications": request.has_certifications or False,
        "has_education": request.has_education or True,
        "projects": [{"title": "Sample Project", "description": "", "skills": request.resume_skills[:3]}]
    }

    res = engine.analyze_gap(resume_data, request.jd_text)
    jd_skills = engine.extract_jd_skills(request.jd_text)

    # Classify skills into detailed breakdown categories
    resume_skills_lower = {s.lower() for s in request.resume_skills}
    matched = res["matched_skills"]
    missing = res["missing_skills"]

    # Identify related skills from skill graph
    related_skills = []
    for s in request.resume_skills:
        related_skills.extend(skill_graph.get_related_skills(s))
    related_skills = list(dict.fromkeys([r for r in related_skills if r.lower() not in resume_skills_lower]))[:5]

    # Generate explainable AI recommendations
    explainable_recs_raw = explainable_engine.generate_recommendations(
        resume_skills=request.resume_skills,
        jd_skills=jd_skills,
        missing_skills=missing,
        target_role="AI Engineer"
    )

    explainable_recs = [
        SkillRecommendation(
            skill=r["skill"],
            priority=r["priority"],
            is_required=r["is_required"],
            is_missing=r["is_missing"],
            why_recommended=r["why_recommended"],
            related_user_skills=r["related_user_skills"],
            target_role_benefit=r["target_role_benefit"],
            demonstration_projects=r["demonstration_projects"],
            evidence_type=r["evidence_type"]
        ) for r in explainable_recs_raw
    ]

    breakdown = res["breakdown"]
    score_breakdown = ScoreBreakdown(
        required_skills_score=breakdown["skill_score"],
        preferred_skills_score=breakdown["skill_score"],
        project_alignment_score=breakdown["project_score"],
        experience_alignment_score=breakdown["experience_score"],
        education_cert_score=breakdown["education_score"]
    )

    scoring_explanation = (
        f"Match Score ({res['overall_match_percentage']}%) calculated transparently using 5 weighted dimensions: "
        f"Required Skills (40%: {breakdown['skill_score']}%), Project Alignment (25%: {breakdown['project_score']}%), "
        f"Experience Alignment (15%: {breakdown['experience_score']}%), Certifications (10%: {breakdown['certification_score']}%), "
        f"Education (10%: {breakdown['education_score']}%)."
    )

    if current_user:
        analysis_record = AnalysisResultModel(
            user_id=current_user.id,
            match_score=res["overall_match_percentage"],
            breakdown_json=json.dumps(breakdown),
            matched_skills_json=json.dumps(matched),
            missing_skills_json=json.dumps(missing),
            priority_ranking_json=json.dumps([r["skill"] for r in explainable_recs_raw]),
            explanations_json=json.dumps(explainable_recs_raw)
        )
        db.add(analysis_record)
        db.commit()

    return GapAnalysisResponse(
        overall_match_percentage=res["overall_match_percentage"],
        breakdown=score_breakdown,
        matched_skills=matched,
        partially_matched_skills=[],
        missing_required_skills=missing,
        missing_preferred_skills=[],
        related_skills=related_skills,
        explainable_recommendations=explainable_recs,
        scoring_explanation=scoring_explanation
    )
