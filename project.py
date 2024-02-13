from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFillRoundFlatButton
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

        self.size_hint = (0.9, 0.9)
        self.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        layout = BoxLayout(orientation="vertical", spacing=5)

        layout.add_widget(Image(source="my_app/assets/Tech-Play-logo_black.png"))

        greeting = MDLabel(
            text="Welcome to F1 Stats!",
            halign="center",
            font_style="H2",
            font_size=38,
            color="#215974",
        )

        btn_driver = MDFillRoundFlatButton(
            text="Driver Overview",
            size_hint=(0.15, 0.15),
            pos_hint={"center_x": 0.5},
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),  # Set your text color
            md_bg_color=(33 / 255, 89 / 255, 116 / 255, 1),
            on_press=self.main,
        )

        btn_champion = MDFillRoundFlatButton(
            text="Championship Standings",
            size_hint=(0.15, 0.15),
            pos_hint={"center_x": 0.5},
            theme_text_color="Custom",
            md_bg_color=(33 / 255, 89 / 255, 116 / 255, 1),
            on_press=self.switch_to_champion_standings,
        )

        btn_history = MDFillRoundFlatButton(
            text="History",
            size_hint=(0.15, 0.15),
            pos_hint={"center_x": 0.5},
            theme_text_color="Custom",
            md_bg_color=(33 / 255, 89 / 255, 116 / 255, 1),
            on_press=self.switch_to_tracks,
        )

        btn_about = MDFillRoundFlatButton(
            text="About Me",
            size_hint=(0.15, 0.15),
            pos_hint={"center_x": 0.5},
            theme_text_color="Custom",
            md_bg_color=(33 / 255, 89 / 255, 116 / 255, 1),
            on_press=self.switch_to_about_me,
        )
        """
        btn5 = MDFillRoundFlatButton(
            text="Test Screen", 
            size_hint=(0.15, 0.15), 
            pos_hint={'center_x': 0.5}, 
            theme_text_color="Custom",
            md_bg_color=(33/255, 89/255, 116/255, 1),
            on_press=self.switch_to_test)"""

        layout.add_widget(greeting)

        layout.add_widget(btn_driver)
        layout.add_widget(btn_champion)
        layout.add_widget(btn_history)
        layout.add_widget(btn_about)
        # layout.add_widget(btn4)

        self.add_widget(layout)

    def main(self, instance):
        self.manager.current = "driver_overview"

    def switch_to_champion_standings(self, instance):
        self.manager.current = "champion_standings"

    def switch_to_tracks(self, instance):
        self.manager.current = "tracks"

    def switch_to_about_me(self, instance):
        self.manager.current = "about_me"

    def switch_to_test(self, instance):
        self.manager.current = "kivymd_page"
        print("switched to test screen")
