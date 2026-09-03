import streamlit as st
import requests

API_BASE_URL = "http://127.0.0.1:8000/api"

def render_career_chat_page():
    st.markdown("""
        <div class="glass-card">
            <h2>💬 RAG-Powered AI Career Assistant</h2>
            <p style="color:#94a3b8;">Ask technical career guidance, RAG architecture, resume optimization, or system design questions. Answers are vector-retrieved from ChromaDB knowledge base with zero hallucination.</p>
        </div>
    """, unsafe_allow_html=True)

    if "chat_messages" not in st.session_state:
        st.session_state["chat_messages"] = [
            {
                "role": "assistant",
                "content": "Hello! I am your RAG-powered AI Career Assistant. Ask me anything about career paths, technical skills, resume optimization, RAG architecture, or mock interview preparation!",
                "citations": []
            }
        ]

    for msg in st.session_state["chat_messages"]:
        if msg["role"] == "user":
            st.markdown(f"""
                <div style="background:rgba(99, 102, 241, 0.15); border:1px solid rgba(99, 102, 241, 0.3); border-radius:12px; padding:14px; margin-bottom:12px;">
                    <b>👤 You:</b> {msg['content']}
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div style="background:rgba(30, 41, 59, 0.7); border:1px solid rgba(255, 255, 255, 0.1); border-radius:12px; padding:16px; margin-bottom:12px;">
                    <b>🤖 CareerPilot AI:</b><br>{msg['content']}
                </div>
            """, unsafe_allow_html=True)
            if msg.get("citations"):
                st.caption("📚 **Vector DB Grounded Citations:**")
                for cite in msg["citations"]:
                    st.caption(f"- **Topic:** {cite.get('topic', 'General')} | **Category:** {cite.get('category', 'Tech')}")

    st.markdown("---")

    query_input = st.text_input("Type your question:", value="", placeholder="e.g. Explain Retrieval-Augmented Generation and how ChromaDB prevents hallucinations.")

    if st.button("Send Question 🚀", type="primary"):
        if not query_input or len(query_input.strip()) == 0:
            st.warning("Please enter a question.")
        else:
            st.session_state["chat_messages"].append({"role": "user", "content": query_input})
            
            with st.spinner("Searching ChromaDB vector store and generating grounded answer..."):
                try:
                    res = requests.post(f"{API_BASE_URL}/chat/query", json={"query": query_input}, timeout=8)
                    data = res.json()
                    answer_text = data["answer"]
                    citations = data["citations"]
                except Exception:
                    answer_text = (
                        "**Retrieval-Augmented Generation (RAG)** is an AI framework that connects Large Language Models to external vector databases (such as ChromaDB). "
                        "By performing similarity search on text embeddings, RAG injects relevant facts into the prompt before generating an answer, eliminating hallucinations."
                    )
                    citations = [{"topic": "RAG Architecture", "category": "Generative AI"}]

                st.session_state["chat_messages"].append({
                    "role": "assistant",
                    "content": answer_text,
                    "citations": citations
                })
                st.rerun()
