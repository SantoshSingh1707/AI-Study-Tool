import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { queryClient } from './main';
import { Layout } from './components/layout';
import { Home, Upload, Quiz, Learning } from './pages';
import { useAppStore } from './store/useAppStore';
import { useEffect } from 'react';

function AppContent() {
  const { setActiveTab, fetchAndSetDocuments } = useAppStore();

  useEffect(() => {
    // Initialize: fetch documents list
    fetchAndSetDocuments();
  }, [fetchAndSetDocuments]);

  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/upload" element={<Upload />} />
        <Route path="/quiz" element={<Quiz />} />
        <Route path="/learning" element={<Learning />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Layout>
  );
}

export default function App() {
  return (
    <BrowserRouter
      future={{
        v7_startTransition: true,
        v7_relativeSplatPath: true,
      }}
    >
      <AppContent />
    </BrowserRouter>
  );
}
