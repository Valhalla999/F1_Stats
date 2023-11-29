from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.list import TwoLineAvatarListItem, MDList
import requests

class ChampionStandingsScreen(Screen):
    def __init__(self, **kwargs):
        super(ChampionStandingsScreen, self).__init__(**kwargs)

        self.size_hint = (0.9, 0.9)
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        layout = BoxLayout(orientation='vertical',spacing=10)

        standings_header = BoxLayout(orientation='horizontal', size_hint_y=None, height=30)
        standings_header.add_widget(Label(text="Position", size_hint_x=0.2))
        standings_header.add_widget(Label(text="Driver", size_hint_x=0.4))
        standings_header.add_widget(Label(text="Points", size_hint_x=0.2))
        layout.add_widget(standings_header)


        standings_data = self.get_driver_standings()
        for standing in standings_data:
            standing_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=30)
            standing_layout.add_widget(Label(text=standing['position'], size_hint_x=0.2))
            standing_layout.add_widget(Label(text=f"{standing['Driver']['givenName']} {standing['Driver']['familyName']}", size_hint_x=0.4))
            standing_layout.add_widget(Label(text=standing['points'], size_hint_x=0.2))
            layout.add_widget(standing_layout)

        back_button = Button(text="Back",
            size_hint=(1, 1), 
            bold=True, 
            background_color='#215974',
            background_normal='') 
        
        back_button.bind(on_press=self.switch_to_main)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def switch_to_main(self, instance):
        self.manager.current = 'main'



    def get_driver_standings(self):
        #Request to Ergast API
        api_url = "https://ergast.com/api/f1/current/driverStandings.json"
        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()
            return data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']
        else:
            print(f"Error fetching data: {response.status_code}")
            return []