from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.label import MDLabel
from kivy.properties import StringProperty, NumericProperty 
from kivy.core.text import LabelBase
from kivy.clock import Clock

Window.size = (350, 550)

class Command(MDLabel):
    text = StringProperty()
    size_hint_x = NumericProperty()
    halign = StringProperty()
    #font_name
    font_size = 17

class Response(MDLabel):
    text = StringProperty()
    size_hint_x = NumericProperty()
    #halign = StringProperty()
    #font_name
    font_size = 17

class ChatBot(MDApp):
    
    def change_screen(self, name):
        screen_manager.current = name
    
    def build(self):
        global screen_manager
        screen_manager = ScreenManager()
        screen_manager.add_widget(Builder.load_file("Main.kv"))
        screen_manager.add_widget(Builder.load_file("Chats.kv"))
        return screen_manager
    
    def response(self, *args):
        response = ""
        if value == "ciao":
            response = "ciao, sono il tuo assistente personale"
        else:
            response = "puoi ripetere?"
        screen_manager.get_screen('chats').chat_list.add_widget(Response(text=response, size_hint_x = .75))
        
    
    def send(self):
        global size, halign, value
        if screen_manager.get_screen('chats').text_input != "":
            value = screen_manager.get_screen('chats').text_input.text
            if len(value) < 6:
                size = .22
            elif len(value) <11:
                size = .32
            elif len(value) < 16:
                size = .45
            elif len(value) < 21:
                size = .58
            elif len(value) < 26:
                size = .71
            else:
                size = .77
            halign = "left"
            screen_manager.get_screen('chats').chat_list.add_widget(Command(text=value, size_hint_x = size, halign = halign))
            Clock.schedule_once(self.response, 2)
            screen_manager.get_screen('chats').text_input.text = ""
            

ChatBot().run()