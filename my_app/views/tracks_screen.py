from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivymd.uix.button import MDFillRoundFlatButton
from kivy.uix.image import Image

from my_app.api import get_circuits, get_race_results, get_seasons


class TracksScreen(Screen):
    def __init__(self, **kwargs):
        super(TracksScreen, self).__init__(**kwargs)

        self.selected_year = "current"
        self.api_year = self.selected_year
        self.api_circuit = ""

        self.layout = BoxLayout(
            orientation="vertical",
            spacing=20,
            padding=20,
        )

        self.ids["results_layout"] = BoxLayout(
            orientation="vertical",
            pos_hint={"center_x": 0.5},
        )

        self.year_button = MDFillRoundFlatButton(
            text="Select Year",
            theme_text_color="Custom",
            pos_hint={"center_x": 0.5},
            size_hint=(0.1, 0.1),
            text_color=(1, 1, 1, 1),
            md_bg_color=(33 / 255, 89 / 255, 116 / 255, 1),
            on_release=self.open_year_menu,
        )

        self.circuit_button = MDFillRoundFlatButton(
            text="Select Circuit",
            theme_text_color="Custom",
            pos_hint={"center_x": 0.5},
            size_hint=(0.1, 0.1),
            text_color=(1, 1, 1, 1),
            md_bg_color=(33 / 255, 89 / 255, 116 / 255, 1),
            on_release=lambda instance: self.open_circuit_menu(instance),
        )

        api_button = MDFillRoundFlatButton(
            text="Get Data",
            theme_text_color="Custom",
            pos_hint={"center_x": 0.5},
            size_hint=(0.1, 0.1),
            text_color=(1, 1, 1, 1),
            md_bg_color=(33 / 255, 89 / 255, 116 / 255, 1),
            on_press=self.on_api_button_press,
        )

        back_button = MDFillRoundFlatButton(
            text="Back to Main",
            theme_text_color="Custom",
            pos_hint={"center_x": 0.5},
            size_hint=(0.1, 0.1),
            text_color=(1, 1, 1, 1),
            md_bg_color=(33 / 255, 89 / 255, 116 / 255, 1),
            on_press=self.switch_to_main,
        )

        logo = Image(
            source="my_app/assets/Tech-Play-logo_black.png",
            size_hint=(0.1, 0.1),
            pos_hint={"center_x": 0.5},
        )

        # Initialize dropdown menus
        self.circuit_menu = MDDropdownMenu(radius=[20, 20, 20, 20], width_mult=4)

        self.year_menu = MDDropdownMenu(radius=[20, 20, 20, 20], width_mult=4)

        self.populate_years()
        self.populate_circuits(year=self.selected_year)

        self.year_label = MDLabel(
            text="Selected Year: Current season",
            pos_hint={"center_x": 0.5},
            size_hint=(None, None),
            theme_text_color="Primary",
            color=(0, 0, 0, 1),
        )

        self.circuit_label = MDLabel(
            text="Select a circuit",
            pos_hint={"center_x": 0.5},
            size_hint=(None, None),
            theme_text_color="Primary",
            color=(0, 0, 0, 1),
        )

        self.layout.add_widget(logo)

        self.layout.add_widget(self.ids["results_layout"])

        self.layout.add_widget(self.year_button)
        self.layout.add_widget(self.year_label)

        self.layout.add_widget(self.circuit_button)
        self.layout.add_widget(self.circuit_label)

        self.layout.add_widget(api_button)
        self.layout.add_widget(back_button)

        self.add_widget(self.layout)

    def switch_to_main(self, instance):
        self.manager.current = "main"

    def open_circuit_menu(self, instance):
        self.circuit_menu.caller = instance
        self.circuit_menu.open()

    def open_year_menu(self, instance):
        self.year_menu.caller = instance
        self.year_menu.open()

    def populate_circuits(self, year):
        circuits = get_circuits(year)

        self.circuit_menu.items = [
            {
                "text": circuit.get("circuitName", "Unknown circuit"),
                "viewclass": "OneLineListItem",
                "on_release": lambda circuit_name=circuit.get("circuitId", ""): (
                    self.select_circuit(circuit_name)
                ),
            }
            for circuit in circuits
            if circuit.get("circuitId")
        ]

    def populate_years(self, year=None):
        all_years = get_seasons()
        sorted_years = sorted(
            all_years,
            key=lambda season: int(season.get("season", 0)),
            reverse=True,
        )

        self.year_menu.items = [
            {
                "text": year.get("season", ""),
                "viewclass": "OneLineListItem",
                "on_release": lambda season=year.get("season", ""): (
                    self.select_year(season)
                ),
            }
            for year in sorted_years
            if year.get("season")
        ]

    def select_circuit(self, circuit):
        self.api_circuit = circuit
        self.circuit_menu.dismiss()
        self.circuit_label.text = f"Selected Circuit: {circuit}"

    def select_year(self, year):
        self.api_year = str(year)
        self.api_circuit = ""
        self.populate_circuits(year)
        self.year_menu.dismiss()
        self.year_label.text = f"Selected Year: {year}"
        self.circuit_label.text = "Select a circuit"

    def on_api_button_press(self, instance):
        if not self.api_year or not self.api_circuit:
            self.show_message("Please select a year and circuit first.")
            return

        api_results = get_race_results(self.api_year, self.api_circuit)
        self.show_results_dialog(api_results)

    def show_message(self, message):
        self.ids["results_layout"].clear_widgets()
        self.ids["results_layout"].add_widget(
            MDLabel(
                text=message,
                theme_text_color="Secondary",
                halign="center",
                size_hint_y=None,
                height=dp(32),
            )
        )

    def show_results_dialog(self, api_results):
        if "results_layout" in self.ids:
            self.ids["results_layout"].clear_widgets()
        else:
            results_layout = BoxLayout(
                orientation="vertical",
                spacing=20,
                padding=20,
            )

            self.ids.results_layout = results_layout

        if api_results:
            for race in api_results:
                race_info = (
                    f"Round: {race.get('round')}, Race: {race.get('raceName')}, "
                    f"Location: {race.get('Circuit', {}).get('Location', {}).get('locality')}, "
                    f"Date: {race.get('date')}"
                )

                label = MDLabel(
                    text=race_info,
                    theme_text_color="Secondary",
                    size_hint_y=None,
                    height=dp(20),
                    padding_x=dp(50),
                )

                self.ids["results_layout"].add_widget(label)

                table_layout = BoxLayout(orientation="vertical", spacing=20, padding=20)

                results_data = race.get("Results", [])

                if results_data:
                    column_data = [
                        ("Position", dp(30)),
                        ("Driver", dp(50)),
                        ("Constructor", dp(50)),
                        ("Points", dp(30)),
                    ]

                    row_data = [
                        (
                            str(result.get("position", "")),
                            result.get("Driver", {}).get("familyName", "")
                            + " "
                            + result.get("Driver", {}).get("givenName", ""),
                            result.get("Constructor", {}).get("name", ""),
                            result.get("points", ""),
                        )
                        for result in results_data
                    ]

                    for i, (column_name, width) in enumerate(column_data):
                        if not isinstance(width, (int, float)):
                            column_data[i] = (column_name, dp(100))

                    table = MDDataTable(
                        column_data=column_data,
                        row_data=row_data,
                        check=False,
                        rows_num=30,
                        use_pagination=False,
                        # size_hint_y=None,
                        height=dp(len(row_data) * 30 + 65),
                    )

                    table_layout.add_widget(table)

                self.ids["results_layout"].add_widget(table_layout)

        else:
            self.show_message("No results to display.")
