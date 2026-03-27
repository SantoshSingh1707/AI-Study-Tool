import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import clsx from 'clsx';
import {
  GitBranch,
  Play,
  Clock,
  RotateCcw,
  ChevronRight,
  CheckCircle,
  XCircle,
  HelpCircle,
} from 'lucide-react';
import { useAppStore } from '@/store/useAppStore';
import { Card, CardHeader, CardContent, CardTitle, Button, Badge, Progress, Alert } from '@/components/ui';
import { motion, AnimatePresence } from 'framer-motion';

export const Quiz = () => {
  const {
    selectedSources,
    topK,
    similarityThreshold,
    numQuestions,
    questionTypes,
    topicFocus,
    difficulty,
    examMode,
    flashcardMode,
    quiz,
    setDifficulty,
    setNumQuestions,
    setQuestionTypes,
    setTopicFocus,
    fetchQuiz,
    startQuiz,
    submitQuiz,
    resetQuiz,
  } = useAppStore();

  const [activeQuestion, setActiveQuestion] = useState(0);
  const [timeRemaining, setTimeRemaining] = useState(null);
  const [selectedAnswer, setSelectedAnswer] = useState(null);

  const {
    questions,
    isSubmitted,
    userAnswers,
    startTime,
    score,
    total,
  } = quiz;

  // Exam mode timer
  useEffect(() => {
    if (examMode && isSubmitted === false && startTime && timeRemaining === null) {
      const duration = 10 * 60 * 1000; // 10 minutes default
      setTimeRemaining(duration);

      const timer = setInterval(() => {
        setTimeRemaining((prev) => {
          if (prev && prev > 1000) {
            return prev - 1000;
          } else {
            clearInterval(timer);
            if (prev !== undefined && prev <= 0) {
              submitQuiz();
            }
            return 0;
          }
        });
      }, 1000);

      return () => clearInterval(timer);
    }
  }, [examMode, isSubmitted, startTime, timeRemaining, submitQuiz]);

  const handleStartQuiz = async () => {
    const options = {
      difficulty,
      num_questions: numQuestions,
      top_k: topK,
      min_score: similarityThreshold,
      source_filter: selectedSources.length > 0 ? selectedSources : undefined,
      topic: topicFocus || undefined,
      question_types: questionTypes,
    };

    await fetchQuiz(options);
    setActiveQuestion(0);
  };

  const handleAnswerSelect = (answer) => {
    if (isSubmitted || (examMode && !flashcardMode)) return;
    setSelectedAnswer(answer);
    useAppStore.getState().setUserAnswer(activeQuestion, answer);

    // Auto-advance after delay
    setTimeout(() => {
      if (activeQuestion < questions.length - 1) {
        setActiveQuestion((prev) => prev + 1);
        setSelectedAnswer(null);
      }
    }, 300);
  };

  const handleSubmit = () => {
    submitQuiz();
  };

  const handleReset = () => {
    resetQuiz();
    setActiveQuestion(0);
    setSelectedAnswer(null);
  };

  const formatTime = (ms) => {
    const minutes = Math.floor(ms / 60000);
    const seconds = Math.floor((ms % 60000) / 1000);
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
  };

  const generateQuiz = questions.length === 0 || isSubmitted === null;

  return (
    <div className="max-w-6xl mx-auto space-y-6 animate-fade-in">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-display font-bold text-dark-100 mb-2">
            Quiz Center
          </h1>
          <p className="text-dark-400">
            Test your knowledge with AI-generated questions
          </p>
        </div>
        {examMode && timeRemaining !== null && (
          <div className="flex items-center gap-2 px-4 py-2 bg-red-500/20 border border-red-500/30 rounded-full">
            <Clock className="w-5 h-5 text-red-400" />
            <span className="font-mono text-red-400">{formatTime(timeRemaining)}</span>
          </div>
        )}
      </div>

      {/* Configuration Panel */}
      {generateQuiz && (
        <Card className="bg-gradient-to-br from-dark-900 to-dark-800">
          <CardContent className="pt-6">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {/* Difficulty */}
              <div>
                <label className="block text-sm font-medium text-dark-300 mb-3">
                  Difficulty
                </label>
                <div className="flex gap-2">
                  {['Easy', 'Medium', 'Hard'].map((level) => (
                    <button
                      key={level}
                      onClick={() => setDifficulty(level)}
                      className={clsx(
                        'px-4 py-2 rounded-lg font-medium transition-colors',
                        difficulty === level
                          ? 'bg-primary-600 text-white'
                          : 'bg-dark-700 text-dark-300 hover:bg-dark-600'
                      )}
                    >
                      {level}
                    </button>
                  ))}
                </div>
              </div>

              {/* Question Types */}
              <div>
                <label className="block text-sm font-medium text-dark-300 mb-3">
                  Question Types
                </label>
                <div className="flex gap-2 flex-wrap">
                  {['MCQ', 'True/False'].map((type) => (
                    <button
                      key={type}
                      onClick={() => {
                        setQuestionTypes(
                          questionTypes.includes(type)
                            ? questionTypes.filter((t) => t !== type)
                            : [...questionTypes, type]
                        );
                      }}
                      className={clsx(
                        'px-4 py-2 rounded-lg font-medium transition-colors',
                        questionTypes.includes(type)
                          ? 'bg-secondary-600 text-white'
                          : 'bg-dark-700 text-dark-300 hover:bg-dark-600'
                      )}
                    >
                      {type}
                    </button>
                  ))}
                </div>
              </div>

              {/* Number of Questions */}
              <div>
                <label className="block text-sm font-medium text-dark-300 mb-3">
                  Number of Questions: {numQuestions}
                </label>
                <input
                  type="range"
                  min="1"
                  max="15"
                  value={numQuestions}
                  onChange={(e) => setNumQuestions(parseInt(e.target.value))}
                  className="w-full h-2 bg-dark-700 rounded-lg appearance-none cursor-pointer accent-primary-600"
                />
              </div>

              {/* Topic Focus */}
              <div className="lg:col-span-3">
                <label className="block text-sm font-medium text-dark-300 mb-3">
                  Topic Focus (Optional)
                </label>
                <input
                  type="text"
                  value={topicFocus}
                  onChange={(e) => setTopicFocus(e.target.value)}
                  placeholder="e.g., Internal Combustion Engine, Neural Networks..."
                  className="input max-w-xl"
                />
              </div>
            </div>

            <div className="mt-8 flex justify-center">
              <Button
                size="lg"
                onClick={handleStartQuiz}
                leftIcon={<Play className="w-5 h-5" />}
                isLoading={useAppStore.getState().isLoading}
              >
                Generate Quiz
              </Button>
            </div>

            {/* Slack Settings */}
            <div className="mt-6 pt-6 border-t border-dark-800 space-y-4">
              <h4 className="font-medium text-dark-200">Advanced Settings</h4>
              <div className="flex flex-wrap gap-6">
                <label className="flex items-center gap-3 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={examMode}
                    onChange={(e) => useAppStore.getState().setExamMode(e.target.checked)}
                    className="w-5 h-5 rounded accent-primary-600"
                  />
                  <span className="text-dark-300">Exam Mode (Timed)</span>
                </label>
                <label className="flex items-center gap-3 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={flashcardMode}
                    onChange={(e) => useAppStore.getState().setFlashcardMode(e.target.checked)}
                    className="w-5 h-5 rounded accent-primary-600"
                  />
                  <span className="text-dark-300">Flashcard Mode</span>
                </label>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Quiz Display */}
      {questions.length > 0 && isSubmitted === false && (
        <Card>
          <CardContent className="pt-6">
            {/* Progress */}
            <div className="mb-6">
              <div className="flex justify-between text-sm text-dark-400 mb-2">
                <span>Question {activeQuestion + 1} of {questions.length}</span>
                <span>
                  {Object.keys(userAnswers).length}/{questions.length} answered
                </span>
              </div>
              <Progress
                value={activeQuestion + 1}
                max={questions.length}
                size="md"
              />
            </div>

            {/* Question */}
            <AnimatePresence mode="wait">
              <motion.div
                key={activeQuestion}
                initial={{ opacity: 0, x: 50 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -50 }}
                transition={{ duration: 0.2 }}
              >
                <div className="mb-6">
                  <div className="flex items-start gap-4">
                    <Badge
                      variant={
                        questions[activeQuestion].type === 'MCQ'
                          ? 'mcq'
                          : 'truefalse'
                      }
                      className="mt-1"
                    >
                      {questions[activeQuestion].type}
                    </Badge>
                    <div className="flex-1">
                      <h3 className="text-xl font-semibold text-dark-100 mb-4">
                        {questions[activeQuestion].question}
                      </h3>

                      <div className="space-y-3">
                        {questions[activeQuestion].options.map((option, idx) => {
                          const isSelected = userAnswers[activeQuestion] === option;
                          const isCorrect = isSubmitted && option === questions[activeQuestion].answer;

                          return (
                            <button
                              key={idx}
                              onClick={() => handleAnswerSelect(option)}
                              disabled={isSubmitted || (examMode && !flashcardMode)}
                              className={clsx(
                                'w-full p-4 rounded-xl text-left transition-all border-2',
                                isSelected
                                  ? 'border-primary-500 bg-primary-600/20'
                                  : 'border-dark-700 bg-dark-800 hover:border-dark-600',
                                isSubmitted && isCorrect && 'border-green-500 bg-green-500/20',
                                isSubmitted && userAnswers[activeQuestion] !== option && isCorrect === false && 'border-red-500 bg-red-500/10'
                              )}
                            >
                              <span className="flex items-center gap-3">
                                <span className="w-8 h-8 rounded-lg bg-dark-700 flex items-center justify-center text-sm font-semibold">
                                  {String.fromCharCode(65 + idx)}
                                </span>
                                <span className="text-dark-200">{option}</span>
                                {isSelected && (
                                  <CheckCircle className="w-5 h-5 ml-auto text-primary-400" />
                                )}
                                {isSubmitted && isCorrect && (
                                  <CheckCircle className="w-5 h-5 ml-auto text-green-400" />
                                )}
                                {isSubmitted && userAnswers[activeQuestion] !== option && isCorrect === false && option === questions[activeQuestion].answer && (
                                  <CheckCircle className="w-5 h-5 ml-auto text-green-400" />
                                )}
                              </span>
                            </button>
                          );
                        })}
                      </div>
                    </div>
                  </div>
                </div>

                {/* Explanation */}
                {isSubmitted && (
                  <motion.div
                    initial={{ opacity: 0, height: 0 }}
                    animate={{ opacity: 1, height: 'auto' }}
                    className="mt-6 p-4 bg-primary-900/30 border border-primary-500/30 rounded-xl"
                  >
                    <h4 className="font-semibold text-primary-300 mb-2 flex items-center gap-2">
                      <HelpCircle className="w-5 h-5" />
                      Explanation
                    </h4>
                    <p className="text-dark-300">{questions[activeQuestion].explanation}</p>
                  </motion.div>
                )}
              </motion.div>
            </AnimatePresence>

            {/* Navigation */}
            <div className="mt-8 flex justify-between items-center">
              <Button
                variant="secondary"
                onClick={() => setActiveQuestion((prev) => Math.max(0, prev - 1))}
                disabled={activeQuestion === 0}
              >
                Previous
              </Button>

              {activeQuestion < questions.length - 1 ? (
                <Button
                  onClick={() => setActiveQuestion((prev) => prev + 1)}
                  disabled={!userAnswers[activeQuestion]}
                >
                  Next <ChevronRight className="w-4 h-4 ml-2" />
                </Button>
              ) : (
                !isSubmitted && (
                  <Button
                    onClick={handleSubmit}
                    disabled={Object.keys(userAnswers).length < questions.length}
                  >
                    Submit Quiz
                  </Button>
                )
              )}
            </div>

            {/* Quick Navigation */}
            <div className="mt-6 flex flex-wrap gap-2 justify-center">
              {questions.map((_, idx) => (
                <button
                  key={idx}
                  onClick={() => setActiveQuestion(idx)}
                  className={clsx(
                    'w-10 h-10 rounded-lg font-medium transition-colors',
                    activeQuestion === idx
                      ? 'bg-primary-600 text-white'
                      : userAnswers[idx]
                      ? 'bg-green-600/30 text-green-400 border border-green-500'
                      : 'bg-dark-700 text-dark-300 hover:bg-dark-600'
                  )}
                >
                  {idx + 1}
                </button>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Results */}
      {isSubmitted && (
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          className="space-y-6"
        >
          <Card className="bg-gradient-to-br from-primary-900/30 to-secondary-900/30 border-primary-500/30">
            <CardContent className="py-12 text-center">
              <h2 className="text-3xl font-display font-bold text-dark-100 mb-6">
                Quiz Complete!
              </h2>
              <div className="flex justify-center items-center gap-12 mb-8">
                <div>
                  <p className="text-dark-400 mb-2">Your Score</p>
                  <div className="text-6xl font-bold text-primary-400">
                    {score}/{total}
                  </div>
                  <p className="text-2xl text-dark-300 mt-2">
                    {Math.round((score / total) * 100)}%
                  </p>
                </div>
                <div className="w-px h-24 bg-dark-700" />
                <div>
                  <p className="text-dark-400 mb-2">Time Taken</p>
                  <div className="text-2xl font-semibold text-dark-100">
                    {startTime && formatTime(Date.now() - startTime)}
                  </div>
                </div>
              </div>

              <div className="flex gap-4 justify-center">
                <Button variant="secondary" onClick={handleReset} leftIcon={<RotateCcw className="w-5 h-5" />}>
                  Try Again
                </Button>
                <Link to="/learning">
                  <Button leftIcon={<HelpCircle className="w-5 h-5" />}>
                    Study More
                  </Button>
                </Link>
              </div>
            </CardContent>
          </Card>

          {/* Answer Review */}
          <Card>
            <CardHeader>
              <CardTitle>Answer Review</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {questions.map((q, idx) => (
                  <div
                    key={idx}
                    className={`p-4 rounded-lg ${
                      userAnswers[idx] === q.answer
                        ? 'bg-green-500/10 border border-green-500/30'
                        : 'bg-red-500/10 border border-red-500/30'
                    }`}
                  >
                    <div className="flex items-start gap-3">
                      {userAnswers[idx] === q.answer ? (
                        <CheckCircle className="w-5 h-5 text-green-400 mt-1 flex-shrink-0" />
                      ) : (
                        <XCircle className="w-5 h-5 text-red-400 mt-1 flex-shrink-0" />
                      )}
                      <div className="flex-1">
                        <p className="font-medium text-dark-100 mb-2">
                          Q{idx + 1}: {q.question}
                        </p>
                        <div className="text-sm space-y-1">
                          <p>
                            <span className="text-dark-400">Your answer: </span>
                            <span
                              className={
                                userAnswers[idx] === q.answer
                                  ? 'text-green-400'
                                  : 'text-red-400'
                              }
                            >
                              {userAnswers[idx] || 'No answer'}
                            </span>
                          </p>
                          {userAnswers[idx] !== q.answer && (
                            <p>
                              <span className="text-dark-400">Correct: </span>
                              <span className="text-green-400">{q.answer}</span>
                            </p>
                          )}
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </motion.div>
      )}
    </div>
  );
};
