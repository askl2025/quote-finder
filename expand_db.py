import requests
import json
import sqlite3
import time
from pathlib import Path

DB_PATH = Path("server/data/quotes.db")
BASE_URL = "https://raw.githubusercontent.com/chinese-poetry/chinese-poetry/master"

def get_connection():
    return sqlite3.connect(DB_PATH)

def insert_quotes(conn, quotes):
    cursor = conn.cursor()
    inserted = 0
    for quote in quotes:
        try:
            cursor.execute("""
                INSERT OR IGNORE INTO quotes (id, text, author, source, dynasty, type, tags, emotion)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                quote['id'], quote['text'], quote.get('author'), quote.get('source'),
                quote.get('dynasty'), quote.get('type'),
                json.dumps(quote.get('tags', []), ensure_ascii=False),
                json.dumps(quote.get('emotion', []), ensure_ascii=False)
            ))
            if cursor.rowcount > 0:
                inserted += 1
        except:
            pass
    conn.commit()
    return inserted

def fetch_json(url):
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None

def collect_tang_poetry(offsets, limit=3000):
    """收集唐诗"""
    print(f"Fetching 唐诗 (offsets: {offsets})...")
    quotes = []
    
    famous_poets = [
        '李白', '杜甫', '王维', '白居易', '李商隐', '杜牧',
        '王昌龄', '孟浩然', '韩愈', '柳宗元', '刘禹锡', '元稹',
        '李贺', '王之涣', '岑参', '高适', '韦应物', '李煜',
        '张九龄', '陈子昂', '张若虚', '王勃', '骆宾王',
        '贺知章', '王翰', '崔颢', '常建', '张继', '韩翃',
        '卢纶', '钱起', '刘长卿', '戴叔伦', '张籍', '王建'
    ]
    
    for offset in offsets:
        url = f"{BASE_URL}/%E5%85%A8%E5%94%90%E8%AF%97/poet.tang.{offset}.json"
        data = fetch_json(url)
        if not data:
            continue
        
        for item in data:
            author = item.get('author', '')
            paragraphs = item.get('paragraphs', [])
            text = ''.join(paragraphs)
            
            is_famous = author in famous_poets
            
            if len(text) >= 10 and (is_famous or len(text) >= 15):
                quotes.append({
                    'id': f"tang_{item.get('id', len(quotes))}",
                    'text': text[:300],
                    'author': author,
                    'source': item.get('title', ''),
                    'dynasty': '唐',
                    'type': '诗词'
                })
        
        print(f"  Offset {offset}: {len(data)} poems, total {len(quotes)}")
        
        if len(quotes) >= limit:
            break
        
        time.sleep(0.3)
    
    print(f"  Got {len(quotes)} items")
    return quotes[:limit]

def collect_song_ci(offsets, limit=2000):
    """收集宋词"""
    print(f"Fetching 宋词 (offsets: {offsets})...")
    quotes = []
    
    famous_poets = [
        '苏轼', '李清照', '辛弃疾', '柳永', '陆游', '欧阳修',
        '晏殊', '晏几道', '秦观', '周邦彦', '姜夔', '岳飞',
        '范仲淹', '王安石', '黄庭坚', '杨万里', '朱熹',
        '张先', '贺铸', '吴文英', '张炎', '周密', '史达祖'
    ]
    
    for offset in offsets:
        url = f"{BASE_URL}/%E5%AE%8B%E8%AF%8D/ci.song.{offset}.json"
        data = fetch_json(url)
        if not data:
            continue
        
        for item in data:
            author = item.get('author', '')
            paragraphs = item.get('paragraphs', [])
            text = ''.join(paragraphs)
            
            is_famous = author in famous_poets
            
            if len(text) >= 10 and (is_famous or len(text) >= 15):
                quotes.append({
                    'id': f"song_{item.get('id', len(quotes))}",
                    'text': text[:300],
                    'author': author,
                    'source': item.get('rhythmic', item.get('title', '')),
                    'dynasty': '宋',
                    'type': '词'
                })
        
        print(f"  Offset {offset}: {len(data)} ci, total {len(quotes)}")
        
        if len(quotes) >= limit:
            break
        
        time.sleep(0.3)
    
    print(f"  Got {len(quotes)} items")
    return quotes[:limit]

def collect_yuan_qu(limit=1000):
    """收集元曲"""
    print("Fetching 元曲...")
    url = f"{BASE_URL}/%E5%85%83%E6%9B%B2/yuanqu.json"
    data = fetch_json(url)
    if not data:
        print("  Failed to fetch")
        return []
    
    quotes = []
    for item in data:
        paragraphs = item.get('paragraphs', [])
        text = ''.join(paragraphs)
        
        if len(text) >= 10:
            quotes.append({
                'id': f"yuan_{item.get('id', len(quotes))}",
                'text': text[:300],
                'author': item.get('author', ''),
                'source': item.get('title', ''),
                'dynasty': '元',
                'type': '曲'
            })
    
    print(f"  Got {len(quotes)} items")
    return quotes[:limit]

def main():
    print("=" * 60)
    print("Expanding quotes database to 5000+")
    print("=" * 60)
    
    conn = get_connection()
    
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM quotes")
    current = cursor.fetchone()[0]
    print(f"Current quotes: {current}")
    
    total_added = 0
    
    # 1. 更多唐诗 (offsets 3000-8000)
    print("\n[1/3] Adding more 唐诗...")
    tang_offsets = list(range(3000, 9000, 1000))
    tang = collect_tang_poetry(tang_offsets, limit=2500)
    inserted = insert_quotes(conn, tang)
    total_added += inserted
    print(f"  Added {inserted} 唐诗")
    
    # 2. 更多宋词 (offsets 1000-5000)
    print("\n[2/3] Adding more 宋词...")
    song_offsets = list(range(1000, 6000, 1000))
    song = collect_song_ci(song_offsets, limit=2000)
    inserted = insert_quotes(conn, song)
    total_added += inserted
    print(f"  Added {inserted} 宋词")
    
    # 3. 元曲
    print("\n[3/3] Adding 元曲...")
    yuan = collect_yuan_qu(limit=1000)
    inserted = insert_quotes(conn, yuan)
    total_added += inserted
    print(f"  Added {inserted} 元曲")
    
    # 最终统计
    cursor.execute("SELECT COUNT(*) FROM quotes")
    final_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT type, COUNT(*) FROM quotes GROUP BY type ORDER BY COUNT(*) DESC")
    type_stats = cursor.fetchall()
    
    conn.close()
    
    print("\n" + "=" * 60)
    print(f"Database updated: {DB_PATH}")
    print(f"Previous: {current}")
    print(f"Added: {total_added}")
    print(f"Total: {final_count}")
    print(f"File size: {DB_PATH.stat().st_size / 1024:.1f} KB")
    print("\nBreakdown:")
    for type_name, count in type_stats:
        print(f"  {type_name}: {count}")
    print("=" * 60)

if __name__ == "__main__":
    main()
