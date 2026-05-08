import requests
import json

API_URL = "https://asklLin-quote-finder.hf.space/match"

# 测试用例：输入 -> 期望匹配的关键词/作者/来源
TEST_CASES = [
    {
        "input": "思念家乡",
        "expect_keywords": ["乡", "家", "归", "故"],
        "expect_authors": ["李白", "王维", "杜甫", "张九龄"],
        "category": "思乡"
    },
    {
        "input": "坚持梦想",
        "expect_keywords": ["志", "梦", "坚", "毅", "不息"],
        "expect_authors": ["诸葛亮", "曹操", "李白"],
        "category": "励志"
    },
    {
        "input": "花 雨天 灯火",
        "expect_keywords": ["花", "雨", "灯", "火"],
        "expect_authors": ["欧阳修", "辛弃疾"],
        "category": "意象"
    },
    {
        "input": "人生短暂",
        "expect_keywords": ["人生", "几何", "短暂", "白发"],
        "expect_authors": ["曹操", "苏轼", "李白"],
        "category": "人生哲理"
    },
    {
        "input": "孤独寂寞",
        "expect_keywords": ["孤", "独", "寂寞", "空"],
        "expect_authors": ["柳永", "李清照", "陈子昂"],
        "category": "情感"
    },
    {
        "input": "爱国报国",
        "expect_keywords": ["国", "家", "忠", "报"],
        "expect_authors": ["岳飞", "文天祥", "陆游"],
        "category": "爱国"
    },
    {
        "input": "离别送别",
        "expect_keywords": ["别", "离", "送", "行"],
        "expect_authors": ["王维", "李白", "高适"],
        "category": "离别"
    },
    {
        "input": "爱情相思",
        "expect_keywords": ["爱", "情", "思", "恋"],
        "expect_authors": ["李商隐", "秦观", "柳永"],
        "category": "爱情"
    },
    {
        "input": "春天美景",
        "expect_keywords": ["春", "花", "绿", "红"],
        "expect_authors": ["杜甫", "白居易", "杨万里"],
        "category": "自然"
    },
    {
        "input": "秋天萧瑟",
        "expect_keywords": ["秋", "落叶", "霜", "凉"],
        "expect_authors": ["杜甫", "刘禹锡"],
        "category": "自然"
    },
    {
        "input": "学习进步",
        "expect_keywords": ["学", "读", "勤", "书"],
        "expect_authors": ["孔子", "荀子", "韩愈"],
        "category": "学习"
    },
    {
        "input": "友情知己",
        "expect_keywords": ["友", "知", "朋", "交"],
        "expect_authors": ["王勃", "李白", "高适"],
        "category": "友情"
    },
]

def test_match(test_case):
    """测试单个用例"""
    query = test_case["input"]
    
    try:
        response = requests.post(API_URL, json={"query": query, "top_k": 5}, timeout=60)
        result = response.json()
        results = result.get("results", [])
    except Exception as e:
        return {"success": False, "error": str(e), "score": 0}
    
    if not results:
        return {"success": False, "error": "No results", "score": 0}
    
    # 计算匹配分数
    keyword_hits = 0
    author_hits = 0
    
    matched_texts = []
    matched_authors = []
    
    for r in results:
        text = r.get("text", "")
        author = r.get("author", "") or ""
        
        matched_texts.append(text[:50])
        matched_authors.append(author)
        
        # 检查关键词
        for kw in test_case.get("expect_keywords", []):
            if kw in text:
                keyword_hits += 1
                break
        
        # 检查作者
        for auth in test_case.get("expect_authors", []):
            if auth in author:
                author_hits += 1
                break
    
    # 计算总分 (满分100)
    keyword_score = (keyword_hits / len(results)) * 60  # 关键词占60分
    author_score = (author_hits / len(results)) * 40    # 作者占40分
    total_score = keyword_score + author_score
    
    return {
        "success": True,
        "score": total_score,
        "keyword_hits": keyword_hits,
        "author_hits": author_hits,
        "matched_texts": matched_texts,
        "matched_authors": matched_authors,
        "top1": f"{results[0].get('text', '')[:40]} - {results[0].get('author', '')}"
    }

def main():
    print("=" * 70)
    print("名句匹配准确性测试")
    print("=" * 70)
    
    results = []
    
    for tc in TEST_CASES:
        print(f"\n[{tc['category']}] 输入: {tc['input']}")
        print("-" * 50)
        
        result = test_match(tc)
        results.append({"test": tc, "result": result})
        
        if result["success"]:
            print(f"  得分: {result['score']:.0f}/100")
            print(f"  关键词命中: {result['keyword_hits']}/5")
            print(f"  作者命中: {result['author_hits']}/5")
            print(f"  Top1: {result['top1']}")
        else:
            print(f"  失败: {result.get('error', 'Unknown')}")
    
    # 汇总
    print("\n" + "=" * 70)
    print("测试汇总")
    print("=" * 70)
    
    successful = [r for r in results if r["result"]["success"]]
    failed = [r for r in results if not r["result"]["success"]]
    
    if successful:
        avg_score = sum(r["result"]["score"] for r in successful) / len(successful)
        high_score = sum(1 for r in successful if r["result"]["score"] >= 60)
        medium_score = sum(1 for r in successful if 30 <= r["result"]["score"] < 60)
        low_score = sum(1 for r in successful if r["result"]["score"] < 30)
        
        print(f"总测试: {len(results)}")
        print(f"成功: {len(successful)}")
        print(f"失败: {len(failed)}")
        print(f"平均得分: {avg_score:.1f}/100")
        print(f"高质量 (>=60分): {high_score}")
        print(f"中等 (30-60分): {medium_score}")
        print(f"低质量 (<30分): {low_score}")
        
        # 详细得分
        print("\n详细得分:")
        for r in results:
            tc = r["test"]
            res = r["result"]
            status = "✓" if res["success"] and res["score"] >= 40 else "✗"
            score = res["score"] if res["success"] else 0
            print(f"  {status} [{tc['category']}] {tc['input']}: {score:.0f}分")

if __name__ == "__main__":
    main()
