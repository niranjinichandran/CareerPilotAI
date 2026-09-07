import json
import streamlit as st
from backend.core.database import SessionLocal
from backend.models.skill import AnalysisResultModel
from ai.project_recommender import ProjectRecommender

def render_projects_page():
    user = st.session_state.get("user")
    user_id = user.get("id") if user else None
    user_name = user.get("full_name", "Candidate") if user else "Candidate"
    target_role = user.get("target_role", "Custom Career Role") if user else "Custom Career Role"

    st.markdown("""
        <div class="glass-card">
            <h2>🛠️ Project Recommendation Engine</h2>
            <p style="color:#94a3b8;">Instead of watching generic tutorials, build real-world hands-on portfolio projects engineered to maximize missing skill coverage in a single build.</p>
        </div>
    """, unsafe_allow_html=True)

    match_data = st.session_state.get("match_data")
    if not match_data and user_id:
        db = SessionLocal()
        try:
            record = db.query(AnalysisResultModel).filter(AnalysisResultModel.user_id == user_id).order_by(AnalysisResultModel.id.desc()).first()
            if record:
                match_data = {
                    "missing_skills": json.loads(record.missing_skills_json or "[]")
                }
        except Exception:
            match_data = None
        finally:
            db.close()

    missing_skills = match_data.get("missing_skills", []) if match_data else []

    if not match_data or not missing_skills:
        st.markdown(f"""
            <div style="background: rgba(99, 102, 241, 0.12); border: 1px solid #6366f1; border-radius: 14px; padding: 24px; text-align: center; margin: 20px 0;">
                <h3 style="color:#818cf8; margin-top:0;">📄 Resume Upload Required</h3>
                <p style="color:#cbd5e1; font-size:15px;">Welcome {user_name}! Upload your resume in <b>📄 Resume & JD Analysis</b> to receive tailored portfolio projects for target role: <b>{target_role}</b>.</p>
            </div>
        """, unsafe_allow_html=True)
        return

    recommender = ProjectRecommender()
    projects = recommender.recommend_projects(missing_skills)

    st.subheader(f"📌 Recommended Portfolio Projects for {target_role}")

    for proj in projects:
        with st.expander(f"🛠️ {proj['title']} — Difficulty: [{proj.get('difficulty', 'Intermediate')}]", expanded=True):
            st.markdown(f"**Why Recommended:** {proj.get('recommendation_reason', 'Maximizes coverage of missing skills.')}")
            st.markdown(f"**Problem Statement:** {proj.get('problem_statement', '')}")
            st.markdown(f"**Project Overview:** {proj.get('overview', '')}")
            st.markdown(f"**Tech Stack:** {', '.join(proj.get('tech_stack', []))}")
            
            st.markdown("**Skills Demonstrated:**")
            for sk in proj.get("skills_demonstrated", []):
                st.markdown(f"- `<span class='badge-matched'>{sk}</span>`", unsafe_allow_html=True)

            st.markdown("**Key Features & Deliverables:**")
            for f in proj.get("features", []):
                st.markdown(f"- ✅ {f}")

            st.markdown("**Step-by-Step Development Plan:**")
            for step in proj.get("development_steps", []):
                st.markdown(f"- {step}")
