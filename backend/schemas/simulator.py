from pydantic import BaseModel
from typing import List, Dict, Any

class SimulationRequest(BaseModel):
    current_skills: List[str]
    selected_to_learn: List[str]
    current_match_score: float
    target_role: str = "AI Engineer"

class UnlockedRole(BaseModel):
    role_title: str
    fit_percentage: float
    status: str

class SimulationResponse(BaseModel):
    current_job_match: float
    estimated_job_match_after: float
    estimated_improvement: float
    newly_covered_requirements: List[str]
    remaining_skill_gaps: List[str]
    unlocked_roles: List[UnlockedRole]
    estimated_learning_time_weeks: int
    score_change_justification: str
    disclaimer: str = "Estimated scenario based on CareerPilot AI's scoring model."
