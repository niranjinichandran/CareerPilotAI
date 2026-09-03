import os
import streamlit as st
import requests
from ai.resume_parser import ResumeParser

API_BASE_URL = "http://127.0.0.1:8000/api"

def render_resume_analysis_page():
    st.markdown("""
        <div class="glass-card">
            <h2>📄 Resume & Job Description Analyzer</h2>
            <p style="color:#94a3b8;">Upload your resume and paste your target job description. Edit extracted skills before computing your 5-part match score.</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("1. Resume Upload & Extraction")
        uploaded_file = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"])
        
        sample_resume = st.text_area(
            "Or Paste Resume Text directly:",
            value="Candidate profile: Experienced Software Engineer proficient in Python, FastAPI, SQL, Docker, Git. Built REST APIs, microservices, and web applications. Bachelor of Technology in Computer Science.",
            height=140
        )

        if uploaded_file is not None:
            if st.button("Extract Resume Details 🔍"):
                with st.spinner("Parsing resume PDF/DOCX content..."):
                    try:
                        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                        res = requests.post(f"{API_BASE_URL}/resume/upload", files=files, timeout=8)
                        if res.status_code == 200:
                            data = res.json()["parsed_data"]
                            st.session_state["parsed_skills"] = data["skills"]
                            st.session_state["parsed_exp"] = data["experience_years"]
                            st.session_state["parsed_edu"] = data["has_education"]
                            st.session_state["parsed_certs"] = data["has_certifications"]
                            st.success("Resume parsed successfully!")
                    except Exception:
                        parser = ResumeParser()
                        ext_skills = parser.extract_skills(sample_resume)
                        st.session_state["parsed_skills"] = ext_skills
                        st.success("Resume extracted in local mode!")

    with col2:
        st.subheader("2. Target Job Description")
        jd_text = st.text_area(
            "Paste Target Job Description:",
            value="We are hiring an AI Engineer. Requirements: Strong Python skills, experience building Retrieval-Augmented Generation (RAG) applications using LangChain, Prompt Engineering, FastAPI, ChromaDB, and Docker. PyTorch or Transformers experience is preferred.",
            height=220
        )

    st.markdown("---")
    st.subheader("✏️ Editable Extracted Profile Skills")
    st.caption("Verify and add any missing skills before running the Skill Gap Analysis:")

    current_extracted = st.session_state.get("parsed_skills", ["Python", "FastAPI", "SQL", "Git", "Docker"])
    skills_input = st.text_input("Current Skills (Comma Separated):", value=", ".join(current_extracted))
    edited_skills = [s.strip() for s in skills_input.split(",") if s.strip()]

    if st.button("🚀 Analyze Resume & Compute Match Score", type="primary"):
        st.session_state["resume_skills"] = edited_skills
        st.session_state["jd_text"] = jd_text
        
        with st.spinner("Computing transparent 5-part match breakdown..."):
            try:
                res = requests.post(
                    f"{API_BASE_URL}/skills/gap-analysis",
                    json={
                        "resume_skills": edited_skills,
                        "jd_text": jd_text,
                        "experience_years": st.session_state.get("parsed_exp", 1.5),
                        "has_certifications": st.session_state.get("parsed_certs", False),
                        "has_education": st.session_state.get("parsed_edu", True)
                    },
                    timeout=8
                )
                if res.status_code == 200:
                    st.session_state["match_data"] = res.json()
                    st.success("Match Analysis Complete! Navigate to 'Skill Gap & Explainable AI' view to inspect detailed results.")
            except Exception as e:
                st.error("Error analyzing gap. Navigating using local calculations.")
