"""
Tests for VectorStore component
"""
import pytest
import numpy as np
from unittest.mock import MagicMock, patch
from src.vector_store import VectorStore


class TestVectorStore:
    """Test suite for VectorStore class"""

    def test_initialize_store(self, mock_vector_store):
        """Test vector store initialization"""
        with patch('src.vector_store.chromadb.PersistentClient') as mock_client:
            mock_client.return_value.get_or_create_collection.return_value = mock_vector_store

            vs = VectorStore(collection_name="test", persist_directory="/tmp/test")

            assert vs.collection_name == "test"
            assert vs.persist_directory == "/tmp/test"
            assert vs.collection is not None

    def test_get_available_sources_empty(self, mock_vector_store):
        """Test getting sources from empty store"""
        mock_vector_store.get.return_value = {'metadatas': []}

        vs = VectorStore()
        vs.collection = mock_vector_store

        sources = vs.get_available_sources()
        assert sources == []

    def test_get_available_sources_with_data(self, mock_vector_store):
        """Test getting sources with documents"""
        mock_vector_store.get.return_value = {
            'metadatas': [
                {'source_file': 'doc1.pdf'},
                {'source_file': 'doc2.pdf'},
                {'source_file': 'doc1.pdf'},  # Duplicate
                {'source_file': 'doc3.pdf'},
            ]
        }

        vs = VectorStore()
        vs.collection = mock_vector_store

        sources = vs.get_available_sources()
        assert len(sources) == 3
        assert 'doc1.pdf' in sources
        assert 'doc2.pdf' in sources
        assert 'doc3.pdf' in sources

    def test_remove_source_success(self, mock_vector_store):
        """Test successful document removal"""
        mock_vector_store.delete.return_value = None

        vs = VectorStore()
        vs.collection = mock_vector_store

        result = vs.remove_source("test.pdf")
        assert result is True
        mock_vector_store.delete.assert_called_once_with(where={"source_file": "test.pdf"})

    def test_remove_source_failure(self, mock_vector_store):
        """Test document removal failure"""
        mock_vector_store.delete.side_effect = Exception("Not found")

        vs = VectorStore()
        vs.collection = mock_vector_store

        result = vs.remove_source("nonexistent.pdf")
        assert result is False

    def test_add_documents_empty(self, mock_vector_store):
        """Test adding empty document list"""
        vs = VectorStore()
        vs.collection = mock_vector_store

        vs.add_documents([], np.array([]))
        mock_vector_store.add.assert_not_called()

    def test_add_documents_mismatch_length(self, mock_vector_store):
        """Test error when documents and embeddings count mismatch"""
        vs = VectorStore()
        vs.collection = mock_vector_store

        docs = [MagicMock(page_content="test", metadata={})]
        embeddings = np.random.rand(2, 384)  # 2 embeddings for 1 doc

        with pytest.raises(ValueError, match="Number of documents must match"):
            vs.add_documents(docs, embeddings)

    def test_add_documents_with_deduplication(self, mock_vector_store, sample_documents, sample_embeddings):
        """Test that duplicates are skipped"""
        vs = VectorStore()
        vs.collection = mock_vector_store

        # Mock existing hash
        mock_vector_store.get.return_value = {
            'metadatas': [
                {'content_hash': 'abc123'}  # Simulate existing document
            ]
        }

        # Mock collection count
        mock_vector_store.count.return_value = 10

        vs.add_documents(sample_documents, sample_embeddings)

        # Should skip adding if all are duplicates
        mock_vector_store.add.assert_not_called()

    def test_add_documents_batch_processing(self, mock_vector_store, sample_documents, sample_embeddings):
        """Test batch processing of documents"""
        vs = VectorStore()
        vs.collection = mock_vector_store
        mock_vector_store.count.return_value = 0

        # No existing documents
        mock_vector_store.get.return_value = {'metadatas': []}

        vs.add_documents(sample_documents, sample_embeddings)

        # Should call add once (all docs fit in one batch)
        mock_vector_store.add.assert_called_once()

        call_args = mock_vector_store.add.call_args
        assert len(call_args[1]['ids']) == 3
        assert len(call_args[1]['embeddings']) == 3
        assert len(call_args[1]['documents']) == 3
        assert len(call_args[1]['metadatas']) == 3

        # Check metadata includes content_hash
        for metadata in call_args[1]['metadatas']:
            assert 'content_hash' in metadata
            assert len(metadata['content_hash']) == 16

    def test_add_documents_large_batch(self, mock_vector_store):
        """Test batch processing with many documents (>5000)"""
        vs = VectorStore()
        vs.collection = mock_vector_store
        mock_vector_store.count.return_value = 0
        mock_vector_store.get.return_value = {'metadatas': []}

        # Create 6000 documents
        docs = [
            MagicMock(page_content=f"Doc {i}", metadata={"source": f"doc{i}.pdf"})
            for i in range(6000)
        ]
        embeddings = np.random.rand(6000, 384).astype(np.float32)

        vs.add_documents(docs, embeddings)

        # Should call add twice (5000 + 1000)
        assert mock_vector_store.add.call_count == 2
