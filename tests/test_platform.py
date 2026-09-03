import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.core.security import get_password_hash, verify_password
from ai.skill_gap_engine import SkillGapEngine
from ai.opportunity_simulator import opportunity_simulator

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_password_hashing():
    pw = "SuperSecret123!"
    hashed = get_password_hash(pw)
    assert verify_password(pw, hashed)
    assert not verify_password("WrongPassword", hashed)

def test_job_analysis():
    response = client.post("/api/jobs/analyze", json={
        "jd_text": "We need a Python developer with ML and GenAI skills.",
        "target_role": "AI Engineer"
    })
    assert response.status_code == 200
    data = response.json()
    assert "title" in data
    assert len(data["normalized_skills"]) > 0

def test_skill_gap_engine():
    engine = SkillGapEngine()
    resume_data = {
        "skills": ["Python", "FastAPI"],
        "experience_years": 1.5,
        "has_certifications": False,
        "has_education": True
    }
    jd_text = "Looking for Python, FastAPI, and RAG developer."
    result = engine.analyze_gap(resume_data, jd_text)
    assert "overall_match_percentage" in result
    assert "matched_skills" in result
    assert "missing_skills" in result

def test_skill_impact_simulator():
    res = opportunity_simulator.simulate_career(
        current_skills=["Python", "FastAPI"],
        selected_skills_to_learn=["RAG", "ChromaDB"],
        current_match_score=60.0
    )
    assert res["estimated_job_match_after"] > 60.0
    assert res["estimated_improvement"] > 0
    assert "disclaimer" in res
