import json
import streamlit as st
from backend.core.database import SessionLocal
from backend.models.skill import AnalysisResultModel
from backend.models.interview import InterviewSessionModel
from frontend.components.cards import render_metric_card
from frontend.components.charts import create_skill_radar_chart, create_skill_gap_bar_chart, create_interview_score_trend_chart

def render_dashboard_page():
    user = st.session_state.get("user")
    if not user:
        st.warning("Please sign in to view your candidate dashboard.")
        return

    user_id = user.get("id")
    user_name = user.get("full_name", "Candidate")
    target_role = user.get("target_role", "Custom Career Role")

    # Query database for saved analysis and interview sessions for THIS candidate user_id
    db = SessionLocal()
    analysis_record = None
    interview_records = []
    try:
        if user_id:
            analysis_record = db.query(AnalysisResultModel).filter(AnalysisResultModel.user_id == user_id).order_by(AnalysisResultModel.id.desc()).first()
            interview_records = db.query(InterviewSessionModel).filter(InterviewSessionModel.user_id == user_id).all()
    except Exception:
        analysis_record = None
    finally:
        db.close()

    st.markdown(f"""
        <div class="glass-card">
            <h2>📊 Candidate Career Progress Dashboard</h2>
            <p style="color:#94a3b8;">Welcome back, <b>{user_name}</b>! Real-time candidate analytics for target role: <b style="color:#818cf8;">{target_role}</b>.</p>
        </div>
    """, unsafe_allow_html=True)

    # STRICT CHECK: Has candidate uploaded a resume?
    has_uploaded_resume = (analysis_record is not None) or (st.session_state.get("match_data") is not None)

    if not has_uploaded_resume:
        # Initial state before resume upload -> ALL SCORES AND SKILL COUNTS ARE 0
        match_score = 0.0
        matched_skills = []
        missing_skills = []
        high_priority_skills = []
        interview_avg_score = 0.0
    else:
        # Resume has been uploaded -> Read real computed values from DB or session
        if analysis_record:
            match_score = round(analysis_record.match_score, 1)
            try:
                matched_skills = json.loads(analysis_record.matched_skills_json or "[]")
                missing_skills = json.loads(analysis_record.missing_skills_json or "[]")
                high_priority_skills = json.loads(analysis_record.priority_ranking_json or "[]")
            except Exception:
                matched_skills = []
                missing_skills = []
                high_priority_skills = []
        else:
            mdata = st.session_state.get("match_data", {})
            match_score = round(mdata.get("overall_match_percentage", 0.0), 1)
            matched_skills = mdata.get("matched_skills", [])
            missing_skills = mdata.get("missing_required_skills") or mdata.get("missing_skills", [])
            high_priority_skills = missing_skills[:2]

        if interview_records:
            scores = [r.overall_score for r in interview_records if r.overall_score is not None and r.overall_score > 0]
            interview_avg_score = round(sum(scores) / len(scores), 1) if scores else 0.0
        else:
            interview_avg_score = 0.0

    # Display Top Metric Cards
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_metric_card("Resume Match Score", f"{match_score}%", "Upload Resume to Compute" if not has_uploaded_resume else "Verified Fit")
    with c2:
        render_metric_card("Skills Matched", str(len(matched_skills)), "0 Matched" if not has_uploaded_resume else "Verified Skills")
    with c3:
        render_metric_card("Skills Missing", str(len(missing_skills)), "0 Missing" if not has_uploaded_resume else "Skill Gap Items")
    with c4:
        render_metric_card("Interview Score", f"{interview_avg_score}/100", "No Interview Conducted" if interview_avg_score == 0 else "Average Performance")

    st.markdown("---")

    if not has_uploaded_resume:
        st.markdown(f"""
            <div style="background: rgba(99, 102, 241, 0.12); border: 1px solid #6366f1; border-radius: 14px; padding: 24px; text-align: center; margin: 20px 0;">
                <h3 style="color:#818cf8; margin-top:0;">📄 Resume Upload Required</h3>
                <p style="color:#cbd5e1; font-size:15px; max-width:650px; margin: 0 auto 15px auto;">
                    Welcome, <b>{user_name}</b>! Your candidate dashboard is currently at <b>0%</b> because you haven't uploaded a resume for target role <b>{target_role}</b> yet.
                </p>
                <p style="color:#94a3b8; font-size:14px; margin-bottom: 0;">
                    Navigate to <b>📄 Resume & JD Analysis</b> in the sidebar to upload your resume, edit your profile skills, and generate your custom career analytics dashboard.
                </p>
            </div>
        """, unsafe_allow_html=True)

        col_chart1, col_chart2 = st.columns(2)
        with col_chart1:
            st.subheader("🎯 Skill Coverage Radar")
            st.plotly_chart(create_skill_radar_chart([], []), use_container_width=True)
        with col_chart2:
            st.subheader("📊 Skill Breakdown Distribution")
            st.plotly_chart(create_skill_gap_bar_chart([], []), use_container_width=True)
    else:
        col_chart1, col_chart2 = st.columns(2)
        with col_chart1:
            st.subheader("🎯 Skill Coverage Radar")
            st.plotly_chart(create_skill_radar_chart(matched_skills, missing_skills), use_container_width=True)
        with col_chart2:
            st.subheader("📊 Skill Breakdown Distribution")
            st.plotly_chart(create_skill_gap_bar_chart(matched_skills, missing_skills), use_container_width=True)

        col_chart3, col_chart4 = st.columns(2)
        with col_chart3:
            st.subheader("🎙️ Mock Interview Performance Score")
            history = st.session_state.get("interview_history", [])
            st.plotly_chart(create_interview_score_trend_chart(history), use_container_width=True)
        with col_chart4:
            st.subheader("⚡ High Priority Focus Items")
            priority_list = high_priority_skills if high_priority_skills else missing_skills[:3]
            st.markdown(f"""
                <div style="background:rgba(15,23,42,0.8); border:1px solid rgba(239,68,68,0.3); border-radius:12px; padding:20px;">
                    <h4 style="color:#f87171; margin-top:0;">🔥 Key Missing Skills to Master:</h4>
                    <ul>
                        {"".join([f"<li style='color:#f1f5f9;'><b>{s}</b></li>" for s in priority_list]) if priority_list else "<li style='color:#94a3b8;'>No missing skills! Excellent profile fit.</li>"}
                    </ul>
                    <h4 style="color:#818cf8; margin-top:15px;">👉 Next Recommended Action:</h4>
                    <p style="color:#cbd5e1; font-size:14px; margin:0;">
                        Use the <b>⚡ Skill Impact Simulator</b> or <b>🛠️ Recommended Projects</b> to start building missing skills.
                    </p>
                </div>
            """, unsafe_allow_html=True)
