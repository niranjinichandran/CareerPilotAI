from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship
from backend.core.database import Base

class ResumeModel(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    filename = Column(String(255), nullable=False)
    raw_text = Column(Text, nullable=False)
    parsed_skills = Column(Text, default="[]")       # JSON array string
    parsed_projects = Column(Text, default="[]")     # JSON array string
    experience_years = Column(Float, default=1.0)
    has_education = Column(Boolean, default=True)
    has_certifications = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="resumes")

class JobDescriptionModel(Base):
    __tablename__ = "job_descriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    company = Column(String(255), default="Target Organization")
    raw_text = Column(Text, nullable=False)
    extracted_skills = Column(Text, default="[]")   # JSON array string
    normalized_skills = Column(Text, default="[]")  # JSON array string
    responsibilities = Column(Text, default="[]")   # JSON array string
    experience_req = Column(String(255), default="1-3 years")
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="job_descriptions")
