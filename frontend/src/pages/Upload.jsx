import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload as UploadIcon, FileText, X, CheckCircle, AlertCircle, Loader2 } from 'lucide-react';
import { useAppStore } from '@/store/useAppStore';
import { Card, CardHeader, CardContent, CardTitle, Button, Alert, Progress } from '@/components/ui';
import clsx from 'clsx';

export const Upload = () => {
  const { uploadDocument, deleteDocument, availableSources, isLoading } = useAppStore();
  const [uploadStatus, setUploadStatus] = useState('idle');
  const [currentFile, setCurrentFile] = useState('');
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');

  const onDrop = useCallback(
    async (acceptedFiles) => {
      const file = acceptedFiles[0];
      if (!file) return;

      setUploadStatus('uploading');
      setCurrentFile(file.name);
      setProgress(0);
      setError('');

      // Simulate progress (API doesn't provide real progress)
      const progressInterval = setInterval(() => {
        setProgress((prev) => Math.min(prev + 10, 90));
      }, 500);

      try {
        const result = await uploadDocument(file);
        clearInterval(progressInterval);
        setProgress(100);
        setUploadStatus('success');
        setSuccessMessage(`${result.message} (${result.chunks_added} chunks added)`);
      } catch (err) {
        clearInterval(progressInterval);
        setUploadStatus('error');
        setError(err.response?.data?.detail || err.message || 'Upload failed');
      }
    },
    [uploadDocument]
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'text/plain': ['.txt'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'application/vnd.openxmlformats-officedocument.presentationml.presentation': ['.pptx'],
    },
    maxSize: 50 * 1024 * 1024, // 50MB
    maxFiles: 1,
  });

  const handleDelete = async (sourceName) => {
    if (window.confirm(`Delete "${sourceName}"?`)) {
      await deleteDocument(sourceName);
    }
  };

  const resetUpload = () => {
    setUploadStatus('idle');
    setCurrentFile('');
    setProgress(0);
    setError('');
    setSuccessMessage('');
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8 animate-fade-in">
      {/* Header */}
      <div>
        <h1 className="text-4xl font-display font-bold text-dark-100 mb-2">
          Upload Documents
        </h1>
        <p className="text-dark-400">
          Upload PDF, TXT, DOCX, or PPTX files to generate quizzes and study materials.
        </p>
      </div>

      {/* Upload Area */}
      <Card
        hover
        className={clsx(
          'cursor-pointer transition-all',
          isDragActive && 'border-primary-500 bg-primary-600/10'
        )}
        {...getRootProps()}
      >
        <input {...getInputProps()} />

        <CardContent className="py-16 text-center">
          {uploadStatus === 'idle' && (
            <>
              <div className="w-20 h-20 mx-auto mb-6 rounded-2xl bg-primary-600/20 flex items-center justify-center">
                <UploadIcon className="w-10 h-10 text-primary-400" />
              </div>
              <h3 className="text-xl font-semibold text-dark-100 mb-2">
                {isDragActive ? 'Drop your file here' : 'Drag & drop your file'}
              </h3>
              <p className="text-dark-400 mb-4">
                or click to browse. Supports PDF, TXT, DOCX, PPTX (max 50MB)
              </p>
              <Button type="button" variant="secondary">
                Choose File
              </Button>
            </>
          )}

          {uploadStatus === 'uploading' && (
            <div className="space-y-4">
              <div className="flex items-center justify-center gap-3">
                <Loader2 className="w-8 h-8 text-primary-400 animate-spin" />
                <span className="text-lg font-medium text-dark-100">
                  Uploading {currentFile}...
                </span>
              </div>
              <Progress value={progress} size="lg" showLabel />
              <p className="text-sm text-dark-400">
                Processing document and generating embeddings...
              </p>
            </div>
          )}

          {uploadStatus === 'success' && (
            <div className="space-y-4">
              <div className="flex items-center justify-center gap-3">
                <CheckCircle className="w-8 h-8 text-green-400" />
                <span className="text-lg font-medium text-dark-100">
                  Upload Successful!
                </span>
              </div>
              <p className="text-dark-400">{successMessage}</p>
              <Button onClick={resetUpload} variant="secondary">
                Upload Another
              </Button>
            </div>
          )}

          {uploadStatus === 'error' && (
            <div className="space-y-4">
              <div className="flex items-center justify gap-3">
                <AlertCircle className="w-8 h-8 text-red-400" />
                <span className="text-lg font-medium text-dark-100">
                  Upload Failed
                </span>
              </div>
              <p className="text-red-400">{error}</p>
              <Button onClick={resetUpload} variant="secondary">
                Try Again
              </Button>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Uploaded Documents */}
      <Card>
        <CardHeader>
          <CardTitle>Uploaded Documents ({availableSources.length})</CardTitle>
        </CardHeader>
        <CardContent>
          {availableSources.length === 0 ? (
            <div className="text-center py-12">
              <FileText className="w-12 h-12 mx-auto mb-4 text-dark-600" />
              <p className="text-dark-400">No documents uploaded yet.</p>
            </div>
          ) : (
            <div className="space-y-3">
              {availableSources.map((source) => (
                <div
                  key={source}
                  className="flex items-center justify-between p-4 rounded-lg bg-dark-900/50 hover:bg-dark-800/50 transition-colors"
                >
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-lg bg-primary-600/20 flex items-center justify-center">
                      <FileText className="w-5 h-5 text-primary-400" />
                    </div>
                    <div>
                      <p className="font-medium text-dark-100">{source}</p>
                      <p className="text-sm text-dark-400">PDF Document</p>
                    </div>
                  </div>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={(e) => {
                      e.stopPropagation();
                      handleDelete(source);
                    }}
                    leftIcon={<X className="w-4 h-4" />}
                    className="text-red-400 hover:bg-red-500/10"
                  >
                    Delete
                  </Button>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Tips */}
      <Card className="bg-primary-900/20 border-primary-500/20">
        <CardContent className="py-6">
          <h3 className="font-semibold text-dark-100 mb-3 flex items-center gap-2">
            <AlertCircle className="w-5 h-5 text-primary-400" />
            Tips for Best Results
          </h3>
          <ul className="space-y-2 text-dark-400 text-sm">
            <li>• Use clear, well-formatted documents with selectable text</li>
            <li>• Larger documents take longer to process (1-3 minutes)</li>
            <li>• Scanned PDFs will use OCR which may take longer</li>
            <li>• Documents are stored locally in ChromaDB vector store</li>
            <li>
              • You can re-upload documents - duplicates are automatically
              detected
            </li>
          </ul>
        </CardContent>
      </Card>
    </div>
  );
};
