import json
import re
import faiss
import numpy as np
from pathlib import Path
from typing import List, Dict, Set, Tuple
from collections import Counter

from .embedding import EmbeddingEngine

class PoetryMatcher:
    def __init__(self, 
                 data_path: str = "data/quotes.json",
                 index_path: str = "data/index.faiss",
                 model_name: str = "BAAI/bge-small-zh-v1.5",
                 semantic_weight: float = 0.7,
                 keyword_weight: float = 0.3):
        
        self.data_path = Path(data_path)
        self.index_path = Path(index_path)
        self.semantic_weight = semantic_weight
        self.keyword_weight = keyword_weight
        
        self.embedding_engine = EmbeddingEngine(model_name)
        
        self.quotes = self._load_quotes_from_json()
        print(f"Loaded {len(self.quotes)} quotes from JSON")
        
        # 构建关键词索引（使用2-gram）
        self.keyword_index = self._build_keyword_index()
        print(f"Built keyword index with {len(self.keyword_index)} unique keywords")
        
        self.index = self._load_or_create_index()
    
    def _load_quotes_from_json(self) -> List[Dict]:
        if not self.data_path.exists():
            print(f"Data file not found: {self.data_path}")
            return []
        
        with open(self.data_path, 'r', encoding='utf-8') as f:
            quotes = json.load(f)
        
        return quotes
    
    def _extract_keywords(self, text: str) -> Set[str]:
        """从文本中提取关键词（单字+2-gram）"""
        # 提取中文字符
        chars = re.findall(r'[\u4e00-\u9fff]', text)
        
        keywords = set()
        
        # 添加单字
        for char in chars:
            keywords.add(char)
        
        # 添加2-gram
        for i in range(len(chars) - 1):
            bigram = chars[i] + chars[i+1]
            keywords.add(bigram)
        
        return keywords
    
    def _build_keyword_index(self) -> Dict[str, List[int]]:
        """构建关键词索引"""
        index = {}
        
        for i, quote in enumerate(self.quotes):
            text = quote.get('text', '')
            keywords = self._extract_keywords(text)
            
            for kw in keywords:
                if kw not in index:
                    index[kw] = []
                index[kw].append(i)
        
        return index
    
    def _calculate_keyword_score(self, query: str, quote_text: str) -> float:
        """计算关键词匹配分数"""
        query_keywords = self._extract_keywords(query)
        quote_keywords = self._extract_keywords(quote_text)
        
        if not query_keywords:
            return 0.0
        
        # 计算交集比例（使用查询关键词的覆盖率）
        intersection = query_keywords & quote_keywords
        
        # 对2-gram给予更高权重
        score = 0.0
        for kw in intersection:
            if len(kw) >= 2:  # 2-gram
                score += 2.0
            else:  # 单字
                score += 1.0
        
        # 归一化到0-1
        max_score = sum(2.0 if len(kw) >= 2 else 1.0 for kw in query_keywords)
        normalized_score = score / max_score if max_score > 0 else 0.0
        
        return min(1.0, normalized_score)
    
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
        
        # 语义搜索 - 获取更多候选结果
        semantic_top_k = min(top_k * 5, 100)  # 获取5倍候选
        query_embedding = self.embedding_engine.encode_single(query)
        query_array = np.array([query_embedding], dtype=np.float32)
        
        semantic_scores, indices = self.index.search(query_array, semantic_top_k)
        
        # 计算混合分数
        results = []
        for sem_score, idx in zip(semantic_scores[0], indices[0]):
            if idx >= 0 and idx < len(self.quotes):
                quote = self.quotes[idx].copy()
                
                # 语义分数（归一化到0-1）
                semantic_score = float(sem_score)
                
                # 关键词分数
                keyword_score = self._calculate_keyword_score(query, quote['text'])
                
                # 混合分数
                final_score = (self.semantic_weight * semantic_score + 
                             self.keyword_weight * keyword_score)
                
                quote['score'] = final_score
                quote['semantic_score'] = semantic_score
                quote['keyword_score'] = keyword_score
                results.append(quote)
        
        # 按混合分数排序
        results.sort(key=lambda x: x['score'], reverse=True)
        
        return results[:top_k]
    
    def get_quotes_count(self) -> int:
        return len(self.quotes)
