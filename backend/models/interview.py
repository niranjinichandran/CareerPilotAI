from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.core.database import Base

class InterviewSessionModel(Base):
    __tablename__ = "interview_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    target_role = Column(String(255), nullable=False)
    difficulty = Column(String(50), default="Intermediate")
    topics = Column(Text, default="[]")           # JSON list of selected topics
    weak_skills_json = Column(Text, default="[]") # JSON list of weak skills
    history_json = Column(Text, default="[]")     # JSON list of Q&A responses & feedback
    overall_score = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="interviews")
