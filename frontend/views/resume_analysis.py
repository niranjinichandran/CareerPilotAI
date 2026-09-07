import json
import streamlit as st
from ai.resume_parser import ResumeParser
from ai.skill_gap_engine import SkillGapEngine
from backend.core.database import SessionLocal
from backend.models.resume import ResumeModel, JobDescriptionModel
from backend.models.skill import AnalysisResultModel

def render_resume_analysis_page():
    user = st.session_state.get("user")
    if not user:
        st.warning("Please sign in to upload and analyze your resume.")
        return

    user_id = user.get("id")
    target_role = user.get("target_role", "Custom Career Role")

    st.markdown("""
        <div class="glass-card">
            <h2>📄 Resume & Job Description Analyzer</h2>
            <p style="color:#94a3b8;">Upload your resume and paste your target job description. Edit and customize your extracted profile skills before computing your transparent 5-part candidate match score.</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("1. Candidate Resume Input")
        uploaded_file = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"], key="resume_file_uploader")
        
        sample_resume = st.text_area(
            "Or Paste Resume Text directly:",
            value=st.session_state.get("raw_resume_text", ""),
            placeholder="Paste your resume text here...",
            height=140,
            key="raw_resume_text_area"
        )

        if st.button("Extract Resume Details 🔍", type="secondary", use_container_width=True):
            parser = ResumeParser()
            if uploaded_file is not None:
                file_bytes = uploaded_file.getvalue()
                filename = uploaded_file.name
                ext = filename.split(".")[-1].lower()
                extracted_text = parser.parse_file(file_bytes, ext)
                ext_skills = parser.extract_skills(extracted_text)
                st.session_state["raw_resume_text"] = extracted_text
                st.session_state["parsed_skills"] = ext_skills
                st.session_state["resume_skills"] = ext_skills
                st.success(f"Extracted {len(ext_skills)} skills from uploaded resume file '{filename}'!")
            elif sample_resume.strip():
                ext_skills = parser.extract_skills(sample_resume)
                st.session_state["raw_resume_text"] = sample_resume
                st.session_state["parsed_skills"] = ext_skills
                st.session_state["resume_skills"] = ext_skills
                st.success(f"Extracted {len(ext_skills)} skills from pasted resume text!")
            else:
                st.warning("Please upload a PDF/DOCX resume file or paste resume text.")

    with col2:
        st.subheader(f"2. Target Job Description ({target_role})")
        jd_text = st.text_area(
            "Paste Target Job Description:",
            value=st.session_state.get("jd_text", f"We are hiring a {target_role}. Key requirements include strong technical skills, problem solving, software design, REST APIs, database management, and cloud tools."),
            height=220,
            key="jd_text_area"
        )
        st.session_state["jd_text"] = jd_text

    st.markdown("---")
    
    # ------------------- EDITABLE EXTRACTED PROFILE SKILLS SECTION -------------------
    st.subheader("✏️ Editable Extracted Profile Skills")
    st.caption("Add, remove, or modify any skills extracted from your resume below before running the match calculation:")

    # Initialize current skills in session state
    if "resume_skills" not in st.session_state or not st.session_state["resume_skills"]:
        st.session_state["resume_skills"] = st.session_state.get("parsed_skills", ["Python", "SQL", "Git", "REST APIs"])

    current_skills_list = st.session_state["resume_skills"]

    # Comma-separated text input for instant editing
    skills_text_val = ", ".join(current_skills_list)
    edited_skills_str = st.text_area(
        "Current Profile Skills (Comma Separated - Edit directly):",
        value=skills_text_val,
        height=80,
        help="You can add new skills or delete skills by editing this comma-separated text."
    )

    # Parse edited skills from text area
    updated_skills = [s.strip() for s in edited_skills_str.split(",") if s.strip()]
    st.session_state["resume_skills"] = updated_skills

    # Display current skills as interactive badge tags
    st.markdown("#### Currently Active Candidate Skills:")
    if updated_skills:
        badges_html = " ".join([f"<span class='badge-matched'>{sk}</span>" for sk in updated_skills])
        st.markdown(badges_html, unsafe_allow_html=True)
    else:
        st.info("No skills listed. Type your skills in the text box above.")

    # Quick Add Skill helper input
    col_add1, col_add2 = st.columns([3, 1])
    with col_add1:
        new_skill_input = st.text_input("Add a missing skill manually:", placeholder="e.g. Docker, TensorFlow, AWS, React...", key="new_skill_input")
    with col_add2:
        st.markdown("<div style='margin-top:28px;'></div>", unsafe_allow_html=True)
        if st.button("➕ Add Skill", type="secondary", use_container_width=True):
            if new_skill_input.strip():
                clean_skill = new_skill_input.strip()
                if clean_skill not in st.session_state["resume_skills"]:
                    st.session_state["resume_skills"].append(clean_skill)
                    st.success(f"Added '{clean_skill}' to profile skills!")
                    st.rerun()

    st.markdown("---")

    # ------------------- RUN MATCH ANALYSIS -------------------
    if st.button("🚀 Analyze Resume & Compute Candidate Match Score", type="primary", use_container_width=True):
        final_candidate_skills = st.session_state["resume_skills"]
        current_jd_text = st.session_state.get("jd_text", jd_text)

        if not final_candidate_skills:
            st.error("Please add at least one skill to your profile before running analysis.")
        elif not current_jd_text.strip():
            st.error("Please provide a target job description.")
        else:
            with st.spinner("Computing transparent 5-part match breakdown & explainable AI recommendations..."):
                engine = SkillGapEngine()
                gap_result = engine.calculate_gap_analysis(
                    resume_skills=final_candidate_skills,
                    jd_text=current_jd_text,
                    experience_years=st.session_state.get("parsed_exp", 2.0),
                    has_certifications=st.session_state.get("parsed_certs", True),
                    has_education=st.session_state.get("parsed_edu", True)
                )

                st.session_state["match_data"] = gap_result
                st.session_state["has_uploaded_resume"] = True

                # PERSIST TO DATABASE FOR CANDIDATE USER_ID
                db = SessionLocal()
                try:
                    # Save Resume record
                    resume_rec = ResumeModel(
                        user_id=user_id,
                        filename=uploaded_file.name if uploaded_file else "Pasted_Resume.txt",
                        raw_text=st.session_state.get("raw_resume_text", "Direct candidate resume text"),
                        parsed_skills=json.dumps(final_candidate_skills),
                        parsed_projects=json.dumps([]),
                        experience_years=2.0,
                        has_education=True,
                        has_certifications=True
                    )
                    db.add(resume_rec)
                    db.commit()
                    db.refresh(resume_rec)

                    # Save Job Description record
                    jd_rec = JobDescriptionModel(
                        user_id=user_id,
                        title=target_role,
                        company="Target Organization",
                        raw_text=current_jd_text,
                        extracted_skills=json.dumps(gap_result.get("missing_required_skills", []) + gap_result.get("matched_skills", [])),
                        normalized_skills=json.dumps(gap_result.get("missing_required_skills", [])),
                        responsibilities=json.dumps(["Deliver high quality technical software solutions"]),
                        experience_req="1-3 years"
                    )
                    db.add(jd_rec)
                    db.commit()
                    db.refresh(jd_rec)

                    # Save Analysis Result record
                    analysis_rec = AnalysisResultModel(
                        user_id=user_id,
                        resume_id=resume_rec.id,
                        jd_id=jd_rec.id,
                        match_score=gap_result["overall_match_percentage"],
                        breakdown_json=json.dumps(gap_result["breakdown"]),
                        matched_skills_json=json.dumps(gap_result["matched_skills"]),
                        missing_skills_json=json.dumps(gap_result.get("missing_required_skills") or gap_result.get("missing_skills", [])),
                        priority_ranking_json=json.dumps([r["skill"] for r in gap_result.get("explainable_recommendations", []) if r.get("priority") == "HIGH PRIORITY"]),
                        explanations_json=json.dumps(gap_result.get("explainable_recommendations", []))
                    )
                    db.add(analysis_rec)
                    db.commit()

                    st.success(f"✅ Resume analysis complete for {user.get('full_name')}! Match Score: {gap_result['overall_match_percentage']}%. Go to Candidate Dashboard to view full results.")
                except Exception as e:
                    db.rollback()
                    st.success(f"Analysis calculated! Match Score: {gap_result['overall_match_percentage']}%.")
                finally:
                    db.close()
