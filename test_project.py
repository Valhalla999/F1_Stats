import importlib.util
from unittest.mock import patch

import pytest

KIVY_AVAILABLE = importlib.util.find_spec("kivy") is not None
pytestmark = pytest.mark.skipif(not KIVY_AVAILABLE, reason="Kivy is not installed")

if KIVY_AVAILABLE:
    from kivy.core.window import Window
    from kivy.uix.screenmanager import ScreenManager
    from main import MyApp
else:
    MyApp = None
    ScreenManager = None
    Window = None


def build_app_without_api_calls():
    with (
        patch("my_app.views.driver_overview.get_current_drivers", return_value=[]),
        patch("my_app.views.champion_standings.get_driver_standings", return_value=[]),
        patch("my_app.views.tracks_screen.get_circuits", return_value=[]),
        patch("my_app.views.tracks_screen.get_seasons", return_value=[]),
    ):
        app = MyApp()
        screen_manager = app.build()

    return app, screen_manager


def test_build_method():
    app, screen_manager = build_app_without_api_calls()

    assert isinstance(screen_manager, ScreenManager)
    assert sorted(screen.name for screen in screen_manager.screens) == [
        "about_me",
        "champion_standings",
        "driver_overview",
        "main",
        "tracks",
    ]


def test_set_window_size_method():
    app = MyApp()
    app.set_window_size()

    assert Window.fullscreen == "auto"


def test_switch_to_champion_standings_method():
    app, _screen_manager = build_app_without_api_calls()
    app.main_screen.switch_to_champion_standings(None)

    assert app.screen_manager.current == "champion_standings"


def test_switch_to_tracks_method():
    app, _screen_manager = build_app_without_api_calls()
    app.main_screen.switch_to_tracks(None)

    assert app.screen_manager.current == "tracks"
