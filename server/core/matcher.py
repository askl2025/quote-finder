import json
import re
import faiss
import numpy as np
from pathlib import Path
from typing import List, Dict, Set

from .embedding import EmbeddingEngine

class PoetryMatcher:
    def __init__(self, 
                 data_path: str = "data/quotes.json",
                 index_path: str = "data/index.faiss",
                 synonym_path: str = "data/synonym_dict.json",
                 model_name: str = "moka-ai/m3e-base",
                 semantic_weight: float = 0.5,
                 keyword_weight: float = 0.25,
                 synonym_weight: float = 0.25):
        
        self.data_path = Path(data_path)
        self.index_path = Path(index_path)
        self.synonym_path = Path(synonym_path)
        self.semantic_weight = semantic_weight
        self.keyword_weight = keyword_weight
        self.synonym_weight = synonym_weight
        
        self.embedding_engine = EmbeddingEngine(model_name)
        
        self.quotes = self._load_quotes_from_json()
        print(f"Loaded {len(self.quotes)} quotes from JSON")
        
        self.synonym_dict = self._load_synonym_dict()
        print(f"Loaded synonym dict with {len(self.synonym_dict)} entries")
        
        self.index = self._load_or_create_index()
    
    def _load_quotes_from_json(self) -> List[Dict]:
        if not self.data_path.exists():
            print(f"Data file not found: {self.data_path}")
            return []
        
        with open(self.data_path, 'r', encoding='utf-8') as f:
            quotes = json.load(f)
        
        return quotes
    
    def _load_synonym_dict(self) -> Dict[str, List[str]]:
        """加载同义词词典"""
        if not self.synonym_path.exists():
            print(f"Synonym dict not found: {self.synonym_path}")
            return {}
        
        with open(self.synonym_path, 'r', encoding='utf-8') as f:
            raw_dict = json.load(f)
        
        # 将分类词典转换为扁平化的映射
        synonym_map = {}
        for category, mappings in raw_dict.items():
            for word, synonyms in mappings.items():
                synonym_map[word] = synonyms
        
        return synonym_map
    
    def _expand_query(self, query: str) -> List[str]:
        """扩展查询词"""
        expanded = [query]  # 原始查询
        
        # 提取中文词
        words = re.findall(r'[\u4e00-\u9fff]+', query)
        
        for word in words:
            # 检查是否有同义词映射
            if word in self.synonym_dict:
                synonyms = self.synonym_dict[word]
                expanded.extend(synonyms)
            
            # 检查2-gram
            if len(word) >= 2:
                for i in range(len(word) - 1):
                    bigram = word[i:i+2]
                    if bigram in self.synonym_dict:
                        synonyms = self.synonym_dict[bigram]
                        expanded.extend(synonyms)
        
        # 去重
        return list(set(expanded))
    
    def _extract_keywords(self, text: str) -> Set[str]:
        """从文本中提取关键词（单字+2-gram）"""
        chars = re.findall(r'[\u4e00-\u9fff]', text)
        
        keywords = set()
        for char in chars:
            keywords.add(char)
        
        for i in range(len(chars) - 1):
            bigram = chars[i] + chars[i+1]
            keywords.add(bigram)
        
        return keywords
    
    def _calculate_keyword_score(self, query: str, quote_text: str) -> float:
        """计算关键词匹配分数"""
        query_keywords = self._extract_keywords(query)
        quote_keywords = self._extract_keywords(quote_text)
        
        if not query_keywords:
            return 0.0
        
        intersection = query_keywords & quote_keywords
        
        score = 0.0
        for kw in intersection:
            if len(kw) >= 2:
                score += 2.0
            else:
                score += 1.0
        
        max_score = sum(2.0 if len(kw) >= 2 else 1.0 for kw in query_keywords)
        normalized_score = score / max_score if max_score > 0 else 0.0
        
        return min(1.0, normalized_score)
    
    def _calculate_synonym_score(self, expanded_queries: List[str], quote_text: str) -> float:
        """计算同义词匹配分数"""
        if len(expanded_queries) <= 1:
            return 0.0
        
        quote_keywords = self._extract_keywords(quote_text)
        
        # 计算扩展词在名句中的命中率
        hit_count = 0
        for eq in expanded_queries[1:]:  # 跳过原始查询
            eq_keywords = self._extract_keywords(eq)
            if eq_keywords & quote_keywords:
                hit_count += 1
        
        # 归一化
        max_hits = len(expanded_queries) - 1
        if max_hits == 0:
            return 0.0
        
        return min(1.0, hit_count / max_hits)
    
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
        
        batch_size = 32
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
        
        # 扩展查询
        expanded_queries = self._expand_query(query)
        
        # 语义搜索
        semantic_top_k = min(top_k * 5, 100)
        query_embedding = self.embedding_engine.encode_single(query)
        query_array = np.array([query_embedding], dtype=np.float32)
        
        semantic_scores, indices = self.index.search(query_array, semantic_top_k)
        
        results = []
        for sem_score, idx in zip(semantic_scores[0], indices[0]):
            if idx >= 0 and idx < len(self.quotes):
                quote = self.quotes[idx].copy()
                
                semantic_score = float(sem_score)
                keyword_score = self._calculate_keyword_score(query, quote['text'])
                synonym_score = self._calculate_synonym_score(expanded_queries, quote['text'])
                
                # 综合分数
                final_score = (self.semantic_weight * semantic_score + 
                             self.keyword_weight * keyword_score +
                             self.synonym_weight * synonym_score)
                
                # 构建返回数据，确保所有字段都存在
                result = {
                    'id': quote.get('id', f'generated_{idx}'),
                    'text': quote.get('text', ''),
                    'author': quote.get('author'),
                    'source': quote.get('source'),
                    'dynasty': quote.get('dynasty'),
                    'type': quote.get('type'),
                    'score': final_score,
                    'semantic_score': semantic_score,
                    'keyword_score': keyword_score,
                    'synonym_score': synonym_score
                }
                
                results.append(result)
        
        results.sort(key=lambda x: x['score'], reverse=True)
        
        return results[:top_k]
    
    def get_quotes_count(self) -> int:
        return len(self.quotes)
