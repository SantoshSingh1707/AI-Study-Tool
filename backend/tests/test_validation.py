"""
Tests for input validation logic
"""
import pytest
from pydantic import ValidationError


class TestInputValidation:
    """Test Pydantic model validation"""

    def test_quiz_request_valid(self):
        """Test valid quiz request"""
        from backend.main import QuizRequest

        request = QuizRequest(
            difficulty="Medium",
            num_questions=5,
            top_k=10,
            min_score=0.2,
            question_types=["MCQ"]
        )
        assert request.difficulty == "Medium"
        assert request.num_questions == 5

    def test_quiz_request_invalid_difficulty(self):
        """Test invalid difficulty value"""
        from backend.main import QuizRequest

        with pytest.raises(ValidationError):
            QuizRequest(
                difficulty="Invalid",
                num_questions=5,
                top_k=10,
                min_score=0.2,
                question_types=["MCQ"]
            )

    def test_quiz_request_too_many_questions(self):
        """Test num_questions exceeds max"""
        from backend.main import QuizRequest

        with pytest.raises(ValidationError):
            QuizRequest(
                difficulty="Easy",
                num_questions=25,  # > 20
                top_k=10,
                min_score=0.2,
                question_types=["MCQ"]
            )

    def test_quiz_request_invalid_score_range(self):
        """Test min_score outside 0-1"""
        from backend.main import QuizRequest

        with pytest.raises(ValidationError):
            QuizRequest(
                difficulty="Hard",
                num_questions=5,
                top_k=10,
                min_score=1.5,  # > 1.0
                question_types=["MCQ"]
            )

    def test_learning_request_valid(self):
        """Test valid learning request"""
        from backend.main import LearningRequest

        request = LearningRequest(
            mode="Summary",
            top_k=20,
            topic="test topic"
        )
        assert request.mode == "Summary"
        assert request.topic == "test topic"

    def test_learning_request_invalid_mode(self):
        """Test invalid learning mode"""
        from backend.main import LearningRequest

        with pytest.raises(ValidationError):
            LearningRequest(
                mode="InvalidMode",
                top_k=10
            )

    def test_source_info_model(self):
        """Test SourceInfo model"""
        from backend.main import SourceInfo

        source = SourceInfo(
            source_file="test.pdf",
            similarity_score=0.85,
            page=1,
            content="test content"
        )
        assert source.source_file == "test.pdf"
        assert source.similarity_score == 0.85

    def test_question_model(self):
        """Test Question model"""
        from backend.main import Question

        question = Question(
            type="MCQ",
            question="What is 2+2?",
            options=["3", "4", "5", "6"],
            answer="4",
            explanation="Because 2+2=4"
        )
        assert question.type == "MCQ"
        assert len(question.options) == 4
        assert question.answer in question.options

    def test_health_response_model(self):
        """Test HealthResponse model"""
        from backend.main import HealthResponse

        health = HealthResponse(
            status="healthy",
            documents_count=100,
            available_sources=["doc1.pdf", "doc2.pdf"]
        )
        assert health.status == "healthy"
        assert health.documents_count == 100
        assert len(health.available_sources) == 2
