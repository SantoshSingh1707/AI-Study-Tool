"""
Pytest fixtures and configuration for backend tests
"""
import os
import sys
import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import MagicMock, patch
import numpy as np

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import Settings


@pytest.fixture(scope="session")
def settings():
    """Test settings with temporary directories"""
    with tempfile.TemporaryDirectory() as tmpdir:
        settings = Settings()
        settings.DATA_DIR = Path(tmpdir) / "data"
        settings.VECTOR_STORE_DIR = settings.DATA_DIR / "vector_store"
        settings.UPLOAD_DIR = settings.DATA_DIR / "uploads"
        os.makedirs(settings.DATA_DIR, exist_ok=True)
        os.makedirs(settings.VECTOR_STORE_DIR, exist_ok=True)
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
        yield settings


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files"""
    tmpdir = tempfile.mkdtemp()
    yield Path(tmpdir)
    shutil.rmtree(tmpdir)


@pytest.fixture
def sample_pdf_path(temp_dir):
    """Create a mock PDF file path (doesn't create actual file)"""
    return temp_dir / "test_document.pdf"


@pytest.fixture
def sample_txt_path(temp_dir):
    """Create a mock TXT file path"""
    return temp_dir / "test_document.txt"


@pytest.fixture(scope="function")
def mock_vector_store():
    """Mock vector store for testing"""
    with patch('src.vector_store.chromadb.PersistentClient') as mock_client:
        mock_collection = MagicMock()
        mock_collection.count.return_value = 0
        mock_client.return_value.get_or_create_collection.return_value = mock_collection
        yield mock_collection


@pytest.fixture(scope="function")
def mock_embedding_manager():
    """Mock embedding manager"""
    with patch('src.embedding.SentenceTransformer') as mock_model:
        mock_model.return_value.encode.return_value = np.random.rand(1, 384).astype(np.float32)
        yield mock_model


@pytest.fixture
def sample_document():
    """Create a sample Document object for testing"""
    from langchain_core.documents import Document
    return Document(
        page_content="This is a test document content.",
        metadata={"source_file": "test.pdf", "page": 1}
    )


@pytest.fixture
def sample_documents():
    """Create multiple sample Document objects"""
    from langchain_core.documents import Document
    return [
        Document(
            page_content=f"Test document {i}",
            metadata={"source_file": f"test_{i}.pdf", "page": i}
        )
        for i in range(3)
    ]


@pytest.fixture
def sample_embeddings():
    """Create sample embeddings array"""
    return np.random.rand(3, 384).astype(np.float32)


@pytest.fixture
def mock_llm():
    """Mock LLM for testing"""
    with patch('langchain_mistralai.ChatMistralAI') as mock:
        mock_instance = MagicMock()
        mock_instance.invoke.return_value.content = "Test response"
        mock.return_value = mock_instance
        yield mock


@pytest.fixture(scope="function")
def client(settings):
    """Create FastAPI test client"""
    from fastapi.testclient import TestClient
    from backend.main import app

    # Override settings for testing
    with patch('backend.main.vectorstore', None), \
         patch('backend.main.embedding_manager', None), \
         patch('backend.main.retriever', None), \
         patch('backend.main.llm', None):
        yield TestClient(app)


class MockResponse:
    """Mock HTTP response for testing"""
    def __init__(self, json_data, status_code=200):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data
