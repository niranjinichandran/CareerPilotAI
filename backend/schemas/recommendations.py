from pydantic import BaseModel
from typing import List, Dict, Any

class ProjectRecommendationRequest(BaseModel):
    missing_skills: List[str]
    target_role: str = "AI Engineer"

class ProjectItem(BaseModel):
    title: str
    problem_statement: str
    overview: str
    features: List[str]
    tech_stack: List[str]
    skills_demonstrated: List[str]
    difficulty: str
    development_steps: List[str]
    recommendation_reason: str

class RoadmapRequest(BaseModel):
    missing_skills: List[str]
    target_role: str = "AI Engineer"

class PhaseItem(BaseModel):
    phase_number: int
    phase_title: str
    focus_skills: List[str]
    milestone: str
    action_items: List[str]

class RoadmapResponse(BaseModel):
    target_role: str
    phases: List[PhaseItem]
