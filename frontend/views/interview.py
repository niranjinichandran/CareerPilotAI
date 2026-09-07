import json
import streamlit as st
from backend.core.database import SessionLocal
from backend.models.interview import InterviewSessionModel
from ai.adaptive_interview import AdaptiveInterviewEngine

def render_interview_page():
    user = st.session_state.get("user")
    user_id = user.get("id") if user else None
    user_name = user.get("full_name", "Candidate") if user else "Candidate"
    user_role = user.get("target_role", "AI Engineer") if user else "AI Engineer"

    st.markdown(f"""
        <div class="glass-card">
            <h2>🎙️ Adaptive AI Mock Interview & Memory Engine</h2>
            <p style="color:#94a3b8;">Practice technical interview questions tailored for <b style="color:#818cf8;">{user_role}</b> that dynamically adapt based on your answer quality and technical depth.</p>
        </div>
    """, unsafe_allow_html=True)

    # Fetch interview sessions from DB for this user_id
    db = SessionLocal()
    db_history = []
    try:
        if user_id:
            records = db.query(InterviewSessionModel).filter(InterviewSessionModel.user_id == user_id).all()
            for r in records:
                try:
                    items = json.loads(r.history_json or "[]")
                    db_history.extend(items)
                except Exception:
                    pass
    except Exception:
        pass
    finally:
        db.close()

    if "interview_history" not in st.session_state:
        st.session_state["interview_history"] = db_history

    col_c1, col_c2, col_c3 = st.columns(3)
    with col_c1:
        target_role = st.text_input("Target Interview Role", value=user_role)
    with col_c2:
        difficulty = st.selectbox("Difficulty Level", ["Intermediate", "Beginner", "Advanced"])
    with col_c3:
        topics = st.multiselect("Interview Topics", ["System Architecture", "Python", "SQL", "REST APIs", "Docker", "Machine Learning", "Prompt Engineering"], default=["System Architecture", "REST APIs"])

    engine = AdaptiveInterviewEngine()

    if st.button("🏁 Start / Reset Mock Interview Session", type="secondary"):
        q = engine.start_session(target_role=target_role, difficulty=difficulty, topics=topics)
        st.session_state["curr_q"] = q
        st.success(f"New interview session started for {target_role}!")

    curr_q = st.session_state.get("curr_q")
    if not curr_q:
        curr_q = engine.start_session(target_role=target_role, difficulty=difficulty, topics=topics)
        st.session_state["curr_q"] = curr_q

    st.markdown("---")
    st.subheader(f"📌 Current Question — Topic: [{curr_q.get('topic', 'General')}] ({curr_q.get('difficulty', 'Intermediate')})")
    
    st.markdown(f"""
        <div style="background:rgba(15,23,42,0.9); border-left:4px solid #6366f1; border-radius:8px; padding:20px; font-size:18px; color:#f8fafc;">
            {curr_q.get('question', '')}
        </div>
    """, unsafe_allow_html=True)

    user_ans = st.text_area("Write your technical answer below:", height=150, placeholder="Explain technical mechanisms, architecture, data structures, trade-offs, and design choices...")

    col_b1, col_b2 = st.columns([1, 1])

    with col_b1:
        if st.button("Submit Answer for AI Evaluation 🚀", type="primary", use_container_width=True):
            if not user_ans or len(user_ans.strip()) < 5:
                st.warning("Please enter a detailed technical answer before submitting.")
            else:
                with st.spinner("AI evaluating technical depth, concept coverage, and reasoning..."):
                    eval_res = engine.evaluate_answer(
                        question_id=curr_q.get("id", "q1"),
                        user_answer=user_ans,
                        question_obj=curr_q
                    )

                    new_hist_item = {
                        "question": curr_q.get("question", ""),
                        "topic": curr_q.get("topic", "General"),
                        "user_answer": user_ans,
                        "score": eval_res["score"],
                        "feedback": eval_res["feedback"]
                    }
                    st.session_state["interview_history"].append(new_hist_item)

                    # SAVE INTERVIEW RECORD TO DB FOR CANDIDATE USER_ID
                    if user_id:
                        db_sess = SessionLocal()
                        try:
                            int_rec = InterviewSessionModel(
                                user_id=user_id,
                                target_role=target_role,
                                difficulty=difficulty,
                                topics=json.dumps(topics),
                                weak_skills_json=json.dumps(eval_res.get("missing_concepts", [])),
                                history_json=json.dumps(st.session_state["interview_history"]),
                                overall_score=eval_res["score"]
                            )
                            db_sess.add(int_rec)
                            db_sess.commit()
                        except Exception:
                            db_sess.rollback()
                        finally:
                            db_sess.close()

                    st.markdown("---")
                    st.markdown(f"### 🎯 Evaluation Score: `{eval_res['score']} / 100`")
                    st.info(f"💡 **AI Feedback:** {eval_res['feedback']}")

                    col_s1, col_s2 = st.columns(2)
                    with col_s1:
                        st.markdown("#### 💪 Key Strengths")
                        for str_item in eval_res.get("strengths", []):
                            st.markdown(f"- ✅ {str_item}")
                        st.markdown(f"**Concepts Covered:** {', '.join(eval_res.get('concepts_covered', [])) if eval_res.get('concepts_covered') else 'None'}")

                    with col_s2:
                        st.markdown("#### 🎯 Areas for Improvement")
                        for wk_item in eval_res.get("weaknesses", []):
                            st.markdown(f"- ⚠️ {wk_item}")
                        st.markdown(f"**Missing Key Concepts:** {', '.join(eval_res.get('missing_concepts', [])) if eval_res.get('missing_concepts') else 'None'}")

                    with st.expander("💡 View Ideal Sample Answer"):
                        st.write(eval_res.get("sample_ideal_answer", ""))

                    if eval_res.get("next_question"):
                        st.session_state["next_q_cache"] = eval_res["next_question"]

    with col_b2:
        if st.button("Next Adaptive Question ➡️", use_container_width=True):
            if "next_q_cache" in st.session_state:
                st.session_state["curr_q"] = st.session_state["next_q_cache"]
                del st.session_state["next_q_cache"]
            else:
                st.session_state["curr_q"] = engine.start_session(target_role=target_role, difficulty=difficulty, topics=topics)
            st.rerun()

    st.markdown("---")
    st.subheader(f"🧠 Interview Memory Log for {user_name}")
    history = st.session_state.get("interview_history", [])
    if not history:
        st.info("No questions answered yet in this session. Submit an answer above to build your memory log!")
    else:
        for idx, h in enumerate(reversed(history)):
            with st.expander(f"Question {len(history)-idx}: [{h.get('topic', 'General')}] — Score: {h.get('score', 0)}/100"):
                st.write(f"**Question:** {h.get('question', '')}")
                st.write(f"**Your Answer:** {h.get('user_answer', '')}")
                st.write(f"**AI Feedback:** {h.get('feedback', '')}")
