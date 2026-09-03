from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from backend.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    target_role = Column(String(255), default="AI Engineer")
    created_at = Column(DateTime, default=datetime.utcnow)

    resumes = relationship("ResumeModel", back_populates="user", cascade="all, delete-orphan")
    job_descriptions = relationship("JobDescriptionModel", back_populates="user", cascade="all, delete-orphan")
    analyses = relationship("AnalysisResultModel", back_populates="user", cascade="all, delete-orphan")
    interviews = relationship("InterviewSessionModel", back_populates="user", cascade="all, delete-orphan")
    progress = relationship("LearningProgressModel", back_populates="user", cascade="all, delete-orphan")
