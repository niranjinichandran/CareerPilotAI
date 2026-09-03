import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "CareerPilot AI"
    PROJECT_VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"

    # Security / Auth
    SECRET_KEY: str = os.getenv("SECRET_KEY", "careerpilot_super_secret_jwt_key_2026_prod_hash_99")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 Days

    # Database
    DB_PATH: str = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "careerpilot.db")
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{DB_PATH}")

    # Directories
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    UPLOAD_DIR: str = os.path.join(BASE_DIR, "uploads")
    VECTOR_DB_DIR: str = os.path.join(BASE_DIR, "vector_db")

    # LLM & RAG Configuration
    OLLAMA_HOST: str = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3")
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
