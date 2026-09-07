import json
import streamlit as st
from backend.core.database import SessionLocal
from backend.models.skill import AnalysisResultModel
from ai.predictive_planner import PredictivePlanner

def render_roadmap_page():
    user = st.session_state.get("user")
    user_id = user.get("id") if user else None
    user_name = user.get("full_name", "Candidate") if user else "Candidate"
    target_role = user.get("target_role", "Custom Career Role") if user else "Custom Career Role"

    st.markdown(f"""
        <div class="glass-card">
            <h2>🗺️ Personalized Learning Roadmap for {target_role}</h2>
            <p style="color:#94a3b8;">Structured phase-by-phase learning plan based on skill dependencies and portfolio project completion. Track your progress phase by phase.</p>
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
                <p style="color:#cbd5e1; font-size:15px;">Welcome {user_name}! Upload your resume in <b>📄 Resume & JD Analysis</b> to generate your personalized learning roadmap for <b>{target_role}</b>.</p>
            </div>
        """, unsafe_allow_html=True)
        return

    planner = PredictivePlanner()
    roadmap = planner.generate_roadmap(missing_skills, target_role)
    phases = roadmap.get("phases", [])

    completed_phases = st.session_state.get("completed_phases", set())
    progress_pct = int((len(completed_phases) / len(phases)) * 100) if phases else 0

    st.subheader(f"📊 Roadmap Completion Progress: `{progress_pct}%`")
    st.progress(progress_pct / 100.0)

    st.markdown("---")

    for p in phases:
        p_num = p["phase_number"]
        is_done = p_num in completed_phases
        
        with st.expander(f"{'✅' if is_done else '📌'} {p['phase_title']}", expanded=(p_num == 1 or p_num == len(completed_phases) + 1)):
            st.caption(f"🎯 **Milestone:** {p.get('milestone', '')}")
            st.markdown(f"**Focus Skills:** {', '.join(p.get('focus_skills', []))}")
            
            st.markdown("**Action Items:**")
            for idx, item in enumerate(p.get("action_items", [])):
                st.checkbox(item, key=f"phase_{p_num}_item_{idx}", value=is_done)
            
            if st.button(f"{'Mark Phase Incomplete' if is_done else 'Mark Phase Complete ✅'}", key=f"btn_phase_{p_num}"):
                if is_done:
                    completed_phases.remove(p_num)
                else:
                    completed_phases.add(p_num)
                st.session_state["completed_phases"] = completed_phases
                st.rerun()
