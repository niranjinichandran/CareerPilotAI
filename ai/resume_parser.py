import os
import re
import json
from typing import Dict, List, Any

try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None

try:
    import docx
except ImportError:
    docx = None

class ResumeParser:
    def __init__(self):
        # Load skills taxonomy database
        skills_db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "datasets", "skills_db.json")
        self.all_known_skills = []
        if os.path.exists(skills_db_path):
            with open(skills_db_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                for cat, skills in data.get("categories", {}).items():
                    self.all_known_skills.extend(skills)
        else:
            self.all_known_skills = [
                "Python", "FastAPI", "Streamlit", "LangChain", "RAG", "Prompt Engineering",
                "ChromaDB", "LLM", "Docker", "SQL", "PyTorch", "TensorFlow", "React",
                "JavaScript", "TypeScript", "Scikit-Learn", "Pandas", "NumPy", "Git",
                "System Design", "Microservices", "REST APIs", "C++", "Java", "Linux"
            ]
        # Remove duplicates preserving order
        seen = set()
        self.all_known_skills = [s for s in self.all_known_skills if not (s.lower() in seen or seen.add(s.lower()))]

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        if fitz is None:
            raise RuntimeError("PyMuPDF (fitz) is not installed.")
        text = ""
        with fitz.open(pdf_path) as doc:
            for page in doc:
                text += page.get_text() + "\n"
        return text

    def extract_text_from_docx(self, docx_path: str) -> str:
        if docx is None:
            raise RuntimeError("python-docx is not installed.")
        doc = docx.Document(docx_path)
        return "\n".join([p.text for p in doc.paragraphs])

    def parse_file(self, file_path: str) -> str:
        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".pdf":
            return self.extract_text_from_pdf(file_path)
        elif ext in [".docx", ".doc"]:
            return self.extract_text_from_docx(file_path)
        else:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()

    def extract_skills(self, text: str) -> List[str]:
        found_skills = []
        text_lower = text.lower()
        for skill in self.all_known_skills:
            # Word boundary regex for accurate matching
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            if re.search(pattern, text_lower):
                found_skills.append(skill)
        return found_skills

    def extract_projects(self, text: str) -> List[Dict[str, Any]]:
        # Structural project detection using line heuristics
        projects = []
        lines = text.split("\n")
        in_project_section = False
        current_project = None

        for line in lines:
            line_str = line.strip()
            if not line_str:
                continue
            if any(h in line_str.lower() for h in ["projects", "personal projects", "academic projects"]):
                in_project_section = True
                continue
            if in_project_section and any(h in line_str.lower() for h in ["experience", "education", "skills", "certifications"]):
                in_project_section = False
                break

            if in_project_section:
                if len(line_str) < 60 and not line_str.startswith("-") and not line_str.startswith("•"):
                    if current_project:
                        projects.append(current_project)
                    current_project = {"title": line_str, "description": "", "skills": self.extract_skills(line_str)}
                elif current_project:
                    current_project["description"] += " " + line_str
                    proj_skills = self.extract_skills(line_str)
                    for s in proj_skills:
                        if s not in current_project["skills"]:
                            current_project["skills"].append(s)

        if current_project:
            projects.append(current_project)

        # Fallback if no specific project heading was found
        if not projects:
            skills = self.extract_skills(text)
            if skills:
                projects.append({
                    "title": "Full-Stack / AI Application",
                    "description": text[:200] + "...",
                    "skills": skills[:4]
                })

        return projects

    def extract_structure(self, text: str) -> Dict[str, Any]:
        skills = self.extract_skills(text)
        projects = self.extract_projects(text)
        
        # Check education & certifications indicators
        text_lower = text.lower()
        has_education = any(word in text_lower for word in ["bachelor", "master", "b.tech", "b.e", "m.tech", "degree", "university", "college", "gpa"])
        has_certifications = any(word in text_lower for word in ["certified", "certification", "coursera", "udemy", "aws certified", "deeplearning.ai", "license"])
        
        # Estimate experience level
        exp_years = 0
        exp_matches = re.findall(r'(\d+)\+?\s*years?\s*(?:of)?\s*experience', text_lower)
        if exp_matches:
            exp_years = max([int(x) for x in exp_matches])
        elif any(word in text_lower for word in ["intern", "student", "fresh graduate", "fresher"]):
            exp_years = 0.5
        else:
            exp_years = 1.5

        return {
            "skills": skills,
            "projects": projects,
            "has_education": has_education,
            "has_certifications": has_certifications,
            "experience_years": exp_years,
            "raw_text": text
        }
