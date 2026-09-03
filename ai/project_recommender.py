import os
import json
from typing import Dict, List, Any

class ProjectRecommender:
    def __init__(self):
        catalog_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "datasets", "projects_catalog.json")
        self.projects_catalog = []
        if os.path.exists(catalog_path):
            with open(catalog_path, "r", encoding="utf-8") as f:
                self.projects_catalog = json.load(f)

    def recommend_projects(self, missing_skills: List[str]) -> List[Dict[str, Any]]:
        if not missing_skills:
            missing_skills = ["FastAPI", "RAG", "LangChain", "ChromaDB", "Prompt Engineering"]

        missing_set = set(s.lower() for s in missing_skills)
        scored_projects = []

        for proj in self.projects_catalog:
            target_skills = set(s.lower() for s in proj.get("target_missing_skills", []))
            overlap = missing_set.intersection(target_skills)
            score = len(overlap)
            scored_projects.append((score, proj, list(overlap)))

        # Sort by highest skill overlap to maximize skill coverage
        scored_projects.sort(key=lambda x: x[0], reverse=True)

        recommendations = []
        for score, proj, covered_skills in scored_projects[:3]:
            recommendations.append({
                "id": proj.get("id", "proj_1"),
                "title": proj.get("title", "AI Knowledge Assistant"),
                "problem_statement": proj.get("problem_statement", "Organizations struggle to search unformatted documents efficiently without hallucination."),
                "overview": proj.get("description", "A production-ready RAG application combining FastAPI backend, ChromaDB vector store, and Streamlit frontend."),
                "features": proj.get("key_deliverables", [
                    "PDF Document Upload & Ingestion",
                    "Vector Embeddings Generation & ChromaDB Storage",
                    "RAG Retrieval Pipeline with Citation Highlights",
                    "Interactive Streamlit Chat UI"
                ]),
                "tech_stack": proj.get("tech_stack", ["Python", "FastAPI", "LangChain", "ChromaDB", "Streamlit"]),
                "skills_demonstrated": proj.get("target_missing_skills", missing_skills[:4]),
                "difficulty": proj.get("difficulty", "Intermediate"),
                "development_steps": [
                    "Step 1: Setup project directory and virtual environment with FastAPI & ChromaDB.",
                    "Step 2: Build document text extraction pipeline for PDF and text files.",
                    "Step 3: Create vector embedding pipeline and store chunks in ChromaDB.",
                    "Step 4: Build RAG retrieval query engine and format prompt context.",
                    "Step 5: Develop FastAPI REST endpoints and connect Streamlit UI."
                ],
                "why_recommended": f"This project covers multiple skills currently missing from your profile: {', '.join(proj.get('target_missing_skills', missing_skills[:3]))}."
            })

        # Dynamic fallback project generator if missing skills are custom
        if not recommendations:
            skills_str = ", ".join(missing_skills[:4])
            recommendations.append({
                "id": "proj_custom_gen",
                "title": f"Custom {missing_skills[0] if missing_skills else 'AI'} Application Platform",
                "problem_statement": f"Demonstrating end-to-end practical mastery in {skills_str} for enterprise career readiness.",
                "overview": f"A comprehensive full-stack solution built specifically to cover your skill gaps in {skills_str}.",
                "features": [
                    f"Core workflow implementation using {skills_str}",
                    "FastAPI REST backend with async task handling",
                    "Interactive UI dashboard and user input validation",
                    "Complete GitHub documentation and unit testing"
                ],
                "tech_stack": missing_skills + ["Python", "FastAPI", "Streamlit"],
                "skills_demonstrated": missing_skills,
                "difficulty": "Intermediate",
                "development_steps": [
                    "Step 1: Define system architecture and API schema.",
                    "Step 2: Implement core algorithm and model logic.",
                    "Step 3: Build REST API endpoints and connect database.",
                    "Step 4: Build interactive frontend and test complete user flow."
                ],
                "why_recommended": f"This project covers multiple skills currently missing from your profile ({skills_str})."
            })

        return recommendations

project_recommender = ProjectRecommender()
