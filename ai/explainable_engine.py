import os
import json
from typing import Dict, List, Any
from backend.ai.skill_graph import skill_graph

class ExplainableRecommendationEngine:
    def __init__(self):
        evidence_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "datasets", "market_evidence.json")
        self.market_data = {}
        if os.path.exists(evidence_path):
            with open(evidence_path, "r", encoding="utf-8") as f:
                self.market_data = json.load(f)

    def generate_recommendations(
        self,
        resume_skills: List[str],
        jd_skills: List[str],
        missing_skills: List[str],
        target_role: str = "AI Engineer"
    ) -> List[Dict[str, Any]]:
        recommendations = []
        user_skills_lower = {s.lower() for s in resume_skills}

        for skill in missing_skills:
            is_req = skill in jd_skills
            related = skill_graph.get_related_skills(skill)
            user_related = [r for r in related if r.lower() in user_skills_lower]

            if is_req and user_related:
                priority = "HIGH PRIORITY"
                evidence_type = "Direct Evidence"
                why = f"Required in target job description for '{target_role}' and directly builds on your existing knowledge of {', '.join(user_related[:2])}."
            elif is_req:
                priority = "HIGH PRIORITY"
                evidence_type = "Direct Evidence"
                why = f"Strictly required by target job description for '{target_role}'."
            elif user_related:
                priority = "MEDIUM PRIORITY"
                evidence_type = "Inferred Relationship"
                why = f"Complements your existing skills ({', '.join(user_related[:2])}) and is commonly required in related high-growth tech roles."
            else:
                priority = "LOW PRIORITY"
                evidence_type = "AI-Generated Suggestion"
                why = f"Recommended to broaden career versatility for '{target_role}'."

            demonstration_projects = [
                f"Build a production-grade {skill} service",
                f"Integrate {skill} into full-stack AI application"
            ]

            recommendations.append({
                "skill": skill,
                "priority": priority,
                "is_required": is_req,
                "is_missing": True,
                "why_recommended": why,
                "related_user_skills": user_related if user_related else ["Python"],
                "target_role_benefit": f"Unlocks advanced capabilities in {target_role} workflows.",
                "demonstration_projects": demonstration_projects,
                "evidence_type": evidence_type
            })

        priority_order = {"HIGH PRIORITY": 1, "MEDIUM PRIORITY": 2, "LOW PRIORITY": 3}
        recommendations.sort(key=lambda x: priority_order.get(x["priority"], 4))
        return recommendations

    def generate_explainability_report(self, missing_skills: List[str]) -> List[Dict[str, Any]]:
        return self.generate_recommendations(["Python"], missing_skills, missing_skills)

ExplainableEngine = ExplainableRecommendationEngine
explainable_engine = ExplainableRecommendationEngine()
