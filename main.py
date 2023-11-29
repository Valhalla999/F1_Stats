from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen

from my_app.views.main_screen import MainScreen
from my_app.views.driver_overview import DriverOverviewScreen
from my_app.views.champion_standings import ChampionStandingsScreen
from my_app.views.test import test


class MyApp(App):
    def build(self):
        self.screen_manager = ScreenManager()

        #Create and add screens:
        self.main_screen = MainScreen(name='main')
        self.driver_overview_screen = DriverOverviewScreen(name='driver_overview')
        self.champion_standing_screen = ChampionStandingsScreen(name='champion_standings')
        self.test_screen = test(name='test')


        self.screen_manager.add_widget(self.main_screen)
        self.screen_manager.add_widget(self.driver_overview_screen)
        self.screen_manager.add_widget(self.champion_standing_screen)
        self.screen_manager.add_widget(self.test_screen)


        return self.screen_manager
        

if __name__ == '__main__':
    MyApp().run()