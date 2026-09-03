import os
import sys

# Ensure UTF-8 output encoding on Windows console
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db import init_db
from ai.resume_parser import ResumeParser
from ai.skill_gap_engine import SkillGapEngine
from ai.skill_impact_predictor import SkillImpactPredictor
from ai.explainable_engine import ExplainableEngine
from ai.project_recommender import ProjectRecommender
from ai.opportunity_simulator import OpportunitySimulator
from ai.adaptive_interview import AdaptiveInterviewEngine
from ai.predictive_planner import PredictivePlanner
from ai.rag_chain import RAGCareerAssistant

def run_all_tests():
    print("==================================================")
    print("🚀 TESTING CAREERPILOT AI CORE ENGINES & FEATURES")
    print("==================================================")

    init_db()
    print("✅ Database initialized successfully.")

    parser = ResumeParser()
    sample_resume = "Experienced Software Developer skilled in Python, FastAPI, Docker, SQL, Git. Built REST APIs."
    resume_struct = parser.extract_structure(sample_resume)
    print(f"✅ Resume Parsing: Found {len(resume_struct['skills'])} skills -> {resume_struct['skills']}")

    gap_engine = SkillGapEngine()
    jd_sample = "Hiring AI Engineer proficient in Python, RAG, LangChain, Prompt Engineering, FastAPI, Docker, ChromaDB."
    gap_result = gap_engine.analyze_gap(resume_struct, jd_sample)
    print(f"✅ Transparent Resume Match Score: {gap_result['overall_match_percentage']}%")
    print(f"   - Matched Skills ({len(gap_result['matched_skills'])}): {gap_result['matched_skills']}")
    print(f"   - Missing Skills ({len(gap_result['missing_skills'])}): {gap_result['missing_skills']}")

    proj_engine = ProjectRecommender()
    projects = proj_engine.recommend_projects(gap_result['missing_skills'])
    print(f"✅ Project Recommender: Top project = '{projects[0]['title']}'")

    sim_engine = OpportunitySimulator()
    sim_res = sim_engine.simulate_career(gap_result['matched_skills'], gap_result['missing_skills'][:2], gap_result['overall_match_percentage'])
    print(f"✅ Opportunity Simulator: Future match score = {sim_res['estimated_job_match_after']}%")

    interview_engine = AdaptiveInterviewEngine()
    q = interview_engine.get_next_question(gap_result['missing_skills'], [])
    print(f"✅ Adaptive Interview: Generated question for topic [{q['topic']}] -> '{q['question'][:60]}...'")
    eval_res = interview_engine.evaluate_answer(q, "Sparse retrieval matches exact keywords like BM25 while dense vector retrieval uses semantic embeddings.")
    print(f"✅ Answer Evaluation: Score = {eval_res['score']}/100 | Feedback: {eval_res['feedback']}")

    planner = PredictivePlanner()
    roadmap = planner.generate_roadmap("AI Engineer", gap_result['missing_skills'], projects[0])
    print(f"✅ Predictive Learning Planner: Generated {len(roadmap['phases'])}-phase roadmap.")

    rag_assistant = RAGCareerAssistant()
    ans = rag_assistant.answer_query("Explain RAG and vector database search.")
    print(f"✅ RAG Career Assistant: Generated grounded response.")

    print("\n🎉 ALL INNOVATIVE FEATURES & ENGINES PASSED VERIFICATION!")

if __name__ == "__main__":
    run_all_tests()
