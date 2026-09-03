from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.db import init_db
from backend.api import auth, resume, jobs, skills, recommend, simulate, interview, chat, dashboard

app = FastAPI(
    title="CareerPilot AI API",
    description="Explainable AI Career Intelligence Platform using RAG, LLMs, and Predictive Skill Analytics",
    version="1.0.0"
)

# Enable CORS for Streamlit frontend interaction
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    init_db()

# Include API Routers
app.include_router(auth.router)
app.include_router(resume.router)
app.include_router(jobs.router)
app.include_router(skills.router)
app.include_router(recommend.router)
app.include_router(simulate.router)
app.include_router(interview.router)
app.include_router(chat.router)
app.include_router(dashboard.router)

@app.get("/")
def home():
    return {
        "status": "success",
        "message": "Welcome to CareerPilot AI Platform 🚀 - Your Intelligent AI Career Mentor",
        "docs_url": "/docs"
    }

@app.get("/health")
def health():
    return {"status": "healthy", "service": "CareerPilot AI Engine"}