from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import OneLineListItem
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDFillRoundFlatButton

from my_app.api import get_current_drivers


def driver_number(driver):
    try:
        return int(driver.get("permanentNumber", 0))
    except (TypeError, ValueError):
        return 0


class DriverOverviewScreen(Screen):
    def __init__(self, **kwargs):
        super(DriverOverviewScreen, self).__init__(**kwargs)

        layout = BoxLayout(
            orientation="vertical",
            spacing=10,
            padding=10,
        )
        layout.bind(minimum_height=layout.setter("height"))

        # Adding Header
        header_layout = MDBoxLayout(
            orientation="horizontal",
            adaptive_height=True,
            spacing=10,
            padding=10,
        )
        header_layout.add_widget(
            OneLineListItem(
                text="Permanent Number",
                size_hint_x=0.2)
        )
        header_layout.add_widget(
            OneLineListItem(
                text="Driver",
                size_hint_x=0.4)
                )
        
        header_layout.add_widget(
            OneLineListItem(
                text="Nationality",
                size_hint_x=0.2)
                )
        
        header_layout.add_widget(
            OneLineListItem(
                text="Date of Birth",
                size_hint_x=0.2)
                )

        layout.add_widget(header_layout)


        # Adding Rows
        drivers_data = get_current_drivers()
        sorted_drivers = sorted(
            drivers_data,
            key=driver_number,
        )

        for driver in sorted_drivers:
            row_layout = MDBoxLayout(
                orientation="horizontal",
                adaptive_height=True,
                spacing=10
            )

            row_layout.add_widget(
                OneLineListItem(
                    text=driver.get("permanentNumber", ""),
                    size_hint_x=0.2)
            )

            row_layout.add_widget(
                OneLineListItem(
                    text=f"{driver.get('givenName', '')} {driver.get('familyName', '')}",
                    size_hint_x=0.4)
            )

            row_layout.add_widget(
                OneLineListItem(
                    text=driver.get("nationality", ""),
                    size_hint_x=0.2)
            )

            row_layout.add_widget(
                OneLineListItem(
                    text=driver.get("dateOfBirth", ""),
                    size_hint_x=0.2)
            )

            layout.add_widget(row_layout)

        # Add Back button
        back_button = MDFillRoundFlatButton(
            text="Back to Main",
            size_hint=(0.15, 0.15),
            pos_hint={"center_x": 0.5,},
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            md_bg_color=(33 / 255, 89 / 255, 116 / 255, 1),
            on_press=self.switch_to_main,
        )

        root = ScrollView(
            size_hint=(1, 1)
            )
        
        root.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        layout.add_widget(back_button)
        root.add_widget(layout)
        self.add_widget(root)

    def switch_to_main(self, instance):
        self.manager.current = "main"
