import plotly.express as px
import plotly.graph_objects as go

def create_skill_radar_chart(matched_skills: list, missing_skills: list):
    categories = ["Required Skills", "Project Alignment", "Experience Fit", "Certifications", "Education"]
    matched_score = min(100, max(20, len(matched_skills) * 18))
    missing_penalty = max(20, 100 - len(missing_skills) * 15)
    
    values = [matched_score, max(45, matched_score - 10), min(90, matched_score + 15), 70, 90]
    target_values = [100, 100, 100, 100, 100]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Current Candidate Profile',
        fillcolor='rgba(99, 102, 241, 0.3)',
        line=dict(color='#6366f1', width=2)
    ))
    fig.add_trace(go.Scatterpolar(
        r=target_values,
        theta=categories,
        fill='toself',
        name='Target Job Benchmark',
        fillcolor='rgba(236, 72, 153, 0.1)',
        line=dict(color='#ec4899', width=1, dash='dash')
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], tickfont=dict(color="#94a3b8"), gridcolor="rgba(255,255,255,0.1)"),
            angularaxis=dict(tickfont=dict(color="#f8fafc", size=12), gridcolor="rgba(255,255,255,0.1)")
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        legend=dict(font=dict(color="#f8fafc")),
        margin=dict(l=40, r=40, t=20, b=20)
    )
    return fig

def create_skill_gap_bar_chart(matched_skills: list, missing_skills: list):
    df = {
        "Skill Category": ["Matched Skills", "Missing Required", "Related Skills"],
        "Count": [len(matched_skills), len(missing_skills), 3],
        "Color": ["#10b981", "#f43f5e", "#818cf8"]
    }
    fig = px.bar(
        df, x="Skill Category", y="Count", color="Skill Category",
        color_discrete_sequence=["#10b981", "#f43f5e", "#818cf8"],
        text="Count"
    )
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="#f8fafc"),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.1)")
    )
    return fig

def create_interview_score_trend_chart(history: list):
    if not history:
        scores = [65, 72, 78, 85, 90]
        attempts = ["Q1", "Q2", "Q3", "Q4", "Q5"]
    else:
        scores = [h.get("score", 70) for h in history]
        attempts = [f"Q{i+1}" for i in range(len(history))]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=attempts, y=scores, mode='lines+markers',
        line=dict(color='#a855f7', width=3),
        marker=dict(size=10, color='#c084fc')
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="#f8fafc"),
        yaxis=dict(range=[0, 100], gridcolor="rgba(255,255,255,0.1)"),
        xaxis=dict(gridcolor="rgba(255,255,255,0.1)")
    )
    return fig
