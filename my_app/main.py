from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

class WelcomeScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(WelcomeScreen, self).__init__(**kwargs)

        # Create a vertical BoxLayout
        self.orientation = 'vertical'

        # Add a Label
        self.add_widget(Label(text='Welcome to My App', font_size=30, size_hint_y=0.7))

        # Add two Buttons
        button_layout = BoxLayout(size_hint_y=0.3)
        button1 = Button(text='Button 1', on_press=self.on_button1_click)
        button2 = Button(text='Button 2', on_press=self.on_button2_click)
        button_layout.add_widget(button1)
        button_layout.add_widget(button2)
        self.add_widget(button_layout)

    def on_button1_click(self, instance):
        print('Button 1 clicked')

    def on_button2_click(self, instance):
        print('Button 2 clicked')

class MyApp(App):
    def build(self):
        return WelcomeScreen()

if __name__ == '__main__':
    MyApp().run()