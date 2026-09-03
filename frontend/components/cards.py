import streamlit as st

def inject_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0b0f19 0%, #111827 50%, #0f172a 100%);
        color: #f8fafc;
    }
    
    /* Modern Glassmorphic Cards */
    .glass-card {
        background: rgba(30, 41, 59, 0.65);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 10px 30px 0 rgba(0, 0, 0, 0.3);
    }
    
    .hero-container {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.2) 0%, rgba(168, 85, 247, 0.2) 50%, rgba(236, 72, 153, 0.15) 100%);
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 20px;
        padding: 40px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.4);
    }
    
    /* Gradient Headers */
    .gradient-text {
        background: linear-gradient(135deg, #818cf8 0%, #c084fc 50%, #f472b6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
    }

    /* Metric Cards */
    .metric-box {
        background: rgba(15, 23, 42, 0.8);
        border: 1px solid rgba(99, 102, 241, 0.25);
        border-radius: 14px;
        padding: 20px;
        text-align: center;
        transition: all 0.3s ease;
    }
    .metric-box:hover {
        border-color: #818cf8;
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.25);
    }
    
    .metric-value {
        font-size: 32px;
        font-weight: 700;
        color: #6366f1;
        margin-top: 5px;
    }
    
    .metric-label {
        font-size: 14px;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* Badges */
    .badge-matched {
        display: inline-block;
        background: rgba(16, 185, 129, 0.15);
        color: #34d399;
        border: 1px solid rgba(16, 185, 129, 0.4);
        padding: 5px 14px;
        border-radius: 20px;
        margin: 4px;
        font-size: 13px;
        font-weight: 600;
    }

    .badge-missing {
        display: inline-block;
        background: rgba(244, 63, 94, 0.15);
        color: #fb7185;
        border: 1px solid rgba(244, 63, 94, 0.4);
        padding: 5px 14px;
        border-radius: 20px;
        margin: 4px;
        font-size: 13px;
        font-weight: 600;
    }

    .badge-priority-high {
        display: inline-block;
        background: rgba(239, 68, 68, 0.2);
        color: #f87171;
        border: 1px solid #ef4444;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 700;
    }

    .badge-priority-medium {
        display: inline-block;
        background: rgba(245, 158, 11, 0.2);
        color: #fbbf24;
        border: 1px solid #f59e0b;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 700;
    }

    .explanation-callout {
        background: rgba(15, 23, 42, 0.85);
        border-left: 4px solid #a855f7;
        padding: 16px;
        border-radius: 8px;
        margin: 12px 0;
    }
    </style>
    """, unsafe_allow_html=True)

def render_metric_card(title: str, value: str, delta: str = None):
    delta_html = f"<div style='color:#34d399; font-size:13px; font-weight:600;'>{delta}</div>" if delta else ""
    st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">{title}</div>
            <div class="metric-value">{value}</div>
            {delta_html}
        </div>
    """, unsafe_allow_html=True)

def render_hero_section():
    st.markdown("""
        <div class="hero-container">
            <h1 style="font-size: 46px; margin-bottom: 10px;">CareerPilot <span class="gradient-text">AI</span></h1>
            <p style="font-size: 20px; color: #cbd5e1; max-width: 750px; margin: 0 auto 24px auto;">
                "Your Intelligent AI Career Mentor"
            </p>
            <p style="font-size: 15px; color: #94a3b8; max-width: 800px; margin: 0 auto;">
                An Explainable AI Career Intelligence Platform utilizing Large Language Models, Retrieval-Augmented Generation (RAG), and Predictive Analytics to guide your candidate readiness.
            </p>
        </div>
    """, unsafe_allow_html=True)
