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
            
            # 跳过空行
            if not text or len(text) < 8:
                continue
            
            # 跳过标题行
            if re.match(r'^【.*】|^日[报评]|^人民|^金句|^摘抄|^汇[总编]|^作文|^热点|^主题|^2021年|^\d{4}年', text):
                continue
            
            # 移除序号（1、2、3... 或 1.2.3...）
            text = re.sub(r'^\d+[、.．]\s*', '', text)
            text = re.sub(r'^[（(]\d+[)）]\s*', '', text)
            
            # 移除引号
            text = text.strip('"""''「」『』【】《》')
            
            # 检查长度
            if 8 <= len(text) <= 300:
                quotes.append(text)
        
        return quotes
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return []

def main():
    folder = "C:/Users/wangjiejin/Desktop/TG047-日报金句文案"
    
    # 只提取这四个文件
    target_files = [
        "【160句】日报评论金句160例（2021年）.docx",
        "【66句】日报时评金句集锦66句.docx",
        "人民日报2021年600条金句汇总.docx",
        "日报5个热点话题，25条作文金句.docx"
    ]
    
    all_quotes = []
    
    for filename in target_files:
        file_path = os.path.join(folder, filename)
        if os.path.exists(file_path):
            print(f"Processing: {filename}")
            quotes = extract_quotes_from_docx(file_path)
            print(f"  Extracted: {len(quotes)} quotes")
            all_quotes.extend(quotes)
        else:
            print(f"File not found: {filename}")
    
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
        print(f"  - {q['text'][:60]}...")

if __name__ == "__main__":
    main()
