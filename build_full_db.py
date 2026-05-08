import requests
import json
import sqlite3
import time
from pathlib import Path

DB_PATH = Path("server/data/quotes.db")

BASE_URL = "https://raw.githubusercontent.com/chinese-poetry/chinese-poetry/master"

def create_database():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS quotes")
    cursor.execute("""
        CREATE TABLE quotes (
            id TEXT PRIMARY KEY,
            text TEXT NOT NULL,
            author TEXT,
            source TEXT,
            dynasty TEXT,
            type TEXT,
            tags TEXT,
            emotion TEXT
        )
    """)
    cursor.execute("CREATE INDEX idx_type ON quotes(type)")
    cursor.execute("CREATE INDEX idx_dynasty ON quotes(dynasty)")
    conn.commit()
    return conn

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
        except Exception as e:
            pass
    conn.commit()
    return inserted

def fetch_json(url):
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"  Error: {e}")
    return None

def collect_shijing():
    """收集诗经"""
    print("Fetching 诗经...")
    url = f"{BASE_URL}/%E8%AF%97%E7%BB%8F/shijing.json"
    data = fetch_json(url)
    if not data:
        return []
    
    quotes = []
    for item in data:
        content = item.get('content', [])
        if isinstance(content, list):
            text = ''.join(content)
        else:
            text = str(content)
        
        if len(text) >= 10:
            quotes.append({
                'id': f"shijing_{item.get('title', len(quotes))}",
                'text': text[:200],
                'author': '佚名',
                'source': item.get('title', '诗经'),
                'dynasty': '先秦',
                'type': '诗经'
            })
    
    print(f"  Got {len(quotes)} items")
    return quotes

def collect_lunyu():
    """收集论语"""
    print("Fetching 论语...")
    url = f"{BASE_URL}/%E8%AE%BA%E8%AF%AD/lunyu.json"
    data = fetch_json(url)
    if not data:
        return []
    
    quotes = []
    for item in data:
        paragraphs = item.get('paragraphs', [])
        for para in paragraphs:
            if len(para) >= 10:
                quotes.append({
                    'id': f"lunyu_{len(quotes)}",
                    'text': para,
                    'author': '孔子',
                    'source': '论语',
                    'dynasty': '春秋',
                    'type': '经典'
                })
    
    print(f"  Got {len(quotes)} items")
    return quotes

def collect_chuci():
    """收集楚辞"""
    print("Fetching 楚辞...")
    url = f"{BASE_URL}/%E6%A5%9A%E8%BE%9E/chuci.json"
    data = fetch_json(url)
    if not data:
        return []
    
    quotes = []
    for item in data:
        paragraphs = item.get('paragraphs', [])
        for para in paragraphs:
            if len(para) >= 10:
                quotes.append({
                    'id': f"chuci_{len(quotes)}",
                    'text': para,
                    'author': item.get('author', '屈原'),
                    'source': item.get('title', '楚辞'),
                    'dynasty': '战国',
                    'type': '楚辞'
                })
    
    print(f"  Got {len(quotes)} items")
    return quotes

def collect_tang_poetry(limit=3000):
    """收集唐诗（选择性）"""
    print("Fetching 唐诗...")
    quotes = []
    
    # 知名诗人列表
    famous_poets = [
        '李白', '杜甫', '王维', '白居易', '李商隐', '杜牧',
        '王昌龄', '孟浩然', '韩愈', '柳宗元', '刘禹锡', '元稹',
        '李贺', '王之涣', '岑参', '高适', '韦应物', '李煜',
        '张九龄', '陈子昂', '张若虚', '王勃', '骆宾王'
    ]
    
    for i in range(0, 58):
        url = f"{BASE_URL}/%E5%85%A8%E5%94%90%E8%AF%97/poet.tang.{i}.json"
        data = fetch_json(url)
        if not data:
            continue
        
        for item in data:
            author = item.get('author', '')
            paragraphs = item.get('paragraphs', [])
            text = ''.join(paragraphs)
            
            # 优先收录知名诗人
            is_famous = author in famous_poets
            
            # 过滤条件：长度>=10字，且（知名诗人或长度>=20字）
            if len(text) >= 10 and (is_famous or len(text) >= 20):
                quotes.append({
                    'id': f"tang_{item.get('id', len(quotes))}",
                    'text': text[:300],
                    'author': author,
                    'source': item.get('title', ''),
                    'dynasty': '唐',
                    'type': '诗词'
                })
        
        print(f"  Batch {i}: {len(data)} poems, total {len(quotes)}")
        
        if len(quotes) >= limit:
            break
        
        time.sleep(0.3)
    
    print(f"  Got {len(quotes)} items")
    return quotes[:limit]

def collect_song_ci(limit=2000):
    """收集宋词"""
    print("Fetching 宋词...")
    quotes = []
    
    # 知名词人
    famous_poets = [
        '苏轼', '李清照', '辛弃疾', '柳永', '陆游', '欧阳修',
        '晏殊', '晏几道', '秦观', '周邦彦', '姜夔', '岳飞',
        '范仲淹', '王安石', '黄庭坚', '杨万里', '朱熹'
    ]
    
    for i in range(0, 22):
        url = f"{BASE_URL}/%E5%AE%8B%E8%AF%8D/ci.song.{i}.json"
        data = fetch_json(url)
        if not data:
            continue
        
        for item in data:
            author = item.get('author', '')
            paragraphs = item.get('paragraphs', [])
            text = ''.join(paragraphs)
            
            is_famous = author in famous_poets
            
            if len(text) >= 10 and (is_famous or len(text) >= 20):
                quotes.append({
                    'id': f"song_{item.get('id', len(quotes))}",
                    'text': text[:300],
                    'author': author,
                    'source': item.get('rhythmic', item.get('title', '')),
                    'dynasty': '宋',
                    'type': '词'
                })
        
        print(f"  Batch {i}: {len(data)} ci, total {len(quotes)}")
        
        if len(quotes) >= limit:
            break
        
        time.sleep(0.3)
    
    print(f"  Got {len(quotes)} items")
    return quotes[:limit]

def collect_classic_quotes():
    """内置经典名句（精选）"""
    quotes = [
        # 论语精选
        {"text": "学而时习之，不亦说乎", "author": "孔子", "source": "论语", "dynasty": "春秋"},
        {"text": "温故而知新，可以为师矣", "author": "孔子", "source": "论语", "dynasty": "春秋"},
        {"text": "学而不思则罔，思而不学则殆", "author": "孔子", "source": "论语", "dynasty": "春秋"},
        {"text": "己所不欲，勿施于人", "author": "孔子", "source": "论语", "dynasty": "春秋"},
        {"text": "三人行，必有我师焉", "author": "孔子", "source": "论语", "dynasty": "春秋"},
        {"text": "君子坦荡荡，小人长戚戚", "author": "孔子", "source": "论语", "dynasty": "春秋"},
        {"text": "知之者不如好之者，好之者不如乐之者", "author": "孔子", "source": "论语", "dynasty": "春秋"},
        {"text": "敏而好学，不耻下问", "author": "孔子", "source": "论语", "dynasty": "春秋"},
        
        # 孟子
        {"text": "生于忧患，死于安乐", "author": "孟子", "source": "孟子", "dynasty": "战国"},
        {"text": "得道多助，失道寡助", "author": "孟子", "source": "孟子", "dynasty": "战国"},
        {"text": "富贵不能淫，贫贱不能移，威武不能屈", "author": "孟子", "source": "孟子", "dynasty": "战国"},
        {"text": "穷则独善其身，达则兼济天下", "author": "孟子", "source": "孟子", "dynasty": "战国"},
        
        # 周易
        {"text": "天行健，君子以自强不息", "author": "佚名", "source": "周易", "dynasty": "先秦"},
        {"text": "地势坤，君子以厚德载物", "author": "佚名", "source": "周易", "dynasty": "先秦"},
        
        # 老子
        {"text": "千里之行，始于足下", "author": "老子", "source": "道德经", "dynasty": "春秋"},
        {"text": "上善若水", "author": "老子", "source": "道德经", "dynasty": "春秋"},
        {"text": "知人者智，自知者明", "author": "老子", "source": "道德经", "dynasty": "春秋"},
        
        # 荀子
        {"text": "锲而不舍，金石可镂", "author": "荀子", "source": "劝学", "dynasty": "战国"},
        {"text": "不积跬步，无以至千里", "author": "荀子", "source": "劝学", "dynasty": "战国"},
        
        # 屈原
        {"text": "路漫漫其修远兮，吾将上下而求索", "author": "屈原", "source": "离骚", "dynasty": "战国"},
        {"text": "长太息以掩涕兮，哀民生之多艰", "author": "屈原", "source": "离骚", "dynasty": "战国"},
        
        # 曹操
        {"text": "老骥伏枥，志在千里", "author": "曹操", "source": "龟虽寿", "dynasty": "东汉"},
        {"text": "对酒当歌，人生几何", "author": "曹操", "source": "短歌行", "dynasty": "东汉"},
        
        # 诸葛亮
        {"text": "鞠躬尽瘁，死而后已", "author": "诸葛亮", "source": "后出师表", "dynasty": "三国"},
        {"text": "非淡泊无以明志，非宁静无以致远", "author": "诸葛亮", "source": "诫子书", "dynasty": "三国"},
        
        # 陶渊明
        {"text": "采菊东篱下，悠然见南山", "author": "陶渊明", "source": "饮酒", "dynasty": "东晋"},
        {"text": "盛年不重来，一日难再晨", "author": "陶渊明", "source": "杂诗", "dynasty": "东晋"},
        
        # 励志
        {"text": "少壮不努力，老大徒伤悲", "author": "佚名", "source": "长歌行", "dynasty": "汉"},
        {"text": "宝剑锋从磨砺出，梅花香自苦寒来", "author": "佚名", "source": "警世贤文", "dynasty": "明"},
        {"text": "千磨万击还坚劲，任尔东西南北风", "author": "郑燮", "source": "竹石", "dynasty": "清"},
        
        # 爱国
        {"text": "天下兴亡，匹夫有责", "author": "顾炎武", "source": "日知录", "dynasty": "明"},
        {"text": "苟利国家生死以，岂因祸福避趋之", "author": "林则徐", "source": "赴戍登程口占示家人", "dynasty": "清"},
        
        # 近现代
        {"text": "横眉冷对千夫指，俯首甘为孺子牛", "author": "鲁迅", "source": "自嘲", "dynasty": "近代"},
        {"text": "世上本没有路，走的人多了也便成了路", "author": "鲁迅", "source": "故乡", "dynasty": "近代"},
    ]
    
    result = []
    for i, q in enumerate(quotes):
        result.append({
            'id': f"classic_{i}",
            'text': q['text'],
            'author': q.get('author'),
            'source': q.get('source'),
            'dynasty': q.get('dynasty'),
            'type': '名句'
        })
    return result

def main():
    print("=" * 60)
    print("Building comprehensive quotes database")
    print("=" * 60)
    
    conn = create_database()
    total = 0
    
    # 1. 经典名句
    print("\n[1/5] Adding classic quotes...")
    classics = collect_classic_quotes()
    inserted = insert_quotes(conn, classics)
    total += inserted
    print(f"  Added {inserted} classic quotes")
    
    # 2. 诗经
    print("\n[2/5] Adding 诗经...")
    shijing = collect_shijing()
    inserted = insert_quotes(conn, shijing)
    total += inserted
    print(f"  Added {inserted} 诗经 items")
    
    # 3. 论语
    print("\n[3/5] Adding 论语...")
    lunyu = collect_lunyu()
    inserted = insert_quotes(conn, lunyu)
    total += inserted
    print(f"  Added {inserted} 论语 items")
    
    # 4. 唐诗
    print("\n[4/5] Adding 唐诗...")
    tang = collect_tang_poetry(limit=3000)
    inserted = insert_quotes(conn, tang)
    total += inserted
    print(f"  Added {inserted} 唐诗 items")
    
    # 5. 宋词
    print("\n[5/5] Adding 宋词...")
    song = collect_song_ci(limit=2000)
    inserted = insert_quotes(conn, song)
    total += inserted
    print(f"  Added {inserted} 宋词 items")
    
    conn.close()
    
    print("\n" + "=" * 60)
    print(f"Database created: {DB_PATH}")
    print(f"Total quotes: {total}")
    print(f"File size: {DB_PATH.stat().st_size / 1024:.1f} KB")
    print("=" * 60)

if __name__ == "__main__":
    main()
