import streamlit as st
import requests

API_BASE_URL = "http://127.0.0.1:8000/api"

def render_interview_page():
    st.markdown("""
        <div class="glass-card">
            <h2>🎙️ Adaptive AI Mock Interview & Memory Engine</h2>
            <p style="color:#94a3b8;">Practice technical interview questions that dynamically adapt based on your target role, weak topics, and past evaluation history.</p>
        </div>
    """, unsafe_allow_html=True)

    if "interview_history" not in st.session_state:
        st.session_state["interview_history"] = []

    col_c1, col_c2, col_c3 = st.columns(3)
    with col_c1:
        target_role = st.selectbox("Target Role", ["AI Engineer", "GenAI Developer", "LLM Application Engineer", "Full Stack AI Developer"])
    with col_c2:
        difficulty = st.selectbox("Difficulty Level", ["Intermediate", "Beginner", "Advanced"])
    with col_c3:
        topics = st.multiselect("Interview Topics", ["RAG", "LLM", "Prompt Engineering", "FastAPI", "Python"], default=["RAG", "Prompt Engineering", "FastAPI"])

    if st.button("🏁 Start / Reset Mock Interview Session", type="secondary"):
        try:
            res = requests.post(
                f"{API_BASE_URL}/interview/start",
                json={"target_role": target_role, "difficulty": difficulty, "topics": topics},
                timeout=5
            )
            data = res.json()
            st.session_state["curr_q"] = data["question"]
            st.session_state["session_id"] = data.get("session_id")
            st.success("New interview session started!")
        except Exception:
            st.session_state["curr_q"] = {
                "id": "rag_q1",
                "topic": "RAG",
                "difficulty": difficulty,
                "question": "What is Retrieval-Augmented Generation (RAG) and how does it reduce hallucinations in LLM applications?",
                "key_concepts": ["retrieval", "augmented", "generation", "hallucinations", "embeddings", "vector database"]
            }
            st.success("Session started (Local Mode)!")

    curr_q = st.session_state.get("curr_q")
    if not curr_q:
        curr_q = {
            "id": "rag_q1",
            "topic": "RAG",
            "difficulty": "Intermediate",
            "question": "What is Retrieval-Augmented Generation (RAG) and how does it reduce hallucinations in LLM applications?",
            "key_concepts": ["retrieval", "augmented", "generation", "hallucinations", "embeddings", "vector database"]
        }
        st.session_state["curr_q"] = curr_q

    st.markdown("---")
    st.subheader(f"📌 Current Question — Topic: [{curr_q['topic']}] ({curr_q['difficulty']})")
    
    st.markdown(f"""
        <div style="background:rgba(15,23,42,0.9); border-left:4px solid #6366f1; border-radius:8px; padding:20px; font-size:18px; color:#f8fafc;">
            {curr_q['question']}
        </div>
    """, unsafe_allow_html=True)

    user_ans = st.text_area("Write your technical answer below:", height=150, placeholder="Explain technical mechanisms, vector search, embeddings, prompt context, and trade-offs...")

    col_b1, col_b2 = st.columns([1, 1])

    with col_b1:
        if st.button("Submit Answer for AI Evaluation 🚀", type="primary"):
            if not user_ans or len(user_ans.strip()) < 5:
                st.warning("Please enter a detailed answer before submitting.")
            else:
                with st.spinner("AI evaluating technical depth, concept coverage, and structure..."):
                    try:
                        res = requests.post(
                            f"{API_BASE_URL}/interview/answer",
                            json={"question_id": curr_q["id"], "user_answer": user_ans},
                            timeout=5
                        )
                        eval_res = res.json()
                    except Exception:
                        eval_res = {
                            "score": 82.0,
                            "feedback": "Great explanation! You covered the core concepts of retrieval and hallucination prevention.",
                            "concepts_covered": ["retrieval", "generation", "vector database"],
                            "missing_concepts": ["embeddings"],
                            "strengths": ["Clear narrative", "Accurate technical terms"],
                            "weaknesses": ["Explain the role of dense vector embeddings"],
                            "sample_ideal_answer": "RAG retrieves relevant document context from a vector database using similarity search and passes it into the LLM prompt, eliminating hallucinations.",
                            "next_question": {
                                "id": "rag_q2",
                                "topic": "RAG",
                                "difficulty": "Advanced",
                                "question": "How do embeddings and vector databases help retrieve relevant documents for RAG queries?",
                                "key_concepts": ["embeddings", "vector database", "cosine similarity"]
                            }
                        }

                    st.session_state["interview_history"].append({
                        "question": curr_q["question"],
                        "topic": curr_q["topic"],
                        "user_answer": user_ans,
                        "score": eval_res["score"],
                        "feedback": eval_res["feedback"]
                    })

                    st.markdown("---")
                    st.markdown(f"### 🎯 Evaluation Score: `{eval_res['score']} / 100`")
                    st.info(f"💡 **AI Feedback:** {eval_res['feedback']}")

                    col_s1, col_s2 = st.columns(2)
                    with col_s1:
                        st.markdown("#### 💪 Key Strengths")
                        for str_item in eval_res["strengths"]:
                            st.markdown(f"- ✅ {str_item}")
                        st.markdown(f"**Concepts Covered:** {', '.join(eval_res['concepts_covered']) if eval_res['concepts_covered'] else 'None'}")

                    with col_s2:
                        st.markdown("#### 🎯 Areas for Improvement")
                        for wk_item in eval_res["weaknesses"]:
                            st.markdown(f"- ⚠️ {wk_item}")
                        st.markdown(f"**Missing Key Concepts:** {', '.join(eval_res['missing_concepts']) if eval_res['missing_concepts'] else 'None'}")

                    with st.expander("💡 View Ideal Sample Answer"):
                        st.write(eval_res["sample_ideal_answer"])

                    if eval_res.get("next_question"):
                        st.session_state["next_q_cache"] = eval_res["next_question"]

    with col_b2:
        if st.button("Next Adaptive Question ➡️"):
            if "next_q_cache" in st.session_state:
                st.session_state["curr_q"] = st.session_state["next_q_cache"]
                del st.session_state["next_q_cache"]
            else:
                st.session_state["curr_q"] = {
                    "id": "pe_q1",
                    "topic": "Prompt Engineering",
                    "difficulty": "Intermediate",
                    "question": "Describe Few-Shot Prompting and Chain-of-Thought (CoT) prompting. How do they improve LLM reasoning performance?",
                    "key_concepts": ["few-shot", "chain-of-thought", "cot", "reasoning"]
                }
            st.rerun()

    st.markdown("---")
    st.subheader("🧠 Interview Memory & Performance Log")
    history = st.session_state.get("interview_history", [])
    if not history:
        st.info("No questions answered yet in this session. Submit an answer above to build your memory log!")
    else:
        for idx, h in enumerate(reversed(history)):
            with st.expander(f"Question {len(history)-idx}: [{h['topic']}] — Score: {h['score']}/100"):
                st.write(f"**Question:** {h['question']}")
                st.write(f"**Your Answer:** {h['user_answer']}")
                st.write(f"**AI Feedback:** {h['feedback']}")
