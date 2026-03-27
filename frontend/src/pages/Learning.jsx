import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import clsx from 'clsx';
import {
  BookOpen,
  FileText,
  Download,
  Loader2,
  RefreshCw,
} from 'lucide-react';
import { useAppStore } from '@/store/useAppStore';
import { Card, CardContent, CardHeader, CardTitle, Button, Badge } from '@/components/ui';

export const Learning = () => {
  const {
    topK,
    similarityThreshold,
    selectedSources,
    topicFocus,
    learningMode,
    setLearningMode,
    learningContent,
    learningSources,
    isLoading,
    setLoading,
    setLearningContent,
    setLearningSources,
  } = useAppStore();

  const [isGenerating, setIsGenerating] = useState(false);

  const handleGenerate = async () => {
    setIsGenerating(true);
    try {
      await useAppStore.getState().fetchLearning({
        mode: learningMode,
        top_k: topK,
        source_filter: selectedSources.length > 0 ? selectedSources : undefined,
        topic: topicFocus || undefined,
      });
    } finally {
      setIsGenerating(false);
    }
  };

  const handleDownload = () => {
    const blob = new Blob([learningContent], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${learningMode.toLowerCase().replace(' ', '-')}_notes.md`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const renderMarkdown = (content) => {
    // Simple markdown rendering
    return content
      .split('\n')
      .map((line, idx) => {
        if (line.startsWith('### ')) {
          return <h3 key={idx} className="text-xl font-bold text-dark-100 mt-6 mb-3">{line.slice(4)}</h3>;
        }
        if (line.startsWith('## ')) {
          return <h2 key={idx} className="text-2xl font-bold text-dark-100 mt-8 mb-4">{line.slice(3)}</h2>;
        }
        if (line.startsWith('# ')) {
          return <h1 key={idx} className="text-3xl font-bold text-dark-100 mt-8 mb-4">{line.slice(2)}</h1>;
        }
        if (line.startsWith('- ')) {
          return (
            <li key={idx} className="ml-6 mb-2 text-dark-300 list-disc">
              {line.slice(2)}
            </li>
          );
        }
        if (line.startsWith('* ')) {
          return (
            <li key={idx} className="ml-6 mb-2 text-dark-300 list-disc">
              {line.slice(2)}
            </li>
          );
        }
        if (line.match(/^\d+\. /)) {
          return (
            <li key={idx} className="ml-6 mb-2 text-dark-300 list-decimal">
              {line.replace(/^\d+\. /, '')}
            </li>
          );
        }
        if (line.trim() === '') {
          return <br key={idx} />;
        }
        return (
          <p key={idx} className="mb-3 text-dark-300 leading-relaxed">
            {line}
          </p>
        );
      });
  };

  return (
    <div className="max-w-6xl mx-auto space-y-6 animate-fade-in">
      {/* Header */}
      <div>
        <h1 className="text-4xl font-display font-bold text-dark-100 mb-2">
          Learning Hub
        </h1>
        <p className="text-dark-400">
          Generate summaries and key notes from your documents.
        </p>
      </div>

      {/* Configuration */}
      <Card className="bg-gradient-to-br from-dark-900 to-dark-800">
        <CardContent className="pt-6">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {/* Mode Selection */}
            <div>
              <label className="block text-sm font-medium text-dark-300 mb-3">
                Learning Mode
              </label>
              <div className="flex gap-2">
                {['Summary', 'Key Notes'].map((mode) => (
                  <button
                    key={mode}
                    onClick={() => setLearningMode(mode)}
                    className={clsx(
                      'px-4 py-2 rounded-lg font-medium transition-colors flex-1',
                      learningMode === mode
                        ? 'bg-secondary-600 text-white'
                        : 'bg-dark-700 text-dark-300 hover:bg-dark-600'
                    )}
                  >
                    {mode}
                  </button>
                ))}
              </div>
            </div>

            {/* Top K */}
            <div>
              <label className="block text-sm font-medium text-dark-300 mb-3">
                Source Chunks: {topK}
              </label>
              <input
                type="range"
                min="5"
                max="50"
                value={topK}
                onChange={(e) =>
                  useAppStore.getState().setTopK(parseInt(e.target.value))
                }
                className="w-full h-2 bg-dark-700 rounded-lg appearance-none cursor-pointer accent-secondary-500"
              />
            </div>

            {/* Topic */}
            <div className="lg:col-span-2">
              <label className="block text-sm font-medium text-dark-300 mb-3">
                Topic Focus (Optional)
              </label>
              <input
                type="text"
                value={topicFocus}
                onChange={(e) => useAppStore.getState().setTopicFocus(e.target.value)}
                placeholder="Focus on a specific topic..."
                className="input max-w-full"
              />
            </div>
          </div>

          <div className="mt-6 flex justify-center">
            <Button
              size="lg"
              onClick={handleGenerate}
              isLoading={isGenerating}
              leftIcon={
                isGenerating ? (
                  <Loader2 className="w-5 h-5 animate-spin" />
                ) : (
                  <BookOpen className="w-5 h-5" />
                )
              }
            >
              {isGenerating ? 'Generating...' : `Generate ${learningMode}`}
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Generated Content */}
      {learningContent && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-4">
            <Card>
              <CardHeader className="flex flex-row items-center justify-between">
                <CardTitle>{learningMode}</CardTitle>
                <Button
                  variant="secondary"
                  size="sm"
                  onClick={handleDownload}
                  leftIcon={<Download className="w-4 h-4" />}
                >
                  Download
                </Button>
              </CardHeader>
              <CardContent>
                <div className="prose prose-invert max-w-none">
                  {renderMarkdown(learningContent)}
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Sidebar */}
          <div className="space-y-4">
            {/* Sources */}
            {learningSources.length > 0 && (
              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">Sources</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {learningSources.map((source, idx) => (
                      <div key={idx} className="flex items-start gap-3 p-3 rounded-lg bg-dark-900/50">
                        <div className="w-8 h-8 rounded-lg bg-primary-600/20 flex items-center justify-center flex-shrink-0">
                          <FileText className="w-4 h-4 text-primary-400" />
                        </div>
                        <div className="flex-1 min-w-0">
                          <p className="text-sm font-medium text-dark-200 truncate">
                            {source.source_file}
                          </p>
                          <div className="flex items-center gap-2 mt-1">
                            <Badge variant="default" className="text-xs">
                              {Math.round(source.similarity_score * 100)}% match
                            </Badge>
                            {source.page && (
                              <span className="text-xs text-dark-400">
                                p. {source.page}
                              </span>
                            )}
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Info Card */}
            <Card className="bg-primary-900/20 border-primary-500/20">
              <CardContent className="pt-6">
                <h3 className="font-semibold text-dark-100 mb-3 flex items-center gap-2">
                  <BookOpen className="w-5 h-5 text-primary-400" />
                  About {learningMode}
                </h3>
                <p className="text-sm text-dark-400">
                  {learningMode === 'Summary'
                    ? 'A comprehensive overview of the document content, organized by main themes and sections. Perfect for understanding the big picture.'
                    : 'A concise list of key facts, formulas, definitions, and important points. Ideal for quick review and memorization.'}
                </p>
              </CardContent>
            </Card>

            {/* Quick Actions */}
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Quick Actions</CardTitle>
              </CardHeader>
              <CardContent className="space-y-2">
                <Button
                  variant="secondary"
                  className="w-full justify-start"
                  onClick={handleGenerate}
                  leftIcon={<RefreshCw className="w-4 h-4" />}
                >
                  Regenerate
                </Button>
                <Link to="/quiz">
                  <Button variant="secondary" className="w-full justify-start">
                    Create Quiz
                  </Button>
                </Link>
              </CardContent>
            </Card>
          </div>
        </div>
      )}

      {/* Empty State */}
      {!learningContent && !isGenerating && (
        <Card className="text-center py-16">
          <CardContent>
            <div className="w-20 h-20 mx-auto mb-6 rounded-2xl bg-secondary-600/20 flex items-center justify-center">
              <BookOpen className="w-10 h-10 text-secondary-400" />
            </div>
            <h3 className="text-xl font-semibold text-dark-100 mb-2">
              Ready to Learn?
            </h3>
            <p className="text-dark-400 mb-6 max-w-md mx-auto">
              Select your preferred mode above and click "Generate" to create
              personalized study materials from your documents.
            </p>
            <div className="flex justify-center">
              <Button variant="secondary" onClick={handleGenerate}>
                Generate First Notes
              </Button>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};
