"""
Configuration settings for the backend
"""
import os
from pathlib import Path

class Settings:
    # Project paths
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / "data"
    VECTOR_STORE_DIR = DATA_DIR / "vector_store"
    UPLOAD_DIR = DATA_DIR / "uploads"

    # API settings
    API_TITLE = "RAG Question Generator API"
    API_VERSION = "1.0.0"
    API_DESCRIPTION = "Backend API for AI-powered study tool"

    # CORS
    CORS_ORIGINS = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:5174",
    ]

    # RAG settings
    DEFAULT_TOP_K = 10
    DEFAULT_MIN_SCORE = 0.2
    DEFAULT_NUM_QUESTIONS = 5
    MAX_QUESTIONS = 20
    MAX_TOPIC_LENGTH = 200

    # File upload
    ALLOWED_EXTENSIONS = {".pdf", ".txt", ".docx", ".pptx"}
    MAX_UPLOAD_SIZE = 50 * 1024 * 1024  # 50MB

    # Embedding model
    EMBEDDING_MODEL = "multi-qa-MiniLM-L6-cos-v1"

    # LLM
    LLM_MODEL = "mistral-small-2506"
    LLM_TEMPERATURE = 0.7

settings = Settings()

# Ensure directories exist
os.makedirs(settings.DATA_DIR, exist_ok=True)
os.makedirs(settings.VECTOR_STORE_DIR, exist_ok=True)
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
