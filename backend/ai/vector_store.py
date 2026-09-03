import os
import json
from typing import List, Dict, Any
from backend.core.config import settings
from backend.ai.embeddings import embedding_service

class CareerVectorStore:
    def __init__(self):
        self.persist_directory = settings.VECTOR_DB_DIR
        self.client = None
        self.collection = None
        self._initialized = False

    def _ensure_init(self):
        if self._initialized:
            return
        os.makedirs(self.persist_directory, exist_ok=True)
        try:
            import chromadb
            self.client = chromadb.PersistentClient(path=self.persist_directory)
            self.collection = self.client.get_or_create_collection(name="career_knowledge_base")
            if self.collection.count() == 0:
                self.seed_knowledge_base()
            self._initialized = True
        except Exception as e:
            print(f"ChromaDB lazy init note: {e}")
            self._initialized = False

    def seed_knowledge_base(self):
        kb_path = os.path.join(settings.BASE_DIR, "datasets", "rag_kb.json")
        documents = []
        metadatas = []
        ids = []
        
        if os.path.exists(kb_path):
            with open(kb_path, "r", encoding="utf-8") as f:
                kb_data = json.load(f)
                for idx, item in enumerate(kb_data):
                    text_content = item.get("text") or item.get("content") or f"Topic: {item.get('topic')}"
                    documents.append(text_content)
                    metadatas.append({
                        "topic": item.get("topic", "General"),
                        "category": item.get("category", "Career")
                    })
                    ids.append(f"doc_{idx}")
        else:
            sample_docs = [
                ("Retrieval-Augmented Generation (RAG) combines external document retrieval with generative LLMs to eliminate hallucinations and ground answers in factual context.", "RAG Architecture", "AI/ML"),
                ("FastAPI is a high-performance Python web framework for building REST APIs with automatic OpenAPI documentation and async support.", "FastAPI", "Backend"),
                ("ChromaDB is an open-source vector database designed to store document embeddings for fast cosine similarity retrieval in AI applications.", "Vector DB", "Database"),
                ("Prompt Engineering involves designing precise instructions, role prompts, few-shot examples, and constraints to maximize LLM performance.", "Prompt Engineering", "AI/ML")
            ]
            for idx, (text, topic, cat) in enumerate(sample_docs):
                documents.append(text)
                metadatas.append({"topic": topic, "category": cat})
                ids.append(f"doc_{idx}")

        if documents and self.collection:
            embeddings = embedding_service.embed_texts(documents)
            self.collection.add(
                documents=documents,
                embeddings=embeddings,
                metadatas=metadatas,
                ids=ids
            )

    def search(self, query: str, n_results: int = 3) -> List[Dict[str, Any]]:
        self._ensure_init()
        if not self.collection or not self._initialized:
            return self._fallback_search(query)
        
        try:
            query_embedding = embedding_service.embed_query(query)
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results
            )
            retrieved = []
            if results and results.get("documents"):
                docs = results["documents"][0]
                metas = results["metadatas"][0] if results.get("metadatas") else [{}] * len(docs)
                for doc, meta in zip(docs, metas):
                    retrieved.append({
                        "text": doc,
                        "topic": meta.get("topic", "General"),
                        "category": meta.get("category", "Tech")
                    })
            return retrieved if retrieved else self._fallback_search(query)
        except Exception:
            return self._fallback_search(query)

    def _fallback_search(self, query: str) -> List[Dict[str, Any]]:
        return [
            {
                "text": "Retrieval-Augmented Generation (RAG) enhances Large Language Models by retrieving relevant factual documents from a vector database like ChromaDB before generating responses.",
                "topic": "RAG Overview",
                "category": "Generative AI"
            },
            {
                "text": "Prompt Engineering is the practice of structuring prompts to guide LLMs effectively, improving answer accuracy, consistency, and format compliance.",
                "topic": "Prompt Engineering",
                "category": "AI Practices"
            }
        ]

vector_store = CareerVectorStore()
