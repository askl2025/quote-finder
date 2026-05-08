import os
import json
from docx import Document
import re

def extract_quotes_from_docx(file_path):
    """从Word文件中提取金句"""
    try:
        doc = Document(file_path)
        quotes = []
        
        for para in doc.paragraphs:
            text = para.text.strip()
            
            # 跳过空行和标题
            if not text or len(text) < 10:
                continue
            
            # 跳过常见的标题格式
            skip_patterns = [
                r'^\d+[、.]',  # 数字开头的标题
                r'^[一二三四五六七八九十]+[、.]',  # 中文数字开头
                r'^【.*】',  # 【】包围的标题
                r'^\*+',  # 星号
                r'^#',  # 井号
                r'^日[报评]',  # 日报/日评开头
                r'^人民',  # 人民开头
                r'^金句',  # 金句开头
                r'^摘抄',  # 摘抄开头
                r'^汇[总编]',  # 汇总/汇编
                r'^作文',  # 作文开头
                r'^热点',  # 热点开头
                r'^主题',  # 主题开头
            ]
            
            is_title = False
            for pattern in skip_patterns:
                if re.match(pattern, text):
                    is_title = True
                    break
            
            if is_title:
                continue
            
            # 清理文本
            # 移除序号
            text = re.sub(r'^\d+[、.．]\s*', '', text)
            text = re.sub(r'^[（(]\d+[)）]\s*', '', text)
            
            # 移除引号
            text = text.strip('"""''「」『』【】《》')
            
            # 检查是否是有效金句（长度在10-200之间）
            if 10 <= len(text) <= 200:
                quotes.append(text)
        
        return quotes
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return []

def main():
    folder = "C:/Users/wangjiejin/Desktop/TG047-日报金句文案"
    
    all_quotes = []
    
    # 遍历所有docx文件
    for filename in os.listdir(folder):
        if filename.endswith('.docx') and not filename.startswith('~'):
            file_path = os.path.join(folder, filename)
            print(f"Processing: {filename}")
            
            quotes = extract_quotes_from_docx(file_path)
            print(f"  Extracted: {len(quotes)} quotes")
            all_quotes.extend(quotes)
    
    # 检查子文件夹
    subfolder = os.path.join(folder, "11月更新")
    if os.path.exists(subfolder):
        for filename in os.listdir(subfolder):
            if filename.endswith('.docx') and not filename.startswith('~'):
                file_path = os.path.join(subfolder, filename)
                print(f"Processing: 11月更新/{filename}")
                
                quotes = extract_quotes_from_docx(file_path)
                print(f"  Extracted: {len(quotes)} quotes")
                all_quotes.extend(quotes)
    
    # 去重
    unique_quotes = list(set(all_quotes))
    print(f"\nTotal unique quotes: {len(unique_quotes)}")
    
    # 转换为标准格式
    formatted_quotes = []
    for i, text in enumerate(unique_quotes):
        formatted_quotes.append({
            "id": f"renmin_ribao_{i}",
            "text": text,
            "author": "人民日报",
            "source": "人民日报",
            "dynasty": "现代",
            "type": "现代名言",
            "tags": ["人民日报", "金句"]
        })
    
    # 保存到JSON文件
    output_file = "server/data/renmin_ribao_quotes.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(formatted_quotes, f, ensure_ascii=False, indent=2)
    
    print(f"\nSaved to: {output_file}")
    print(f"Total quotes: {len(formatted_quotes)}")
    
    # 显示前5个示例
    print("\nSample quotes:")
    for q in formatted_quotes[:5]:
        print(f"  - {q['text'][:50]}...")

if __name__ == "__main__":
    main()
