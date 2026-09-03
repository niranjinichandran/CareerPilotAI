import os
import json
import numpy as np
from typing import Dict, List, Any
from sklearn.linear_model import LinearRegression

class SkillImpactPredictor:
    def __init__(self):
        skills_db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "datasets", "skills_db.json")
        self.skill_importance = {}
        if os.path.exists(skills_db_path):
            with open(skills_db_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.skill_importance = data.get("skill_weights", {})
        
        # Default importance weight fallback for unlisted skills
        self.default_weight = 0.75

    def get_skill_weight(self, skill: str) -> float:
        return self.skill_importance.get(skill, self.default_weight)

    def predict_impact(self, current_match_score: float, missing_skills: List[str], current_matched_skills: List[str]) -> Dict[str, Any]:
        if not missing_skills:
            return {
                "current_score": current_match_score,
                "projected_max_score": current_match_score,
                "skill_impacts": []
            }

        total_missing = len(missing_skills)
        remaining_gap = 100.0 - current_match_score
        
        # Calculate raw weights for missing skills
        weights = [self.get_skill_weight(s) for s in missing_skills]
        total_weight = sum(weights) if sum(weights) > 0 else 1.0

        skill_impacts = []
        cumulative_score = current_match_score

        for skill, weight in zip(missing_skills, weights):
            # Calculate point boost proportional to skill importance and remaining score potential (weighted by 40% skill score contribution)
            raw_gain = (weight / total_weight) * (remaining_gap * 0.75)
            point_gain = round(max(3.5, min(18.0, raw_gain)), 1)
            
            projected_score = min(98.5, round(cumulative_score + point_gain, 1))
            skill_impacts.append({
                "skill": skill,
                "point_gain": point_gain,
                "projected_score": projected_score,
                "importance_rating": "High ⭐⭐⭐⭐⭐" if weight > 0.85 else "Medium ⭐⭐⭐⭐"
            })
            cumulative_score = projected_score

        # Sort skill impacts by highest point gain (ROI)
        skill_impacts.sort(key=lambda x: x["point_gain"], reverse=True)

        return {
            "current_score": current_match_score,
            "projected_max_score": min(98.5, round(current_match_score + sum(s["point_gain"] for s in skill_impacts[:3]), 1)),
            "skill_impacts": skill_impacts
        }
