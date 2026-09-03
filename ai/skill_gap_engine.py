import os
import re
import json
from typing import Dict, List, Any, Tuple

class SkillGapEngine:
    def __init__(self):
        skills_db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "datasets", "skills_db.json")
        self.skill_weights = {}
        if os.path.exists(skills_db_path):
            with open(skills_db_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.skill_weights = data.get("skill_weights", {})

    def extract_jd_skills(self, jd_text: str) -> List[str]:
        from ai.resume_parser import ResumeParser
        parser = ResumeParser()
        jd_skills = parser.extract_skills(jd_text)
        if not jd_skills:
            # Basic fallback keyword extraction if text is short
            words = set(re.findall(r'\b[A-Za-z0-9+#.-]{2,}\b', jd_text))
            jd_skills = [w for w in words if w.capitalize() in parser.all_known_skills]
        return list(dict.fromkeys(jd_skills))

    def analyze_gap(self, resume_data: Dict[str, Any], jd_text: str) -> Dict[str, Any]:
        resume_skills = resume_data.get("skills", [])
        jd_skills = self.extract_jd_skills(jd_text)

        # Standardize skill matching case-insensitively
        resume_skills_lower = {s.lower(): s for s in resume_skills}
        matched_skills = []
        missing_skills = []

        for skill in jd_skills:
            if skill.lower() in resume_skills_lower:
                matched_skills.append(skill)
            else:
                missing_skills.append(skill)

        # Calculate 5 Transparent Breakdown Component Scores:
        # 1. Skill Score (40% weight)
        if jd_skills:
            skill_score = min(100.0, (len(matched_skills) / len(jd_skills)) * 100.0)
        else:
            skill_score = 80.0

        # 2. Project Score (25% weight)
        projects = resume_data.get("projects", [])
        if len(projects) >= 3:
            project_score = 95.0
        elif len(projects) == 2:
            project_score = 85.0
        elif len(projects) == 1:
            project_score = 70.0
        else:
            project_score = 45.0

        # 3. Experience Score (15% weight)
        exp_years = resume_data.get("experience_years", 1.0)
        if exp_years >= 3.0:
            exp_score = 95.0
        elif exp_years >= 1.0:
            exp_score = 80.0
        elif exp_years >= 0.5:
            exp_score = 70.0
        else:
            exp_score = 55.0

        # 4. Certification Score (10% weight)
        cert_score = 90.0 if resume_data.get("has_certifications", False) else 60.0

        # 5. Education Score (10% weight)
        edu_score = 95.0 if resume_data.get("has_education", True) else 70.0

        # Weighted Total Score calculation
        overall_match = round(
            (skill_score * 0.40) +
            (project_score * 0.25) +
            (exp_score * 0.15) +
            (cert_score * 0.10) +
            (edu_score * 0.10),
            1
        )

        return {
            "overall_match_percentage": overall_match,
            "breakdown": {
                "skill_score": round(skill_score, 1),
                "project_score": round(project_score, 1),
                "experience_score": round(exp_score, 1),
                "certification_score": round(cert_score, 1),
                "education_score": round(edu_score, 1)
            },
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "total_jd_skills_count": len(jd_skills),
            "resume_skills_count": len(resume_skills)
        }
