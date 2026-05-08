import json
import re

def is_quality_text(text):
    """检查文本质量"""
    # 过滤条件
    if not text or len(text) < 10:
        return False
    
    # 过滤包含占位符的文本
    if '□' in text or '■' in text or '�' in text:
        return False
    
    # 过滤包含过多特殊字符的文本
    special_chars = re.findall(r'[^\u4e00-\u9fff\u3400-\u4dbf，。！？、；：""''（）《》\s]', text)
    if len(special_chars) > len(text) * 0.1:  # 特殊字符超过10%
        return False
    
    # 过滤乱码文本（连续多个生僻字）
    rare_chars = re.findall(r'[\u3100-\u312f\u31a0-\u31bf]', text)
    if len(rare_chars) > 3:
        return False
    
    # 过滤过长的文本（超过300字可能是长篇）
    if len(text) > 300:
        return False
    
    return True

def clean_quotes(input_file, output_file):
    """清洗数据"""
    with open(input_file, 'r', encoding='utf-8') as f:
        quotes = json.load(f)
    
    print(f"原始数据: {len(quotes)} 条")
    
    # 统计各类型
    type_stats = {}
    for q in quotes:
        t = q.get('type', 'unknown')
        type_stats[t] = type_stats.get(t, 0) + 1
    print(f"类型分布: {type_stats}")
    
    # 清洗
    cleaned = []
    removed = 0
    
    for q in quotes:
        text = q.get('text', '')
        
        if is_quality_text(text):
            # 标准化文本
            text = text.strip()
            text = re.sub(r'\s+', ' ', text)  # 合并多个空格
            
            q['text'] = text
            cleaned.append(q)
        else:
            removed += 1
    
    print(f"清洗后: {len(cleaned)} 条")
    print(f"移除: {removed} 条")
    
    # 统计清洗后各类型
    type_stats_after = {}
    for q in cleaned:
        t = q.get('type', 'unknown')
        type_stats_after[t] = type_stats_after.get(t, 0) + 1
    print(f"清洗后类型分布: {type_stats_after}")
    
    # 保存
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(cleaned, f, ensure_ascii=False, indent=2)
    
    print(f"保存到: {output_file}")
    return cleaned

if __name__ == "__main__":
    clean_quotes('server/data/quotes.json', 'server/data/quotes_cleaned.json')
