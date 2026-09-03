import random
from typing import Dict, List, Any

class AdaptiveInterviewEngine:
    def __init__(self):
        self.question_bank = {
            "RAG": [
                {
                    "id": "rag_q1",
                    "topic": "RAG",
                    "difficulty": "Intermediate",
                    "question": "What is Retrieval-Augmented Generation (RAG) and how does it reduce hallucinations in LLM applications?",
                    "key_concepts": ["retrieval", "augmented", "generation", "hallucinations", "embeddings", "vector database", "context"],
                    "sample_ideal_answer": "Retrieval-Augmented Generation (RAG) retrieves relevant document context from a vector database using similarity search and passes it into the LLM prompt. This grounds the LLM response in external factual data, eliminating hallucinations and enabling real-time knowledge integration without model fine-tuning."
                },
                {
                    "id": "rag_q2",
                    "topic": "RAG",
                    "difficulty": "Advanced",
                    "question": "How do embeddings and vector databases help retrieve relevant documents for RAG queries?",
                    "key_concepts": ["embeddings", "vector database", "cosine similarity", "dense retrieval", "semantic search"],
                    "sample_ideal_answer": "Embeddings transform unstructured text into dense vector representations where semantic similarity corresponds to vector proximity. Vector databases index these vectors to execute sub-second cosine or k-NN similarity searches across millions of chunks."
                }
            ],
            "LLM": [
                {
                    "id": "llm_q1",
                    "topic": "LLM",
                    "difficulty": "Intermediate",
                    "question": "What are the core differences between LLM Fine-Tuning and In-Context Learning (RAG/Prompting)?",
                    "key_concepts": ["fine-tuning", "in-context learning", "weights", "prompting", "latency", "cost"],
                    "sample_ideal_answer": "Fine-tuning updates model weights using domain-specific dataset gradients for specialized style/format, while In-Context Learning injects context dynamically into the prompt window without weight modification."
                }
            ],
            "Prompt Engineering": [
                {
                    "id": "pe_q1",
                    "topic": "Prompt Engineering",
                    "difficulty": "Intermediate",
                    "question": "Describe Few-Shot Prompting and Chain-of-Thought (CoT) prompting. How do they improve LLM reasoning performance?",
                    "key_concepts": ["few-shot", "chain-of-thought", "cot", "reasoning", "examples", "step-by-step"],
                    "sample_ideal_answer": "Few-Shot prompting provides exemplar input-output pairs in the prompt. Chain-of-Thought instructs the LLM to write out step-by-step reasoning before outputting the final answer, significantly reducing logical errors."
                }
            ],
            "FastAPI": [
                {
                    "id": "fa_q1",
                    "topic": "FastAPI",
                    "difficulty": "Intermediate",
                    "question": "How does FastAPI achieve high performance with Python async/await, and how does Pydantic fit into request validation?",
                    "key_concepts": ["async", "await", "starlette", "pydantic", "schema", "validation", "uvicorn"],
                    "sample_ideal_answer": "FastAPI utilizes Starlette's ASGI event loop for non-blocking asynchronous request handling. Pydantic handles automatic request data serialization, schema validation, and interactive documentation generation."
                }
            ],
            "Python": [
                {
                    "id": "py_q1",
                    "topic": "Python",
                    "difficulty": "Intermediate",
                    "question": "Explain Python GIL (Global Interpreter Lock) and how it affects multi-threading vs multi-processing.",
                    "key_concepts": ["gil", "global interpreter lock", "multithreading", "multiprocessing", "cpu-bound", "io-bound"],
                    "sample_ideal_answer": "The GIL ensures only one thread executes Python bytecode at a time. CPU-bound tasks require multiprocessing to utilize multiple CPU cores, while I/O-bound tasks benefit from multithreading or async I/O."
                }
            ]
        }

    def get_next_question(self, weak_topics: List[str], history: List[Dict[str, Any]]) -> Dict[str, Any]:
        asked_ids = set([h.get("question_id") for h in history])

        # Adaptive logic: Check if user scored low on recent questions
        recent_weak_topics = []
        for h in reversed(history[-3:]):
            if h.get("score", 100) < 70:
                recent_weak_topics.append(h.get("topic", ""))

        target_topics = recent_weak_topics + weak_topics
        for topic in target_topics:
            if topic in self.question_bank:
                available = [q for q in self.question_bank[topic] if q["id"] not in asked_ids]
                if available:
                    return random.choice(available)

        # Pick any unasked question
        all_questions = []
        for topic, q_list in self.question_bank.items():
            all_questions.extend(q_list)
        available = [q for q in all_questions if q["id"] not in asked_ids]
        if available:
            return random.choice(available)

        return {
            "id": "gen_fallback",
            "topic": "System Design & AI Architecture",
            "difficulty": "Intermediate",
            "question": "How would you design a scalable microservices architecture for serving RAG and LLM models under high concurrent traffic?",
            "key_concepts": ["load balancer", "caching", "async queue", "vector db", "fastapi"],
            "sample_ideal_answer": "Use a load balancer (Nginx), FastAPI async workers, Redis caching for frequent vector queries, and an asynchronous queue (Celery/RabbitMQ) for long-running LLM generation tasks."
        }

    def evaluate_answer(self, question: Dict[str, Any], user_answer: str) -> Dict[str, Any]:
        key_concepts = question.get("key_concepts", [])
        if not user_answer or len(user_answer.strip()) < 10:
            return {
                "score": 35.0,
                "feedback": "Answer is too short. Be sure to explain technical concepts, vector database mechanisms, and architectural trade-offs.",
                "concepts_covered": [],
                "missing_concepts": key_concepts,
                "strengths": ["Submitted answer for evaluation"],
                "weaknesses": ["Answer lacked technical depth and essential terminology"],
                "sample_ideal_answer": question.get("sample_ideal_answer", "")
            }

        answer_lower = user_answer.lower()
        covered = [c for c in key_concepts if c.lower() in answer_lower]
        missing = [c for c in key_concepts if c.lower() not in answer_lower]

        coverage_ratio = len(covered) / len(key_concepts) if key_concepts else 0.7
        base_score = (coverage_ratio * 70.0) + min(20.0, (len(user_answer) / 250.0) * 20.0) + 10.0
        final_score = round(min(98.0, max(40.0, base_score)), 1)

        strengths = []
        weaknesses = []

        if covered:
            strengths.append(f"Good explanation of {', '.join(covered[:3])}.")
        if missing:
            weaknesses.append(f"Explain the role of {', '.join(missing[:3])}.")
        if len(user_answer) > 200:
            strengths.append("Provided detailed narrative structure.")

        if final_score >= 80:
            feedback = f"Great response! You covered key concepts clearly."
        elif final_score >= 65:
            feedback = f"Good effort. Incorporate missing topics like {', '.join(missing[:2]) if missing else 'system trade-offs'} to boost score."
        else:
            feedback = f"Needs improvement. Focus on explaining how {key_concepts[0] if key_concepts else 'the concept'} operates under the hood."

        return {
            "score": final_score,
            "feedback": feedback,
            "concepts_covered": covered,
            "missing_concepts": missing,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "sample_ideal_answer": question.get("sample_ideal_answer", "")
        }

adaptive_interview_engine = AdaptiveInterviewEngine()
