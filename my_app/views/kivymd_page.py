from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout

class KivyMDPage(Screen):
    def __init__(self, **kwargs):
        super(KivyMDPage, self).__init__(**kwargs)

        # Create a box layout for KivyMD buttons
        box_layout = MDBoxLayout(orientation='vertical')

        # Create KivyMD buttons
        button1 = MDRaisedButton(text="Button 1", on_release=self.on_button_press)
        button2 = MDRaisedButton(text="Button 2", on_release=self.on_button_press)
        
        # Add buttons to the box layout
        box_layout.add_widget(button1)
        box_layout.add_widget(button2)

        # Add the box layout to the screen
        self.add_widget(box_layout)

    def on_button_press(self, instance):
        print(f"Button {instance.text} pressed")