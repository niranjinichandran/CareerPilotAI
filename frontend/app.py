import streamlit as st
from frontend.components.cards import inject_custom_css
from frontend.components.sidebar import render_sidebar
from frontend.views.home import render_home_page
from frontend.views.auth_page import render_auth_page
from frontend.views.dashboard import render_dashboard_page
from frontend.views.resume_analysis import render_resume_analysis_page
from frontend.views.job_analysis import render_job_analysis_page
from frontend.views.skill_gap import render_skill_gap_page
from frontend.views.simulator import render_simulator_page
from frontend.views.projects import render_projects_page
from frontend.views.roadmap import render_roadmap_page
from frontend.views.interview import render_interview_page
from frontend.views.career_chat import render_career_chat_page

# Set Streamlit Page Config & Title
st.set_page_config(
    page_title="CareerPilot AI - Intelligent Career Mentor",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject Custom CSS Theme
inject_custom_css()

# Session State Initialization
if "user" not in st.session_state:
    st.session_state["user"] = None
if "resume_skills" not in st.session_state:
    st.session_state["resume_skills"] = ["Python", "FastAPI", "SQL", "Git", "Docker"]
if "match_data" not in st.session_state:
    st.session_state["match_data"] = None

# Render Sidebar & Navigation Routing
selected_menu = render_sidebar()

# Authentication Gatekeeper: If user is not logged in, force Login / Register page!
if st.session_state.get("user") is None:
    render_auth_page()
else:
    if selected_menu == "📊 Candidate Dashboard":
        render_dashboard_page()
    elif selected_menu == "📄 Resume & JD Analysis":
        render_resume_analysis_page()
    elif selected_menu == "🎯 Job Description Analyzer":
        render_job_analysis_page()
    elif selected_menu == "📊 Skill Gap & Explainable AI":
        render_skill_gap_page()
    elif selected_menu == "⚡ Skill Impact Simulator":
        render_simulator_page()
    elif selected_menu == "🛠️ Recommended Projects":
        render_projects_page()
    elif selected_menu == "🗺️ Personalized Roadmap":
        render_roadmap_page()
    elif selected_menu == "🎙️ Adaptive Mock Interview":
        render_interview_page()
    elif selected_menu == "💬 RAG Career Assistant":
        render_career_chat_page()
    elif selected_menu == "🏠 Platform Overview":
        render_home_page()
    else:
        render_dashboard_page()
