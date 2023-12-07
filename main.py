from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp

from my_app.views.main_screen import MainScreen
from my_app.views.driver_overview import DriverOverviewScreen
from my_app.views.champion_standings import ChampionStandingsScreen
from my_app.views.kivymd_page import KivyMDPage


class MyApp(MDApp):
    def build(self):
        self.screen_manager = ScreenManager()

        # Create and add screens
        self.main_screen = MainScreen(name="main")
        self.driver_overview_screen = DriverOverviewScreen(name="driver_overview")
        self.champion_standing_screen = ChampionStandingsScreen(
            name="champion_standings"
        )
        self.kivymd_page = KivyMDPage(name="kivymd_page")  # Add the new screen

        self.screen_manager.add_widget(self.main_screen)
        self.screen_manager.add_widget(self.driver_overview_screen)
        self.screen_manager.add_widget(self.champion_standing_screen)
        self.screen_manager.add_widget(self.kivymd_page)  # Add the new screen

        return self.screen_manager


if __name__ == "__main__":
    MyApp().run()
