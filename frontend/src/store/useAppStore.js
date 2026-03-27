import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import * as api from '@/services/api';

const initialState = {
  availableSources: [],
  selectedSources: [],
  topK: 10,
  similarityThreshold: 0.2,
  numQuestions: 5,
  questionTypes: ['MCQ'],
  topicFocus: '',
  difficulty: 'Medium',
  examMode: false,
  flashcardMode: false,
  learningContent: '',
  learningMode: 'Summary',
  learningSources: [],
  quiz: {
    questions: [],
    sources: [],
    userAnswers: {},
    isSubmitted: false,
    startTime: null,
    score: 0,
    total: 0,
  },
  history: [],
  isLoading: false,
  activeTab: 'learning',
};

export const useAppStore = create(
  persist(
    (set, get) => ({
      ...initialState,

      // Document sources
      setAvailableSources: (sources) => set({ availableSources: sources }),
      setSelectedSources: (sources) => set({ selectedSources: sources }),
      toggleSource: (source) => {
        const { selectedSources } = get();
        if (selectedSources.includes(source)) {
          set({ selectedSources: selectedSources.filter((s) => s !== source) });
        } else {
          set({ selectedSources: [...selectedSources, source] });
        }
      },

      // Settings
      setTopK: (topK) => set({ topK }),
      setSimilarityThreshold: (similarityThreshold) => set({ similarityThreshold }),
      setNumQuestions: (numQuestions) => set({ numQuestions }),
      setQuestionTypes: (questionTypes) => set({ questionTypes }),
      setTopicFocus: (topicFocus) => set({ topicFocus }),
      setDifficulty: (difficulty) => set({ difficulty }),
      setExamMode: (examMode) => set({ examMode }),
      setFlashcardMode: (flashcardMode) => set({ flashcardMode }),

      // Learning
      setLearningContent: (learningContent) => set({ learningContent }),
      setLearningMode: (learningMode) => set({ learningMode }),
      setLearningSources: (learningSources) => set({ learningSources }),

      // Quiz
      setQuestions: (questions) =>
        set((state) => ({
          quiz: { ...state.quiz, questions },
        })),
      setQuizSources: (sources) =>
        set((state) => ({
          quiz: { ...state.quiz, sources },
        })),
      setUserAnswer: (questionIndex, answer) =>
        set((state) => ({
          quiz: {
            ...state.quiz,
            userAnswers: { ...state.quiz.userAnswers, [questionIndex]: answer },
          },
        })),
      submitQuiz: () => {
        const { quiz } = get();
        let score = 0;
        quiz.questions.forEach((q, idx) => {
          if (quiz.userAnswers[idx] === q.answer) {
            score++;
          }
        });
        set({
          quiz: {
            ...quiz,
            isSubmitted: true,
            score,
            total: quiz.questions.length,
          },
        });

        // Add to history
        get().addHistoryEntry({
          date: new Date().toISOString(),
          score,
          total: quiz.questions.length,
          document: get().selectedSources.join(', ') || 'All sources',
          difficulty: get().difficulty,
        });
      },
      resetQuiz: () =>
        set({
          quiz: {
            ...initialState.quiz,
            questions: get().quiz.questions,
            sources: get().quiz.sources,
          },
        }),
      startQuiz: () =>
        set((state) => ({
          quiz: {
            ...state.quiz,
            isSubmitted: false,
            startTime: Date.now(),
            userAnswers: {},
            score: 0,
            total: state.quiz.questions.length,
          },
        })),

      // History
      addHistoryEntry: (entry) =>
        set((state) => ({
          history: [{ ...entry, date: new Date().toISOString() }, ...state.history].slice(0, 50),
        })),
      clearHistory: () => set({ history: [] }),

      // UI
      setLoading: (isLoading) => set({ isLoading }),
      setActiveTab: (activeTab) => set({ activeTab }),

      // API actions
      fetchAndSetDocuments: async () => {
        try {
          const data = await api.listDocuments();
          set({ availableSources: data.sources });
        } catch (error) {
          console.error('Failed to fetch documents:', error);
        }
      },

      uploadDocument: async (file) => {
        set({ isLoading: true });
        try {
          const result = await api.uploadDocument(file);
          await get().fetchAndSetDocuments();
          return result;
        } finally {
          set({ isLoading: false });
        }
      },

      deleteDocument: async (sourceName) => {
        set({ isLoading: true });
        try {
          await api.deleteDocument(sourceName);
          await get().fetchAndSetDocuments();
          // Remove from selected sources if present
          const { selectedSources } = get();
          set({
            selectedSources: selectedSources.filter((s) => s !== sourceName),
          });
        } finally {
          set({ isLoading: false });
        }
      },

      fetchQuiz: async (request) => {
        set({ isLoading: true });
        try {
          const result = await api.generateQuiz(request);
          set({
            quiz: {
              ...initialState.quiz,
              questions: result.questions,
              sources: result.sources,
            },
          });
          get().startQuiz();
        } finally {
          set({ isLoading: false });
        }
      },

      fetchLearning: async (request) => {
        set({ isLoading: true });
        try {
          const result = await api.generateLearning(request);
          set({
            learningContent: result.content,
            learningSources: result.sources,
          });
        } finally {
          set({ isLoading: false });
        }
      },
    }),
    {
      name: 'rag-quiz-storage',
      partialize: (state) => ({
        // Only persist these fields
        history: state.history.slice(0, 10),
      }),
    }
  )
);
