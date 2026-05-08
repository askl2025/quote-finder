import json
import faiss
import numpy as np
from pathlib import Path
from typing import List, Dict

from .embedding import EmbeddingEngine

class PoetryMatcher:
    def __init__(self, 
                 data_path: str = "data/quotes.json",
                 index_path: str = "data/index.faiss",
                 model_name: str = "BAAI/bge-small-zh-v1.5"):
        
        self.data_path = Path(data_path)
        self.index_path = Path(index_path)
        
        self.embedding_engine = EmbeddingEngine(model_name)
        
        self.quotes = self._load_quotes_from_json()
        print(f"Loaded {len(self.quotes)} quotes from JSON")
        
        self.index = self._load_or_create_index()
    
    def _load_quotes_from_json(self) -> List[Dict]:
        if not self.data_path.exists():
            print(f"Data file not found: {self.data_path}")
            return []
        
        with open(self.data_path, 'r', encoding='utf-8') as f:
            quotes = json.load(f)
        
        return quotes
    
    def _load_or_create_index(self) -> faiss.Index:
        if self.index_path.exists():
            print(f"Loading existing index from {self.index_path}")
            return faiss.read_index(str(self.index_path))
        else:
            print("No existing index found, building now...")
            self.build_index()
            return self.index
    
    def build_index(self):
        if len(self.quotes) == 0:
            print("No quotes to index")
            return
        
        print(f"Building index for {len(self.quotes)} quotes...")
        
        batch_size = 64
        all_embeddings = []
        
        for i in range(0, len(self.quotes), batch_size):
            batch = self.quotes[i:i+batch_size]
            texts = [q['text'] for q in batch]
            embeddings = self.embedding_engine.encode(texts, use_cache=False)
            all_embeddings.append(embeddings)
            
            if (i // batch_size) % 10 == 0:
                print(f"Processed {min(i+batch_size, len(self.quotes))}/{len(self.quotes)}")
        
        all_embeddings = np.vstack(all_embeddings).astype('float32')
        
        dimension = all_embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dimension)
        self.index.add(all_embeddings)
        
        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        faiss.write_index(self.index, str(self.index_path))
        print(f"Index saved to {self.index_path}")
        print(f"Index contains {self.index.ntotal} vectors")
    
    def match(self, query: str, top_k: int = 5) -> List[Dict]:
        if self.index is None or self.index.ntotal == 0:
            return []
        
        query_embedding = self.embedding_engine.encode_single(query)
        query_array = np.array([query_embedding], dtype=np.float32)
        
        scores, indices = self.index.search(query_array, top_k)
        
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx >= 0 and idx < len(self.quotes):
                quote = self.quotes[idx].copy()
                quote['score'] = float(score)
                results.append(quote)
        
        return results
    
    def get_quotes_count(self) -> int:
        return len(self.quotes)
