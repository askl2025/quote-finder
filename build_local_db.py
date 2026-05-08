import sqlite3
import json
import requests
import time
from pathlib import Path

DB_PATH = Path("server/data/quotes.db")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def create_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quotes (
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
        except:
            pass
    conn.commit()
    return inserted

def collect_classic_quotes():
    quotes = [
        # 论语
        {"text": "学而时习之，不亦说乎", "author": "孔子", "source": "论语", "dynasty": "春秋"},
        {"text": "温故而知新，可以为师矣", "author": "孔子", "source": "论语", "dynasty": "春秋"},
        {"text": "学而不思则罔，思而不学则殆", "author": "孔子", "source": "论语", "dynasty": "春秋"},
        {"text": "知之为知之，不知为不知，是知也", "author": "孔子", "source": "论语", "dynasty": "春秋"},
        {"text": "己所不欲，勿施于人", "author": "孔子", "source": "论语", "dynasty": "春秋"},
        {"text": "三人行，必有我师焉", "author": "孔子", "source": "论语", "dynasty": "春秋"},
        {"text": "君子坦荡荡，小人长戚戚", "author": "孔子", "source": "论语", "dynasty": "春秋"},
        {"text": "见贤思齐焉，见不贤而内自省也", "author": "孔子", "source": "论语", "dynasty": "春秋"},
        {"text": "德不孤，必有邻", "author": "孔子", "source": "论语", "dynasty": "春秋"},
        {"text": "敏而好学，不耻下问", "author": "孔子", "source": "论语", "dynasty": "春秋"},
        {"text": "知之者不如好之者，好之者不如乐之者", "author": "孔子", "source": "论语", "dynasty": "春秋"},
        {"text": "默而识之，学而不厌，诲人不倦", "author": "孔子", "source": "论语", "dynasty": "春秋"},
        {"text": "发愤忘食，乐以忘忧", "author": "孔子", "source": "论语", "dynasty": "春秋"},
        
        # 孟子
        {"text": "生于忧患，死于安乐", "author": "孟子", "source": "孟子", "dynasty": "战国"},
        {"text": "得道多助，失道寡助", "author": "孟子", "source": "孟子", "dynasty": "战国"},
        {"text": "富贵不能淫，贫贱不能移，威武不能屈", "author": "孟子", "source": "孟子", "dynasty": "战国"},
        {"text": "老吾老以及人之老，幼吾幼以及人之幼", "author": "孟子", "source": "孟子", "dynasty": "战国"},
        {"text": "天时不如地利，地利不如人和", "author": "孟子", "source": "孟子", "dynasty": "战国"},
        {"text": "穷则独善其身，达则兼济天下", "author": "孟子", "source": "孟子", "dynasty": "战国"},
        
        # 周易
        {"text": "天行健，君子以自强不息", "author": "佚名", "source": "周易", "dynasty": "先秦"},
        {"text": "地势坤，君子以厚德载物", "author": "佚名", "source": "周易", "dynasty": "先秦"},
        {"text": "穷则变，变则通，通则久", "author": "佚名", "source": "周易", "dynasty": "先秦"},
        
        # 老子
        {"text": "千里之行，始于足下", "author": "老子", "source": "道德经", "dynasty": "春秋"},
        {"text": "上善若水", "author": "老子", "source": "道德经", "dynasty": "春秋"},
        {"text": "知人者智，自知者明", "author": "老子", "source": "道德经", "dynasty": "春秋"},
        {"text": "大器晚成", "author": "老子", "source": "道德经", "dynasty": "春秋"},
        
        # 荀子
        {"text": "锲而不舍，金石可镂", "author": "荀子", "source": "劝学", "dynasty": "战国"},
        {"text": "不积跬步，无以至千里", "author": "荀子", "source": "劝学", "dynasty": "战国"},
        {"text": "青出于蓝而胜于蓝", "author": "荀子", "source": "劝学", "dynasty": "战国"},
        
        # 屈原
        {"text": "路漫漫其修远兮，吾将上下而求索", "author": "屈原", "source": "离骚", "dynasty": "战国"},
        {"text": "长太息以掩涕兮，哀民生之多艰", "author": "屈原", "source": "离骚", "dynasty": "战国"},
        {"text": "亦余心之所善兮，虽九死其犹未悔", "author": "屈原", "source": "离骚", "dynasty": "战国"},
        
        # 曹操
        {"text": "老骥伏枥，志在千里", "author": "曹操", "source": "龟虽寿", "dynasty": "东汉"},
        {"text": "烈士暮年，壮心不已", "author": "曹操", "source": "龟虽寿", "dynasty": "东汉"},
        {"text": "山不厌高，海不厌深", "author": "曹操", "source": "短歌行", "dynasty": "东汉"},
        {"text": "对酒当歌，人生几何", "author": "曹操", "source": "短歌行", "dynasty": "东汉"},
        {"text": "周公吐哺，天下归心", "author": "曹操", "source": "短歌行", "dynasty": "东汉"},
        
        # 曹植
        {"text": "捐躯赴国难，视死忽如归", "author": "曹植", "source": "白马篇", "dynasty": "三国"},
        {"text": "本是同根生，相煎何太急", "author": "曹植", "source": "七步诗", "dynasty": "三国"},
        
        # 诸葛亮
        {"text": "鞠躬尽瘁，死而后已", "author": "诸葛亮", "source": "后出师表", "dynasty": "三国"},
        {"text": "非淡泊无以明志，非宁静无以致远", "author": "诸葛亮", "source": "诫子书", "dynasty": "三国"},
        {"text": "静以修身，俭以养德", "author": "诸葛亮", "source": "诫子书", "dynasty": "三国"},
        
        # 陶渊明
        {"text": "采菊东篱下，悠然见南山", "author": "陶渊明", "source": "饮酒", "dynasty": "东晋"},
        {"text": "羁鸟恋旧林，池鱼思故渊", "author": "陶渊明", "source": "归园田居", "dynasty": "东晋"},
        {"text": "盛年不重来，一日难再晨", "author": "陶渊明", "source": "杂诗", "dynasty": "东晋"},
        {"text": "及时当勉励，岁月不待人", "author": "陶渊明", "source": "杂诗", "dynasty": "东晋"},
        
        # 唐代名句
        {"text": "海内存知己，天涯若比邻", "author": "王勃", "source": "送杜少府之任蜀州", "dynasty": "唐"},
        {"text": "落霞与孤鹜齐飞，秋水共长天一色", "author": "王勃", "source": "滕王阁序", "dynasty": "唐"},
        {"text": "前不见古人，后不见来者", "author": "陈子昂", "source": "登幽州台歌", "dynasty": "唐"},
        {"text": "念天地之悠悠，独怆然而涕下", "author": "陈子昂", "source": "登幽州台歌", "dynasty": "唐"},
        {"text": "春江潮水连海平，海上明月共潮生", "author": "张若虚", "source": "春江花月夜", "dynasty": "唐"},
        {"text": "人生代代无穷已，江月年年望相似", "author": "张若虚", "source": "春江花月夜", "dynasty": "唐"},
        {"text": "欲穷千里目，更上一层楼", "author": "王之涣", "source": "登鹳雀楼", "dynasty": "唐"},
        {"text": "黄河远上白云间，一片孤城万仞山", "author": "王之涣", "source": "凉州词", "dynasty": "唐"},
        {"text": "独在异乡为异客，每逢佳节倍思亲", "author": "王维", "source": "九月九日忆山东兄弟", "dynasty": "唐"},
        {"text": "劝君更尽一杯酒，西出阳关无故人", "author": "王维", "source": "送元二使安西", "dynasty": "唐"},
        {"text": "大漠孤烟直，长河落日圆", "author": "王维", "source": "使至塞上", "dynasty": "唐"},
        {"text": "明月松间照，清泉石上流", "author": "王维", "source": "山居秋暝", "dynasty": "唐"},
        {"text": "行到水穷处，坐看云起时", "author": "王维", "source": "终南别业", "dynasty": "唐"},
        {"text": "天生我材必有用，千金散尽还复来", "author": "李白", "source": "将进酒", "dynasty": "唐"},
        {"text": "长风破浪会有时，直挂云帆济沧海", "author": "李白", "source": "行路难", "dynasty": "唐"},
        {"text": "举杯邀明月，对影成三人", "author": "李白", "source": "月下独酌", "dynasty": "唐"},
        {"text": "抽刀断水水更流，举杯消愁愁更愁", "author": "李白", "source": "宣州谢朓楼饯别校书叔云", "dynasty": "唐"},
        {"text": "安能摧眉折腰事权贵，使我不得开心颜", "author": "李白", "source": "梦游天姥吟留别", "dynasty": "唐"},
        {"text": "仰天大笑出门去，我辈岂是蓬蒿人", "author": "李白", "source": "南陵别儿童入京", "dynasty": "唐"},
        {"text": "会当凌绝顶，一览众山小", "author": "杜甫", "source": "望岳", "dynasty": "唐"},
        {"text": "读书破万卷，下笔如有神", "author": "杜甫", "source": "奉赠韦左丞丈二十二韵", "dynasty": "唐"},
        {"text": "出师未捷身先死，长使英雄泪满襟", "author": "杜甫", "source": "蜀相", "dynasty": "唐"},
        {"text": "无边落木萧萧下，不尽长江滚滚来", "author": "杜甫", "source": "登高", "dynasty": "唐"},
        {"text": "安得广厦千万间，大庇天下寒士俱欢颜", "author": "杜甫", "source": "茅屋为秋风所破歌", "dynasty": "唐"},
        {"text": "露从今夜白，月是故乡明", "author": "杜甫", "source": "月夜忆舍弟", "dynasty": "唐"},
        {"text": "忽如一夜春风来，千树万树梨花开", "author": "岑参", "source": "白雪歌送武判官归京", "dynasty": "唐"},
        {"text": "沉舟侧畔千帆过，病树前头万木春", "author": "刘禹锡", "source": "酬乐天扬州初逢席上见赠", "dynasty": "唐"},
        {"text": "旧时王谢堂前燕，飞入寻常百姓家", "author": "刘禹锡", "source": "乌衣巷", "dynasty": "唐"},
        {"text": "千淘万漉虽辛苦，吹尽狂沙始到金", "author": "刘禹锡", "source": "浪淘沙", "dynasty": "唐"},
        {"text": "野火烧不尽，春风吹又生", "author": "白居易", "source": "赋得古原草送别", "dynasty": "唐"},
        {"text": "同是天涯沦落人，相逢何必曾相识", "author": "白居易", "source": "琵琶行", "dynasty": "唐"},
        {"text": "在天愿作比翼鸟，在地愿为连理枝", "author": "白居易", "source": "长恨歌", "dynasty": "唐"},
        {"text": "千呼万唤始出来，犹抱琵琶半遮面", "author": "白居易", "source": "琵琶行", "dynasty": "唐"},
        {"text": "曾经沧海难为水，除却巫山不是云", "author": "元稹", "source": "离思", "dynasty": "唐"},
        {"text": "黑云压城城欲摧，甲光向日金鳞开", "author": "李贺", "source": "雁门太守行", "dynasty": "唐"},
        {"text": "男儿何不带吴钩，收取关山五十州", "author": "李贺", "source": "南园", "dynasty": "唐"},
        {"text": "商女不知亡国恨，隔江犹唱后庭花", "author": "杜牧", "source": "泊秦淮", "dynasty": "唐"},
        {"text": "停车坐爱枫林晚，霜叶红于二月花", "author": "杜牧", "source": "山行", "dynasty": "唐"},
        {"text": "东风不与周郎便，铜雀春深锁二乔", "author": "杜牧", "source": "赤壁", "dynasty": "唐"},
        {"text": "春蚕到死丝方尽，蜡炬成灰泪始干", "author": "李商隐", "source": "无题", "dynasty": "唐"},
        {"text": "身无彩凤双飞翼，心有灵犀一点通", "author": "李商隐", "source": "无题", "dynasty": "唐"},
        {"text": "夕阳无限好，只是近黄昏", "author": "李商隐", "source": "登乐游原", "dynasty": "唐"},
        {"text": "黄沙百战穿金甲，不破楼兰终不还", "author": "王昌龄", "source": "从军行", "dynasty": "唐"},
        {"text": "洛阳亲友如相问，一片冰心在玉壶", "author": "王昌龄", "source": "芙蓉楼送辛渐", "dynasty": "唐"},
        {"text": "莫愁前路无知己，天下谁人不识君", "author": "高适", "source": "别董大", "dynasty": "唐"},
        {"text": "桃花潭水深千尺，不及汪伦送我情", "author": "李白", "source": "赠汪伦", "dynasty": "唐"},
        
        # 宋代名句
        {"text": "先天下之忧而忧，后天下之乐而乐", "author": "范仲淹", "source": "岳阳楼记", "dynasty": "宋"},
        {"text": "不以物喜，不以己悲", "author": "范仲淹", "source": "岳阳楼记", "dynasty": "宋"},
        {"text": "醉翁之意不在酒，在乎山水之间也", "author": "欧阳修", "source": "醉翁亭记", "dynasty": "宋"},
        {"text": "人生自是有情痴，此恨不关风与月", "author": "欧阳修", "source": "玉楼春", "dynasty": "宋"},
        {"text": "衣带渐宽终不悔，为伊消得人憔悴", "author": "柳永", "source": "蝶恋花", "dynasty": "宋"},
        {"text": "今宵酒醒何处？杨柳岸，晓风残月", "author": "柳永", "source": "雨霖铃", "dynasty": "宋"},
        {"text": "多情自古伤离别，更那堪冷落清秋节", "author": "柳永", "source": "雨霖铃", "dynasty": "宋"},
        {"text": "但愿人长久，千里共婵娟", "author": "苏轼", "source": "水调歌头", "dynasty": "宋"},
        {"text": "大江东去，浪淘尽，千古风流人物", "author": "苏轼", "source": "念奴娇·赤壁怀古", "dynasty": "宋"},
        {"text": "竹杖芒鞋轻胜马，谁怕？一蓑烟雨任平生", "author": "苏轼", "source": "定风波", "dynasty": "宋"},
        {"text": "回首向来萧瑟处，归去，也无风雨也无晴", "author": "苏轼", "source": "定风波", "dynasty": "宋"},
        {"text": "十年生死两茫茫，不思量，自难忘", "author": "苏轼", "source": "江城子", "dynasty": "宋"},
        {"text": "人生到处知何似，应似飞鸿踏雪泥", "author": "苏轼", "source": "和子由渑池怀旧", "dynasty": "宋"},
        {"text": "不识庐山真面目，只缘身在此山中", "author": "苏轼", "source": "题西林壁", "dynasty": "宋"},
        {"text": "人生如逆旅，我亦是行人", "author": "苏轼", "source": "临江仙·送钱穆父", "dynasty": "宋"},
        {"text": "两情若是久长时，又岂在朝朝暮暮", "author": "秦观", "source": "鹊桥仙", "dynasty": "宋"},
        {"text": "此情无计可消除，才下眉头，却上心头", "author": "李清照", "source": "一剪梅", "dynasty": "宋"},
        {"text": "寻寻觅觅，冷冷清清，凄凄惨惨戚戚", "author": "李清照", "source": "声声慢", "dynasty": "宋"},
        {"text": "生当作人杰，死亦为鬼雄", "author": "李清照", "source": "夏日绝句", "dynasty": "宋"},
        {"text": "三十功名尘与土，八千里路云和月", "author": "岳飞", "source": "满江红", "dynasty": "宋"},
        {"text": "莫等闲，白了少年头，空悲切", "author": "岳飞", "source": "满江红", "dynasty": "宋"},
        {"text": "壮志饥餐胡虏肉，笑谈渴饮匈奴血", "author": "岳飞", "source": "满江红", "dynasty": "宋"},
        {"text": "山重水复疑无路，柳暗花明又一村", "author": "陆游", "source": "游山西村", "dynasty": "宋"},
        {"text": "王师北定中原日，家祭无忘告乃翁", "author": "陆游", "source": "示儿", "dynasty": "宋"},
        {"text": "小楼一夜听春雨，深巷明朝卖杏花", "author": "陆游", "source": "临安春雨初霁", "dynasty": "宋"},
        {"text": "出师一表真名世，千载谁堪伯仲间", "author": "陆游", "source": "书愤", "dynasty": "宋"},
        {"text": "位卑未敢忘忧国", "author": "陆游", "source": "病起书怀", "dynasty": "宋"},
        {"text": "纸上得来终觉浅，绝知此事要躬行", "author": "陆游", "source": "冬夜读书示子聿", "dynasty": "宋"},
        {"text": "人生自古谁无死，留取丹心照汗青", "author": "文天祥", "source": "过零丁洋", "dynasty": "宋"},
        {"text": "臣心一片磁针石，不指南方不肯休", "author": "文天祥", "source": "扬子江", "dynasty": "宋"},
        {"text": "问渠那得清如许，为有源头活水来", "author": "朱熹", "source": "观书有感", "dynasty": "宋"},
        {"text": "等闲识得东风面，万紫千红总是春", "author": "朱熹", "source": "春日", "dynasty": "宋"},
        {"text": "众里寻他千百度，蓦然回首，那人却在，灯火阑珊处", "author": "辛弃疾", "source": "青玉案·元夕", "dynasty": "宋"},
        {"text": "想当年，金戈铁马，气吞万里如虎", "author": "辛弃疾", "source": "永遇乐·京口北固亭怀古", "dynasty": "宋"},
        {"text": "醉里挑灯看剑，梦回吹角连营", "author": "辛弃疾", "source": "破阵子", "dynasty": "宋"},
        {"text": "稻花香里说丰年，听取蛙声一片", "author": "辛弃疾", "source": "西江月·夜行黄沙道中", "dynasty": "宋"},
        {"text": "春色满园关不住，一枝红杏出墙来", "author": "叶绍翁", "source": "游园不值", "dynasty": "宋"},
        {"text": "接天莲叶无穷碧，映日荷花别样红", "author": "杨万里", "source": "晓出净慈寺送林子方", "dynasty": "宋"},
        {"text": "小荷才露尖尖角，早有蜻蜓立上头", "author": "杨万里", "source": "小池", "dynasty": "宋"},
        
        # 明清名句
        {"text": "落红不是无情物，化作春泥更护花", "author": "龚自珍", "source": "己亥杂诗", "dynasty": "清"},
        {"text": "我劝天公重抖擞，不拘一格降人才", "author": "龚自珍", "source": "己亥杂诗", "dynasty": "清"},
        {"text": "苟利国家生死以，岂因祸福避趋之", "author": "林则徐", "source": "赴戍登程口占示家人", "dynasty": "清"},
        {"text": "海到无边天作岸，山登绝顶我为峰", "author": "林则徐", "source": "出老", "dynasty": "清"},
        {"text": "我自横刀向天笑，去留肝胆两昆仑", "author": "谭嗣同", "source": "狱中题壁", "dynasty": "清"},
        {"text": "千磨万击还坚劲，任尔东西南北风", "author": "郑燮", "source": "竹石", "dynasty": "清"},
        {"text": "天下兴亡，匹夫有责", "author": "顾炎武", "source": "日知录", "dynasty": "明"},
        {"text": "宝剑锋从磨砺出，梅花香自苦寒来", "author": "佚名", "source": "警世贤文", "dynasty": "明"},
        
        # 近现代名句
        {"text": "横眉冷对千夫指，俯首甘为孺子牛", "author": "鲁迅", "source": "自嘲", "dynasty": "近代"},
        {"text": "寄意寒星荃不察，我以我血荐轩辕", "author": "鲁迅", "source": "自题小像", "dynasty": "近代"},
        {"text": "心事浩茫连广宇，于无声处听惊雷", "author": "鲁迅", "source": "无题", "dynasty": "近代"},
        {"text": "世上本没有路，走的人多了也便成了路", "author": "鲁迅", "source": "故乡", "dynasty": "近代"},
        
        # 励志名句
        {"text": "书山有路勤为径，学海无涯苦作舟", "author": "韩愈", "source": "增广贤文", "dynasty": "唐"},
        {"text": "业精于勤荒于嬉，行成于思毁于随", "author": "韩愈", "source": "进学解", "dynasty": "唐"},
        {"text": "黑发不知勤学早，白首方悔读书迟", "author": "颜真卿", "source": "劝学", "dynasty": "唐"},
        {"text": "少壮不努力，老大徒伤悲", "author": "佚名", "source": "长歌行", "dynasty": "汉"},
        {"text": "盛年不重来，一日难再晨", "author": "陶渊明", "source": "杂诗", "dynasty": "东晋"},
        {"text": "及时当勉励，岁月不待人", "author": "陶渊明", "source": "杂诗", "dynasty": "东晋"},
        {"text": "莫等闲，白了少年头，空悲切", "author": "岳飞", "source": "满江红", "dynasty": "宋"},
        
        # 思乡名句
        {"text": "举头望明月，低头思故乡", "author": "李白", "source": "静夜思", "dynasty": "唐"},
        {"text": "露从今夜白，月是故乡明", "author": "杜甫", "source": "月夜忆舍弟", "dynasty": "唐"},
        {"text": "日暮乡关何处是？烟波江上使人愁", "author": "崔颢", "source": "黄鹤楼", "dynasty": "唐"},
        {"text": "近乡情更怯，不敢问来人", "author": "宋之问", "source": "渡汉江", "dynasty": "唐"},
        {"text": "乡书何处达？归雁洛阳边", "author": "王湾", "source": "次北固山下", "dynasty": "唐"},
        {"text": "独在异乡为异客，每逢佳节倍思亲", "author": "王维", "source": "九月九日忆山东兄弟", "dynasty": "唐"},
        
        # 离别名句
        {"text": "海内存知己，天涯若比邻", "author": "王勃", "source": "送杜少府之任蜀州", "dynasty": "唐"},
        {"text": "莫愁前路无知己，天下谁人不识君", "author": "高适", "source": "别董大", "dynasty": "唐"},
        {"text": "桃花潭水深千尺，不及汪伦送我情", "author": "李白", "source": "赠汪伦", "dynasty": "唐"},
        {"text": "洛阳亲友如相问，一片冰心在玉壶", "author": "王昌龄", "source": "芙蓉楼送辛渐", "dynasty": "唐"},
        {"text": "劝君更尽一杯酒，西出阳关无故人", "author": "王维", "source": "送元二使安西", "dynasty": "唐"},
        {"text": "又送王孙去，萋萋满别情", "author": "白居易", "source": "赋得古原草送别", "dynasty": "唐"},
        
        # 人生哲理
        {"text": "沉舟侧畔千帆过，病树前头万木春", "author": "刘禹锡", "source": "酬乐天扬州初逢席上见赠", "dynasty": "唐"},
        {"text": "人生如逆旅，我亦是行人", "author": "苏轼", "source": "临江仙·送钱穆父", "dynasty": "宋"},
        {"text": "世事一场大梦，人生几度秋凉", "author": "苏轼", "source": "西江月", "dynasty": "宋"},
        {"text": "人有悲欢离合，月有阴晴圆缺", "author": "苏轼", "source": "水调歌头", "dynasty": "宋"},
        {"text": "人生到处知何似，应似飞鸿踏雪泥", "author": "苏轼", "source": "和子由渑池怀旧", "dynasty": "宋"},
        {"text": "山重水复疑无路，柳暗花明又一村", "author": "陆游", "source": "游山西村", "dynasty": "宋"},
        {"text": "问渠那得清如许，为有源头活水来", "author": "朱熹", "source": "观书有感", "dynasty": "宋"},
        {"text": "不畏浮云遮望眼，自缘身在最高层", "author": "王安石", "source": "登飞来峰", "dynasty": "宋"},
        {"text": "春风又绿江南岸，明月何时照我还", "author": "王安石", "source": "泊船瓜洲", "dynasty": "宋"},
        
        # 爱情名句
        {"text": "两情若是久长时，又岂在朝朝暮暮", "author": "秦观", "source": "鹊桥仙", "dynasty": "宋"},
        {"text": "在天愿作比翼鸟，在地愿为连理枝", "author": "白居易", "source": "长恨歌", "dynasty": "唐"},
        {"text": "春蚕到死丝方尽，蜡炬成灰泪始干", "author": "李商隐", "source": "无题", "dynasty": "唐"},
        {"text": "身无彩凤双飞翼，心有灵犀一点通", "author": "李商隐", "source": "无题", "dynasty": "唐"},
        {"text": "曾经沧海难为水，除却巫山不是云", "author": "元稹", "source": "离思", "dynasty": "唐"},
        {"text": "十年生死两茫茫，不思量，自难忘", "author": "苏轼", "source": "江城子", "dynasty": "宋"},
        {"text": "此情无计可消除，才下眉头，却上心头", "author": "李清照", "source": "一剪梅", "dynasty": "宋"},
        {"text": "衣带渐宽终不悔，为伊消得人憔悴", "author": "柳永", "source": "蝶恋花", "dynasty": "宋"},
        
        # 自然景色
        {"text": "大漠孤烟直，长河落日圆", "author": "王维", "source": "使至塞上", "dynasty": "唐"},
        {"text": "明月松间照，清泉石上流", "author": "王维", "source": "山居秋暝", "dynasty": "唐"},
        {"text": "接天莲叶无穷碧，映日荷花别样红", "author": "杨万里", "source": "晓出净慈寺送林子方", "dynasty": "宋"},
        {"text": "小荷才露尖尖角，早有蜻蜓立上头", "author": "杨万里", "source": "小池", "dynasty": "宋"},
        {"text": "落霞与孤鹜齐飞，秋水共长天一色", "author": "王勃", "source": "滕王阁序", "dynasty": "唐"},
        {"text": "春江潮水连海平，海上明月共潮生", "author": "张若虚", "source": "春江花月夜", "dynasty": "唐"},
        {"text": "忽如一夜春风来，千树万树梨花开", "author": "岑参", "source": "白雪歌送武判官归京", "dynasty": "唐"},
        {"text": "稻花香里说丰年，听取蛙声一片", "author": "辛弃疾", "source": "西江月·夜行黄沙道中", "dynasty": "宋"},
        {"text": "停车坐爱枫林晚，霜叶红于二月花", "author": "杜牧", "source": "山行", "dynasty": "唐"},
        {"text": "春风又绿江南岸，明月何时照我还", "author": "王安石", "source": "泊船瓜洲", "dynasty": "宋"},
    ]
    
    result = []
    for i, q in enumerate(quotes):
        result.append({
            "id": f"classic_{i}",
            "text": q["text"],
            "author": q.get("author"),
            "source": q.get("source"),
            "dynasty": q.get("dynasty"),
            "type": "名句",
            "tags": [],
            "emotion": []
        })
    return result

if __name__ == "__main__":
    print("=" * 60)
    print("Building quotes database locally...")
    print("=" * 60)
    
    conn = create_database()
    total = 0
    
    print("\nAdding classic quotes...")
    classics = collect_classic_quotes()
    inserted = insert_quotes(conn, classics)
    total += inserted
    print(f"  Added {inserted} classic quotes")
    
    conn.close()
    
    print("\n" + "=" * 60)
    print(f"Database created: {DB_PATH}")
    print(f"Total quotes: {total}")
    print(f"File size: {DB_PATH.stat().st_size / 1024:.1f} KB")
    print("=" * 60)
