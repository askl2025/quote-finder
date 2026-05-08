import requests
import json

url = 'https://asklLin-quote-finder.hf.space/match'

tests = [
    '思念家乡',
    '坚持梦想',
    '花 雨天 灯火',
    '人生短暂',
    '孤独寂寞'
]

results = []
results.append('=' * 60)
results.append('名句匹配测试结果')
results.append('=' * 60)

for query in tests:
    results.append(f'\n输入: {query}')
    results.append('-' * 40)
    
    try:
        response = requests.post(url, json={'query': query, 'top_k': 3}, timeout=60)
        result = response.json()
        
        for i, r in enumerate(result['results'], 1):
            text = r['text']
            author = r.get('author', '佚名') or '佚名'
            source = r.get('source', '') or ''
            score = r['score']
            results.append(f'  {i}. {text}')
            results.append(f'     {author}《{source}》 匹配度:{score:.0%}')
    except Exception as e:
        results.append(f'  错误: {e}')

results.append('\n' + '=' * 60)
results.append('测试完成!')

with open('test_result.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(results))

print('结果已保存到 test_result.txt')
