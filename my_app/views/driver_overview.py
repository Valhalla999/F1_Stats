from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import OneLineListItem
from kivymd.uix.button import MDFillRoundFlatButton

import requests


class DriverOverviewScreen(Screen):
    def __init__(self, **kwargs):
        super(DriverOverviewScreen, self).__init__(**kwargs)

        layout = GridLayout(cols=1, spacing=1, size_hint_y=None)
        layout.bind(minimum_height=layout.setter("height"))

        # Header Layout
        header_layout = MDBoxLayout(
            orientation="horizontal", adaptive_height=True, spacing=10
        )
        header_layout.add_widget(
            OneLineListItem(text="Permanent Number", size_hint_x=0.2)
        )
        header_layout.add_widget(OneLineListItem(text="Driver", size_hint_x=0.4))
        header_layout.add_widget(OneLineListItem(text="Nationality", size_hint_x=0.2))
        header_layout.add_widget(OneLineListItem(text="Date of Birth", size_hint_x=0.2))

        layout.add_widget(header_layout)

        # Driver Data
        drivers_data = self.get_current_f1_drivers()
        for driver in drivers_data:
            row_layout = MDBoxLayout(
                orientation="horizontal", adaptive_height=True, spacing=10
            )
            row_layout.add_widget(
                OneLineListItem(text=driver["permanentNumber"], size_hint_x=0.2)
            )
            row_layout.add_widget(
                OneLineListItem(
                    text=f"{driver['givenName']} {driver['familyName']}",
                    size_hint_x=0.4,
                )
            )
            row_layout.add_widget(
                OneLineListItem(text=driver["nationality"], size_hint_x=0.2)
            )
            row_layout.add_widget(
                OneLineListItem(text=driver["dateOfBirth"], size_hint_x=0.2)
            )

            layout.add_widget(row_layout)

        # Add Back button
        back_button = MDFillRoundFlatButton(
            text="Back to Main",
            size_hint=(None, None),
            size=(200, 50),
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            md_bg_color=(33 / 255, 89 / 255, 116 / 255, 1),  # Change background color
            on_press=self.switch_to_main,
        )

        root = ScrollView(size_hint=(1, 1))
        root.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        layout.add_widget(back_button)
        root.add_widget(layout)
        self.add_widget(root)

    def switch_to_main(self, instance):
        self.manager.current = "main"

    def get_current_f1_drivers(self):
        # Request to Ergast API
        api_url = "https://ergast.com/api/f1/current/drivers.json"
        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()
            return data["MRData"]["DriverTable"]["Drivers"]
        else:
            print(f"Error fetching data: {response.status_code}")
            return []
