import streamlit as st
import requests
from frontend.components.cards import render_metric_card
from frontend.components.charts import create_skill_radar_chart, create_skill_gap_bar_chart, create_interview_score_trend_chart

API_BASE_URL = "http://127.0.0.1:8000/api"

def render_dashboard_page():
    user = st.session_state.get("user")
    user_name = user.get("full_name", "Candidate") if user else "Candidate"
    target_role = user.get("target_role", "AI Engineer") if user else "AI Engineer"

    st.markdown(f"""
        <div class="glass-card">
            <h2>📊 Candidate Career Progress Dashboard</h2>
            <p style="color:#94a3b8;">Welcome back, <b>{user_name}</b>! Here is your real-time career readiness analytics for <b>{target_role}</b>.</p>
        </div>
    """, unsafe_allow_html=True)

    try:
        res = requests.get(f"{API_BASE_URL}/dashboard/summary", timeout=4)
        summary = res.json()
    except Exception:
        summary = {
            "resume_match_score": 72.0,
            "skills_matched_count": 6,
            "skills_missing_count": 4,
            "learning_progress_pct": 65.0,
            "interview_score": 78.0,
            "matched_skills": ["Python", "FastAPI", "SQL", "Git", "Docker"],
            "missing_skills": ["RAG", "LangChain", "Prompt Engineering", "ChromaDB"],
            "high_priority_skills": ["RAG", "Prompt Engineering"],
            "next_recommended_action": "Build the AI Knowledge Assistant project to cover RAG and ChromaDB."
        }

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_metric_card("Resume Match Score", f"{summary['resume_match_score']}%", "+14% Potential")
    with c2:
        render_metric_card("Skills Matched", str(summary['skills_matched_count']), "Strong Foundation")
    with c3:
        render_metric_card("Skills Missing", str(summary['skills_missing_count']), "Action Items")
    with c4:
        render_metric_card("Interview Score", f"{summary['interview_score']}/100", "Above Average")

    st.markdown("---")

    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        st.subheader("🎯 Skill Coverage Radar")
        st.plotly_chart(
            create_skill_radar_chart(summary['matched_skills'], summary['missing_skills']),
            use_container_width=True
        )
    with col_chart2:
        st.subheader("📊 Skill Breakdown Distribution")
        st.plotly_chart(
            create_skill_gap_bar_chart(summary['matched_skills'], summary['missing_skills']),
            use_container_width=True
        )

    col_chart3, col_chart4 = st.columns(2)
    with col_chart3:
        st.subheader("🎙️ Mock Interview Score Trend")
        history = st.session_state.get("interview_history", [])
        st.plotly_chart(create_interview_score_trend_chart(history), use_container_width=True)
    with col_chart4:
        st.subheader("⚡ High Priority Focus Items")
        st.markdown(f"""
            <div style="background:rgba(15,23,42,0.8); border:1px solid rgba(239,68,68,0.3); border-radius:12px; padding:20px;">
                <h4 style="color:#f87171; margin-top:0;">🔥 High Priority Skills to Master:</h4>
                <ul>
                    {"".join([f"<li style='color:#f1f5f9;'><b>{s}</b></li>" for s in summary['high_priority_skills']])}
                </ul>
                <h4 style="color:#818cf8; margin-top:15px;">👉 Next Recommended Action:</h4>
                <p style="color:#cbd5e1; font-size:14px; margin:0;">{summary['next_recommended_action']}</p>
            </div>
        """, unsafe_allow_html=True)
