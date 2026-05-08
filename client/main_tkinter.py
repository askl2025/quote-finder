import tkinter as tk
from tkinter import ttk, messagebox, font
import requests
import threading
import json

API_URL = "https://asklLin-quote-finder.hf.space"

class QuoteFinderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("名句匹配")
        self.root.geometry("500x700")
        self.root.minsize(400, 600)
        
        # 设置中文字体
        self.setup_fonts()
        
        # 创建UI
        self.create_widgets()
        
        # API客户端
        self.session = requests.Session()
    
    def setup_fonts(self):
        """设置中文字体"""
        # 尝试使用系统中文字体
        chinese_fonts = ["Microsoft YaHei", "SimHei", "SimSun", "NSimSun"]
        self.default_font = None
        
        available_fonts = font.families()
        for f in chinese_fonts:
            if f in available_fonts:
                self.default_font = f
                break
        
        if self.default_font:
            self.root.option_add("*Font", f"{self.default_font} 10")
    
    def create_widgets(self):
        """创建界面组件"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        title_font = (self.default_font or "TkDefaultFont", 24, "bold")
        title_label = ttk.Label(main_frame, text="名句匹配", font=title_font)
        title_label.pack(pady=(0, 5))
        
        # 副标题
        subtitle_font = (self.default_font or "TkDefaultFont", 10)
        subtitle_label = ttk.Label(
            main_frame, 
            text="输入句子或关键词，找到最契合的名句",
            font=subtitle_font,
            foreground="gray"
        )
        subtitle_label.pack(pady=(0, 15))
        
        # 搜索框框架
        search_frame = ttk.Frame(main_frame)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 搜索输入框
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(
            search_frame, 
            textvariable=self.search_var,
            font=(self.default_font or "TkDefaultFont", 12)
        )
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.search_entry.bind("<Return>", lambda e: self.do_search())
        
        # 搜索按钮
        self.search_btn = ttk.Button(
            search_frame, 
            text="搜索", 
            command=self.do_search
        )
        self.search_btn.pack(side=tk.RIGHT)
        
        # 状态标签
        self.status_var = tk.StringVar(value="就绪")
        self.status_label = ttk.Label(
            main_frame, 
            textvariable=self.status_var,
            foreground="gray"
        )
        self.status_label.pack(anchor=tk.W, pady=(0, 10))
        
        # 结果列表框架
        result_frame = ttk.Frame(main_frame)
        result_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建滚动条
        scrollbar = ttk.Scrollbar(result_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 结果列表
        self.result_list = tk.Listbox(
            result_frame,
            font=(self.default_font or "TkDefaultFont", 11),
            yscrollcommand=scrollbar.set,
            selectmode=tk.SINGLE,
            activestyle='none'
        )
        self.result_list.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.result_list.yview)
        
        # 绑定点击事件
        self.result_list.bind("<Double-Button-1>", self.show_detail)
        
        # 存储搜索结果
        self.current_results = []
        
        # 示例提示
        examples = [
            "试试输入：思念家乡",
            "试试输入：坚持梦想",
            "试试输入：花 雨天 灯火",
            "试试输入：孤独寂寞",
        ]
        for ex in examples:
            self.result_list.insert(tk.END, ex)
            self.result_list.itemconfigure(tk.END, fg="gray")
    
    def do_search(self):
        """执行搜索"""
        query = self.search_var.get().strip()
        if not query:
            return
        
        # 禁用搜索按钮
        self.search_btn.config(state=tk.DISABLED)
        self.status_var.set("搜索中...")
        self.result_list.delete(0, tk.END)
        
        # 异步搜索
        threading.Thread(target=self._search_thread, args=(query,), daemon=True).start()
    
    def _search_thread(self, query):
        """搜索线程"""
        try:
            response = self.session.post(
                f"{API_URL}/match",
                json={"query": query, "top_k": 10},
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            
            # 更新UI（必须在主线程）
            self.root.after(0, self._update_results, data)
            
        except requests.exceptions.ConnectionError:
            self.root.after(0, self._show_error, "连接失败，请检查网络")
        except requests.exceptions.Timeout:
            self.root.after(0, self._show_error, "请求超时，请稍后重试")
        except Exception as e:
            self.root.after(0, self._show_error, f"错误: {str(e)}")
    
    def _update_results(self, data):
        """更新搜索结果"""
        self.search_btn.config(state=tk.NORMAL)
        self.current_results = data.get("results", [])
        
        if not self.current_results:
            self.status_var.set("未找到匹配结果")
            self.result_list.insert(tk.END, "没有找到匹配的名句")
            self.result_list.insert(tk.END, "试试其他关键词？")
            return
        
        self.status_var.set(f"找到 {len(self.current_results)} 条匹配结果")
        
        for i, quote in enumerate(self.current_results):
            text = quote.get("text", "")
            author = quote.get("author", "") or "佚名"
            source = quote.get("source", "") or ""
            score = quote.get("score", 0)
            
            # 截断过长的文本
            if len(text) > 40:
                text = text[:40] + "..."
            
            # 格式化显示
            display_text = f"{text}"
            self.result_list.insert(tk.END, display_text)
            
            # 作者和来源
            info = f"    ——{author}"
            if source:
                info += f"《{source}》"
            info += f"  匹配度:{score:.0%}"
            self.result_list.insert(tk.END, info)
            self.result_list.itemconfigure(tk.END, fg="gray")
            
            # 分隔线
            self.result_list.insert(tk.END, "─" * 50)
            self.result_list.itemconfigure(tk.END, fg="lightgray")
    
    def _show_error(self, message):
        """显示错误"""
        self.search_btn.config(state=tk.NORMAL)
        self.status_var.set(message)
        self.result_list.delete(0, tk.END)
        self.result_list.insert(tk.END, message)
    
    def show_detail(self, event):
        """显示详情"""
        selection = self.result_list.curselection()
        if not selection:
            return
        
        # 计算结果索引（每3行一个结果）
        idx = selection[0] // 3
        if idx < len(self.current_results):
            quote = self.current_results[idx]
            
            # 创建详情窗口
            detail_window = tk.Toplevel(self.root)
            detail_window.title("名句详情")
            detail_window.geometry("400x300")
            
            # 详情内容
            text = quote.get("text", "")
            author = quote.get("author", "") or "佚名"
            source = quote.get("source", "") or ""
            dynasty = quote.get("dynasty", "") or ""
            score = quote.get("score", 0)
            
            detail_text = f"{text}\n\n"
            if dynasty:
                detail_text += f"朝代: {dynasty}\n"
            detail_text += f"作者: {author}\n"
            if source:
                detail_text += f"来源: {source}\n"
            detail_text += f"\n匹配度: {score:.0%}"
            
            text_widget = tk.Text(
                detail_window,
                font=(self.default_font or "TkDefaultFont", 12),
                wrap=tk.WORD,
                padx=20,
                pady=20
            )
            text_widget.pack(fill=tk.BOTH, expand=True)
            text_widget.insert(tk.END, detail_text)
            text_widget.config(state=tk.DISABLED)

def main():
    root = tk.Tk()
    app = QuoteFinderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
