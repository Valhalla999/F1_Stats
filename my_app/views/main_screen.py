from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color,Rectangle

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

        self.size_hint = (0.9, 0.9)
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        
        layout = BoxLayout(orientation='vertical', spacing=10)


        layout.add_widget(Image(source="my_app/assets/Tech-Play-logo-white.png"))

        greeting = Label(text="Welcome to F1 Stats!", font_size=36, color='#FFFFFF')
        layout.add_widget(greeting)


        btn1 = Button(
            text="Driver Overview",
            size_hint=(1, 1), 
            bold=True, 
            background_color='#215974',
            background_normal='')    

        btn2 = Button(text="Championship Standings", 
                      size_hint=(1, 1), 
                      bold=True, 
                      background_color='#215974',
                      background_normal='')
        
        btn3 = Button(text="Test Screen", 
                      size_hint=(1, 1), 
                      bold=True, 
                      background_color='#215974',
                      background_normal='')
        

        btn1.bind(on_press=self.switch_to_driver_overview)
        btn2.bind(on_press=self.switch_to_champion_standings)
        btn3.bind(on_press=self.switch_to_test)

        layout.add_widget(btn1)
        layout.add_widget(btn2)
        layout.add_widget(btn3)

        self.add_widget(layout)

    def switch_to_driver_overview(self, instance):
        self.manager.current = 'driver_overview'

    def switch_to_champion_standings(self, instance):
        self.manager.current = 'champion_standings'

    def switch_to_test(self, instance):
        self.manager.current = 'test'
            
