"""
Tests for search module (RAG retrieval and generation)
"""
import pytest
from unittest.mock import MagicMock, patch
from src.search import RAGRetrieval, rag_simple, rag_enhanced, generate_questions, generate_learning_content


class TestRAGRetrieval:
    """Test suite for RAGRetrieval class"""

    def test_retrieve_no_results(self, mock_vector_store, mock_embedding_manager):
        """Test retrieve when no documents match"""
        mock_vector_store.collection.query.return_value = {
            'documents': [[]],
            'metadatas': [[]],
            'distances': [[]],
            'ids': [[]]
        }

        retriever = RAGRetrieval(mock_vector_store, mock_embedding_manager)
        mock_embedding_manager.generate_embeddings.return_value = [[0.1, 0.2, 0.3]]

        results = retriever.retrieve("test query", top_k=5)

        assert results == []

    def test_retrieve_with_results(self, mock_vector_store, mock_embedding_manager):
        """Test retrieve with matching documents"""
        mock_vector_store.collection.query.return_value = {
            'documents': [['doc1', 'doc2']],
            'metadatas': [[{'source_file': 'test.pdf'}, {'source_file': 'test2.pdf'}]],
            'distances': [[0.5, 1.0]],
            'ids': [['id1', 'id2']]
        }

        retriever = RAGRetrieval(mock_vector_store, mock_embedding_manager)
        mock_embedding_manager.generate_embeddings.return_value = [[0.1, 0.2, 0.3]]

        results = retriever.retrieve("test query", top_k=5, score_threshold=0.3)

        assert len(results) == 2
        assert results[0]['content'] == 'doc1'
        assert results[0]['metadata']['source_file'] == 'test.pdf'
        assert 'similarity_score' in results[0]
        assert results[0]['rank'] == 1

    def test_retrieve_score_threshold(self, mock_vector_store, mock_embedding_manager):
        """Test that score threshold filters correctly"""
        mock_vector_store.collection.query.return_value = {
            'documents': [['doc1', 'doc2', 'doc3']],
            'metadatas': [[{}, {}, {}]],
            'distances': [[0.3, 1.0, 1.5]],  # Scores: 1.05, 0.75, 0.5 (1.5 - dist/2)
            'ids': [['id1', 'id2', 'id3']]
        }

        retriever = RAGRetrieval(mock_vector_store, mock_embedding_manager)
        mock_embedding_manager.generate_embeddings.return_value = [[0.1, 0.2, 0.3]]

        # Only doc3 should pass (score 0.5 > 0.4)
        results = retriever.retrieve("test", top_k=3, score_threshold=0.4)

        assert len(results) == 1
        assert results[0]['content'] == 'doc3'

    def test_retrieve_source_filter(self, mock_vector_store, mock_embedding_manager):
        """Test filtering by source"""
        mock_vector_store.collection.query.return_value = {
            'documents': [['doc1']],
            'metadatas': [[{'source_file': 'filtered.pdf'}]],
            'distances': [[0.5]],
            'ids': [['id1']]
        }

        retriever = RAGRetrieval(mock_vector_store, mock_embedding_manager)
        mock_embedding_manager.generate_embeddings.return_value = [[0.1, 0.2, 0.3]]

        results = retriever.retrieve("test", source_filter=['filtered.pdf'])

        # Check that where clause was passed
        call_kwargs = mock_vector_store.collection.query.call_args[1]
        assert 'where' in call_kwargs
        assert call_kwargs['where'] == {'source_file': 'filtered.pdf'}

    def test_retrieve_source_filter_multiple(self, mock_vector_store, mock_embedding_manager):
        """Test filtering by multiple sources"""
        mock_vector_store.collection.query.return_value = {
            'documents': [['doc1']],
            'metadatas': [[{'source_file': 'doc1.pdf'}]],
            'distances': [[0.5]],
            'ids': [['id1']]
        }

        retriever = RAGRetrieval(mock_vector_store, mock_embedding_manager)
        mock_embedding_manager.generate_embeddings.return_value = [[0.1, 0.2, 0.3]]

        results = retriever.retrieve("test", source_filter=['doc1.pdf', 'doc2.pdf'])

        call_kwargs = mock_vector_store.collection.query.call_args[1]
        assert call_kwargs['where'] == {'source_file': {'$in': ['doc1.pdf', 'doc2.pdf']}}

    def test_retrieve_empty_query(self, mock_vector_store, mock_embedding_manager):
        """Test retrieve with empty query"""
        retriever = RAGRetrieval(mock_vector_store, mock_embedding_manager)
        mock_embedding_manager.generate_embeddings.return_value = [[0.1, 0.2, 0.3]]

        results = retriever.retrieve("", top_k=5)

        # Should still query with empty string
        mock_embedding_manager.generate_embeddings.assert_called_once_with([""], is_query=True)
        mock_vector_store.collection.query.assert_called_once()


class TestRAGPipelines:
    """Test suite for RAG pipeline functions"""

    def test_rag_simple_no_context(self, mock_retriever):
        """Test simple RAG with no context found"""
        mock_retriever.retrieve.return_value = []

        result = rag_simple("test query", mock_retriever, MagicMock())

        assert result == "No relevant context found"

    def test_rag_simple_with_context(self, mock_retriever, mock_llm):
        """Test simple RAG with context"""
        mock_retriever.retrieve.return_value = [
            {'content': 'Context 1'},
            {'content': 'Context 2'}
        ]
        mock_llm.invoke.return_value.content = "Test answer"

        result = rag_simple("test query", mock_retriever, mock_llm, top_k=2)

        assert result == "Test answer"
        mock_llm.invoke.assert_called_once()
        prompt = mock_llm.invoke.call_args[0][0][0]
        assert "Context 1" in prompt
        assert "Context 2" in prompt
        assert "test query" in prompt

    def test_rag_enhanced_empty(self, mock_retriever):
        """Test enhanced RAG with no results"""
        mock_retriever.retrieve.return_value = []

        result = rag_enhanced("test", mock_retriever, MagicMock())

        assert result['answer'] == 'No relevant context found'
        assert result['sources'] == []
        assert result['confidence'] == 0.0

    def test_rag_enhanced_with_sources(self, mock_retriever, mock_llm):
        """Test enhanced RAG returns sources and confidence"""
        mock_retriever.retrieve.return_value = [
            {
                'content': 'Test content',
                'metadata': {'source_file': 'test.pdf', 'page': 1},
                'similarity_score': 0.9
            }
        ]
        mock_llm.invoke.return_value.content = "Answer"

        result = rag_enhanced("test", mock_retriever, mock_llm, return_context=True)

        assert result['answer'] == 'Answer'
        assert len(result['sources']) == 1
        assert result['sources'][0]['source_file'] == 'test.pdf'
        assert result['confidence'] == 0.9
        assert 'context' in result

    def test_generate_questions_no_context(self, mock_retriever):
        """Test question generation with no context"""
        mock_retriever.retrieve.return_value = []

        result = generate_questions(
            difficulty="Medium",
            retriever=mock_retriever,
            llm=MagicMock(),
            num_questions=5
        )

        assert result['questions'] == []
        assert result['sources'] == []

    def test_generate_questions_success(self, mock_retriever, mock_llm):
        """Test successful question generation"""
        mock_retriever.retrieve.return_value = [
            {'content': 'Context about topic', 'similarity_score': 0.8}
        ]
        mock_llm.invoke.return_value.content = '''
        [
            {
                "type": "MCQ",
                "question": "What is the topic?",
                "options": ["A", "B", "C", "D"],
                "answer": "A",
                "explanation": "Because A is correct"
            }
        ]
        '''

        result = generate_questions(
            difficulty="Easy",
            retriever=mock_retriever,
            llm=mock_llm,
            num_questions=1,
            topic="test topic"
        )

        assert len(result['questions']) == 1
        assert result['questions'][0]['type'] == 'MCQ'
        assert len(result['questions'][0]['options']) == 4
        assert result['questions'][0]['answer'] in result['questions'][0]['options']

    def test_generate_questions_json_parsing(self, mock_retriever, mock_llm):
        """Test JSON parsing from LLM response"""
        mock_retriever.retrieve.return_value = [
            {'content': 'Context', 'similarity_score': 0.8}
        ]
        mock_llm.invoke.return_value.content = '''
        ```json
        [
            {
                "type": "True/False",
                "question": "Is this true?",
                "options": ["True", "False"],
                "answer": "True",
                "explanation": "It is true"
            }
        ]
        ```
        '''

        result = generate_questions(
            difficulty="Hard",
            retriever=mock_retriever,
            llm=mock_llm
        )

        assert result['questions'][0]['type'] == 'True/False'
        assert result['questions'][0]['options'] == ['True', 'False']

    def test_generate_questions_invalid_json(self, mock_retriever, mock_llm):
        """Test handling of invalid JSON from LLM"""
        mock_retriever.retrieve.return_value = [
            {'content': 'Context', 'similarity_score': 0.8}
        ]
        mock_llm.invoke.return_value.content = "Not valid JSON at all"

        result = generate_questions(
            difficulty="Medium",
            retriever=mock_retriever,
            llm=mock_llm
        )

        # Should return empty questions on parse error
        assert result['questions'] == []

    def test_generate_learning_content_success(self, mock_retriever, mock_llm):
        """Test learning content generation"""
        mock_retriever.retrieve.return_value = [
            {'content': 'Document content', 'similarity_score': 0.7}
        ]
        mock_llm.invoke.return_value.content = "# Summary\n\nThis is a summary of the document."

        result = generate_learning_content(
            mode="Summary",
            retriever=mock_retriever,
            llm=mock_llm,
            topic="specific topic"
        )

        assert "# Summary" in result
        mock_llm.invoke.assert_called_once()
        prompt = mock_llm.invoke.call_args[0][0][0]
        assert "specific topic" in prompt

    def test_generate_learning_content_key_notes(self, mock_retriever, mock_llm):
        """Test key notes generation"""
        mock_retriever.retrieve.return_value = [
            {'content': 'Document content', 'similarity_score': 0.7}
        ]
        mock_llm.invoke.return_value.content = "- Important point 1\n- Important point 2"

        result = generate_learning_content(
            mode="Key Notes",
            retriever=mock_retriever,
            llm=mock_llm
        )

        assert "Important point" in result

    def test_generate_learning_content_no_context(self, mock_retriever, mock_llm):
        """Test learning content with no context"""
        mock_retriever.retrieve.return_value = []

        result = generate_learning_content(
            mode="Summary",
            retriever=mock_retriever,
            llm=mock_llm
        )

        assert "No relevant content" in result
