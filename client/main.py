from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle

from api.client import APIClient

Window.size = (400, 700)

class QuoteCard(BoxLayout):
    def __init__(self, quote_data, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = 130
        self.padding = [15, 10]
        self.spacing = 5
        
        with self.canvas.before:
            Color(0.95, 0.95, 0.97, 1)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[10])
            self.bind(pos=self.update_rect, size=self.update_rect)
        
        quote_label = Label(
            text=quote_data['text'],
            font_size=16,
            text_size=(None, None),
            halign='left',
            valign='top',
            color=(0.15, 0.15, 0.15, 1),
            size_hint_y=None,
            height=60
        )
        quote_label.bind(size=quote_label.setter('text_size'))
        self.add_widget(quote_label)
        
        info_parts = []
        if quote_data.get('author'):
            info_parts.append(quote_data['author'])
        if quote_data.get('source'):
            info_parts.append(f"《{quote_data['source']}》")
        
        if info_parts:
            info_label = Label(
                text='——' + ' '.join(info_parts),
                font_size=13,
                color=(0.5, 0.5, 0.5, 1),
                halign='right',
                size_hint_y=None,
                height=25
            )
            self.add_widget(info_label)
        
        score = quote_data.get('score', 0)
        score_label = Label(
            text=f"匹配度: {score:.0%}",
            font_size=12,
            color=(0.3, 0.65, 0.3, 1),
            halign='left',
            size_hint_y=None,
            height=20
        )
        self.add_widget(score_label)
    
    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

class MainScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 15
        
        self.api_client = APIClient()
        
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.bg = Rectangle(pos=self.pos, size=self.size)
            self.bind(pos=self.update_bg, size=self.update_bg)
        
        title = Label(
            text='名句匹配',
            font_size=32,
            size_hint_y=None,
            height=50,
            color=(0.15, 0.15, 0.15, 1)
        )
        self.add_widget(title)
        
        subtitle = Label(
            text='输入句子或关键词，找到最契合的名句',
            font_size=14,
            size_hint_y=None,
            height=30,
            color=(0.6, 0.6, 0.6, 1)
        )
        self.add_widget(subtitle)
        
        input_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=50,
            spacing=10
        )
        
        self.query_input = TextInput(
            hint_text='例如：思念家乡、坚持梦想、花 雨天...',
            multiline=False,
            font_size=16,
            padding=[15, 15],
            background_color=(0.96, 0.96, 0.96, 1),
            foreground_color=(0.2, 0.2, 0.2, 1),
            cursor_color=(0.2, 0.6, 1, 1)
        )
        self.query_input.bind(on_text_validate=self.on_search)
        input_layout.add_widget(self.query_input)
        
        search_btn = Button(
            text='搜索',
            size_hint_x=None,
            width=80,
            font_size=16,
            background_color=(0.2, 0.6, 1, 1),
            color=(1, 1, 1, 1)
        )
        search_btn.bind(on_press=self.on_search)
        input_layout.add_widget(search_btn)
        
        self.add_widget(input_layout)
        
        self.results_scroll = ScrollView()
        self.results_layout = GridLayout(
            cols=1,
            spacing=10,
            size_hint_y=None,
            padding=[0, 10]
        )
        self.results_layout.bind(minimum_height=self.results_layout.setter('height'))
        self.results_scroll.add_widget(self.results_layout)
        self.add_widget(self.results_scroll)
        
        self.status_label = Label(
            text='就绪',
            size_hint_y=None,
            height=30,
            font_size=12,
            color=(0.6, 0.6, 0.6, 1)
        )
        self.add_widget(self.status_label)
    
    def update_bg(self, instance, value):
        self.bg.pos = instance.pos
        self.bg.size = instance.size
    
    def on_search(self, instance):
        query = self.query_input.text.strip()
        if not query:
            return
        
        self.status_label.text = '搜索中...'
        self.results_layout.clear_widgets()
        
        Clock.schedule_once(lambda dt: self._do_search(query), 0.1)
    
    def _do_search(self, query):
        try:
            response = self.api_client.match(query, top_k=10)
            
            if not response.get('results'):
                self.status_label.text = '未找到匹配结果'
                no_result = Label(
                    text='没有找到匹配的名句\n试试其他关键词？',
                    font_size=16,
                    color=(0.6, 0.6, 0.6, 1),
                    size_hint_y=None,
                    height=80
                )
                self.results_layout.add_widget(no_result)
                return
            
            for quote in response['results']:
                card = QuoteCard(quote)
                self.results_layout.add_widget(card)
            
            self.status_label.text = f'找到 {len(response["results"])} 条匹配结果'
            
        except requests.exceptions.ConnectionError:
            self.status_label.text = '连接失败，请检查网络'
        except requests.exceptions.Timeout:
            self.status_label.text = '请求超时，请稍后重试'
        except Exception as e:
            self.status_label.text = f'错误: {str(e)}'

from kivy.graphics import Rectangle

class QuoteFinderApp(App):
    def build(self):
        self.title = '名句匹配'
        return MainScreen()

if __name__ == '__main__':
    QuoteFinderApp().run()
