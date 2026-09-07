import streamlit as st

def render_sidebar():
    user = st.session_state.get("user")
    
    with st.sidebar:
        st.markdown("""
            <div style="text-align: center; padding: 10px 0;">
                <h2 style="margin:0; font-size:24px; color:#818cf8;">🚀 CareerPilot AI</h2>
                <p style="margin:0; font-size:12px; color:#94a3b8;">Your Intelligent AI Career Mentor</p>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("---")
        
        if not user:
            st.info("🔐 **Access Gated**\nPlease Sign In or Register an account to unlock career intelligence features.")
            st.markdown("---")
            st.caption("Powered by FastAPI • ChromaDB • Streamlit")
            return "🔑 Auth"
        else:
            st.markdown(f"👤 **Candidate Name:** {user.get('full_name', 'Candidate')}")
            st.markdown(f"🎯 **Target Role:** {user.get('target_role', 'Custom Role')}")
            st.markdown("---")

            menu_options = [
                "📊 Candidate Dashboard",
                "📄 Resume & JD Analysis",
                "🎯 Job Description Analyzer",
                "📊 Skill Gap & Explainable AI",
                "⚡ Skill Impact Simulator",
                "🛠️ Recommended Projects",
                "🗺️ Personalized Roadmap",
                "🎙️ Adaptive Mock Interview",
                "💬 RAG Career Assistant",
                "🏠 Platform Overview"
            ]
            
            selected_menu = st.radio("Platform Navigation", menu_options)
            st.markdown("---")
            
            if st.button("🔒 Sign Out / Logout Candidate", use_container_width=True):
                # Clear all user session data
                st.session_state["user"] = None
                st.session_state["match_data"] = None
                st.session_state["parsed_skills"] = []
                st.session_state["resume_skills"] = []
                st.session_state["completed_phases"] = set()
                st.session_state["interview_history"] = []
                st.rerun()

            st.caption("Powered by FastAPI • ChromaDB • Streamlit")
            return selected_menu
