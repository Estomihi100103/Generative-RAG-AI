from sentence_transformers import SentenceTransformer
import torch
from typing import Optional

class EmbeddingModel:
    _instance: Optional['EmbeddingModel'] = None
    _model: Optional[SentenceTransformer] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # Initialize model pada instance pertama
            cls._instance._initialize_model()
        return cls._instance
    
    def _initialize_model(self):
        if self._model is None:
            self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
            print(f"Loading model on {self.device}...")
            self._model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
            self._model.to(self.device)
            print("Model loaded successfully")
    
    @property
    def model(self):
        return self._model
    
    @property
    def get_device(self):
        return self.device

# Global instance
embedding_model = EmbeddingModel()