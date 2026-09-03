import streamlit as st
import requests

API_BASE_URL = "http://127.0.0.1:8000/api"

def render_roadmap_page():
    st.markdown("""
        <div class="glass-card">
            <h2>🗺️ Personalized Learning Roadmap</h2>
            <p style="color:#94a3b8;">Structured phase-by-phase learning plan based on skill dependencies and portfolio project completion. Track your progress phase by phase.</p>
        </div>
    """, unsafe_allow_html=True)

    match_data = st.session_state.get("match_data")
    missing_skills = match_data.get("missing_skills", ["Prompt Engineering", "Embeddings", "Vector Databases", "RAG", "FastAPI"]) if match_data else ["Prompt Engineering", "Embeddings", "Vector Databases", "RAG", "FastAPI"]

    try:
        res = requests.post(f"{API_BASE_URL}/recommendations/roadmap", json={"missing_skills": missing_skills, "target_role": "AI Engineer"}, timeout=5)
        roadmap = res.json()
        phases = roadmap["phases"]
    except Exception:
        phases = [
            {
                "phase_number": 1,
                "phase_title": "PHASE 1: Prompt Engineering & LLM Basics",
                "focus_skills": ["Prompt Engineering", "LLMs"],
                "milestone": "Master prompt techniques (system prompts, CoT, few-shot).",
                "action_items": [
                    "Study zero-shot, few-shot, and chain-of-thought prompt design.",
                    "Build system prompts with clear guidelines and output formatting.",
                    "Test prompt templates using Ollama or OpenAI APIs."
                ]
            },
            {
                "phase_number": 2,
                "phase_title": "PHASE 2: Vector Embeddings & Text Processing",
                "focus_skills": ["Embeddings", "Sentence-Transformers"],
                "milestone": "Generate and evaluate semantic text embeddings.",
                "action_items": [
                    "Understand dense text representations and cosine similarity.",
                    "Use SentenceTransformers (bge-small-en-v1.5) to embed document text.",
                    "Implement chunking strategies for long documents."
                ]
            },
            {
                "phase_number": 3,
                "phase_title": "PHASE 3: Vector Databases (ChromaDB)",
                "focus_skills": ["Vector Databases", "ChromaDB"],
                "milestone": "Store and query vector embeddings efficiently.",
                "action_items": [
                    "Set up ChromaDB persistent collections.",
                    "Ingest embedded document chunks with rich metadata.",
                    "Perform fast similarity search queries."
                ]
            },
            {
                "phase_number": 4,
                "phase_title": "PHASE 4: Retrieval-Augmented Generation (RAG)",
                "focus_skills": ["RAG", "LangChain"],
                "milestone": "Build end-to-end RAG retrieval pipeline without hallucinations.",
                "action_items": [
                    "Combine vector retrieval with LLM prompt context.",
                    "Implement source citation tracking and context verification.",
                    "Evaluate RAG retrieval accuracy and response groundness."
                ]
            },
            {
                "phase_number": 5,
                "phase_title": "PHASE 5: FastAPI REST Backend Architecture",
                "focus_skills": ["FastAPI", "Python", "REST APIs"],
                "milestone": "Deploy async REST endpoints serving RAG services.",
                "action_items": [
                    "Design Pydantic request/response validation schemas.",
                    "Create asynchronous endpoint routes for model inference.",
                    "Implement error middleware and OpenAPI documentation."
                ]
            },
            {
                "phase_number": 6,
                "phase_title": "PHASE 6: Build Full AI Portfolio Project",
                "focus_skills": ["Full-Stack AI", "Streamlit", "Docker"],
                "milestone": "Complete production build of AI Knowledge Assistant project.",
                "action_items": [
                    "Implement complete feature set for AI Knowledge Assistant.",
                    "Build interactive Streamlit frontend UI with Plotly metrics.",
                    "Write clean README, architecture diagram, and publish on GitHub."
                ]
            },
            {
                "phase_number": 7,
                "phase_title": "PHASE 7: Adaptive AI Mock Interview Prep",
                "focus_skills": ["Interview Practice", "System Design"],
                "milestone": "Achieve 85%+ score in CareerPilot AI Adaptive Mock Interviews.",
                "action_items": [
                    "Practice targeted technical interview questions on weak skills.",
                    "Review AI feedback and refine explanation of system trade-offs.",
                    "Complete candidate readiness audit."
                ]
            }
        ]

    completed_phases = st.session_state.get("completed_phases", set())
    progress_pct = int((len(completed_phases) / len(phases)) * 100) if phases else 0

    st.subheader(f"📊 Roadmap Completion Progress: `{progress_pct}%`")
    st.progress(progress_pct / 100.0)

    st.markdown("---")

    for p in phases:
        p_num = p["phase_number"]
        is_done = p_num in completed_phases
        
        with st.expander(f"{'✅' if is_done else '📌'} {p['phase_title']}", expanded=(p_num == 1 or p_num == len(completed_phases) + 1)):
            st.caption(f"🎯 **Milestone:** {p['milestone']}")
            st.markdown(f"**Focus Skills:** {', '.join(p['focus_skills'])}")
            
            st.markdown("**Action Items:**")
            for idx, item in enumerate(p["action_items"]):
                chk = st.checkbox(item, key=f"phase_{p_num}_item_{idx}", value=is_done)
            
            if st.button(f"{'Mark Phase Incomplete' if is_done else 'Mark Phase Complete ✅'}", key=f"btn_phase_{p_num}"):
                if is_done:
                    completed_phases.remove(p_num)
                else:
                    completed_phases.add(p_num)
                st.session_state["completed_phases"] = completed_phases
                st.rerun()
