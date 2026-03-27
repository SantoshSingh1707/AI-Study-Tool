import React from 'react';
import { Link } from 'react-router-dom';
import clsx from 'clsx';
import {
  FileText,
  GitBranch,
  BookOpen,
  ArrowRight,
  Upload,
  Zap,
  Shield,
  BarChart3,
} from 'lucide-react';
import { useAppStore } from '@/store/useAppStore';
import { Card, CardHeader, CardContent, CardTitle, Button, Badge, Progress } from '@/components/ui';

export const Home = () => {
  const {
    availableSources,
    history,
    topK,
    numQuestions,
    fetchAndSetDocuments,
    setActiveTab,
  } = useAppStore();

  React.useEffect(() => {
    fetchAndSetDocuments();
  }, [fetchAndSetDocuments]);

  const avgScore =
    history.length > 0
      ? Math.round(
          history.reduce((acc, h) => acc + (h.score / h.total) * 100, 0) /
            history.length
        )
      : null;

  return (
    <div className="max-w-6xl mx-auto space-y-8 animate-fade-in">
      {/* Hero Section */}
      <div className="text-center space-y-4 py-12">
        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary-600/20 text-primary-400 text-sm font-medium mb-4">
          <Zap className="w-4 h-4" />
          AI-Powered Learning
        </div>
        <h1 className="text-5xl font-display font-bold text-dark-100">
          Study Smarter with{' '}
          <span className="bg-gradient-to-r from-primary-400 to-secondary-400 bg-clip-text text-transparent">
            RAG
          </span>
        </h1>
        <p className="text-xl text-dark-400 max-w-2xl mx-auto">
          Transform your documents into interactive quizzes, summaries, and key notes.
          Upload your PDFs and let AI create the perfect study experience.
        </p>

        <div className="flex gap-4 justify-center pt-4">
          <Link to="/upload">
            <Button size="lg" leftIcon={<Upload className="w-5 h-5" />}>
              Upload Document
            </Button>
          </Link>
          <Link to="/quiz">
            <Button size="lg" variant="secondary" rightIcon={<ArrowRight className="w-5 h-5" />}>
              Start Quizzing
            </Button>
          </Link>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card padding="md" hover>
          <CardContent>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-dark-400 text-sm">Documents</p>
                <p className="text-3xl font-bold text-dark-100">{availableSources.length}</p>
              </div>
              <div className="w-12 h-12 rounded-xl bg-primary-600/20 flex items-center justify-center">
                <FileText className="w-6 h-6 text-primary-400" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card padding="md" hover>
          <CardContent>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-dark-400 text-sm">Quiz Questions</p>
                <p className="text-3xl font-bold text-dark-100">{numQuestions}</p>
              </div>
              <div className="w-12 h-12 rounded-xl bg-secondary-600/20 flex items-center justify-center">
                <GitBranch className="w-6 h-6 text-secondary-400" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card padding="md" hover>
          <CardContent>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-dark-400 text-sm">Top K Context</p>
                <p className="text-3xl font-bold text-dark-100">{topK}</p>
              </div>
              <div className="w-12 h-12 rounded-xl bg-purple-600/20 flex items-center justify-center">
                <Zap className="w-6 h-6 text-purple-400" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card padding="md" hover>
          <CardContent>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-dark-400 text-sm">Avg Score</p>
                <p className="text-3xl font-bold text-dark-100">{avgScore ?? '--'}%</p>
              </div>
              <div className="w-12 h-12 rounded-xl bg-yellow-600/20 flex items-center justify-center">
                <BarChart3 className="w-6 h-6 text-yellow-400" />
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card hover className="group cursor-pointer" onClick={() => setActiveTab('quiz')}>
          <CardContent className="pt-6">
            <div className="flex items-start justify-between">
              <div className="space-y-3">
                <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-primary-500 to-primary-700 flex items-center justify-center shadow-lg group-hover:shadow-glow transition-shadow">
                  <GitBranch className="w-7 h-7 text-white" />
                </div>
                <div>
                  <CardTitle>Generate Quiz</CardTitle>
                  <p className="text-dark-400 mt-2">
                    Create multiple choice and true/false questions from your documents.
                    Configurable difficulty and topic focus.
                  </p>
                </div>
                <div className="flex gap-2 pt-2">
                  <Badge variant="mcq">MCQ</Badge>
                  <Badge variant="truefalse">True/False</Badge>
                </div>
              </div>
              <ArrowRight className="w-6 h-6 text-primary-400 group-hover:translate-x-1 transition-transform" />
            </div>
          </CardContent>
        </Card>

        <Card hover className="group cursor-pointer" onClick={() => setActiveTab('learning')}>
          <CardContent className="pt-6">
            <div className="flex items-start justify-between">
              <div className="space-y-3">
                <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-secondary-500 to-secondary-700 flex items-center justify-center shadow-lg group-hover:shadow-glow transition-shadow">
                  <BookOpen className="w-7 h-7 text-white" />
                </div>
                <div>
                  <CardTitle>Learning Materials</CardTitle>
                  <p className="text-dark-400 mt-2">
                    Generate comprehensive summaries and key notes from your documents.
                    Perfect for quick reviews and deep dives.
                  </p>
                </div>
                <div className="flex gap-2 pt-2">
                  <Badge variant="default">Summary</Badge>
                  <Badge variant="default">Key Notes</Badge>
                </div>
              </div>
              <ArrowRight className="w-6 h-6 text-secondary-400 group-hover:translate-x-1 transition-transform" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Recent History */}
      {history.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Recent Quizzes</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {history.slice(0, 5).map((entry, idx) => (
                <div
                  key={idx}
                  className="flex items-center justify-between p-3 rounded-lg bg-dark-900/50"
                >
                  <div className="flex items-center gap-4">
                    <Badge
                      variant={
                        entry.difficulty === 'Easy'
                          ? 'easy'
                          : entry.difficulty === 'Medium'
                          ? 'medium'
                          : 'hard'
                      }
                    >
                      {entry.difficulty}
                    </Badge>
                    <div>
                      <p className="text-sm font-medium text-dark-200">
                        {entry.document || 'All documents'}
                      </p>
                      <p className="text-xs text-dark-400">
                        {new Date(entry.date).toLocaleDateString()}
                      </p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p
                      className={`text-lg font-bold ${
                        entry.score / entry.total >= 0.7
                          ? 'text-green-400'
                          : entry.score / entry.total >= 0.5
                          ? 'text-yellow-400'
                          : 'text-red-400'
                      }`}
                    >
                      {entry.score}/{entry.total}
                    </p>
                    <p className="text-xs text-dark-400">
                      {Math.round((entry.score / entry.total) * 100)}%
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Features Section */}
      <div className="py-8">
        <h2 className="text-3xl font-display font-bold text-dark-100 mb-8 text-center">
          Why Choose RAG Quiz?
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="text-center space-y-3 p-6">
            <div className="w-16 h-16 mx-auto rounded-2xl bg-primary-600/20 flex items-center justify-center">
              <Shield className="w-8 h-8 text-primary-400" />
            </div>
            <h3 className="text-lg font-semibold text-dark-100">
              Privacy First
            </h3>
            <p className="text-dark-400">
              All processing happens locally. Your documents stay on your machine.
            </p>
          </div>

          <div className="text-center space-y-3 p-6">
            <div className="w-16 h-16 mx-auto rounded-2xl bg-secondary-600/20 flex items-center justify-center">
              <Zap className="w-8 h-8 text-secondary-400" />
            </div>
            <h3 className="text-lg font-semibold text-dark-100">
              Fast & Accurate
            </h3>
            <p className="text-dark-400">
              Powered by state-of-the-art embeddings and Mistral AI for quality.
            </p>
          </div>

          <div className="text-center space-y-3 p-6">
            <div className="w-16 h-16 mx-auto rounded-2xl bg-purple-600/20 flex items-center justify-center">
              <BarChart3 className="w-8 h-8 text-purple-400" />
            </div>
            <h3 className="text-lg font-semibold text-dark-100">
              Track Progress
            </h3>
            <p className="text-dark-400">
              Monitor your performance over time with detailed analytics.
            </p>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <Card className="bg-gradient-to-br from-primary-900/50 to-secondary-900/50 border-primary-500/30">
        <CardContent className="py-12 text-center">
          <h2 className="text-3xl font-display font-bold text-dark-100 mb-4">
            Ready to Start Learning?
          </h2>
          <p className="text-dark-400 mb-8 max-w-xl mx-auto">
            Upload your first document and let AI create a personalized learning
            experience. No credit card required.
          </p>
          <div className="flex gap-4 justify-center">
            <Link to="/upload">
              <Button size="lg" leftIcon={<Upload className="w-5 h-5" />}>
                Upload Your First Document
              </Button>
            </Link>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};
