import requests
import json
import os

def download_hitokoto():
    """下载hitokoto三个JSON文件"""
    base_url = "https://raw.githubusercontent.com/hitokoto-osc/sentences-bundle/master/sentences"
    
    categories = {
        'd': '文学',
        'i': '诗词',
        'k': '哲学'
    }
    
    os.makedirs('data/hitokoto', exist_ok=True)
    
    for key, name in categories.items():
        url = f"{base_url}/{key}.json"
        print(f"Downloading {name} ({key}.json)...")
        
        try:
            response = requests.get(url, timeout=120)
            if response.status_code == 200:
                data = response.json()
                
                # 保存原始文件
                with open(f'data/hitokoto/{key}.json', 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                
                print(f"  Downloaded: {len(data)} entries")
            else:
                print(f"  Error: HTTP {response.status_code}")
        except Exception as e:
            print(f"  Error: {e}")

if __name__ == "__main__":
    download_hitokoto()
