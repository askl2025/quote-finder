import json
import sys
import requests
from typing import List, Dict

class QuoteFinderTest:
    def __init__(self, api_url: str):
        self.api_url = api_url.rstrip('/')
        self.test_cases = self._load_test_cases()
    
    def _load_test_cases(self) -> List[Dict]:
        with open("tests/test_cases.json", "r", encoding="utf-8") as f:
            return json.load(f)["test_cases"]
    
    def test_health(self) -> bool:
        try:
            response = requests.get(f"{self.api_url}/health", timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(f"Health check passed: {data.get('quotes_count', 0)} quotes loaded")
                return True
            else:
                print(f"Health check failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"Health check error: {e}")
            return False
    
    def test_match(self, test_case: Dict) -> Dict:
        try:
            response = requests.post(
                f"{self.api_url}/match",
                json={"query": test_case["input"], "top_k": 5},
                timeout=15
            )
            
            if response.status_code != 200:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.text}"
                }
            
            data = response.json()
            results = data.get("results", [])
            
            hits = []
            for expected in test_case.get("expected", []):
                for result in results:
                    if expected in result["text"]:
                        hits.append(expected)
                        break
            
            return {
                "success": True,
                "hits": hits,
                "total_expected": len(test_case.get("expected", [])),
                "hit_rate": len(hits) / len(test_case.get("expected", [])) if test_case.get("expected") else 0,
                "top_results": [
                    {
                        "text": r["text"][:50],
                        "author": r.get("author", ""),
                        "score": r.get("score", 0)
                    }
                    for r in results[:3]
                ]
            }
        except requests.exceptions.ConnectionError:
            return {"success": False, "error": "Connection failed"}
        except requests.exceptions.Timeout:
            return {"success": False, "error": "Request timeout"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def run_all_tests(self):
        print("=" * 70)
        print("Quote Finder API Test Suite")
        print("=" * 70)
        
        print(f"\nAPI URL: {self.api_url}")
        
        print("\n[1/2] Health Check...")
        if not self.test_health():
            print("ERROR: Health check failed. Is the server running?")
            return False
        
        print("\n[2/2] Running test cases...")
        print("-" * 70)
        
        results = []
        for i, test_case in enumerate(self.test_cases, 1):
            print(f"\nTest {i}: [{test_case['category']}] {test_case['input']}")
            
            result = self.test_match(test_case)
            results.append({
                "id": test_case["id"],
                "input": test_case["input"],
                "category": test_case["category"],
                **result
            })
            
            if result["success"]:
                status = "PASS" if result["hit_rate"] > 0 else "FAIL"
                print(f"  Status: {status} (Hit rate: {result['hit_rate']:.0%})")
                print(f"  Hits: {result['hits']}")
                print(f"  Top3:")
                for r in result["top_results"]:
                    print(f"    - {r['text']} ({r['author']}) [{r['score']:.2f}]")
            else:
                print(f"  Status: ERROR - {result['error']}")
        
        print("\n" + "=" * 70)
        print("Summary")
        print("=" * 70)
        
        total = len(results)
        passed = sum(1 for r in results if r.get("success") and r.get("hit_rate", 0) > 0)
        errors = sum(1 for r in results if not r.get("success"))
        avg_hit_rate = sum(r.get("hit_rate", 0) for r in results if r.get("success")) / max(1, total - errors)
        
        print(f"Total tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed - errors}")
        print(f"Errors: {errors}")
        print(f"Average hit rate: {avg_hit_rate:.0%}")
        
        return passed == total

def main():
    if len(sys.argv) < 2:
        api_url = "http://localhost:7860"
        print(f"Usage: python {sys.argv[0]} <api_url>")
        print(f"Using default: {api_url}")
    else:
        api_url = sys.argv[1]
    
    tester = QuoteFinderTest(api_url)
    success = tester.run_all_tests()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
