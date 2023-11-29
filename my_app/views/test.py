from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import TwoLineAvatarListItem, MDList
import requests

class test(Screen):
    def __init__(self, **kwargs):
        super(test, self).__init__(**kwargs)
        self.size_hint = (0.9, 0.9)
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        layout = BoxLayout(orientation='vertical',spacing=10)

            
        back_button = Button(text="Back",
                size_hint=(1, 1), 
                bold=True, 
                background_color='#215974',
                background_normal='') 
            
        back_button.bind(on_press=self.switch_to_main)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def switch_to_main(self, instance):
        self.manager.current = 'main'