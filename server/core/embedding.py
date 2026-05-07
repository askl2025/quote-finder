import hashlib
import json
import numpy as np
from pathlib import Path
from typing import List, Dict
from sentence_transformers import SentenceTransformer
import torch

class EmbeddingEngine:
    def __init__(self, model_name: str = "BAAI/bge-small-zh-v1.5"):
        print(f"Loading model: {model_name}")
        self.model = SentenceTransformer(model_name, device="cpu")
        
        if hasattr(torch, 'set_num_threads'):
            torch.set_num_threads(2)
        
        self.dimension = 512
        self.cache: Dict[str, np.ndarray] = {}
        self.cache_max_size = 50000
        
        print(f"Model loaded. Dimension: {self.dimension}")
    
    def _get_cache_key(self, text: str) -> str:
        return hashlib.md5(text.encode()).hexdigest()
    
    def encode(self, texts: List[str], use_cache: bool = True) -> np.ndarray:
        if use_cache:
            results = []
            uncached_texts = []
            uncached_indices = []
            
            for i, text in enumerate(texts):
                cache_key = self._get_cache_key(text)
                if cache_key in self.cache:
                    results.append((i, self.cache[cache_key]))
                else:
                    uncached_texts.append(text)
                    uncached_indices.append(i)
            
            if uncached_texts:
                new_embeddings = self.model.encode(
                    uncached_texts,
                    normalize_embeddings=True,
                    show_progress_bar=False
                )
                
                for text, embedding in zip(uncached_texts, new_embeddings):
                    cache_key = self._get_cache_key(text)
                    if len(self.cache) < self.cache_max_size:
                        self.cache[cache_key] = embedding
                
                for idx, embedding in zip(uncached_indices, new_embeddings):
                    results.append((idx, embedding))
            
            results.sort(key=lambda x: x[0])
            return np.array([r[1] for r in results], dtype=np.float32)
        else:
            return self.model.encode(
                texts,
                normalize_embeddings=True,
                show_progress_bar=False
            ).astype(np.float32)
    
    def encode_single(self, text: str) -> np.ndarray:
        return self.encode([text])[0]
