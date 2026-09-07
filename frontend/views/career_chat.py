import streamlit as st
import requests
from backend.ai.rag_pipeline import RAGPipeline

API_BASE_URL = "http://127.0.0.1:8000/api"

def render_career_chat_page():
    user = st.session_state.get("user")
    user_name = user.get("full_name", "Candidate") if user else "Candidate"
    target_role = user.get("target_role", "Custom Role") if user else "Custom Role"

    st.markdown(f"""
        <div class="glass-card">
            <h2>💬 RAG-Powered AI Career Assistant</h2>
            <p style="color:#94a3b8;">Ask technical career guidance, system design, or interview preparation questions for <b style="color:#818cf8;">{target_role}</b>. Answers are vector-retrieved from ChromaDB knowledge base with citations.</p>
        </div>
    """, unsafe_allow_html=True)

    if "chat_messages" not in st.session_state:
        st.session_state["chat_messages"] = [
            {
                "role": "assistant",
                "content": f"Hello {user_name}! I am your RAG-powered AI Career Assistant. Ask me anything about career paths, technical skills, resume optimization, architecture, or interview preparation for {target_role}!",
                "citations": []
            }
        ]

    for msg in st.session_state["chat_messages"]:
        if msg["role"] == "user":
            st.markdown(f"""
                <div style="background:rgba(99, 102, 241, 0.15); border:1px solid rgba(99, 102, 241, 0.3); border-radius:12px; padding:14px; margin-bottom:12px;">
                    <b>👤 {user_name}:</b> {msg['content']}
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div style="background:rgba(30, 41, 59, 0.7); border:1px solid rgba(255, 255, 255, 0.1); border-radius:12px; padding:16px; margin-bottom:12px;">
                    <b>🤖 CareerPilot AI Assistant:</b><br>{msg['content']}
                </div>
            """, unsafe_allow_html=True)
            if msg.get("citations"):
                st.caption("📚 **Vector DB Grounded Citations:**")
                for cite in msg["citations"]:
                    st.caption(f"- **Topic:** {cite.get('topic', 'General')} | **Category:** {cite.get('category', 'Tech')}")

    st.markdown("---")

    query_input = st.text_input("Type your career question:", value="", placeholder=f"e.g. What are the key skills needed for a {target_role} and how do I prepare?", key="career_chat_input")

    if st.button("Send Question 🚀", type="primary", use_container_width=True):
        if not query_input or len(query_input.strip()) == 0:
            st.warning("Please enter a question.")
        else:
            st.session_state["chat_messages"].append({"role": "user", "content": query_input})
            
            with st.spinner("Searching ChromaDB vector store and generating grounded answer..."):
                try:
                    res = requests.post(f"{API_BASE_URL}/chat/query", json={"query": query_input}, timeout=4)
                    data = res.json()
                    answer_text = data["answer"]
                    citations = data["citations"]
                except Exception:
                    rag = RAGPipeline()
                    res_dict = rag.query(query_input)
                    answer_text = res_dict["answer"]
                    citations = res_dict.get("citations", [])

                st.session_state["chat_messages"].append({
                    "role": "assistant",
                    "content": answer_text,
                    "citations": citations
                })
                st.rerun()
