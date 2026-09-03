from typing import Dict, List, Any

class OpportunitySimulator:
    def __init__(self):
        self.role_requirements = {
            "AI Engineer": ["Python", "RAG", "LangChain", "LLM", "Prompt Engineering", "FastAPI", "ChromaDB"],
            "GenAI Developer": ["Python", "Prompt Engineering", "LangChain", "OpenAI API", "ChromaDB", "RAG"],
            "LLM Application Engineer": ["Python", "LangChain", "RAG", "Vector Embeddings", "Transformers", "FastAPI"],
            "Full Stack AI Developer": ["Python", "FastAPI", "React", "Streamlit", "Docker", "SQL", "LLM"],
            "ML Backend Engineer": ["Python", "FastAPI", "Scikit-Learn", "Docker", "Redis", "Microservices"]
        }

    def simulate_career(
        self,
        current_skills: List[str],
        selected_skills_to_learn: List[str],
        current_match_score: float,
        jd_skills: List[str] = None
    ) -> Dict[str, Any]:
        if jd_skills is None:
            jd_skills = ["Python", "FastAPI", "LLM", "RAG", "Prompt Engineering", "ChromaDB", "Docker"]

        # Normalize skill sets
        current_skills_lower = {s.lower(): s for s in current_skills}
        selected_skills_lower = {s.lower(): s for s in selected_skills_to_learn}
        all_future_skills_lower = {**current_skills_lower, **selected_skills_lower}

        # Calculate newly covered requirements vs remaining skill gaps
        newly_covered = []
        remaining_gaps = []

        for jd_s in jd_skills:
            if jd_s.lower() in selected_skills_lower:
                newly_covered.append(jd_s)
            elif jd_s.lower() not in current_skills_lower:
                remaining_gaps.append(jd_s)

        # Formula calculation for score increase:
        # Each newly covered JD requirement adds transparent percentage weight
        score_gain_per_skill = 5.5 if len(jd_skills) == 0 else (40.0 / max(1, len(jd_skills))) * 1.2
        estimated_gain = round(len(newly_covered) * score_gain_per_skill, 1)
        estimated_after_score = min(98.0, round(current_match_score + estimated_gain, 1))
        realized_improvement = round(estimated_after_score - current_match_score, 1)

        # Role unlocking evaluation
        unlocked_roles = []
        for role, reqs in self.role_requirements.items():
            reqs_lower = [r.lower() for r in reqs]
            matched_count = sum(1 for r in reqs_lower if r in all_future_skills_lower)
            fit_pct = round((matched_count / len(reqs)) * 100.0, 1)
            status = "Highly Aligned 🚀" if fit_pct >= 80 else ("Aligned 📈" if fit_pct >= 60 else "Developing 🎯")
            unlocked_roles.append({
                "role_title": role,
                "fit_percentage": fit_pct,
                "status": status
            })

        # Project opportunities unlocked
        project_opportunities = [
            f"Build an end-to-end production platform integrating {', '.join(selected_skills_to_learn[:3])}",
            f"Deploy an enterprise RAG pipeline using {selected_skills_to_learn[0] if selected_skills_to_learn else 'FastAPI'}"
        ]

        learning_weeks = max(1, int(len(selected_skills_to_learn) * 1.5))
        justification = (
            f"Learning {', '.join(selected_skills_to_learn)} satisfies {len(newly_covered)} required job skills "
            f"which increases your skill coverage dimension by +{realized_improvement}%, raising your overall career readiness."
        )

        return {
            "current_job_match": current_match_score,
            "estimated_job_match_after": estimated_after_score,
            "estimated_improvement": realized_improvement,
            "newly_covered_requirements": newly_covered if newly_covered else selected_skills_to_learn,
            "remaining_skill_gaps": remaining_gaps,
            "project_opportunities": project_opportunities,
            "unlocked_roles": unlocked_roles,
            "estimated_learning_time_weeks": learning_weeks,
            "score_change_justification": justification,
            "disclaimer": "Estimated scenario based on CareerPilot AI's scoring model."
        }

opportunity_simulator = OpportunitySimulator()
