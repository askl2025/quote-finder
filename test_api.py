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

print('=' * 60)
print('名句匹配测试')
print('=' * 60)

for query in tests:
    print(f'\n输入: {query}')
    print('-' * 40)
    
    try:
        response = requests.post(url, json={'query': query, 'top_k': 3}, timeout=60)
        result = response.json()
        
        for i, r in enumerate(result['results'], 1):
            text = r['text']
            author = r.get('author', '佚名') or '佚名'
            source = r.get('source', '') or ''
            score = r['score']
            print(f'  {i}. {text}')
            print(f'     {author}《{source}》 匹配度:{score:.0%}')
    except Exception as e:
        print(f'  错误: {e}')

print('\n' + '=' * 60)
print('测试完成!')
