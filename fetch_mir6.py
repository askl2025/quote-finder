import requests
import json
import time

def fetch_mir6_quotes(txt, name, target_count=100):
    """批量获取米人语录"""
    url = f'https://api.mir6.com/api/yulu?type=json&txt={txt}'
    
    quotes = []
    seen = set()
    attempts = 0
    max_attempts = target_count * 3  # 最多尝试3倍次数
    
    print(f"Fetching {name} (txt={txt}), target: {target_count}...")
    
    while len(quotes) < target_count and attempts < max_attempts:
        try:
            r = requests.get(url, timeout=15)
            if r.status_code == 200:
                data = r.json()
                text = data.get('text', '').strip()
                
                if text and text not in seen and len(text) >= 8:
                    seen.add(text)
                    quotes.append({
                        'id': f'mir6_{txt}_{len(quotes)}',
                        'text': text,
                        'author': '米人语录',
                        'source': name,
                        'dynasty': '现代',
                        'type': '现代名言',
                        'tags': ['米人语录', name]
                    })
            
            attempts += 1
            
            # 控制QPS
            time.sleep(0.1)
                
        except Exception as e:
            print(f"  Error: {e}")
            time.sleep(1)
    
    print(f"  Fetched: {len(quotes)} quotes (attempts: {attempts})")
    return quotes

def main():
    print("=" * 60)
    print("Fetching quotes from 米人语录 API")
    print("=" * 60)
    
    all_quotes = []
    
    # 14: 经典语录
    quotes_14 = fetch_mir6_quotes(14, '经典语录', target_count=100)
    all_quotes.extend(quotes_14)
    
    # 7: 爱情语录
    quotes_7 = fetch_mir6_quotes(7, '爱情语录', target_count=100)
    all_quotes.extend(quotes_7)
    
    # 9: 伤感语录
    quotes_9 = fetch_mir6_quotes(9, '伤感语录', target_count=100)
    all_quotes.extend(quotes_9)
    
    # 保存
    output_file = 'server/data/mir6_quotes.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_quotes, f, ensure_ascii=False, indent=2)
    
    print("\n" + "=" * 60)
    print(f"Total: {len(all_quotes)} quotes")
    print(f"Saved to: {output_file}")
    print("=" * 60)

if __name__ == "__main__":
    main()
