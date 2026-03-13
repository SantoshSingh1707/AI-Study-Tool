import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List
import sys
import os

class EmbeddingManager:
    """Manages sentence embeddings using SentenceTransformer"""
    
    def __init__(self, model_name: str = "multi-qa-MiniLM-L6-cos-v1", device: str = None):
        self.model_name = model_name
        self.device = device
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load the embedding model"""
        try:
            import torch
            if self.device is None:
                self.device = "cuda" if torch.cuda.is_available() else "cpu"
            
            print("-" * 50)
            print(f"DEVICE DETECTION: {'GPU (CUDA)' if self.device == 'cuda' else 'CPU'}")
            print(f"Loading embedding model: {self.model_name}")
            print(f"Target Device: {self.device}")
            self.model = SentenceTransformer(self.model_name, device=self.device)
            print(f"Model loaded successfully on {self.device}")
            print("-" * 50)
        except Exception as e:
            print(f"Error loading model : {self.model_name}")
            raise e
    
    def generate_embeddings(self, texts: List[str], is_query: bool = False) -> np.ndarray:
        """Generate embeddings with optional query prefix"""
        if not self.model:
            raise ValueError("Model not loaded")
        
        # Add prefix for better Q&A embeddings
        if is_query:
            texts = [f"query: {text}" for text in texts]
        else:
            texts = [f"passage: {text}" for text in texts]
        
        print(f"Generating embeddings for {len(texts)} texts")
        embeddings = self.model.encode(texts, show_progress_bar=True)
        print(f"Generated embeddings with shape {embeddings.shape}")
        return embeddings
