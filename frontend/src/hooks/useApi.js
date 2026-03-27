import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import * as api from '@/services/api';

// Queries
export const useDocuments = () => {
  return useQuery({
    queryKey: ['documents'],
    queryFn: api.listDocuments,
    staleTime: 1000 * 60 * 5, // 5 minutes
  });
};

export const useHealth = () => {
  return useQuery({
    queryKey: ['health'],
    queryFn: api.healthCheck,
    refetchInterval: 1000 * 30, // Every 30 seconds
  });
};

// Mutations
export const useUploadDocument = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: api.uploadDocument,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['documents'] });
    },
  });
};

export const useDeleteDocument = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: api.deleteDocument,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['documents'] });
    },
  });
};

export const useGenerateQuiz = () => {
  return useMutation({
    mutationFn: api.generateQuiz,
  });
};

export const useGenerateLearning = () => {
  return useMutation({
    mutationFn: api.generateLearning,
  });
};
