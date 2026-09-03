from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class ResumeParsedData(BaseModel):
    filename: str
    skills: List[str]
    projects: List[Dict[str, Any]]
    experience_years: float
    has_education: bool
    has_certifications: bool
    raw_text: str

class ResumeUpdateRequest(BaseModel):
    skills: List[str]
    experience_years: float
    has_education: bool
    has_certifications: bool
