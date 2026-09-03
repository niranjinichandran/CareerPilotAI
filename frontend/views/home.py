import streamlit as st
from frontend.components.cards import render_hero_section

def render_home_page():
    render_hero_section()

    st.markdown("### 🌟 Platform Key Capabilities")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
            <div class="glass-card">
                <h3>📄 Transparent Resume Match</h3>
                <p style="color:#94a3b8; font-size:14px;">
                    Upload PDF or DOCX resumes. Extracts skills, projects, and experience to calculate a transparent 5-dimension match score.
                </p>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("""
            <div class="glass-card">
                <h3>⚡ Skill Impact Simulator</h3>
                <p style="color:#94a3b8; font-size:14px;">
                    Simulate learning missing skills to preview real-time score increases, newly satisfied requirements, and unlocked roles.
                </p>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div class="glass-card">
                <h3>🧠 Explainable AI Engine</h3>
                <p style="color:#94a3b8; font-size:14px;">
                    Understands WHY each skill is recommended with transparent priority rankings (HIGH/MED/LOW) and direct market evidence.
                </p>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("""
            <div class="glass-card">
                <h3>🎙️ Adaptive AI Mock Interview</h3>
                <p style="color:#94a3b8; font-size:14px;">
                    Practice technical interview questions that dynamically adapt to weak skills, track performance, and build interview memory.
                </p>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
            <div class="glass-card">
                <h3>🛠️ Maximized Project Engine</h3>
                <p style="color:#94a3b8; font-size:14px;">
                    Recommends hands-on portfolio projects covering multiple missing skills simultaneously with step-by-step guides.
                </p>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("""
            <div class="glass-card">
                <h3>💬 RAG Career Assistant</h3>
                <p style="color:#94a3b8; font-size:14px;">
                    Vector search grounded in ChromaDB to answer tech, resume, and architecture questions with zero hallucination.
                </p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🔄 How CareerPilot AI Works")
    
    steps = [
        ("1. Upload Resume", "Parse PDF/DOCX to extract skills, projects, education, and years of experience."),
        ("2. Select Target Role", "Input target role and paste job description to extract required competencies."),
        ("3. Analyze Skill Gap", "Calculate transparent 5-part match breakdown & explainable skill priority."),
        ("4. Simulate Growth", "Select skills to simulate learning and view projected match score gains."),
        ("5. Build & Practice", "Follow personalized learning roadmaps, build projects, and practice adaptive mock interviews.")
    ]

    cols = st.columns(5)
    for idx, (title, desc) in enumerate(steps):
        with cols[idx]:
            st.markdown(f"""
                <div style="background:rgba(15, 23, 42, 0.7); border:1px solid rgba(99, 102, 241, 0.2); border-radius:12px; padding:16px; min-height:180px; text-align:center;">
                    <h4 style="color:#818cf8; font-size:16px; margin-bottom:8px;">{title}</h4>
                    <p style="color:#94a3b8; font-size:12px; margin:0;">{desc}</p>
                </div>
            """, unsafe_allow_html=True)
