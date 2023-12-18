from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.button import MDFlatButton
from kivymd.uix.datatables import MDDataTable
from kivy.uix.screenmanager import Screen
from kivy.metrics import dp
from kivymd.uix.button import MDFillRoundFlatButton

import requests


class TracksScreen(Screen):
    def __init__(self, **kwargs):
        super(TracksScreen, self).__init__(**kwargs)

        self.selected_year = 2023
        self.api_year = 2023
        self.api_circuit = 'albert_park'

        # Create the layout
        self.layout = BoxLayout(
            orientation='vertical',
            spacing=20,
            padding=40,
        ) 
        
        self.ids['results_layout'] = BoxLayout(
            orientation='vertical'
        )
        
        self.year_button = MDFillRoundFlatButton(
            text="Select Year",
            theme_text_color='Custom',
            pos_hint={"center_x": 0.5},
            size_hint=(0.1, 0.1),
            text_color=(1, 1, 1, 1),
            md_bg_color=(33 / 255, 89 / 255, 116 / 255, 1),
            on_release=self.open_year_menu
            )
        
        self.circuit_button = MDFillRoundFlatButton(
            text="Select Circuit",
            theme_text_color='Custom',
            pos_hint={"center_x": 0.5},
            size_hint=(0.1, 0.1),
            text_color=(1, 1, 1, 1),
            md_bg_color=(33 / 255, 89 / 255, 116 / 255, 1),
            on_release=lambda instance: self.open_circuit_menu(instance)
            )
        
        api_button = MDFillRoundFlatButton(
            text="Get Data",
            theme_text_color="Custom",
            pos_hint={"center_x": 0.5},
            size_hint=(0.1, 0.1),
            text_color=(1, 1, 1, 1),
            md_bg_color=(33 / 255, 89 / 255, 116 / 255, 1),
            on_press=self.on_api_button_press)
        
        debug_button = MDFillRoundFlatButton(
            text="Debug",
            theme_text_color="Custom",
            pos_hint={"center_x": 0.5},
            size_hint=(0.1, 0.1),
            text_color=(1, 1, 1, 1),
            md_bg_color=(33 / 255, 89 / 255, 116 / 255, 1),
            on_press=self.debug_button)
        
        back_button = MDFillRoundFlatButton(
            text="Back to Main",
            theme_text_color="Custom",
            pos_hint={"center_x": 0.5},
            size_hint=(0.1, 0.1),          
            text_color=(1, 1, 1, 1),
            md_bg_color=(33 / 255, 89 / 255, 116 / 255, 1),
            on_press=self.switch_to_main,
        )
        
        # Initialize dropdown menus
        self.circuit_menu = MDDropdownMenu(
            radius=[20, 20, 20, 20],
            width_mult=4
            )
        
        self.year_menu = MDDropdownMenu(
            radius=[20, 20, 20, 20],
            width_mult=4
            )

        self.populate_years()
        self.populate_circuits(year=self.selected_year)


        
        
        
        #self.layout.add_widget(label_year)
        self.layout.add_widget(self.year_button)
        self.layout.add_widget(self.circuit_button)
        self.layout.add_widget(api_button)
        self.layout.add_widget(debug_button)
        self.layout.add_widget(back_button)

        self.layout.add_widget(self.ids['results_layout'])
        self.add_widget(self.layout)
        
        
    def switch_to_main(self, instance):
        self.manager.current = "main"

    def debug_button(self, instance):
        print(f'Year: {self.api_circuit}')
        print(f'Circuit: {self.api_year}')



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


    def select_circuit(self, circuit ):
        # Handle circuit selection
        print(circuit)
        self.api_circuit = circuit
        self.circuit_menu.dismiss()

        label_circuit_text = f"Selected Circuit: {circuit}"
        label_id = 'circuit_label'

        # Check if a label with id 'circuit_label' already exists in self.layout
        existing_circuit_label = next((widget for widget in self.layout.children if isinstance(widget, Label) and widget.id == label_id), None)

        if existing_circuit_label:
            # Update the text of the existing label
            existing_circuit_label.text = label_circuit_text
        else:
            # Create a new label with id 'circuit_label' if it doesn't exist
            label = Label(
                text=label_circuit_text,
                pos_hint={"center_x": 0.5},
                size_hint=(None, None),
                color=(0, 0, 0, 1)
            )
            label.id = label_id
            self.layout.add_widget(label)

    def select_year(self, year):
        # Handle year selection
        print(year)
        self.api_year = year
        self.populate_circuits(year)
        self.year_menu.dismiss() 

        label_year_text = f"Selected Year: {year}"
        label_id = 'year_label'

        existing_year_label = next((widget for widget in self.layout.children if isinstance(widget, Label) and widget.id == label_id), None)

        if existing_year_label:
            # Update the text of the existing label
            existing_year_label.text = label_year_text
        else:
            # Create a new label with id 'year_label' if it doesn't exist
            label = Label(
                text=label_year_text,
                pos_hint={"center_x": 0.5},
                size_hint=(None, None),
                color=(0, 0, 0, 1)
            )
            label.id = label_id
            self.layout.add_widget(label)

    def on_api_button_press(self, instance):

        if self.circuit_menu.caller is not None and self.year_menu.caller.text is not None:
            circuit = self.circuit_menu.caller.text
            year = self.year_menu.caller.text
        

            api_url = f'http://ergast.com/api/f1/{self.api_year}/circuits/{self.api_circuit}/results.json'
            response = requests.get(api_url)
            api_results = response.json().get('MRData', {}).get('RaceTable', {}).get('Races', [])
            
            self.show_results_dialog(api_results)

            print(f"API Results for {self.api_year} at {self.api_circuit}:") #api_results)

        else:
            print("Please select a circuit and a year before making the API request.")


    def show_results_dialog(self, api_results):
            
            if hasattr(self.ids, 'results_layout'):
                self.ids.results_layout.clear_widgets()
            else:
                # Create an MDBoxLayout for displaying the results
                results_layout = BoxLayout(
                    orientation='vertical',
                    spacing=2,
                    padding=2,
                )
                self.ids.results_layout = results_layout

            if api_results:
                for race in api_results:
                    race_info = f"Round: {race.get('round')}, Race: {race.get('raceName')}, " \
                                f"Location: {race.get('Circuit', {}).get('Location', {}).get('locality')}, " \
                                f"Date: {race.get('date')}"

                    label = MDLabel(
                        text=race_info,
                        theme_text_color="Secondary",
                        size_hint_y=None,
                        height=dp(20)
                    )
                    self.ids.results_layout.add_widget(label)

                    table_layout = BoxLayout(orientation='vertical')
                    results_data = race.get('Results', [])

                    if results_data:
                        column_data = [
                            ("Position", dp(30)),
                            ("Driver", dp(50)),
                            ("Constructor", dp(50)),
                            ("Points", dp(30)),
                        ]

                        row_data = [
                            (str(result.get('position', '')),
                            result.get('Driver', {}).get('familyName', '') + ' ' + result.get('Driver', {}).get('givenName', ''),
                            result.get('Constructor', {}).get('name', ''),
                            result.get('points', ''))
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
                            elevation=2,
                            size_hint_y=None,
                            height=dp(len(row_data)*30 + 65)
                            )
                        
                        table_layout.add_widget(table)

                    self.ids.results_layout.add_widget(table_layout)

            else:
                print("No results to display.")