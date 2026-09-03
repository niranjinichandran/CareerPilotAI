from fastapi import APIRouter
from typing import List
from backend.schemas.recommendations import (
    ProjectRecommendationRequest, ProjectItem, RoadmapRequest, RoadmapResponse, PhaseItem
)
from ai.project_recommender import project_recommender
from ai.predictive_planner import predictive_planner

router = APIRouter(prefix="/api/recommendations", tags=["Recommendations & Roadmap"])

@router.post("/projects", response_model=List[ProjectItem])
def get_project_recommendations(request: ProjectRecommendationRequest):
    projects_raw = project_recommender.recommend_projects(request.missing_skills)
    results = []
    for p in projects_raw:
        results.append(ProjectItem(
            title=p["title"],
            problem_statement=p["problem_statement"],
            overview=p["overview"],
            features=p["features"],
            tech_stack=p["tech_stack"],
            skills_demonstrated=p["skills_demonstrated"],
            difficulty=p["difficulty"],
            development_steps=p["development_steps"],
            recommendation_reason=p["why_recommended"]
        ))
    return results

@router.post("/roadmap", response_model=RoadmapResponse)
def get_learning_roadmap(request: RoadmapRequest):
    projects_raw = project_recommender.recommend_projects(request.missing_skills)
    top_proj = projects_raw[0] if projects_raw else None
    
    roadmap_raw = predictive_planner.generate_roadmap(
        target_role=request.target_role,
        missing_skills=request.missing_skills,
        recommended_project=top_proj
    )

    phases = [
        PhaseItem(
            phase_number=p["phase_number"],
            phase_title=p["phase_title"],
            focus_skills=p["focus_skills"],
            milestone=p["milestone"],
            action_items=p["action_items"]
        ) for p in roadmap_raw["phases"]
    ]

    return RoadmapResponse(
        target_role=request.target_role,
        phases=phases
    )
