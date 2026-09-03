import os
import shutil
import json
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.core.config import settings
from backend.core.security import get_current_user_optional
from backend.models.user import User
from backend.models.resume import ResumeModel
from backend.schemas.resume import ResumeParsedData, ResumeUpdateRequest
from ai.resume_parser import ResumeParser

router = APIRouter(prefix="/api/resume", tags=["Resume Processing"])

@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_optional)
):
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(settings.UPLOAD_DIR, file.filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    parser = ResumeParser()
    try:
        extracted_text = parser.parse_file(file_path)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error parsing resume file: {str(e)}")

    structured = parser.extract_structure(extracted_text)

    # Save to database if user is logged in
    resume_id = None
    if current_user:
        new_resume = ResumeModel(
            user_id=current_user.id,
            filename=file.filename,
            raw_text=extracted_text,
            parsed_skills=json.dumps(structured["skills"]),
            parsed_projects=json.dumps(structured["projects"]),
            experience_years=structured["experience_years"],
            has_education=structured["has_education"],
            has_certifications=structured["has_certifications"]
        )
        db.add(new_resume)
        db.commit()
        db.refresh(new_resume)
        resume_id = new_resume.id

    return {
        "status": "success",
        "resume_id": resume_id,
        "filename": file.filename,
        "parsed_data": {
            "skills": structured["skills"],
            "projects": structured["projects"],
            "experience_years": structured["experience_years"],
            "has_education": structured["has_education"],
            "has_certifications": structured["has_certifications"],
            "raw_text_preview": extracted_text[:300] + "..."
        }
    }
