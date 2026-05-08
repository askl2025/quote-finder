import requests
import json

API_URL = 'https://asklLin-quote-finder.hf.space'

tests = [
    '我喜欢小狗',
    '思念家乡', 
    '坚持梦想',
    '花 雨天 灯火',
    '孤独寂寞',
    '人生短暂',
    '爱情',
    '学习进步'
]

results = ['=' * 60, '优化后测试结果', '=' * 60, '']

for query in tests:
    try:
        r = requests.post(f'{API_URL}/match', json={'query': query, 'top_k': 3}, timeout=120)
        result = r.json()
        
        results.append(f'输入: {query}')
        results.append('-' * 40)
        
        if 'results' in result:
            for i, item in enumerate(result['results'][:2], 1):
                text = item['text'][:60]
                author = item.get('author', '') or '佚名'
                score = item.get('score', 0)
                sem = item.get('semantic_score', 0)
                results.append(f'  {i}. {text}')
                results.append(f'     {author} | 综合:{score:.3f} 语义:{sem:.3f}')
        else:
            results.append(f'  Error: {json.dumps(result, ensure_ascii=False)[:100]}')
        
        results.append('')
    except Exception as e:
        results.append(f'输入: {query}')
        results.append('-' * 40)
        results.append(f'  Exception: {e}')
        results.append('')

results.append('=' * 60)
results.append('测试完成!')

with open('final_test_report.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(results))

print('Report saved to final_test_report.txt')
