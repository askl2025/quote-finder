import requests
from typing import Dict, List, Optional

class APIClient:
    def __init__(self, base_url: str = None):
        self.base_url = base_url or "https://askllin-quote-finder.hf.space"
        self.session = requests.Session()
        self.timeout = 15
    
    def match(self, query: str, top_k: int = 5) -> Dict:
        response = self.session.post(
            f"{self.base_url}/match",
            json={"query": query, "top_k": top_k},
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()
    
    def health_check(self) -> Dict:
        response = self.session.get(
            f"{self.base_url}/health",
            timeout=5
        )
        response.raise_for_status()
        return response.json()
