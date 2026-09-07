import json
import streamlit as st
from backend.core.database import SessionLocal
from backend.models.skill import AnalysisResultModel

def render_skill_gap_page():
    user = st.session_state.get("user")
    user_id = user.get("id") if user else None
    user_name = user.get("full_name", "Candidate") if user else "Candidate"
    target_role = user.get("target_role", "Custom Career Role") if user else "Custom Career Role"

    st.markdown("""
        <div class="glass-card">
            <h2>🧠 Skill Gap Analysis & Explainable AI Engine</h2>
            <p style="color:#94a3b8;">CareerPilot AI explains EXACTLY why each score was calculated and why every skill is recommended using transparent evidence.</p>
        </div>
    """, unsafe_allow_html=True)

    # Check session state match data or fetch latest DB analysis record for candidate user_id
    match_data = st.session_state.get("match_data")
    if not match_data and user_id:
        db = SessionLocal()
        try:
            record = db.query(AnalysisResultModel).filter(AnalysisResultModel.user_id == user_id).order_by(AnalysisResultModel.id.desc()).first()
            if record:
                match_data = {
                    "overall_match_percentage": round(record.match_score, 1),
                    "breakdown": json.loads(record.breakdown_json or "{}"),
                    "matched_skills": json.loads(record.matched_skills_json or "[]"),
                    "missing_required_skills": json.loads(record.missing_skills_json or "[]"),
                    "explainable_recommendations": json.loads(record.explanations_json or "[]"),
                    "scoring_explanation": "Match Score calculated using transparent weighted formula: Required Skills (40%), Project Alignment (25%), Experience (15%), Certifications (10%), Education (10%)."
                }
                st.session_state["match_data"] = match_data
        except Exception:
            match_data = None
        finally:
            db.close()

    # If candidate has not uploaded a resume yet
    if not match_data:
        st.markdown(f"""
            <div style="background: rgba(99, 102, 241, 0.12); border: 1px solid #6366f1; border-radius: 14px; padding: 24px; text-align: center; margin: 20px 0;">
                <h3 style="color:#818cf8; margin-top:0;">📄 Resume Upload Required</h3>
                <p style="color:#cbd5e1; font-size:15px; max-width:650px; margin: 0 auto 15px auto;">
                    Welcome, <b>{user_name}</b>! You haven't uploaded a resume for target role <b>{target_role}</b> yet.
                </p>
                <p style="color:#94a3b8; font-size:14px; margin-bottom:0;">
                    Please go to <b>📄 Resume & JD Analysis</b> in the sidebar to upload your resume, edit your extracted profile skills, and generate your transparent skill gap breakdown.
                </p>
            </div>
        """, unsafe_allow_html=True)
        return

    score = match_data.get("overall_match_percentage", 0.0)
    bd = match_data.get("breakdown", {})

    st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(99, 102, 241, 0.25) 0%, rgba(168, 85, 247, 0.25) 100%); border: 1px solid #6366f1; border-radius: 16px; padding: 24px; text-align: center; margin-bottom: 24px;">
            <h3 style="margin:0; color:#cbd5e1; font-size:18px;">TRANSPARENT CANDIDATE MATCH SCORE FOR {target_role.upper()}</h3>
            <h1 style="font-size: 56px; color: #818cf8; margin: 10px 0;">{score}%</h1>
            <p style="color:#94a3b8; font-size:14px; max-width:700px; margin:0 auto;">{match_data.get('scoring_explanation', '')}</p>
        </div>
    """, unsafe_allow_html=True)

    st.subheader("📊 5-Dimension Transparent Score Breakdown")
    b1, b2, b3, b4, b5 = st.columns(5)
    b1.metric("Required Skills (40%)", f"{bd.get('required_skills_score', 0)}%")
    b2.metric("Preferred Skills", f"{bd.get('preferred_skills_score', 0)}%")
    b3.metric("Project Alignment (25%)", f"{bd.get('project_alignment_score', 0)}%")
    b4.metric("Experience Fit (15%)", f"{bd.get('experience_alignment_score', 0)}%")
    b5.metric("Edu & Certs (20%)", f"{bd.get('education_cert_score', 0)}%")

    st.markdown("---")

    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.subheader("✅ Matched Skills")
        matched = match_data.get("matched_skills", [])
        if matched:
            for s in matched:
                st.markdown(f"<span class='badge-matched'>{s}</span>", unsafe_allow_html=True)
        else:
            st.info("No matched skills found yet.")

    with col_m2:
        st.subheader("⚠️ Missing Skills (Skill Gap)")
        missing = match_data.get("missing_required_skills") or match_data.get("missing_skills", [])
        if missing:
            for s in missing:
                st.markdown(f"<span class='badge-missing'>{s}</span>", unsafe_allow_html=True)
        else:
            st.success("No missing required skills! Excellent fit.")

    st.markdown("---")
    st.subheader("💡 Explainable AI Recommendations & Skill Priority Engine")

    recs = match_data.get("explainable_recommendations", [])
    if not recs:
        st.info("Upload a resume and job description to view explainable recommendations.")
    else:
        for rec in recs:
            with st.expander(f"📌 {rec['skill']} — [{rec.get('priority', 'HIGH PRIORITY')}] ({rec.get('evidence_type', 'Direct Evidence')})", expanded=True):
                st.markdown(f"**Why Recommended:** {rec.get('why_recommended', 'Essential skill for target role.')}")
                st.markdown(f"**Required in Job Description?** {'Yes ✅' if rec.get('is_required', True) else 'No (Preferred) ℹ️'}")
                st.markdown(f"**Complements Candidate Skills:** {', '.join(rec.get('related_user_skills', []))}")
                st.markdown(f"**Career Benefit:** {rec.get('target_role_benefit', 'Enhances candidate qualifications.')}")
                st.markdown("**Recommended Demonstration Projects:**")
                for proj in rec.get("demonstration_projects", []):
                    st.markdown(f"- 🛠️ {proj}")
