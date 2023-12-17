from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivymd.uix.label import MDLabel
from kivy.uix.button import Button
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog

import requests


class TracksScreen(Screen):
    def __init__(self, **kwargs):
        super(TracksScreen, self).__init__(**kwargs)

        self.selected_year = 2023

        # Create the layout
        layout = BoxLayout(
            orientation='vertical',
            spacing=20,
            padding=40,
        )

            

        # Labels
        label_circuit = Label(
            text="Select Circuit:",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            #size_hint=(None, None),
            color=(0, 0, 0, 1)
            )
        
        label_year = MDLabel(
            text="Select Year:",
            pos_hint={"center_x": 0.5},
            size_hint=(None, None),
            color=(0, 0, 0, 1)
            )



        #Buttons
        self.circuit_button = MDFlatButton(
            text="Select Circuit",
            theme_text_color='Custom',
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            size_hint=(None, None),
            text_color=(1, 1, 1, 1),
            md_bg_color=(33 / 255, 89 / 255, 116 / 255, 1),
            on_release=lambda instance: self.open_circuit_menu(instance)
            )
        
        self.year_button = MDFlatButton(
            text="Select Year",
            theme_text_color='Custom',
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            size_hint=(None, None),
            text_color=(1, 1, 1, 1),
            md_bg_color=(33 / 255, 89 / 255, 116 / 255, 1),
            on_release=self.open_year_menu
            )
        
        api_button = MDFlatButton(
            text="Get Data",
            theme_text_color="Custom",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            size_hint=(None, None),
            text_color=(1, 1, 1, 1),
            md_bg_color=(33 / 255, 89 / 255, 116 / 255, 1),
            on_press=self.on_api_button_press)

        # Initialize dropdown menus
        self.circuit_menu = MDDropdownMenu(
            radius=[24, 0, 24, 0],
            width_mult=4
            )
        
        self.year_menu = MDDropdownMenu(
            radius=[24, 0, 24, 0],
            width_mult=4
            )

        # Add items to dropdowns (you need to fetch the available circuits and years from the Ergast API)
        self.populate_years()
        self.populate_circuits(year=self.selected_year)

        # Add widgets to the layout

        layout.add_widget(label_year)
        layout.add_widget(self.year_button)

        layout.add_widget(label_circuit)
        layout.add_widget(self.circuit_button)

        layout.add_widget(api_button)
        self.add_widget(layout)





    def open_circuit_menu(self, instance):
        self.circuit_menu.caller = instance
        self.circuit_menu.open()

    def open_year_menu(self, instance):
        self.year_menu.caller = instance
        self.year_menu.open()

    def populate_circuits(self, year):

        print(f'{year}')
        response = requests.get(f'http://ergast.com/api/f1/{year}/circuits.json')
        circuits = response.json().get('MRData', {}).get('CircuitTable', {}).get('Circuits', [])

        # Add items to the dropdown
        self.circuit_menu.items = [
            {
                'text': circuit['circuitName'],
                'viewclass': 'OneLineListItem',
                'on_release': lambda circuit_name=circuit['circuitId']: self.select_circuit(circuit_name)
            }
            for circuit in circuits
        ]

    
    
    def populate_years(self,year=None):
            url = 'http://ergast.com/api/f1/seasons.json'
            more_data = True
            offset = 0

            all_years = []

            while more_data:
                params = {'limit': 100, 'offset': offset}  # Adjust the limit based on API requirements
                response = requests.get(url, params=params)
                data = response.json().get('MRData', {}).get('SeasonTable', {}).get('Seasons', [])

                all_years.extend(data)

                # Check if there are more pages
                offset += len(data)
                more_data = len(data) > 0

            # Sort the years in descending order
            sorted_years = sorted(all_years, key=lambda x: int(x['season']), reverse=True)

            # Add items to the dropdown
            for year in sorted_years:
                item = {
                    'text': year['season'],
                    'viewclass': 'OneLineListItem',
                    'on_release': lambda season=year['season']: self.select_year(season)
                }
                self.year_menu.items.append(item)


    def select_circuit(self, circuit):
        # Handle circuit selection
        print(circuit)
        self.circuit_menu.dismiss()

    def select_year(self, year):
        # Handle year selection
        print(year)
        self.year_menu.dismiss()
        self.populate_circuits(year)

    def on_api_button_press(self, instance):
        '''try:
            circuit_item = self.circuit_menu.caller.text
            year_item = self.year_menu.caller.text
        except AttributeError:
            circuit_item = None
            year_item = None'''

        if self.circuit_menu.caller is not None and self.year_menu.caller.text is not None:
            circuit = self.circuit_menu.caller.text
            year = self.year_menu.caller.text
        

            # Make API request using the selected circuit and year
            api_url = f'http://ergast.com/api/f1/{year}/circuits/{circuit}/results.json'
            response = requests.get(api_url)


            print(f"API Results for {year} at {circuit}:") #api_results)

            # Add your logic to handle and display the results
            #self.show_results_dialog()
        else:
            print("Please select a circuit and a year before making the API request.")

    def show_results_dialog(self):
        results_dialog = MDDialog(title="API Results", text="Dummy API Results")
        results_dialog.open()
