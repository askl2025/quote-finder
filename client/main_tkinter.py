import tkinter as tk
from tkinter import ttk, font
import requests
import threading
import json

API_URL = "https://asklLin-quote-finder.hf.space"

COLORS = {
    'bg': '#faf8f5',
    'card_bg': '#ffffff',
    'primary': '#2c3e50',
    'primary_light': '#34495e',
    'accent': '#e74c3c',
    'text': '#2c3e50',
    'text_light': '#7f8c8d',
    'border': '#ecf0f1',
    'tag_bg': '#f8f9fa',
    'tag_hover': '#2c3e50',
    'score_bg': '#667eea',
    'white': '#ffffff',
}

class QuoteFinderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("名句匹配")
        self.root.geometry("560x780")
        self.root.minsize(380, 500)
        self.root.configure(bg=COLORS['bg'])

        self.setup_fonts()

        self.session = requests.Session()
        self.placeholder = "例如：思念家乡、坚持梦想、花 雨天..."
        self.current_results = []
        self.card_widgets = []

        self.create_widgets()

        self.root.bind('<Return>', lambda e: self.do_search())
        self.root.bind('<Configure>', self.on_window_resize)

    def setup_fonts(self):
        available_fonts = font.families()
        if 'Microsoft YaHei' in available_fonts:
            self.default_font = 'Microsoft YaHei'
        elif 'SimHei' in available_fonts:
            self.default_font = 'SimHei'
        else:
            self.default_font = 'TkDefaultFont'

        if 'SimSun' in available_fonts:
            self.quote_font = 'SimSun'
        elif 'NSimSun' in available_fonts:
            self.quote_font = 'NSimSun'
        else:
            self.quote_font = self.default_font

        self.fonts = {
            'title': (self.default_font, 26, 'bold'),
            'subtitle': (self.default_font, 11),
            'input': (self.default_font, 13),
            'button': (self.default_font, 12),
            'tag': (self.default_font, 10),
            'quote': (self.quote_font, 15),
            'author': (self.default_font, 11),
            'score': (self.default_font, 10),
            'status': (self.default_font, 10),
            'empty': (self.default_font, 13),
        }

    def get_wrap_length(self):
        w = self.root.winfo_width()
        return max(200, w - 100)

    def on_window_resize(self, event):
        if event.widget != self.root:
            return
        wrap = self.get_wrap_length()
        for label in self.card_widgets:
            try:
                label.config(wraplength=wrap)
            except:
                pass

    def create_widgets(self):
        self.main_frame = tk.Frame(self.root, bg=COLORS['bg'])
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=16, pady=10)

        self.create_header()
        self.create_search_section()
        self.create_results_section()
        self.create_status_bar()

    def create_header(self):
        header_frame = tk.Frame(self.main_frame, bg=COLORS['bg'])
        header_frame.pack(fill=tk.X, pady=(10, 8))

        title_label = tk.Label(
            header_frame, text="名 句 匹 配",
            font=self.fonts['title'], fg=COLORS['primary'], bg=COLORS['bg']
        )
        title_label.pack()

        subtitle_label = tk.Label(
            header_frame, text="输入句子或关键词，找到最契合的名句",
            font=self.fonts['subtitle'], fg=COLORS['text_light'], bg=COLORS['bg']
        )
        subtitle_label.pack(pady=(4, 0))

    def create_search_section(self):
        search_frame = tk.Frame(
            self.main_frame, bg=COLORS['card_bg'],
            highlightbackground=COLORS['border'], highlightthickness=1
        )
        search_frame.pack(fill=tk.X, pady=(0, 8))

        search_inner = tk.Frame(search_frame, bg=COLORS['card_bg'])
        search_inner.pack(fill=tk.X, padx=12, pady=10)

        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(
            search_inner, textvariable=self.search_var,
            font=self.fonts['input'], bg=COLORS['card_bg'],
            fg=COLORS['text_light'], insertbackground=COLORS['primary'],
            relief=tk.FLAT, highlightthickness=0
        )
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.search_entry.insert(0, self.placeholder)
        self.search_entry.bind('<FocusIn>', self.on_entry_focus_in)
        self.search_entry.bind('<FocusOut>', self.on_entry_focus_out)

        self.search_btn = tk.Button(
            search_inner, text="搜索", font=self.fonts['button'],
            bg=COLORS['primary'], fg=COLORS['white'],
            activebackground=COLORS['primary_light'], activeforeground=COLORS['white'],
            relief=tk.FLAT, cursor="hand2", padx=20, pady=6,
            command=self.do_search
        )
        self.search_btn.pack(side=tk.RIGHT)

        self.create_tags()

    def on_entry_focus_in(self, event):
        if self.search_entry.get() == self.placeholder:
            self.search_entry.delete(0, tk.END)
            self.search_entry.config(fg=COLORS['text'])

    def on_entry_focus_out(self, event):
        if not self.search_entry.get():
            self.search_entry.insert(0, self.placeholder)
            self.search_entry.config(fg=COLORS['text_light'])

    def create_tags(self):
        tags_frame = tk.Frame(self.main_frame, bg=COLORS['bg'])
        tags_frame.pack(fill=tk.X, pady=(0, 10))

        tags = ["思念家乡", "坚持梦想", "孤独寂寞", "爱情", "人生短暂", "离别", "春天美景", "学习进步"]

        for i, tag_text in enumerate(tags):
            tag = tk.Label(
                tags_frame, text=tag_text, font=self.fonts['tag'],
                fg=COLORS['text_light'], bg=COLORS['tag_bg'],
                relief=tk.FLAT, padx=10, pady=4, cursor="hand2"
            )
            row = i // 4
            col = i % 4
            tag.grid(row=row, column=col, padx=4, pady=3, sticky="ew")

            tag.bind('<Button-1>', lambda e, t=tag_text: self.on_tag_click(t))
            tag.bind('<Enter>', lambda e, t=tag: t.config(bg=COLORS['primary'], fg=COLORS['white']))
            tag.bind('<Leave>', lambda e, t=tag: t.config(bg=COLORS['tag_bg'], fg=COLORS['text_light']))

        for c in range(4):
            tags_frame.columnconfigure(c, weight=1)

    def on_tag_click(self, tag_text):
        self.search_var.set(tag_text)
        self.search_entry.config(fg=COLORS['text'])
        self.do_search()

    def create_results_section(self):
        container = tk.Frame(self.main_frame, bg=COLORS['bg'])
        container.pack(fill=tk.BOTH, expand=True)

        self.results_canvas = tk.Canvas(container, bg=COLORS['bg'], highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(container, orient=tk.VERTICAL, command=self.results_canvas.yview)
        self.results_frame = tk.Frame(self.results_canvas, bg=COLORS['bg'])

        self.results_frame.bind(
            "<Configure>",
            lambda e: self.results_canvas.configure(scrollregion=self.results_canvas.bbox("all"))
        )

        self.canvas_window = self.results_canvas.create_window((0, 0), window=self.results_frame, anchor="nw")
        self.results_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.results_canvas.bind('<Configure>', self.on_canvas_resize)

        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.results_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.results_canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)

        self.show_empty_state()

    def on_canvas_resize(self, event):
        self.results_canvas.itemconfig(self.canvas_window, width=event.width)

    def on_mouse_wheel(self, event):
        self.results_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def show_empty_state(self):
        self.clear_results()
        empty_frame = tk.Frame(self.results_frame, bg=COLORS['bg'])
        empty_frame.pack(fill=tk.X, pady=40)

        icon_label = tk.Label(empty_frame, text="📖", font=('TkDefaultFont', 48), bg=COLORS['bg'])
        icon_label.pack()

        text_label = tk.Label(
            empty_frame,
            text="输入你想表达的意思\n或者点击上方的快捷标签\n找到最契合的名句",
            font=self.fonts['empty'], fg=COLORS['text_light'],
            bg=COLORS['bg'], justify=tk.CENTER
        )
        text_label.pack(pady=(12, 0))

    def clear_results(self):
        self.card_widgets = []
        for widget in self.results_frame.winfo_children():
            widget.destroy()

    def create_status_bar(self):
        self.status_var = tk.StringVar(value="就绪")
        status_label = tk.Label(
            self.main_frame, textvariable=self.status_var,
            font=self.fonts['status'], fg=COLORS['text_light'],
            bg=COLORS['bg'], anchor=tk.W
        )
        status_label.pack(fill=tk.X, pady=(6, 0))

    def do_search(self):
        query = self.search_var.get().strip()
        if not query or query == self.placeholder:
            return

        self.search_btn.config(state=tk.DISABLED, text="搜索中...")
        self.status_var.set("正在搜索...")
        self.clear_results()

        loading_frame = tk.Frame(self.results_frame, bg=COLORS['bg'])
        loading_frame.pack(fill=tk.X, pady=40)
        tk.Label(
            loading_frame, text="正在搜索...",
            font=self.fonts['empty'], fg=COLORS['text_light'], bg=COLORS['bg']
        ).pack()

        threading.Thread(target=self._search_thread, args=(query,), daemon=True).start()

    def _search_thread(self, query):
        try:
            response = self.session.post(
                f"{API_URL}/match", json={"query": query, "top_k": 8}, timeout=30
            )
            response.raise_for_status()
            data = response.json()
            self.root.after(0, self._update_results, data)
        except requests.exceptions.ConnectionError:
            self.root.after(0, self._show_error, "连接失败，请检查网络")
        except requests.exceptions.Timeout:
            self.root.after(0, self._show_error, "请求超时，请稍后重试")
        except Exception as e:
            self.root.after(0, self._show_error, f"错误: {str(e)}")

    def _update_results(self, data):
        self.search_btn.config(state=tk.NORMAL, text="搜索")
        self.current_results = data.get("results", [])

        if not self.current_results:
            self.status_var.set("未找到匹配结果")
            self.show_empty_state()
            return

        self.status_var.set(f"找到 {len(self.current_results)} 条匹配结果")
        self.clear_results()

        for i, quote in enumerate(self.current_results):
            self.create_quote_card(quote, i)

    def _show_error(self, message):
        self.search_btn.config(state=tk.NORMAL, text="搜索")
        self.status_var.set(message)
        self.clear_results()

        error_frame = tk.Frame(self.results_frame, bg=COLORS['bg'])
        error_frame.pack(fill=tk.X, pady=40)
        tk.Label(
            error_frame, text=f"😔\n{message}",
            font=self.fonts['empty'], fg=COLORS['text_light'],
            bg=COLORS['bg'], justify=tk.CENTER
        ).pack()

    def create_quote_card(self, quote, index):
        text = quote.get('text', '')
        author = quote.get('author', '') or '佚名'
        source = quote.get('source', '') or ''
        score = quote.get('score', 0)

        card_frame = tk.Frame(
            self.results_frame, bg=COLORS['card_bg'],
            highlightbackground=COLORS['border'], highlightthickness=1
        )
        card_frame.pack(fill=tk.X, padx=2, pady=(0, 8))

        inner_frame = tk.Frame(card_frame, bg=COLORS['card_bg'])
        inner_frame.pack(fill=tk.X, padx=16, pady=12)

        wrap = self.get_wrap_length()

        quote_label = tk.Label(
            inner_frame, text=text, font=self.fonts['quote'],
            fg=COLORS['primary'], bg=COLORS['card_bg'],
            wraplength=wrap, justify=tk.LEFT, anchor=tk.W
        )
        quote_label.pack(fill=tk.X, pady=(0, 10))
        self.card_widgets.append(quote_label)

        bottom_frame = tk.Frame(inner_frame, bg=COLORS['card_bg'])
        bottom_frame.pack(fill=tk.X)

        author_text = f"——{author}"
        if source:
            author_text += f"《{source}》"

        tk.Label(
            bottom_frame, text=author_text, font=self.fonts['author'],
            fg=COLORS['text_light'], bg=COLORS['card_bg'], anchor=tk.W
        ).pack(side=tk.LEFT)

        score_text = f"匹配度 {int(score * 100)}%"
        tk.Label(
            bottom_frame, text=score_text, font=self.fonts['score'],
            fg=COLORS['white'], bg=COLORS['score_bg'], padx=10, pady=3
        ).pack(side=tk.RIGHT)

def main():
    root = tk.Tk()
    app = QuoteFinderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
