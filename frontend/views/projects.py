import streamlit as st
import requests

API_BASE_URL = "http://127.0.0.1:8000/api"

def render_projects_page():
    st.markdown("""
        <div class="glass-card">
            <h2>🛠️ Project Recommendation Engine</h2>
            <p style="color:#94a3b8;">Instead of watching generic tutorials, build real-world hands-on portfolio projects engineered to maximize missing skill coverage in a single build.</p>
        </div>
    """, unsafe_allow_html=True)

    match_data = st.session_state.get("match_data")
    missing_skills = match_data.get("missing_skills", ["RAG", "LangChain", "Prompt Engineering", "ChromaDB"]) if match_data else ["RAG", "LangChain", "Prompt Engineering", "ChromaDB"]

    try:
        res = requests.post(f"{API_BASE_URL}/recommendations/projects", json={"missing_skills": missing_skills}, timeout=5)
        projects = res.json()
    except Exception:
        projects = [
            {
                "title": "AI Knowledge Assistant with ChromaDB & RAG",
                "problem_statement": "Organizations struggle to retrieve precise insights from unstructured PDF documents without hallucination.",
                "overview": "A production-ready RAG application combining FastAPI backend, ChromaDB vector store, LangChain, and Streamlit frontend.",
                "features": [
                    "PDF & Text Document Parsing",
                    "Dense Vector Embeddings Ingestion in ChromaDB",
                    "RAG Retrieval Engine with Citation Highlights",
                    "Interactive Streamlit QA Chatbot"
                ],
                "tech_stack": ["Python", "FastAPI", "LangChain", "ChromaDB", "Streamlit"],
                "skills_demonstrated": ["RAG", "LangChain", "Prompt Engineering", "ChromaDB", "FastAPI"],
                "difficulty": "Intermediate",
                "development_steps": [
                    "Step 1: Setup project directory and virtual environment with FastAPI & ChromaDB.",
                    "Step 2: Build document text extraction pipeline for PDF files.",
                    "Step 3: Create vector embedding pipeline and store chunks in ChromaDB.",
                    "Step 4: Build RAG retrieval query engine and format prompt context.",
                    "Step 5: Develop FastAPI REST endpoints and connect Streamlit UI."
                ],
                "recommendation_reason": "This project covers multiple skills currently missing from your profile: RAG, LangChain, Prompt Engineering, ChromaDB."
            }
        ]

    st.subheader("📌 Recommended Projects Maximizing Skill Coverage")

    for proj in projects:
        with st.expander(f"🛠️ {proj['title']} — Difficulty: [{proj['difficulty']}]", expanded=True):
            st.markdown(f"**Why Recommended:** {proj['recommendation_reason']}")
            st.markdown(f"**Problem Statement:** {proj['problem_statement']}")
            st.markdown(f"**Project Overview:** {proj['overview']}")
            st.markdown(f"**Tech Stack:** {', '.join(proj['tech_stack'])}")
            
            st.markdown("**Skills Demonstrated:**")
            for sk in proj["skills_demonstrated"]:
                st.markdown(f"- `<span class='badge-matched'>{sk}</span>`", unsafe_allow_html=True)

            st.markdown("**Key Features & Deliverables:**")
            for f in proj["features"]:
                st.markdown(f"- ✅ {f}")

            st.markdown("**Step-by-Step Development Steps:**")
            for step in proj["development_steps"]:
                st.markdown(f"- {step}")
