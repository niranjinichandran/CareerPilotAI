import re
import streamlit as st
from backend.core.database import SessionLocal
from backend.models.user import User
from backend.core.security import verify_password, get_password_hash

def validate_password(password: str) -> tuple[bool, list[str]]:
    """Validate password strength rules."""
    rules = []
    if len(password) < 8:
        rules.append("Minimum 8 characters long")
    if not re.search(r"[A-Z]", password):
        rules.append("At least one uppercase letter (A-Z)")
    if not re.search(r"[a-z]", password):
        rules.append("At least one lowercase letter (a-z)")
    if not re.search(r"[0-9]", password):
        rules.append("At least one number (0-9)")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        rules.append("At least one special character (!@#$%^&*)")
    
    return len(rules) == 0, rules

def render_auth_page():
    st.markdown("""
        <div style="text-align: center; margin-bottom: 25px;">
            <h1 style="font-size: 42px; margin-bottom: 5px;">CareerPilot <span class="gradient-text">AI</span></h1>
            <p style="font-size: 18px; color: #818cf8; font-weight: 500;">"Your Intelligent AI Career Mentor"</p>
            <p style="font-size: 14px; color: #94a3b8; max-width: 600px; margin: 0 auto;">
                Welcome! Please sign in with your registered credentials or register a new candidate account to access your career intelligence platform.
            </p>
        </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 2, 1])

    with c2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        tab_login, tab_register = st.tabs(["🔒 Sign In to Account", "📝 Register New Candidate"])

        # ------------------- LOGIN TAB -------------------
        with tab_login:
            st.markdown("### Candidate Sign In")
            login_email = st.text_input("Email Address", key="login_email", placeholder="candidate@example.com").strip().lower()
            login_password = st.text_input("Password", type="password", key="login_pass", placeholder="••••••••")
            
            if st.button("Sign In 🚀", type="primary", use_container_width=True):
                if not login_email or not login_password:
                    st.error("Please enter both email address and password.")
                else:
                    db = SessionLocal()
                    try:
                        user = db.query(User).filter(User.email == login_email).first()
                        if not user:
                            st.error("❌ Account not registered with this email ID. Please register a new account first.")
                        elif not verify_password(login_password, user.password_hash):
                            st.error("❌ Wrong password or email ID. Please check and correct your credentials.")
                        else:
                            st.session_state["user"] = {
                                "id": user.id,
                                "email": user.email,
                                "full_name": user.full_name,
                                "target_role": user.target_role or "AI Engineer"
                            }
                            # Reset profile state for newly logged-in candidate
                            st.session_state["match_data"] = None
                            st.session_state["parsed_skills"] = []
                            st.session_state["resume_skills"] = []
                            
                            st.success(f"Welcome back, {user.full_name}! Unlocking platform...")
                            st.rerun()
                    finally:
                        db.close()

        # ------------------- REGISTER TAB -------------------
        with tab_register:
            st.markdown("### Candidate Registration")
            reg_name = st.text_input("Full Name", key="reg_name", placeholder="Alex Engineer").strip()
            reg_email = st.text_input("Email Address", key="reg_email", placeholder="alex@example.com").strip().lower()
            
            # FREE TEXT INPUT FOR TARGET CAREER ROLE (ANY ROLE TYPED BY USER)
            reg_role = st.text_input(
                "Target Career Role (Type any role)",
                key="reg_role",
                placeholder="e.g. Data Scientist, Cloud Architect, Cybersecurity Engineer, Full Stack Developer..."
            ).strip()
            
            st.markdown("""
                <div style="background:rgba(15,23,42,0.6); border:1px solid rgba(99,102,241,0.3); border-radius:8px; padding:10px; font-size:12px; color:#cbd5e1; margin:10px 0;">
                    <b>🔑 Password Strength Requirements:</b><br>
                    • At least 8 characters long<br>
                    • At least 1 uppercase letter (A-Z)<br>
                    • At least 1 lowercase letter (a-z)<br>
                    • At least 1 number (0-9)<br>
                    • At least 1 special character (!@#$%^&*)
                </div>
            """, unsafe_allow_html=True)
            
            reg_password = st.text_input("Create Password", type="password", key="reg_pass", placeholder="••••••••")
            reg_confirm = st.text_input("Confirm Password", type="password", key="reg_confirm", placeholder="••••••••")

            if st.button("Create Candidate Account ✨", type="primary", use_container_width=True):
                if not reg_name or not reg_email or not reg_password:
                    st.error("Please fill in all required fields.")
                elif not reg_role:
                    st.error("Please specify your target career role.")
                elif reg_password != reg_confirm:
                    st.error("Passwords do not match. Please re-enter your password.")
                else:
                    is_valid_pw, pw_errors = validate_password(reg_password)
                    if not is_valid_pw:
                        st.error("❌ Password does not meet security requirements:\n" + "\n".join([f"• {e}" for e in pw_errors]))
                    else:
                        db = SessionLocal()
                        try:
                            existing_user = db.query(User).filter(User.email == reg_email).first()
                            if existing_user:
                                st.error("⚠️ An account with this email is already registered. Please sign in.")
                            else:
                                hashed_pwd = get_password_hash(reg_password)
                                new_user = User(
                                    email=reg_email,
                                    password_hash=hashed_pwd,
                                    full_name=reg_name,
                                    target_role=reg_role
                                )
                                db.add(new_user)
                                db.commit()
                                db.refresh(new_user)
                                st.success("✅ Account created successfully! Please sign in using your email and password.")
                        except Exception as e:
                            db.rollback()
                            st.error(f"Error creating account: {str(e)}")
                        finally:
                            db.close()

        st.markdown('</div>', unsafe_allow_html=True)
