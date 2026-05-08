import requests
import json

url = 'https://asklLin-quote-finder.hf.space/match'

tests = [
    '思念家乡',
    '坚持梦想',
    '花 雨天 灯火',
    '人生短暂',
    '孤独寂寞',
    '爱国',
    '离别',
    '爱情'
]

results = []
results.append('=' * 60)
results.append('名句匹配测试结果 (7327条数据)')
results.append('=' * 60)

for query in tests:
    results.append(f'\n输入: {query}')
    results.append('-' * 40)
    
    try:
        response = requests.post(url, json={'query': query, 'top_k': 3}, timeout=60)
        result = response.json()
        
        if result.get('results'):
            for i, r in enumerate(result['results'], 1):
                text = r['text']
                author = r.get('author', '佚名') or '佚名'
                source = r.get('source', '') or ''
                score = r['score']
                
                # 截断过长的文本
                if len(text) > 60:
                    text = text[:60] + '...'
                
                results.append(f'  {i}. {text}')
                results.append(f'     {author}《{source}》 匹配度:{score:.0%}')
        else:
            results.append('  无匹配结果')
    except Exception as e:
        results.append(f'  错误: {e}')

results.append('\n' + '=' * 60)
results.append('测试完成!')

with open('match_result.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(results))

print('结果已保存到 match_result.txt')
