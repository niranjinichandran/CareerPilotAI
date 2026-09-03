import streamlit as st
import requests

API_BASE_URL = "http://127.0.0.1:8000/api"

def render_job_analysis_page():
    st.markdown("""
        <div class="glass-card">
            <h2>🎯 Job Description Analyzer & Skill Normalization</h2>
            <p style="color:#94a3b8;">Extract technical competencies, responsibilities, and experience requirements while normalizing abbreviation equivalents (e.g. ML ➜ Machine Learning, GenAI ➜ Generative AI).</p>
        </div>
    """, unsafe_allow_html=True)

    jd_input = st.text_area(
        "Paste Job Description text:",
        value="Looking for a Full Stack AI Developer with ML experience, proficiency in JS/TS, building GenAI applications using LLMs, Prompt Engineering, RAG with ChromaDB, and REST APIs via FastAPI.",
        height=180
    )
    
    role_input = st.text_input("Target Role Title:", value="AI Engineer")

    if st.button("Parse Job Description & Normalize Skills 🚀", type="primary"):
        with st.spinner("Extracting & normalizing skills..."):
            try:
                res = requests.post(f"{API_BASE_URL}/jobs/analyze", json={"jd_text": jd_input, "target_role": role_input}, timeout=5)
                if res.status_code == 200:
                    data = res.json()
                    
                    st.markdown(f"### 📋 Job Title: `{data['title']}` — Experience Required: `{data['experience_req']}`")
                    
                    st.markdown("### 🔄 Skill Normalization Breakdown")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.subheader("Original Skills Found")
                        for norm in data["normalized_skills"]:
                            st.markdown(f"- `<span class='badge-missing'>{norm['original']}</span>`", unsafe_allow_html=True)

                    with col2:
                        st.subheader("Normalized Standard Skills")
                        for norm in data["normalized_skills"]:
                            st.markdown(f"- `<span class='badge-matched'>{norm['normalized']}</span>`", unsafe_allow_html=True)

                    st.markdown("---")
                    st.markdown("### 💼 Extracted Responsibilities")
                    for resp in data["responsibilities"]:
                        st.markdown(f"- {resp}")
            except Exception as e:
                st.error("Error communicating with backend API.")
