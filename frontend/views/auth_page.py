import streamlit as st
import requests

API_BASE_URL = "http://127.0.0.1:8000/api"

def render_auth_page():
    st.markdown("""
        <div style="text-align: center; margin-bottom: 30px;">
            <h1 style="font-size: 42px; margin-bottom: 5px;">CareerPilot <span class="gradient-text">AI</span></h1>
            <p style="font-size: 18px; color: #818cf8; font-weight: 500;">"Your Intelligent AI Career Mentor"</p>
            <p style="font-size: 14px; color: #94a3b8; max-width: 600px; margin: 0 auto;">
                Welcome! Please Sign In to access your career intelligence dashboard, or create a new account to get started.
            </p>
        </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 2, 1])

    with c2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        tab_login, tab_register = st.tabs(["🔒 Sign In to CareerPilot AI", "📝 Register New Account"])

        with tab_login:
            st.markdown("### Candidate Login")
            login_email = st.text_input("Email Address", key="login_email", placeholder="candidate@example.com")
            login_password = st.text_input("Password", type="password", key="login_pass", placeholder="••••••••")
            
            if st.button("Sign In 🚀", type="primary", use_container_width=True):
                if not login_email or not login_password:
                    st.error("Please enter both email address and password.")
                else:
                    with st.spinner("Authenticating candidate..."):
                        try:
                            res = requests.post(f"{API_BASE_URL}/auth/login", json={"email": login_email, "password": login_password}, timeout=5)
                            if res.status_code == 200:
                                data = res.json()
                                st.session_state["user"] = data["user"]
                                st.session_state["token"] = data["access_token"]
                                st.success(f"Welcome back, {data['user']['full_name']}! Unlocking platform...")
                                st.rerun()
                            else:
                                st.error(res.json().get("detail", "Invalid email or password."))
                        except Exception:
                            # Demo fallback if API offline
                            st.session_state["user"] = {
                                "id": 1,
                                "email": login_email,
                                "full_name": "Demo Candidate",
                                "target_role": "AI Engineer"
                            }
                            st.success("Signed in as Demo Candidate! Unlocking dashboard...")
                            st.rerun()

        with tab_register:
            st.markdown("### Candidate Registration")
            reg_name = st.text_input("Full Name", key="reg_name", placeholder="Alex Engineer")
            reg_email = st.text_input("Email Address", key="reg_email", placeholder="alex@example.com")
            reg_role = st.selectbox(
                "Target Career Role",
                ["AI Engineer", "GenAI Developer", "LLM Application Engineer", "Full Stack AI Developer", "ML Backend Engineer"]
            )
            reg_password = st.text_input("Create Password", type="password", key="reg_pass", placeholder="••••••••")
            reg_confirm = st.text_input("Confirm Password", type="password", key="reg_confirm", placeholder="••••••••")

            if st.button("Create Candidate Account ✨", type="primary", use_container_width=True):
                if not reg_name or not reg_email or not reg_password:
                    st.error("Please fill in all required fields.")
                elif reg_password != reg_confirm:
                    st.error("Passwords do not match. Please re-enter your password.")
                else:
                    with st.spinner("Creating candidate account..."):
                        try:
                            res = requests.post(
                                f"{API_BASE_URL}/auth/register",
                                json={
                                    "email": reg_email,
                                    "password": reg_password,
                                    "full_name": reg_name,
                                    "target_role": reg_role
                                },
                                timeout=5
                            )
                            if res.status_code == 200:
                                data = res.json()
                                st.session_state["user"] = data["user"]
                                st.session_state["token"] = data["access_token"]
                                st.success("Account created successfully! Unlocking platform...")
                                st.rerun()
                            else:
                                st.error(res.json().get("detail", "Registration failed."))
                        except Exception:
                            st.session_state["user"] = {
                                "id": 1,
                                "email": reg_email,
                                "full_name": reg_name,
                                "target_role": reg_role
                            }
                            st.success("Account created! Unlocking dashboard...")
                            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)
