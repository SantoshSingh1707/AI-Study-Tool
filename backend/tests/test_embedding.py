"""
Tests for EmbeddingManager component
"""
import pytest
import numpy as np
from unittest.mock import patch, MagicMock
from src.embedding import EmbeddingManager


class TestEmbeddingManager:
    """Test suite for EmbeddingManager class"""

    def test_init_loads_model(self):
        """Test that initializing loads the model"""
        with patch('src.embedding.SentenceTransformer') as mock_st:
            mock_model = MagicMock()
            mock_st.return_value = mock_model

            with patch('torch.cuda.is_available', return_value=False):
                em = EmbeddingManager(model_name="test-model")

            mock_st.assert_called_once_with("test-model", device="cpu")
            assert em.model == mock_model

    def test_init_uses_gpu_if_available(self):
        """Test that GPU is used if available"""
        with patch('src.embedding.SentenceTransformer') as mock_st:
            mock_model = MagicMock()
            mock_st.return_value = mock_model

            with patch('torch.cuda.is_available', return_value=True):
                em = EmbeddingManager(model_name="test-model")

            mock_st.assert_called_once_with("test-model", device="cuda")

    def test_generate_embeddings_single_text(self):
        """Test generating embedding for single text"""
        with patch('src.embedding.SentenceTransformer') as mock_st:
            mock_model = MagicMock()
            mock_model.encode.return_value = np.array([[0.1, 0.2, 0.3]])
            mock_st.return_value = mock_model

            with patch('torch.cuda.is_available', return_value=False):
                em = EmbeddingManager()
                em.model = mock_model

            texts = ["Single test text"]
            embeddings = em.generate_embeddings(texts, is_query=False)

            assert embeddings.shape == (1, 3)
            # Should add passage prefix
            mock_model.encode.assert_called_once()
            call_args = mock_model.encode.call_args[0][0]
            assert call_args[0].startswith("passage:")

    def test_generate_embeddings_multiple_texts(self):
        """Test generating embeddings for multiple texts"""
        with patch('src.embedding.SentenceTransformer') as mock_st:
            mock_model = MagicMock()
            mock_model.encode.return_value = np.random.rand(3, 384).astype(np.float32)
            mock_st.return_value = mock_model

            with patch('torch.cuda.is_available', return_value=False):
                em = EmbeddingManager()
                em.model = mock_model

            texts = ["Text 1", "Text 2", "Text 3"]
            embeddings = em.generate_embeddings(texts, is_query=True)

            assert embeddings.shape == (3, 384)
            # Should add query prefix
            call_args = mock_model.encode.call_args[0][0]
            assert all(t.startswith("query:") for t in call_args)

    def test_generate_embeddings_empty_list(self):
        """Test error when empty text list provided"""
        with patch('src.embedding.SentenceTransformer') as mock_st:
            mock_model = MagicMock()
            mock_st.return_value = mock_model

            with patch('torch.cuda.is_available', return_value=False):
                em = EmbeddingManager()
                em.model = mock_model

            with pytest.raises(ValueError, match="Model not loaded"):
                em.generate_embeddings([])

    def test_prefix_added_correctly(self):
        """Test that correct prefixes are added"""
        with patch('src.embedding.SentenceTransformer') as mock_st:
            mock_model = MagicMock()
            mock_model.encode.return_value = np.random.rand(1, 384).astype(np.float32)
            mock_st.return_value = mock_model

            with patch('torch.cuda.is_available', return_value=False):
                em = EmbeddingManager()
                em.model = mock_model

                # Test query prefix
                em.generate_embeddings(["test query"], is_query=True)
                query_call = mock_model.encode.call_args[0][0][0]
                assert query_call == "query: test query"

                # Reset mock
                mock_model.encode.reset_mock()

                # Test passage prefix
                em.generate_embeddings(["test passage"], is_query=False)
                passage_call = mock_model.encode.call_args[0][0][0]
                assert passage_call == "passage: test passage"
