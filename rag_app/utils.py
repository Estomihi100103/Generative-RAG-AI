from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List
from .embeddings import embedding_model

class RAGHandler:
    def __init__(self):
        self.model = embedding_model.model
        self.device = embedding_model.get_device

    def generate_embeddings(self, texts: List[str]) -> List[np.ndarray]:
        """
        Generate embeddings for a list of texts
        """
        embeddings = self.model.encode(
            texts,
            convert_to_tensor=True,
            device=self.device,
            show_progress_bar=True,
            batch_size=32
        )
        return embeddings.cpu().numpy()

    def generate_single_embedding(self, text: str) -> np.ndarray:
        """
        Generate embedding for a single text
        """
        embedding = self.model.encode(
            text,
            convert_to_tensor=True,
            device=self.device
        )
        return embedding.cpu().numpy()