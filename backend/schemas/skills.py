from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class GapAnalysisRequest(BaseModel):
    resume_skills: List[str]
    jd_text: str
    experience_years: Optional[float] = 1.0
    has_certifications: Optional[bool] = False
    has_education: Optional[bool] = True

class ScoreBreakdown(BaseModel):
    required_skills_score: float
    preferred_skills_score: float
    project_alignment_score: float
    experience_alignment_score: float
    education_cert_score: float

class SkillRecommendation(BaseModel):
    skill: str
    priority: str  # HIGH, MEDIUM, LOW
    is_required: bool
    is_missing: bool
    why_recommended: str
    related_user_skills: List[str]
    target_role_benefit: str
    demonstration_projects: List[str]
    evidence_type: str  # Direct Evidence, Inferred Relationship, AI-Generated Suggestion

class GapAnalysisResponse(BaseModel):
    overall_match_percentage: float
    breakdown: ScoreBreakdown
    matched_skills: List[str]
    partially_matched_skills: List[str]
    missing_required_skills: List[str]
    missing_preferred_skills: List[str]
    related_skills: List[str]
    explainable_recommendations: List[SkillRecommendation]
    scoring_explanation: str
