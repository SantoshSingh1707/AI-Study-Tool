import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 300000, // 5 minutes (LLM generation can take time)
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      console.error(
        `API Error ${error.response.status}:`,
        error.response.data
      );
    } else if (error.request) {
      console.error('API Error: No response received');
    }
    return Promise.reject(error);
  }
);

// Health Check
export const healthCheck = async () => {
  const response = await api.get('/health');
  return response.data;
};

// Documents
export const listDocuments = async () => {
  const response = await api.get('/api/documents');
  return response.data;
};

export const deleteDocument = async (sourceName) => {
  const response = await api.delete(`/api/documents/${encodeURIComponent(sourceName)}`);
  return response.data;
};

export const uploadDocument = async (file) => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await api.post('/api/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

// Generation
export const generateQuiz = async (request) => {
  const response = await api.post('/api/generate/quiz', request);
  return response.data;
};

export const generateLearning = async (request) => {
  const response = await api.post('/api/generate/learning', request);
  return response.data;
};

export default api;
