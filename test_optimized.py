import requests
import json

API_URL = "https://asklLin-quote-finder.hf.space/match"

TEST_CASES = [
    {"input": "思念家乡", "expect_keywords": ["乡", "家", "归", "故"], "category": "思乡"},
    {"input": "坚持梦想", "expect_keywords": ["志", "梦", "坚", "毅"], "category": "励志"},
    {"input": "花 雨天 灯火", "expect_keywords": ["花", "雨", "灯", "火"], "category": "意象"},
    {"input": "人生短暂", "expect_keywords": ["人生", "几何", "短暂"], "category": "人生"},
    {"input": "孤独寂寞", "expect_keywords": ["孤", "独", "寂寞"], "category": "孤独"},
    {"input": "爱国报国", "expect_keywords": ["国", "家", "忠", "报"], "category": "爱国"},
    {"input": "离别送别", "expect_keywords": ["别", "离", "送"], "category": "离别"},
    {"input": "爱情相思", "expect_keywords": ["爱", "情", "思", "恋"], "category": "爱情"},
    {"input": "春天美景", "expect_keywords": ["春", "花", "绿", "红"], "category": "春天"},
    {"input": "学习进步", "expect_keywords": ["学", "读", "勤", "书"], "category": "学习"},
]

results = []
results.append("=" * 60)
results.append("优化后测试报告 (混合匹配)")
results.append("=" * 60)

total_score = 0
for tc in TEST_CASES:
    try:
        response = requests.post(API_URL, json={"query": tc["input"], "top_k": 5}, timeout=60)
        data = response.json()
        matches = data.get("results", [])
        
        if matches:
            top1 = matches[0]
            text = top1.get("text", "")[:60]
            author = top1.get("author", "佚名") or "佚名"
            score = top1.get("score", 0)
            semantic = top1.get("semantic_score", 0)
            keyword = top1.get("keyword_score", 0)
            
            # 检查关键词命中
            keyword_hits = sum(1 for kw in tc["expect_keywords"] if kw in top1.get("text", ""))
            match_score = min(100, keyword_hits * 25)
            total_score += match_score
            
            results.append("")
            results.append(f'[{tc["category"]}] 输入: {tc["input"]}')
            results.append(f"  Top1: {text}...")
            results.append(f"  作者: {author}")
            results.append(f"  混合分: {score:.3f} (语义:{semantic:.3f} + 关键词:{keyword:.3f})")
            results.append(f"  关键词命中: {keyword_hits}/{len(tc['expect_keywords'])}")
            results.append(f"  得分: {match_score}/100")
    except Exception as e:
        results.append("")
        results.append(f'[{tc["category"]}] 输入: {tc["input"]}')
        results.append(f"  错误: {e}")

avg_score = total_score / len(TEST_CASES)
results.append("")
results.append("=" * 60)
results.append(f"平均得分: {avg_score:.1f}/100")
results.append("=" * 60)

with open("optimized_report.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(results))

print(f"Report saved. Avg score: {avg_score:.1f}/100")
