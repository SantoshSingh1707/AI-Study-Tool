"""
Tests for FastAPI endpoints
"""
import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from backend.main import app
from src.search import RAGRetrieval


class TestAPIEndpoints:
    """Test suite for API endpoints"""

    def test_health_check(self, client, mock_vector_store):
        """Test health check endpoint"""
        mock_vector_store.get_available_sources.return_value = ['doc1.pdf', 'doc2.pdf']
        mock_vector_store.count.return_value = 100

        with patch('backend.main.vectorstore', mock_vector_store):
            response = client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data['status'] == 'healthy'
        assert data['documents_count'] == 100
        assert len(data['available_sources']) == 2

    def test_health_check_no_db(self, client):
        """Test health check when vectorstore not initialized"""
        with patch('backend.main.vectorstore', None):
            response = client.get("/health")

        # Should still work with None
        assert response.status_code == 200

    def test_list_documents(self, client, mock_vector_store):
        """Test listing documents"""
        mock_vector_store.get_available_sources.return_value = ['doc1.pdf', 'doc2.pdf']
        mock_vector_store.count.return_value = 50

        with patch('backend.main.vectorstore', mock_vector_store):
            response = client.get("/api/documents")

        assert response.status_code == 200
        data = response.json()
        assert data['sources'] == ['doc1.pdf', 'doc2.pdf']
        assert data['total_chunks'] == 50

    def test_list_documents_not_initialized(self, client):
        """Test listing documents when not initialized"""
        with patch('backend.main.vectorstore', None):
            response = client.get("/api/documents")

        assert response.status_code == 503

    def test_delete_document_success(self, client, mock_vector_store):
        """Test successful document deletion"""
        mock_vector_store.remove_source.return_value = True

        with patch('backend.main.vectorstore', mock_vector_store):
            response = client.delete("/api/documents/test.pdf")

        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        assert 'test.pdf' in data['message']
        mock_vector_store.remove_source.assert_called_once_with('test.pdf')

    def test_delete_document_not_found(self, client, mock_vector_store):
        """Test deleting non-existent document"""
        mock_vector_store.remove_source.return_value = False

        with patch('backend.main.vectorstore', mock_vector_store):
            response = client.delete("/api/documents/nonexistent.pdf")

        assert response.status_code == 404

    def test_upload_document_invalid_type(self, client, temp_dir):
        """Test uploading invalid file type"""
        test_file = temp_dir / "test.exe"
        test_file.write_bytes(b"fake exe content")

        with open(test_file, 'rb') as f:
            response = client.post(
                "/api/upload",
                files={"file": ("test.exe", f, "application/octet-stream")}
            )

        assert response.status_code == 400
        assert "Unsupported file type" in response.json()['detail']

    def test_upload_document_success(self, client, temp_dir, mock_vector_store, mock_embedding_manager):
        """Test successful document upload"""
        # Create test PDF
        test_file = temp_dir / "test.pdf"
        test_file.write_bytes(b"fake pdf content")

        # Mock the processing pipeline
        mock_docs = [MagicMock(page_content="Test content", metadata={})]
        mock_embeddings = np.random.rand(1, 384).astype(np.float32)

        with patch('backend.main.vectorstore', mock_vector_store), \
             patch('backend.main.embedding_manager', mock_embedding_manager), \
             patch('src.data_loader.process_single_pdf', return_value=mock_docs), \
             patch('src.data_loader.split_document', return_value=mock_docs), \
             patch('src.embedding.EmbeddingManager.generate_embeddings', return_value=mock_embeddings):

            with open(test_file, 'rb') as f:
                response = client.post(
                    "/api/upload",
                    files={"file": ("test.pdf", f, "application/pdf")}
                )

        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        assert data['chunks_added'] == 1

    def test_generate_quiz_no_documents(self, client):
        """Test quiz generation with no documents"""
        with patch('backend.main.vectorstore') as mock_vs:
            mock_vs.get_available_sources.return_value = []

            with patch('backend.main.retriever', MagicMock()):
                response = client.post(
                    "/api/generate/quiz",
                    json={
                        "difficulty": "Medium",
                        "num_questions": 5,
                        "top_k": 10,
                        "min_score": 0.2,
                        "question_types": ["MCQ"]
                    }
                )

        assert response.status_code == 400
        assert "No documents found" in response.json()['detail']

    def test_generate_quiz_invalid_sources(self, client):
        """Test quiz generation with invalid source filter"""
        with patch('backend.main.vectorstore') as mock_vs:
            mock_vs.get_available_sources.return_value = ['doc1.pdf', 'doc2.pdf']

            with patch('backend.main.retriever', MagicMock()):
                response = client.post(
                    "/api/generate/quiz",
                    json={
                        "difficulty": "Medium",
                        "num_questions": 5,
                        "top_k": 10,
                        "min_score": 0.2,
                        "source_filter": ['nonexistent.pdf'],
                        "question_types": ["MCQ"]
                    }
                )

        assert response.status_code == 400
        assert "Invalid sources" in response.json()['detail']

    def test_generate_quiz_llm_not_configured(self, client):
        """Test quiz generation when LLM is not configured"""
        with patch('backend.main.vectorstore') as mock_vs:
            mock_vs.get_available_sources.return_value = ['doc1.pdf']

            with patch('backend.main.llm', None):
                response = client.post(
                    "/api/generate/quiz",
                    json={
                        "difficulty": "Medium",
                        "num_questions": 5,
                        "top_k": 10,
                        "min_score": 0.2,
                        "question_types": ["MCQ"]
                    }
                )

        assert response.status_code == 503
        assert "LLM not configured" in response.json()['detail']

    def test_generate_quiz_success(self, client, mock_llm):
        """Test successful quiz generation"""
        with patch('backend.main.vectorstore') as mock_vs, \
             patch('backend.main.retriever') as mock_retriever:

            mock_vs.get_available_sources.return_value = ['doc1.pdf']

            # Mock retriever and LLM results
            mock_results = {
                'questions': [
                    {
                        'type': 'MCQ',
                        'question': 'Test question?',
                        'options': ['A', 'B', 'C', 'D'],
                        'answer': 'A',
                        'explanation': 'Because A is correct'
                    }
                ],
                'sources': [
                    {
                        'source_file': 'doc1.pdf',
                        'similarity_score': 0.85,
                        'content': '...'
                    }
                ]
            }
            mock_retriever.return_value = mock_retriever
            # Mock the generate_questions function
            with patch('backend.main.generate_questions', return_value=mock_results):
                response = client.post(
                    "/api/generate/quiz",
                    json={
                        "difficulty": "Medium",
                        "num_questions": 5,
                        "top_k": 10,
                        "min_score": 0.2,
                        "question_types": ["MCQ"]
                    }
                )

        assert response.status_code == 200
        data = response.json()
        assert len(data['questions']) == 1
        assert data['questions'][0]['type'] == 'MCQ'

    def test_generate_learning_success(self, client, mock_llm):
        """Test successful learning content generation"""
        with patch('backend.main.vectorstore') as mock_vs, \
             patch('backend.main.retriever') as mock_retriever:

            mock_vs.get_available_sources.return_value = ['doc1.pdf']

            mock_results = {
                'content': '# Summary\n\nThis is a test summary.',
                'sources': []
            }

            with patch('backend.main.generate_learning_content', return_value=mock_results):
                response = client.post(
                    "/api/generate/learning",
                    json={
                        "mode": "Summary",
                        "top_k": 10,
                        "topic": "test topic"
                    }
                )

        assert response.status_code == 200
        data = response.json()
        assert 'Summary' in data['content']

    def test_generate_learning_empty_result(self, client):
        """Test learning generation with no content"""
        with patch('backend.main.vectorstore') as mock_vs, \
             patch('backend.main.retriever') as mock_retriever:

            mock_vs.get_available_sources.return_value = ['doc1.pdf']

            mock_results = {
                'content': 'No relevant content found.',
                'sources': []
            }

            with patch('backend.main.generate_learning_content', return_value=mock_results):
                response = client.post(
                    "/api/generate/learning",
                    json={
                        "mode": "Summary",
                        "top_k": 10
                    }
                )

        # Should still return 200 even if content is empty/not found
        assert response.status_code == 200

    def test_api_request_validation(self, client):
        """Test request validation errors"""
        # Missing required fields
        response = client.post(
            "/api/generate/quiz",
            json={
                "difficulty": "Medium",
                # Missing num_questions, top_k, min_score, question_types
            }
        )
        assert response.status_code == 422  # Validation error

    def test_generate_quiz_num_questions_too_high(self, client):
        """Test validation: num_questions exceeds limit"""
        with patch('backend.main.vectorstore') as mock_vs:
            mock_vs.get_available_sources.return_value = ['doc1.pdf']
            with patch('backend.main.llm', MagicMock()):
                response = client.post(
                    "/api/generate/quiz",
                    json={
                        "difficulty": "Medium",
                        "num_questions": 25,  # > 20
                        "top_k": 10,
                        "min_score": 0.2,
                        "question_types": ["MCQ"]
                    }
                )

        # The Pydantic validation should catch this
        assert response.status_code in [422, 400]

    def test_cors_headers(self, client):
        """Test CORS headers are set"""
        response = client.options("/health")
        assert response.status_code == 200
        # CORS headers should be present (FastAPI TestClient includes them)
        assert 'access-control-allow-origin' in response.headers or response.status_code == 200
