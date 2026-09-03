from typing import Dict, List, Any

class PredictivePlanner:
    def generate_roadmap(
        self,
        target_role: str = "AI Engineer",
        missing_skills: List[str] = None,
        recommended_project: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        if not missing_skills:
            missing_skills = ["Prompt Engineering", "Embeddings", "Vector Databases", "RAG", "FastAPI"]

        proj_title = recommended_project.get("title", "AI Knowledge Assistant") if recommended_project else "AI Application Platform"

        # Standard phase templates ordered by skill dependencies
        standard_phases_catalog = [
            {
                "skill": "Prompt Engineering",
                "title": "PHASE 1: Prompt Engineering & LLM Basics",
                "focus_skills": ["Prompt Engineering", "LLMs"],
                "milestone": "Master prompt techniques (system prompts, chain-of-thought, few-shot).",
                "action_items": [
                    "Study zero-shot, few-shot, and chain-of-thought prompt design.",
                    "Build system prompts with clear guidelines and output formatting.",
                    "Test prompt templates using Ollama or OpenAI APIs."
                ]
            },
            {
                "skill": "Embeddings",
                "title": "PHASE 2: Vector Embeddings & Text Processing",
                "focus_skills": ["Embeddings", "Sentence-Transformers"],
                "milestone": "Generate and evaluate semantic text embeddings.",
                "action_items": [
                    "Understand dense text representations and cosine similarity.",
                    "Use SentenceTransformers (bge-small-en-v1.5) to embed document text.",
                    "Implement chunking strategies for long documents."
                ]
            },
            {
                "skill": "Vector Databases",
                "title": "PHASE 3: Vector Databases (ChromaDB)",
                "focus_skills": ["Vector Databases", "ChromaDB"],
                "milestone": "Store and query vector embeddings efficiently.",
                "action_items": [
                    "Set up ChromaDB persistent collections.",
                    "Ingest embedded document chunks with rich metadata.",
                    "Perform fast similarity search queries."
                ]
            },
            {
                "skill": "RAG",
                "title": "PHASE 4: Retrieval-Augmented Generation (RAG)",
                "focus_skills": ["RAG", "LangChain"],
                "milestone": "Build end-to-end RAG retrieval pipeline without hallucinations.",
                "action_items": [
                    "Combine vector retrieval with LLM prompt context.",
                    "Implement source citation tracking and context verification.",
                    "Evaluate RAG retrieval accuracy and response groundness."
                ]
            },
            {
                "skill": "FastAPI",
                "title": "PHASE 5: FastAPI REST Backend Architecture",
                "focus_skills": ["FastAPI", "Python", "REST APIs"],
                "milestone": "Deploy async REST endpoints serving RAG services.",
                "action_items": [
                    "Design Pydantic request/response validation schemas.",
                    "Create asynchronous endpoint routes for model inference.",
                    "Implement error middleware and OpenAPI documentation."
                ]
            },
            {
                "skill": "Build Full AI Project",
                "title": "PHASE 6: Build Full AI Portfolio Project",
                "focus_skills": ["Full-Stack AI", "Streamlit", "Docker"],
                "milestone": f"Complete production build of '{proj_title}'.",
                "action_items": [
                    f"Implement complete feature set for '{proj_title}'.",
                    "Build interactive Streamlit frontend UI with Plotly metrics.",
                    "Write clean README, architecture diagram, and publish on GitHub."
                ]
            },
            {
                "skill": "Mock Interview",
                "title": "PHASE 7: Adaptive AI Mock Interview Prep",
                "focus_skills": ["Interview Practice", "System Design"],
                "milestone": "Achieve 85%+ score in CareerPilot AI Adaptive Mock Interviews.",
                "action_items": [
                    "Practice targeted technical interview questions on weak skills.",
                    "Review AI feedback and refine explanation of system trade-offs.",
                    "Complete candidate readiness audit."
                ]
            }
        ]

        # Filter phases relevant to missing skills or build full 7-phase roadmap
        phases = []
        phase_num = 1
        for template in standard_phases_catalog:
            phases.append({
                "phase_number": phase_num,
                "phase_title": template["title"],
                "focus_skills": template["focus_skills"],
                "milestone": template["milestone"],
                "action_items": template["action_items"]
            })
            phase_num += 1

        return {
            "target_role": target_role,
            "phases": phases,
            "total_phases": len(phases)
        }

predictive_planner = PredictivePlanner()
