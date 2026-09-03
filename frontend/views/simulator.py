import streamlit as st
import requests

API_BASE_URL = "http://127.0.0.1:8000/api"

def render_simulator_page():
    st.markdown("""
        <div class="glass-card">
            <h2>⚡ Skill Impact & Career Opportunity Simulator</h2>
            <p style="color:#94a3b8;">Select skills you plan to learn. The simulator recalculates your candidate match score, shows newly covered requirements, and highlights unlocked target job roles.</p>
        </div>
    """, unsafe_allow_html=True)

    match_data = st.session_state.get("match_data")
    current_score = match_data.get("overall_match_percentage", 68.5) if match_data else 68.5
    missing_skills = match_data.get("missing_skills", ["RAG", "LangChain", "Prompt Engineering", "ChromaDB"]) if match_data else ["RAG", "LangChain", "Prompt Engineering", "ChromaDB"]
    current_skills = st.session_state.get("resume_skills", ["Python", "FastAPI", "SQL", "Git", "Docker"])

    st.subheader("1. Select Skills to Simulate Learning")
    selected_to_learn = st.multiselect(
        "Choose missing skills you plan to acquire:",
        options=missing_skills,
        default=missing_skills[:2] if len(missing_skills) >= 2 else missing_skills
    )

    if st.button("🔮 Run Skill Impact Simulation", type="primary"):
        if not selected_to_learn:
            st.warning("Please select at least one skill to simulate.")
        else:
            with st.spinner("Calculating scenario score impact..."):
                try:
                    res = requests.post(
                        f"{API_BASE_URL}/simulator/run",
                        json={
                            "current_skills": current_skills,
                            "selected_to_learn": selected_to_learn,
                            "current_match_score": current_score,
                            "target_role": "AI Engineer"
                        },
                        timeout=5
                    )
                    sim = res.json()
                except Exception:
                    sim = {
                        "current_job_match": current_score,
                        "estimated_job_match_after": min(96.0, round(current_score + len(selected_to_learn) * 7.0, 1)),
                        "estimated_improvement": round(len(selected_to_learn) * 7.0, 1),
                        "newly_covered_requirements": selected_to_learn,
                        "remaining_skill_gaps": [s for s in missing_skills if s not in selected_to_learn],
                        "unlocked_roles": [
                            {"role_title": "AI Engineer", "fit_percentage": 88.0, "status": "Highly Aligned 🚀"},
                            {"role_title": "GenAI Developer", "fit_percentage": 82.0, "status": "Aligned 📈"}
                        ],
                        "estimated_learning_time_weeks": max(2, len(selected_to_learn) * 2),
                        "score_change_justification": f"Learning {', '.join(selected_to_learn)} directly covers key job requirements, increasing your skill score.",
                        "disclaimer": "Estimated scenario based on CareerPilot AI's scoring model."
                    }

                st.markdown("---")
                st.markdown(f"> ℹ️ **Disclaimer:** *{sim['disclaimer']}*")

                m1, m2, m3 = st.columns(3)
                m1.metric("Current Job Match", f"{sim['current_job_match']}%")
                m2.metric("Estimated Match After Learning", f"{sim['estimated_job_match_after']}%", f"+{sim['estimated_improvement']}% Gain")
                m3.metric("Est. Learning Duration", f"~{sim['estimated_learning_time_weeks']} Weeks")

                st.info(f"💡 **Score Change Rationale:** {sim['score_change_justification']}")

                col_cov1, col_cov2 = st.columns(2)
                with col_cov1:
                    st.subheader("✅ Newly Covered Requirements")
                    for s in sim["newly_covered_requirements"]:
                        st.markdown(f"- `<span class='badge-matched'>{s}</span>`", unsafe_allow_html=True)

                with col_cov2:
                    st.subheader("⚠️ Remaining Skill Gaps")
                    for s in sim["remaining_skill_gaps"]:
                        st.markdown(f"- `<span class='badge-missing'>{s}</span>`", unsafe_allow_html=True)

                st.markdown("---")
                st.subheader("💼 Unlocked Eligible Roles")
                for r in sim["unlocked_roles"]:
                    st.markdown(f"- **{r['role_title']}** (`{r['fit_percentage']}% Fit`) — {r['status']}")
