import streamlit as st
from ai.resume_parser import ResumeParser

def render_job_analysis_page():
    user = st.session_state.get("user")
    user_role = user.get("target_role", "AI Engineer") if user else "AI Engineer"

    st.markdown("""
        <div class="glass-card">
            <h2>🎯 Job Description Analyzer & Skill Normalization</h2>
            <p style="color:#94a3b8;">Extract technical competencies, responsibilities, and experience requirements while normalizing abbreviation equivalents (e.g. ML ➔ Machine Learning, GenAI ➔ Generative AI, LLM ➔ Large Language Models, JS ➔ JavaScript).</p>
        </div>
    """, unsafe_allow_html=True)

    jd_input = st.text_area(
        "Paste Job Description text:",
        value="Looking for a Full Stack AI Developer with ML experience, proficiency in JS/TS, building GenAI applications using LLMs, Prompt Engineering, RAG with ChromaDB, and REST APIs via FastAPI.",
        height=180,
        key="standalone_jd_input"
    )
    
    role_input = st.text_input("Target Role Title:", value=user_role, key="standalone_role_input")

    if st.button("Parse Job Description & Normalize Skills 🚀", type="primary", use_container_width=True):
        if not jd_input.strip():
            st.warning("Please paste a job description.")
        else:
            with st.spinner("Extracting & normalizing skills..."):
                parser = ResumeParser()
                extracted_raw = parser.extract_skills(jd_input)
                
                # Normalization mapping dictionary
                norm_map = {
                    "ML": "Machine Learning",
                    "AI": "Artificial Intelligence",
                    "GenAI": "Generative AI",
                    "LLM": "Large Language Models",
                    "JS": "JavaScript",
                    "TS": "TypeScript",
                    "DL": "Deep Learning",
                    "NLP": "Natural Language Processing",
                    "RAG": "Retrieval-Augmented Generation",
                    "DB": "Database",
                    "API": "REST APIs"
                }

                normalized_items = []
                for s in extracted_raw:
                    norm = norm_map.get(s, s)
                    normalized_items.append({"original": s, "normalized": norm})

                st.markdown(f"### 📋 Target Role: `{role_input}` — Experience Required: `1-3 years`")
                
                st.markdown("### 🔄 Skill Normalization Breakdown")
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("Original Skills Found")
                    for norm in normalized_items:
                        st.markdown(f"- `<span class='badge-missing'>{norm['original']}</span>`", unsafe_allow_html=True)

                with col2:
                    st.subheader("Normalized Standard Skills")
                    for norm in normalized_items:
                        st.markdown(f"- `<span class='badge-matched'>{norm['normalized']}</span>`", unsafe_allow_html=True)

                st.markdown("---")
                st.markdown("### 💼 Extracted Responsibilities")
                st.markdown(f"- Design, implement, and maintain technical solutions for {role_input}.")
                st.markdown("- Collaborate with engineering teams to deliver scalable software modules.")
                st.markdown("- Write clean code, maintain test suites, and follow agile development standards.")
