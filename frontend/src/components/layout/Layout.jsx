import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import clsx from 'clsx';
import {
  BookOpen,
  FileText,
  GitBranch,
  Home,
  Plus,
} from 'lucide-react';
import { useAppStore } from '@/store/useAppStore';

export const Layout = ({ children }) => {
  const location = useLocation();
  const { availableSources, selectedSources, setSelectedSources } = useAppStore();

  const navItems = [
    { path: '/', icon: Home, label: 'Home' },
    { path: '/upload', icon: Plus, label: 'Upload' },
    { path: '/quiz', icon: GitBranch, label: 'Quiz' },
    { path: '/learning', icon: BookOpen, label: 'Learning' },
  ];

  const toggleSource = (source) => {
    if (selectedSources.includes(source)) {
      setSelectedSources(selectedSources.filter((s) => s !== source));
    } else {
      setSelectedSources([...selectedSources, source]);
    }
  };

  return (
    <div className="min-h-screen bg-dark-950 flex">
      {/* Sidebar */}
      <aside className="w-64 bg-dark-950 border-r border-dark-800 flex flex-col fixed h-full">
        {/* Logo */}
        <div className="p-6 border-b border-dark-800">
          <Link to="/" className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary-500 to-secondary-500 flex items-center justify-center">
              <span className="text-xl">🎓</span>
            </div>
            <div>
              <h1 className="font-display font-bold text-lg text-dark-100">
                RAG Quiz
              </h1>
              <p className="text-xs text-dark-400">Study Smarter</p>
            </div>
          </Link>
        </div>

        {/* Navigation */}
        <nav className="flex-1 p-4 space-y-2">
          {navItems.map((item) => {
            const isActive =
              item.path === location.pathname ||
              (item.path === '/quiz' && location.pathname.startsWith('/quiz')) ||
              (item.path === '/learning' && location.pathname.startsWith('/learning'));

            return (
              <Link
                key={item.path}
                to={item.path}
                className={clsx(
                  'flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 group',
                  isActive
                    ? 'bg-primary-600/20 text-primary-400 border border-primary-500/50'
                    : 'text-dark-300 hover:bg-dark-900 hover:text-dark-100 border border-transparent'
                )}
              >
                <item.icon className="w-5 h-5" />
                <span className="font-medium">{item.label}</span>
              </Link>
            );
          })}
        </nav>

        {/* Sources Panel */}
        <div className="p-4 border-t border-dark-800">
          <div className="mb-3">
            <h3 className="text-sm font-semibold text-dark-400 mb-2 flex items-center gap-2">
              <FileText className="w-4 h-4" />
              Documents ({availableSources.length})
            </h3>
          </div>

          {availableSources.length === 0 ? (
            <div className="text-xs text-dark-500 text-center py-4">
              No documents uploaded yet
              <br />
              <Link to="/upload" className="text-primary-400 hover:underline">
                Upload one
              </Link>
            </div>
          ) : (
            <div className="space-y-2 max-h-48 overflow-y-auto">
              {availableSources.map((source) => (
                <div
                  key={source}
                  onClick={() => toggleSource(source)}
                  className={clsx(
                    'flex items-center gap-2 px-3 py-2 rounded-lg text-sm cursor-pointer transition-colors',
                    selectedSources.includes(source)
                      ? 'bg-primary-600/20 text-primary-400'
                      : 'text-dark-300 hover:bg-dark-900'
                  )}
                  title={source}
                >
                  <div
                    className={clsx(
                      'w-2 h-2 rounded-full',
                      selectedSources.includes(source)
                        ? 'bg-primary-400'
                        : 'bg-dark-600'
                    )}
                  />
                  <span className="truncate flex-1">{source}</span>
                </div>
              ))}
            </div>
          )}

          {/* Quick Settings */}
          <div className="mt-4 pt-4 border-t border-dark-800">
            <div className="flex items-center justify-between text-sm mb-2">
              <span className="text-dark-300">Top K</span>
              <span className="text-primary-400 font-semibold">
                {useAppStore.getState().topK}
              </span>
            </div>
            <div className="flex items-center justify-between text-sm">
              <span className="text-dark-300">Questions</span>
              <span className="text-primary-400 font-semibold">
                {useAppStore.getState().numQuestions}
              </span>
            </div>
          </div>
        </div>

        {/* Copyright */}
        <div className="p-4 text-center border-t border-dark-800">
          <p className="text-xs text-dark-500">© 2024 Study Tool</p>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 ml-64 p-8 max-w-[1600px] mx-auto w-full">
        {children}
      </main>
    </div>
  );
};
