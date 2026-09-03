from typing import Dict, List, Any
from backend.ai.vector_store import vector_store
from backend.ai.llm import llm_client

class RAGPipeline:
    def answer_question(self, query: str, user_context: Dict[str, Any] = None) -> Dict[str, Any]:
        # Step 1: Retrieve context from ChromaDB
        retrieved = vector_store.search(query, n_results=3)
        context_str = "\n\n".join([f"[{item['topic']}]: {item['text']}" for item in retrieved])
        
        # Step 2: Extract citations
        citations = [{"topic": item["topic"], "category": item["category"]} for item in retrieved]
        
        # Step 3: Check relevance threshold
        query_words = set(query.lower().split())
        has_relevant = any(any(w in item["text"].lower() for w in query_words if len(w) > 3) for item in retrieved)
        
        # Step 4: Build prompt & query LLM
        prompt = f"""Use the following retrieved context to answer the user query accurately.
If the context does not contain sufficient information, state clearly what is known and mention that context is limited.

Retrieved Context:
{context_str}

User Query: {query}
"""
        system_prompt = "You are CareerPilot AI, an explainable career mentor. Provide precise, structured answers grounded in technical facts."
        answer = llm_client.generate(prompt, system_prompt=system_prompt)
        
        if not has_relevant:
            answer = "Note: Specific documents for this exact query were limited in our vector store, but based on core career guidelines: " + answer

        return {
            "answer": answer,
            "citations": citations,
            "retrieved_context": context_str,
            "has_relevant_context": has_relevant
        }

rag_pipeline = RAGPipeline()
