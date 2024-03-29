from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.button import MDIconButton, MDFillRoundFlatButton
from kivymd.uix.label import MDLabel
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.metrics import dp
import webbrowser


class AboutMeScreen(Screen):
    def __init__(self, **kwargs):
        super(AboutMeScreen, self).__init__(**kwargs)

        main_layout = GridLayout(
            cols=1,
            padding=20,
        )

        # Top Row: Phrase and Logo
        top_row = BoxLayout(
            orientation="vertical",
            spacing=20,
        )

        logo = Image(
            source="my_app/assets/Tech-Play-logo_black.png",
            pos_hint={
                "center_x": 0.5,
            },
        )

        phrase_label = MDLabel(
            text=(
                "“Sometimes when you innovate, you make mistakes. "
                "It is best to admit them quickly and get on with improving your other innovations.”"
                "\n"
                "\n - Steve Jobs"
            ),
            font_style="H5",
            halign="center",
            color="#215974",
        )

        # Second Row: LinkedIn and Twitter Buttons
        social_buttons = BoxLayout(orientation="horizontal")

        btn_twitter = MDIconButton(
            icon="twitter",
            icon_size=dp(100),
            size_hint=(0.5, 0.5),
            on_press=self.open_twitter,
        )

        btn_linkedIn = MDIconButton(
            icon="linkedin",
            icon_size=dp(100),
            size_hint=(0.5, 0.5),
            pos_hint={
                "center_x": 0.5,
            },
            on_press=self.open_linkedin,
        )

        # Back Button
        back_button = MDFillRoundFlatButton(
            text="Back to Main",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            size_hint=(0.15, 0.15),
            pos_hint={
                "center_x": 0.5,
            },
            md_bg_color=(33 / 255, 89 / 255, 116 / 255, 1),
            on_press=self.switch_to_main,
        )

        top_row.add_widget(logo)
        top_row.add_widget(phrase_label)

        social_buttons.add_widget(btn_twitter)
        social_buttons.add_widget(btn_linkedIn)

        main_layout.add_widget(top_row)
        main_layout.add_widget(social_buttons)
        main_layout.add_widget(back_button)

        self.add_widget(main_layout)

    def open_twitter(self, instance):
        twitter_profile_url = "https://twitter.com/Valhalla999J"
        webbrowser.open(twitter_profile_url)

    def open_linkedin(self, instance):
        linkedin_profile_url = "https://www.linkedin.com/in/fabian-ottowitz-71a83379/"
        webbrowser.open(linkedin_profile_url)

    def switch_to_main(self, instance):
        self.manager.current = "main"
