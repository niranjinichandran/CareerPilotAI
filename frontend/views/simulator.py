import json
import streamlit as st
from backend.core.database import SessionLocal
from backend.models.skill import AnalysisResultModel
from ai.opportunity_simulator import OpportunitySimulator

def render_simulator_page():
    user = st.session_state.get("user")
    user_id = user.get("id") if user else None
    user_name = user.get("full_name", "Candidate") if user else "Candidate"
    target_role = user.get("target_role", "Custom Career Role") if user else "Custom Career Role"

    st.markdown("""
        <div class="glass-card">
            <h2>⚡ Skill Impact & Career Opportunity Simulator</h2>
            <p style="color:#94a3b8;">Select missing skills you plan to learn. The simulator recalculates your candidate match score, shows newly covered requirements, and highlights unlocked target job roles.</p>
        </div>
    """, unsafe_allow_html=True)

    match_data = st.session_state.get("match_data")
    if not match_data and user_id:
        db = SessionLocal()
        try:
            record = db.query(AnalysisResultModel).filter(AnalysisResultModel.user_id == user_id).order_by(AnalysisResultModel.id.desc()).first()
            if record:
                match_data = {
                    "overall_match_percentage": round(record.match_score, 1),
                    "matched_skills": json.loads(record.matched_skills_json or "[]"),
                    "missing_skills": json.loads(record.missing_skills_json or "[]")
                }
                st.session_state["match_data"] = match_data
        except Exception:
            match_data = None
        finally:
            db.close()

    if not match_data:
        st.markdown(f"""
            <div style="background: rgba(99, 102, 241, 0.12); border: 1px solid #6366f1; border-radius: 14px; padding: 24px; text-align: center; margin: 20px 0;">
                <h3 style="color:#818cf8; margin-top:0;">📄 Resume Upload Required</h3>
                <p style="color:#cbd5e1; font-size:15px;">Welcome {user_name}! Please upload your resume in <b>📄 Resume & JD Analysis</b> to enable the Skill Impact Simulator.</p>
            </div>
        """, unsafe_allow_html=True)
        return

    current_score = match_data.get("overall_match_percentage", 65.0)
    missing_skills = match_data.get("missing_skills", [])
    current_skills = st.session_state.get("resume_skills") or match_data.get("matched_skills", [])

    if not missing_skills:
        st.success("🎉 You have matched all required skills! No missing skills to simulate.")
        return

    st.subheader("1. Select Skills to Simulate Learning")
    selected_to_learn = st.multiselect(
        "Choose missing skills you plan to acquire:",
        options=missing_skills,
        default=missing_skills[:2] if len(missing_skills) >= 2 else missing_skills
    )

    if st.button("🔮 Run Skill Impact Simulation", type="primary", use_container_width=True):
        if not selected_to_learn:
            st.warning("Please select at least one skill to simulate.")
        else:
            with st.spinner("Calculating scenario score impact..."):
                simulator = OpportunitySimulator()
                sim = simulator.simulate_skill_acquisition(
                    current_skills=current_skills,
                    selected_to_learn=selected_to_learn,
                    current_match_score=current_score,
                    target_role=target_role
                )

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
                st.subheader(f"💼 Unlocked Eligible Roles for {target_role}")
                for r in sim["unlocked_roles"]:
                    st.markdown(f"- **{r['role_title']}** (`{r['fit_percentage']}% Fit`) — {r['status']}")
