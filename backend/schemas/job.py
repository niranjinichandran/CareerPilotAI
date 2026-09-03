from pydantic import BaseModel
from typing import List, Optional, Dict

class JobAnalysisRequest(BaseModel):
    jd_text: str
    target_role: Optional[str] = "AI Engineer"

class NormalizedSkill(BaseModel):
    original: str
    normalized: str
    category: str

class JobAnalysisResponse(BaseModel):
    title: str
    extracted_skills: List[str]
    normalized_skills: List[NormalizedSkill]
    responsibilities: List[str]
    experience_req: str
