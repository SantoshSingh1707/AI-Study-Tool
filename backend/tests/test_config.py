"""
Tests for configuration module
"""
import pytest
from pathlib import Path
from config import Settings


class TestSettings:
    """Test suite for Settings class"""

    def test_settings_creation(self):
        """Test that settings can be instantiated"""
        settings = Settings()
        assert settings is not None

    def test_default_values(self):
        """Test default configuration values"""
        settings = Settings()
        assert settings.DEFAULT_TOP_K == 10
        assert settings.DEFAULT_MIN_SCORE == 0.2
        assert settings.DEFAULT_NUM_QUESTIONS == 5
        assert settings.MAX_QUESTIONS == 20
        assert settings.MAX_TOPIC_LENGTH == 200

    def test_allowed_extensions(self):
        """Test file extension whitelist"""
        settings = Settings()
        allowed = settings.ALLOWED_EXTENSIONS
        assert '.pdf' in allowed
        assert '.txt' in allowed
        assert '.docx' in allowed
        assert '.pptx' in allowed
        assert '.exe' not in allowed

    def test_max_upload_size(self):
        """Test max upload size is 50MB"""
        settings = Settings()
        assert settings.MAX_UPLOAD_SIZE == 50 * 1024 * 1024

    def test_embedding_model(self):
        """Test embedding model name"""
        settings = Settings()
        assert settings.EMBEDDING_MODEL == "multi-qa-MiniLM-L6-cos-v1"

    def test_llm_settings(self):
        """Test LLM configuration"""
        settings = Settings()
        assert settings.LLM_MODEL == "mistral-small-2506"
        assert settings.LLM_TEMPERATURE == 0.7

    def test_cors_origins(self):
        """Test CORS configuration includes localhost"""
        settings = Settings()
        assert "http://localhost:3000" in settings.CORS_ORIGINS
        assert "http://localhost:5173" in settings.CORS_ORIGINS
