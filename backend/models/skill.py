from datetime import datetime
from sqlalchemy import Column, Integer, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.core.database import Base

class AnalysisResultModel(Base):
    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=True)
    jd_id = Column(Integer, ForeignKey("job_descriptions.id"), nullable=True)
    match_score = Column(Float, nullable=False)
    breakdown_json = Column(Text, nullable=False)      # JSON string
    matched_skills_json = Column(Text, nullable=False) # JSON array string
    missing_skills_json = Column(Text, nullable=False) # JSON array string
    priority_ranking_json = Column(Text, default="[]") # JSON array string
    explanations_json = Column(Text, default="[]")     # JSON array string
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="analyses")
