from fastapi import APIRouter
from backend.schemas.simulator import SimulationRequest, SimulationResponse, UnlockedRole
from ai.opportunity_simulator import opportunity_simulator

router = APIRouter(prefix="/api/simulator", tags=["Skill Impact Simulator"])

@router.post("/run", response_model=SimulationResponse)
def run_simulation(request: SimulationRequest):
    res = opportunity_simulator.simulate_career(
        current_skills=request.current_skills,
        selected_skills_to_learn=request.selected_to_learn,
        current_match_score=request.current_match_score
    )

    unlocked_roles = [
        UnlockedRole(
            role_title=r["role_title"],
            fit_percentage=r["fit_percentage"],
            status=r["status"]
        ) for r in res["unlocked_roles"]
    ]

    return SimulationResponse(
        current_job_match=res["current_job_match"],
        estimated_job_match_after=res["estimated_job_match_after"],
        estimated_improvement=res["estimated_improvement"],
        newly_covered_requirements=res["newly_covered_requirements"],
        remaining_skill_gaps=res["remaining_skill_gaps"],
        unlocked_roles=unlocked_roles,
        estimated_learning_time_weeks=res["estimated_learning_time_weeks"],
        score_change_justification=res["score_change_justification"],
        disclaimer=res["disclaimer"]
    )
