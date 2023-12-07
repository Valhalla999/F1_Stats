from kivy.uix.label import Label
from kivymd.uix.label import MDLabel
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.app import runTouchApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFillRoundFlatButton
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.list import  OneLineListItem
import requests

class ChampionStandingsScreen(Screen):
    def __init__(self, **kwargs):
        super(ChampionStandingsScreen, self).__init__(**kwargs)

        self.size_hint = (0.9, 0.9)
        #self.pos_hint = {'center_x': 0.5, 'center_y': 1}

        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        root = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        

        # Standings Header
        standings_header = MDBoxLayout(orientation='horizontal', adaptive_height=True, spacing=10)
        standings_header.add_widget(OneLineListItem(text="Position", size_hint_x=0.25))
        standings_header.add_widget(OneLineListItem(text="Driver", size_hint_x=0.45))
        standings_header.add_widget(OneLineListItem(text="Points", size_hint_x=0.25))
        layout.add_widget(standings_header)

        # Standings Data
        standings_data = self.get_driver_standings()
        for standing in standings_data:
            standing_layout = MDBoxLayout(orientation='horizontal', adaptive_height=True, spacing=10)
            standing_layout.add_widget(OneLineListItem(text=standing['position'], size_hint_x=0.25))
            standing_layout.add_widget(OneLineListItem(text=f"{standing['Driver']['givenName']} {standing['Driver']['familyName']}", size_hint_x=0.45))            
            standing_layout.add_widget(OneLineListItem(text=standing['points'], size_hint_x=0.25))
            layout.add_widget(standing_layout)
       
        back_button = MDFillRoundFlatButton(
            text="Back",
            size_hint=(0.25, 0.25), 
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),  # Set your text color
            md_bg_color=(33/255, 89/255, 116/255, 1),
            on_press=self.switch_to_main) 
        
        root.add_widget(layout)
        layout.add_widget(back_button)
        self.add_widget(root)

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