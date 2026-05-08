import json
import re

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(data, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def is_quality_text(text):
    """检查文本质量"""
    if not text or len(text) < 8:
        return False
    if '□' in text or '■' in text or '�' in text:
        return False
    if len(text) > 200:
        return False
    # 检查中文比例
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    if chinese_chars / len(text) < 0.5:
        return False
    return True

def get_modern_quotes():
    """现代名言"""
    return [
        # 励志
        {"text": "生活不是等待暴风雨过去，而是学会在雨中跳舞", "author": "未知", "type": "现代名言", "tags": ["励志"]},
        {"text": "你不能左右天气，但可以改变心情", "author": "未知", "type": "现代名言", "tags": ["心态"]},
        {"text": "每一个不曾起舞的日子，都是对生命的辜负", "author": "尼采", "type": "现代名言", "tags": ["励志"]},
        {"text": "世上只有一种英雄主义，就是在认清生活真相之后依然热爱生活", "author": "罗曼罗兰", "type": "现代名言", "tags": ["励志"]},
        {"text": "人生就像一杯茶，不会苦一辈子，但总会苦一阵子", "author": "未知", "type": "现代名言", "tags": ["人生"]},
        {"text": "不要因为走得太远，而忘记为什么出发", "author": "未知", "type": "现代名言", "tags": ["初心"]},
        {"text": "你的问题主要在于读书不多而想得太多", "author": "杨绛", "type": "现代名言", "tags": ["学习"]},
        {"text": "人生没有彩排，每一天都是现场直播", "author": "未知", "type": "现代名言", "tags": ["人生"]},
        {"text": "好看的皮囊千篇一律，有趣的灵魂万里挑一", "author": "未知", "type": "现代名言", "tags": ["人生"]},
        {"text": "愿你出走半生，归来仍是少年", "author": "未知", "type": "现代名言", "tags": ["青春"]},
        
        # 爱情
        {"text": "我喜欢你，像风走了八千里，不问归期", "author": "未知", "type": "现代名言", "tags": ["爱情"]},
        {"text": "人生若只如初见，何事秋风悲画扇", "author": "纳兰性德", "type": "古诗词", "tags": ["爱情"]},
        {"text": "玲珑骰子安红豆，入骨相思知不知", "author": "温庭筠", "type": "古诗词", "tags": ["爱情"]},
        {"text": "曾经沧海难为水，除却巫山不是云", "author": "元稹", "type": "古诗词", "tags": ["爱情"]},
        {"text": "两情若是久长时，又岂在朝朝暮暮", "author": "秦观", "type": "古诗词", "tags": ["爱情"]},
        
        # 友情
        {"text": "海内存知己，天涯若比邻", "author": "王勃", "type": "古诗词", "tags": ["友情"]},
        {"text": "莫愁前路无知己，天下谁人不识君", "author": "高适", "type": "古诗词", "tags": ["友情"]},
        {"text": "桃花潭水深千尺，不及汪伦送我情", "author": "李白", "type": "古诗词", "tags": ["友情"]},
        
        # 思乡
        {"text": "举头望明月，低头思故乡", "author": "李白", "type": "古诗词", "tags": ["思乡"]},
        {"text": "独在异乡为异客，每逢佳节倍思亲", "author": "王维", "type": "古诗词", "tags": ["思乡"]},
        {"text": "露从今夜白，月是故乡明", "author": "杜甫", "type": "古诗词", "tags": ["思乡"]},
        
        # 人生哲理
        {"text": "人生如逆旅，我亦是行人", "author": "苏轼", "type": "古诗词", "tags": ["人生"]},
        {"text": "世事一场大梦，人生几度秋凉", "author": "苏轼", "type": "古诗词", "tags": ["人生"]},
        {"text": "人有悲欢离合，月有阴晴圆缺", "author": "苏轼", "type": "古诗词", "tags": ["人生"]},
        {"text": "山重水复疑无路，柳暗花明又一村", "author": "陆游", "type": "古诗词", "tags": ["人生"]},
        {"text": "沉舟侧畔千帆过，病树前头万木春", "author": "刘禹锡", "type": "古诗词", "tags": ["人生"]},
        
        # 励志古诗
        {"text": "长风破浪会有时，直挂云帆济沧海", "author": "李白", "type": "古诗词", "tags": ["励志"]},
        {"text": "会当凌绝顶，一览众山小", "author": "杜甫", "type": "古诗词", "tags": ["励志"]},
        {"text": "千磨万击还坚劲，任尔东西南北风", "author": "郑燮", "type": "古诗词", "tags": ["励志"]},
        {"text": "宝剑锋从磨砺出，梅花香自苦寒来", "author": "佚名", "type": "古诗词", "tags": ["励志"]},
        {"text": "少壮不努力，老大徒伤悲", "author": "佚名", "type": "古诗词", "tags": ["励志"]},
        {"text": "天生我材必有用，千金散尽还复来", "author": "李白", "type": "古诗词", "tags": ["励志"]},
        
        # 自然
        {"text": "接天莲叶无穷碧，映日荷花别样红", "author": "杨万里", "type": "古诗词", "tags": ["自然"]},
        {"text": "小荷才露尖尖角，早有蜻蜓立上头", "author": "杨万里", "type": "古诗词", "tags": ["自然"]},
        {"text": "忽如一夜春风来，千树万树梨花开", "author": "岑参", "type": "古诗词", "tags": ["自然"]},
        {"text": "大漠孤烟直，长河落日圆", "author": "王维", "type": "古诗词", "tags": ["自然"]},
        {"text": "明月松间照，清泉石上流", "author": "王维", "type": "古诗词", "tags": ["自然"]},
        
        # 学习
        {"text": "学而时习之，不亦说乎", "author": "孔子", "type": "古文", "tags": ["学习"]},
        {"text": "温故而知新，可以为师矣", "author": "孔子", "type": "古文", "tags": ["学习"]},
        {"text": "学而不思则罔，思而不学则殆", "author": "孔子", "type": "古文", "tags": ["学习"]},
        {"text": "三人行，必有我师焉", "author": "孔子", "type": "古文", "tags": ["学习"]},
        {"text": "知之者不如好之者，好之者不如乐之者", "author": "孔子", "type": "古文", "tags": ["学习"]},
        {"text": "书山有路勤为径，学海无涯苦作舟", "author": "韩愈", "type": "古文", "tags": ["学习"]},
        {"text": "业精于勤荒于嬉，行成于思毁于随", "author": "韩愈", "type": "古文", "tags": ["学习"]},
        
        # 品德
        {"text": "己所不欲，勿施于人", "author": "孔子", "type": "古文", "tags": ["品德"]},
        {"text": "君子坦荡荡，小人长戚戚", "author": "孔子", "type": "古文", "tags": ["品德"]},
        {"text": "静以修身，俭以养德", "author": "诸葛亮", "type": "古文", "tags": ["品德"]},
        {"text": "非淡泊无以明志，非宁静无以致远", "author": "诸葛亮", "type": "古文", "tags": ["品德"]},
        {"text": "鞠躬尽瘁，死而后已", "author": "诸葛亮", "type": "古文", "tags": ["品德"]},
        
        # 爱国
        {"text": "人生自古谁无死，留取丹心照汗青", "author": "文天祥", "type": "古诗词", "tags": ["爱国"]},
        {"text": "王师北定中原日，家祭无忘告乃翁", "author": "陆游", "type": "古诗词", "tags": ["爱国"]},
        {"text": "苟利国家生死以，岂因祸福避趋之", "author": "林则徐", "type": "古诗词", "tags": ["爱国"]},
        {"text": "先天下之忧而忧，后天下之乐而乐", "author": "范仲淹", "type": "古文", "tags": ["爱国"]},
        
        # 哲理
        {"text": "千里之行，始于足下", "author": "老子", "type": "古文", "tags": ["哲理"]},
        {"text": "上善若水", "author": "老子", "type": "古文", "tags": ["哲理"]},
        {"text": "知人者智，自知者明", "author": "老子", "type": "古文", "tags": ["哲理"]},
        {"text": "天行健，君子以自强不息", "author": "佚名", "type": "古文", "tags": ["哲理"]},
        {"text": "穷则独善其身，达则兼济天下", "author": "孟子", "type": "古文", "tags": ["哲理"]},
        
        # 生活
        {"text": "采菊东篱下，悠然见南山", "author": "陶渊明", "type": "古诗词", "tags": ["生活"]},
        {"text": "行到水穷处，坐看云起时", "author": "王维", "type": "古诗词", "tags": ["生活"]},
        {"text": "但愿人长久，千里共婵娟", "author": "苏轼", "type": "古诗词", "tags": ["生活"]},
        
        # 离别
        {"text": "劝君更尽一杯酒，西出阳关无故人", "author": "王维", "type": "古诗词", "tags": ["离别"]},
        {"text": "洛阳亲友如相问，一片冰心在玉壶", "author": "王昌龄", "type": "古诗词", "tags": ["离别"]},
        {"text": "相见时难别亦难，东风无力百花残", "author": "李商隐", "type": "古诗词", "tags": ["离别"]},
        
        # 时间
        {"text": "盛年不重来，一日难再晨", "author": "陶渊明", "type": "古诗词", "tags": ["时间"]},
        {"text": "及时当勉励，岁月不待人", "author": "陶渊明", "type": "古诗词", "tags": ["时间"]},
        {"text": "莫等闲，白了少年头，空悲切", "author": "岳飞", "type": "古诗词", "tags": ["时间"]},
        
        # 孤独
        {"text": "前不见古人，后不见来者", "author": "陈子昂", "type": "古诗词", "tags": ["孤独"]},
        {"text": "独在异乡为异客", "author": "王维", "type": "古诗词", "tags": ["孤独"]},
        {"text": "举杯邀明月，对影成三人", "author": "李白", "type": "古诗词", "tags": ["孤独"]},
        
        # 坚持
        {"text": "锲而不舍，金石可镂", "author": "荀子", "type": "古文", "tags": ["坚持"]},
        {"text": "不积跬步，无以至千里", "author": "荀子", "type": "古文", "tags": ["坚持"]},
        {"text": "路漫漫其修远兮，吾将上下而求索", "author": "屈原", "type": "古诗词", "tags": ["坚持"]},
        
        # 现代生活感悟
        {"text": "人生就像一场旅行，不必在乎目的地，在乎的是沿途的风景", "author": "未知", "type": "现代名言", "tags": ["人生"]},
        {"text": "简单的生活，高贵的灵魂，是人生的至高境界", "author": "未知", "type": "现代名言", "tags": ["生活"]},
        {"text": "真正的平静，不是避开车马喧嚣，而是在心中修篱种菊", "author": "未知", "type": "现代名言", "tags": ["生活"]},
        {"text": "你若盛开，蝴蝶自来", "author": "未知", "type": "现代名言", "tags": ["励志"]},
        {"text": "温柔半两，从容一生", "author": "三毛", "type": "现代名言", "tags": ["生活"]},
        {"text": "心若向阳，无畏悲伤", "author": "未知", "type": "现代名言", "tags": ["心态"]},
        {"text": "岁月不饶人，我亦未曾饶过岁月", "author": "木心", "type": "现代名言", "tags": ["人生"]},
        {"text": "从前慢，一生只够爱一个人", "author": "木心", "type": "现代名言", "tags": ["爱情"]},
        {"text": "你站在桥上看风景，看风景的人在楼上看你", "author": "卞之琳", "type": "现代名言", "tags": ["哲理"]},
        {"text": "黑夜给了我黑色的眼睛，我却用它寻找光明", "author": "顾城", "type": "现代名言", "tags": ["励志"]},
        {"text": "草在结它的种子，风在摇它的叶子，我们站着，不说话，就十分美好", "author": "顾城", "type": "现代名言", "tags": ["生活"]},
        {"text": "从明天起，做一个幸福的人，喂马、劈柴、周游世界", "author": "海子", "type": "现代名言", "tags": ["生活"]},
        {"text": "面朝大海，春暖花开", "author": "海子", "type": "现代名言", "tags": ["生活"]},
        {"text": "人生得意须尽欢，莫使金樽空对月", "author": "李白", "type": "古诗词", "tags": ["人生"]},
        {"text": "对酒当歌，人生几何", "author": "曹操", "type": "古诗词", "tags": ["人生"]},
        {"text": "老骥伏枥，志在千里", "author": "曹操", "type": "古诗词", "tags": ["励志"]},
    ]

def main():
    print("=" * 60)
    print("Optimizing dataset...")
    print("=" * 60)
    
    # 加载现有数据
    quotes = load_json('server/data/quotes.json')
    print(f"Original: {len(quotes)} quotes")
    
    # 统计各类型
    type_stats = {}
    for q in quotes:
        t = q.get('type', 'unknown')
        type_stats[t] = type_stats.get(t, 0) + 1
    print(f"Type distribution: {type_stats}")
    
    # 分离元曲和其他
    yuanqu = [q for q in quotes if q.get('type') == '曲']
    others = [q for q in quotes if q.get('type') != '曲']
    
    # 限制元曲数量（只保留高质量的）
    yuanqu_kept = [q for q in yuanqu if is_quality_text(q.get('text', ''))][:500]
    print(f"Yuanqu: {len(yuanqu)} -> {len(yuanqu_kept)}")
    
    # 添加现代名言
    modern = get_modern_quotes()
    print(f"Modern quotes: {len(modern)}")
    
    # 合并
    final = others + yuanqu_kept + modern
    
    # 去重
    seen = set()
    unique = []
    for q in final:
        text = q.get('text', '')
        if text not in seen:
            seen.add(text)
            unique.append(q)
    
    print(f"Final: {len(unique)} unique quotes")
    
    # 统计最终类型分布
    final_stats = {}
    for q in unique:
        t = q.get('type', 'unknown')
        final_stats[t] = final_stats.get(t, 0) + 1
    print(f"Final type distribution: {final_stats}")
    
    # 保存
    save_json(unique, 'server/data/quotes.json')
    print(f"Saved to server/data/quotes.json")

if __name__ == "__main__":
    main()
