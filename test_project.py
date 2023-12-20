from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from project import MyApp


def test_build_method():
    app = MyApp()
    screen_manager = app.build()
    assert isinstance(screen_manager, ScreenManager)
    assert len(screen_manager.children) == 1  # Assuming you have 6 screens

def test_set_window_size_method():
    app = MyApp()
    app.set_window_size()
    assert Window.fullscreen == "auto"

def test_switch_to_driver_overview_method():
    app = MyApp()
    app.build()
    app.main_screen.switch_to_driver_overview(None)
    assert app.screen_manager.current == "driver_overview"

def test_switch_to_champion_standings_method():
    app = MyApp()
    app.build()
    app.main_screen.switch_to_champion_standings(None)
    assert app.screen_manager.current == "champion_standings"

def test_switch_to_tracks_method():
    app = MyApp()
    app.build()
    app.main_screen.switch_to_tracks(None)
    assert app.screen_manager.current == "tracks"