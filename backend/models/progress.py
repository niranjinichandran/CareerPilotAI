from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.core.database import Base

class LearningProgressModel(Base):
    __tablename__ = "learning_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    target_role = Column(String(255), default="AI Engineer")
    completed_skills_json = Column(Text, default="[]") # JSON list of learned skills
    current_phase = Column(Integer, default=1)
    roadmap_json = Column(Text, default="[]")           # JSON roadmap steps
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="progress")
