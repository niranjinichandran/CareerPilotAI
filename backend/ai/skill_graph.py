import os
import json
from typing import Dict, List, Set

class SkillKnowledgeGraph:
    """Lightweight skill relationship graph mapping dependencies, categories, and related skills."""
    def __init__(self):
        self.graph: Dict[str, Dict[str, List[str]]] = {
            "Python": {
                "categories": ["Programming Language"],
                "prerequisites": [],
                "enables": ["FastAPI", "Machine Learning", "Data Analysis", "PyTorch", "TensorFlow", "Scikit-Learn"],
                "related": ["C++", "Java", "R", "Go"]
            },
            "FastAPI": {
                "categories": ["Backend Framework", "API Development"],
                "prerequisites": ["Python"],
                "enables": ["REST APIs", "Microservices", "AI Backend Deployment"],
                "related": ["Flask", "Django", "Node.js", "Express"]
            },
            "Machine Learning": {
                "categories": ["AI/ML Core"],
                "prerequisites": ["Python", "NumPy", "Pandas"],
                "enables": ["Deep Learning", "LLM", "Scikit-Learn", "PyTorch"],
                "related": ["Data Science", "Statistics", "Computer Vision", "NLP"]
            },
            "LLM": {
                "categories": ["Generative AI"],
                "prerequisites": ["Python", "Machine Learning"],
                "enables": ["Prompt Engineering", "RAG", "LangChain", "Fine-Tuning"],
                "related": ["Transformers", "HuggingFace", "Ollama", "OpenAI API"]
            },
            "Prompt Engineering": {
                "categories": ["Generative AI"],
                "prerequisites": ["LLM"],
                "enables": ["Agentic AI", "Few-Shot Learning", "RAG Optimization"],
                "related": ["LLM", "Chain-of-Thought", "LangChain"]
            },
            "RAG": {
                "categories": ["Generative AI", "Information Retrieval"],
                "prerequisites": ["LLM", "Embeddings", "Vector Database"],
                "enables": ["AI Knowledge Assistants", "Enterprise Search"],
                "related": ["LangChain", "ChromaDB", "LlamaIndex"]
            },
            "Embeddings": {
                "categories": ["NLP", "Vector Search"],
                "prerequisites": ["Python"],
                "enables": ["Vector Database", "RAG", "Semantic Search"],
                "related": ["Sentence Transformers", "Cosine Similarity"]
            },
            "Vector Database": {
                "categories": ["Database", "AI Infrastructure"],
                "prerequisites": ["Embeddings"],
                "enables": ["ChromaDB", "Pinecone", "FAISS", "RAG"],
                "related": ["SQL", "MongoDB"]
            },
            "ChromaDB": {
                "categories": ["Vector Database"],
                "prerequisites": ["Vector Database", "Python"],
                "enables": ["Local RAG", "Semantic Search Apps"],
                "related": ["Pinecone", "FAISS", "Qdrant"]
            },
            "LangChain": {
                "categories": ["AI Framework"],
                "prerequisites": ["Python", "LLM"],
                "enables": ["RAG Pipelines", "AI Agents"],
                "related": ["LlamaIndex", "Haystack", "Autogen"]
            },
            "SQL": {
                "categories": ["Database"],
                "prerequisites": [],
                "enables": ["PostgreSQL", "SQLite", "Data Analysis", "SQLAlchemy"],
                "related": ["NoSQL", "MongoDB", "Redis"]
            },
            "Docker": {
                "categories": ["DevOps", "Infrastructure"],
                "prerequisites": ["Linux"],
                "enables": ["Containerization", "Microservices", "Cloud Deployment"],
                "related": ["Kubernetes", "CI/CD"]
            }
        }

    def get_related_skills(self, skill_name: str) -> List[str]:
        node = self.graph.get(skill_name)
        if not node:
            return []
        related = set(node.get("related", []) + node.get("enables", []) + node.get("prerequisites", []))
        return list(related)

    def get_prerequisites(self, skill_name: str) -> List[str]:
        node = self.graph.get(skill_name)
        return node.get("prerequisites", []) if node else []

    def get_enabled_skills(self, skill_name: str) -> List[str]:
        node = self.graph.get(skill_name)
        return node.get("enables", []) if node else []

skill_graph = SkillKnowledgeGraph()
