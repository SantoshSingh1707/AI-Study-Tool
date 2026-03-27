import { describe, it, expect, beforeEach, vi } from 'vitest';
import { useAppStore } from '@/store/useAppStore';

// Mock API
vi.mock('@/services/api', () => ({
  listDocuments: vi.fn(),
  uploadDocument: vi.fn(),
  deleteDocument: vi.fn(),
  generateQuiz: vi.fn(),
  generateLearning: vi.fn(),
}));

describe('useAppStore', () => {
  beforeEach(() => {
    // Reset store state before each test
    useAppStore.getState().resetQuiz();
    useAppStore.getState().clearHistory();
    useAppStore.getState().setLoading(false);
    useAppStore.getState().setActiveTab('learning');
    useAppStore.getState().setAvailableSources([]);
    useAppStore.getState().setSelectedSources([]);
    useAppStore.getState().setTopK(10);
    useAppStore.getState().setSimilarityThreshold(0.2);
    useAppStore.getState().setNumQuestions(5);
    useAppStore.getState().setQuestionTypes(['MCQ']);
    useAppStore.getState().setTopicFocus('');
    useAppStore.getState().setDifficulty('Medium');
    useAppStore.getState().setExamMode(false);
    useAppStore.getState().setFlashcardMode(false);
    useAppStore.getState().setLearningContent('');
    useAppStore.getState().setLearningMode('Summary');
    useAppStore.getState().setLearningSources([]);
    useAppStore.getState().setQuestions([]);
    useAppStore.getState().setQuizSources([]);
  });

  describe('Document Sources', () => {
    it('sets available sources', () => {
      const { setAvailableSources } = useAppStore.getState();
      setAvailableSources(['doc1.pdf', 'doc2.pdf']);

      expect(useAppStore.getState().availableSources).toEqual(['doc1.pdf', 'doc2.pdf']);
    });

    it('sets selected sources', () => {
      const { setSelectedSources } = useAppStore.getState();
      setSelectedSources(['doc1.pdf']);

      expect(useAppStore.getState().selectedSources).toEqual(['doc1.pdf']);
    });

    it('toggles source selection', () => {
      const { toggleSource, setAvailableSources } = useAppStore.getState();

      setAvailableSources(['doc1.pdf', 'doc2.pdf']);
      toggleSource('doc1.pdf');

      expect(useAppStore.getState().selectedSources).toContain('doc1.pdf');

      toggleSource('doc1.pdf');
      expect(useAppStore.getState().selectedSources).not.toContain('doc1.pdf');
    });
  });

  describe('Settings', () => {
    it('updates topK', () => {
      const { setTopK } = useAppStore.getState();
      setTopK(20);
      expect(useAppStore.getState().topK).toBe(20);
    });

    it('updates similarityThreshold', () => {
      const { setSimilarityThreshold } = useAppStore.getState();
      setSimilarityThreshold(0.5);
      expect(useAppStore.getState().similarityThreshold).toBe(0.5);
    });

    it('updates numQuestions', () => {
      const { setNumQuestions } = useAppStore.getState();
      setNumQuestions(10);
      expect(useAppStore.getState().numQuestions).toBe(10);
    });

    it('updates questionTypes', () => {
      const { setQuestionTypes } = useAppStore.getState();
      setQuestionTypes(['MCQ', 'True/False']);
      expect(useAppStore.getState().questionTypes).toEqual(['MCQ', 'True/False']);
    });

    it('updates topicFocus', () => {
      const { setTopicFocus } = useAppStore.getState();
      setTopicFocus('Neural Networks');
      expect(useAppStore.getState().topicFocus).toBe('Neural Networks');
    });

    it('updates difficulty', () => {
      const { setDifficulty } = useAppStore.getState();
      setDifficulty('Hard');
      expect(useAppStore.getState().difficulty).toBe('Hard');
    });

    it('toggles examMode', () => {
      const { setExamMode } = useAppStore.getState();
      setExamMode(true);
      expect(useAppStore.getState().examMode).toBe(true);
    });

    it('toggles flashcardMode', () => {
      const { setFlashcardMode } = useAppStore.getState();
      setFlashcardMode(true);
      expect(useAppStore.getState().flashcardMode).toBe(true);
    });
  });

  describe('Quiz Management', () => {
    const mockQuestions = [
      {
        type: 'MCQ',
        question: 'Test question 1?',
        options: ['A', 'B', 'C', 'D'],
        answer: 'A',
        explanation: 'Because A',
      },
      {
        type: 'True/False',
        question: 'Test question 2?',
        options: ['True', 'False'],
        answer: 'True',
        explanation: 'It is true',
      },
    ];

    it('sets quiz questions', () => {
      const { setQuestions } = useAppStore.getState();
      setQuestions(mockQuestions);

      expect(useAppStore.getState().quiz.questions).toEqual(mockQuestions);
    });

    it('records user answers', () => {
      const { setQuestions, setUserAnswer } = useAppStore.getState();

      setQuestions(mockQuestions);
      setUserAnswer(0, 'A');
      setUserAnswer(1, 'True');

      expect(useAppStore.getState().quiz.userAnswers[0]).toBe('A');
      expect(useAppStore.getState().quiz.userAnswers[1]).toBe('True');
    });

    it('submits quiz and calculates score', () => {
      const { setQuestions, setUserAnswer, submitQuiz } = useAppStore.getState();

      setQuestions(mockQuestions);
      setUserAnswer(0, 'A'); // Correct
      setUserAnswer(1, 'False'); // Incorrect (should be True)
      submitQuiz();

      const quiz = useAppStore.getState().quiz;
      expect(quiz.isSubmitted).toBe(true);
      expect(quiz.score).toBe(1); // Only first correct
      expect(quiz.total).toBe(2);
    });

    it('resets quiz but keeps questions', () => {
      const { setQuestions, setUserAnswer, resetQuiz } = useAppStore.getState();

      setQuestions(mockQuestions);
      setUserAnswer(0, 'A');
      resetQuiz();

      const quiz = useAppStore.getState().quiz;
      expect(quiz.userAnswers).toEqual({});
      expect(quiz.isSubmitted).toBe(false);
      expect(quiz.questions).toEqual(mockQuestions); // Questions remain
    });

    it('starts quiz with current time', () => {
      const { setQuestions, startQuiz } = useAppStore.getState();

      setQuestions(mockQuestions);
      startQuiz();

      const quiz = useAppStore.getState().quiz;
      expect(quiz.isSubmitted).toBe(false);
      expect(quiz.startTime).toBeInstanceOf(Number);
      expect(quiz.userAnswers).toEqual({});
    });
  });

  describe('History Tracking', () => {
    it('adds history entry', () => {
      const { addHistoryEntry } = useAppStore.getState();

      addHistoryEntry({
        date: '2024-01-15T10:30:00.000Z',
        score: 8,
        total: 10,
        document: 'test.pdf',
        difficulty: 'Medium',
      });

      const history = useAppStore.getState().history;
      expect(history.length).toBe(1);
      expect(history[0].score).toBe(8);
      expect(history[0].total).toBe(10);
    });

    it('limits history to 50 entries', () => {
      const { addHistoryEntry } = useAppStore.getState();

      // Add 51 entries
      for (let i = 0; i < 51; i++) {
        addHistoryEntry({
          date: `2024-01-${(i % 28) + 1}T10:30:00.000Z`,
          score: i,
          total: 10,
          document: `doc${i}.pdf`,
          difficulty: 'Medium',
        });
      }

      expect(useAppStore.getState().history.length).toBe(50);
    });

    it('clears history', () => {
      const { addHistoryEntry, clearHistory } = useAppStore.getState();

      addHistoryEntry({
        date: '2024-01-15T10:30:00.000Z',
        score: 5,
        total: 10,
        document: 'test.pdf',
        difficulty: 'Easy',
      });

      clearHistory();
      expect(useAppStore.getState().history).toEqual([]);
    });
  });

  describe('Learning Content', () => {
    it('sets learning content', () => {
      const { setLearningContent } = useAppStore.getState();
      const content = '# Test Summary\n\nThis is test content.';

      setLearningContent(content);
      expect(useAppStore.getState().learningContent).toBe(content);
    });

    it('sets learning mode', () => {
      const { setLearningMode } = useAppStore.getState();
      setLearningMode('Key Notes');
      expect(useAppStore.getState().learningMode).toBe('Key Notes');
    });
  });

  describe('UI State', () => {
    it('sets loading state', () => {
      const { setLoading } = useAppStore.getState();
      setLoading(true);
      expect(useAppStore.getState().isLoading).toBe(true);
    });

    it('sets active tab', () => {
      const { setActiveTab } = useAppStore.getState();
      setActiveTab('quiz');
      expect(useAppStore.getState().activeTab).toBe('quiz');
    });
  });
});
