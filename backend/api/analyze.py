import os
import shutil
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from ai.resume_parser import ResumeParser
from ai.skill_gap_engine import SkillGapEngine

router = APIRouter(prefix="/api/analyze", tags=["Analysis"])

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

class JDAnalysisRequest(BaseModel):
    jd_text: str
    target_role: Optional[str] = "Software Engineer"

@router.post("/resume")
async def upload_resume(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    parser = ResumeParser()
    extracted_text = parser.parse_file(file_path)
    structured_data = parser.extract_structure(extracted_text)

    return {
        "status": "success",
        "filename": file.filename,
        "parsed_skills": structured_data["skills"],
        "parsed_projects": structured_data["projects"],
        "experience_years": structured_data["experience_years"],
        "has_certifications": structured_data["has_certifications"],
        "has_education": structured_data["has_education"],
        "raw_text_preview": extracted_text[:300] + "..."
    }

@router.post("/match")
def match_resume_to_jd(resume_skills: List[str], jd_text: str, experience_years: float = 1.0, has_certs: bool = False, has_edu: bool = True):
    gap_engine = SkillGapEngine()
    resume_data = {
        "skills": resume_skills,
        "experience_years": experience_years,
        "has_certifications": has_certs,
        "has_education": has_edu,
        "projects": [{"title": "Sample Project", "description": "", "skills": resume_skills[:3]}]
    }

    result = gap_engine.analyze_gap(resume_data, jd_text)
    return {"status": "success", "result": result}
