from kivy.uix.scrollview import ScrollView
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFillRoundFlatButton
from kivy.uix.screenmanager import Screen
from kivymd.uix.list import OneLineListItem
from kivy.uix.boxlayout import BoxLayout
import requests


class ChampionStandingsScreen(Screen):
    def __init__(self, **kwargs):
        super(ChampionStandingsScreen, self).__init__(**kwargs)

        layout = BoxLayout(orientation="vertical", spacing=10, padding=10)

        layout.bind(minimum_height=layout.setter("height"))

        # Adding Header
        standings_header = MDBoxLayout(
            orientation="horizontal", adaptive_height=True, spacing=10
        )

        standings_header.add_widget(OneLineListItem(text="Position", size_hint_x=0.25))

        standings_header.add_widget(OneLineListItem(text="Driver", size_hint_x=0.45))

        standings_header.add_widget(OneLineListItem(text="Points", size_hint_x=0.25))

        layout.add_widget(standings_header)

        # Adding Data
        standings_data = self.get_driver_standings()

        for standing in standings_data:
            standing_layout = MDBoxLayout(
                orientation="horizontal", adaptive_height=True, spacing=10
            )

            standing_layout.add_widget(
                OneLineListItem(text=standing["position"], size_hint_x=0.25)
            )

            standing_layout.add_widget(
                OneLineListItem(
                    text=f"{standing['Driver']['givenName']} {standing['Driver']['familyName']}",
                    size_hint_x=0.45,
                )
            )

            standing_layout.add_widget(
                OneLineListItem(text=standing["points"], size_hint_x=0.25)
            )

            layout.add_widget(standing_layout)

        back_button = MDFillRoundFlatButton(
            text="Back to Main",
            size_hint=(0.15, 0.15),
            pos_hint={"center_x": 0.5},
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            md_bg_color=(33 / 255, 89 / 255, 116 / 255, 1),
            on_press=self.switch_to_main,
        )

        root = ScrollView(size_hint=(1, 1))
        root.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        layout.add_widget(back_button)
        root.add_widget(layout)
        self.add_widget(root)

    def switch_to_main(self, instance):
        self.manager.current = "main"

    def get_driver_standings(self):
        api_url = "https://ergast.com/api/f1/current/driverStandings.json"
        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()
            return data["MRData"]["StandingsTable"]["StandingsLists"][0][
                "DriverStandings"
            ]
        else:
            print(f"Error fetching data: {response.status_code}")
            return []
