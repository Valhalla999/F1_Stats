from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivy.core.window import Window
from my_app.views.main_screen import MainScreen
from my_app.views.driver_overview import DriverOverviewScreen
from my_app.views.champion_standings import ChampionStandingsScreen
from my_app.views.tracks_screen import TracksScreen
from my_app.views.kivymd_page import KivyMDPage
from my_app.views.about_me_screen import AboutMeScreen


class MyApp(MDApp):
    def build(self):
        self.screen_manager = ScreenManager()
        self.set_window_size()

        # Create and add screens
        self.main_screen = MainScreen(name="main")
        self.driver_overview_screen = DriverOverviewScreen(name="driver_overview")
        self.champion_standing_screen = ChampionStandingsScreen(name="champion_standings")
        self.tracks_screen = TracksScreen(name="tracks")
        self.about_me_screen = AboutMeScreen(name="about_me")
        self.kivymd_page = KivyMDPage(name="kivymd_page")

        self.screen_manager.add_widget(self.main_screen)
        self.screen_manager.add_widget(self.driver_overview_screen)
        self.screen_manager.add_widget(self.champion_standing_screen)
        self.screen_manager.add_widget(self.tracks_screen)
        self.screen_manager.add_widget(self.about_me_screen)
        self.screen_manager.add_widget(self.kivymd_page)

        return self.screen_manager
    
    def set_window_size(self):
        #Window.size = (width, height)
        Window.fullscreen = 'auto'


if __name__ == "__main__":
    MyApp().run()
