from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog

import requests


class TracksScreen(Screen):
    def __init__(self, **kwargs):
        self.circuit_menu = MDDropdownMenu()
        self.year_menu = MDDropdownMenu()

        super(TracksScreen, self).__init__(**kwargs)

        # Create the layout
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Create labels with black text color
        label_circuit = Label(text="Select Circuit:", color=(0, 0, 0, 1))
        label_year = Label(text="Select Year:", color=(0, 0, 0, 1))

        # Create buttons for dropdowns with black text color
        self.circuit_button = MDFlatButton(
            text="Select Circuit",
            on_release=lambda instance: self.open_circuit_menu(instance),
            theme_text_color='Custom',
            text_color=(0, 0, 0, 1))
        self.year_button = MDFlatButton(text="Select Year", on_release=self.open_year_menu, theme_text_color='Custom', text_color=(0, 0, 0, 1))



        # Add items to dropdowns (you need to fetch the available circuits and years from the Ergast API)
        self.populate_circuits()
        self.populate_years()

        # Create button to trigger API request
        api_button = Button(text="Get Data", on_press=self.on_api_button_press)

        # Add widgets to the layout
        layout.add_widget(label_circuit)
        layout.add_widget(self.circuit_button)
        layout.add_widget(label_year)
        layout.add_widget(self.year_button)
        layout.add_widget(api_button)

        self.add_widget(layout)

        # Initialize dropdown menus
        #self.circuit_menu = MDDropdownMenu()
        #self.year_menu = MDDropdownMenu()

    def open_circuit_menu(self, instance):
        self.circuit_menu.caller = instance
        self.circuit_menu.open()

    def open_year_menu(self, instance):
        self.year_menu.caller = instance
        self.year_menu.open()

   # Modify the populate_circuits method
    def populate_circuits(self):
        response = requests.get('http://ergast.com/api/f1/circuits.json')
        circuits = response.json().get('MRData', {}).get('CircuitTable', {}).get('Circuits', [])

        # Add items to the dropdown
        for circuit in circuits:
            item = {'text': circuit['circuitName'], 'viewclass': 'OneLineListItem', 'on_release': lambda instance_menu_item, circuit=circuit['circuitName']: self.select_circuit(instance_menu_item, circuit)}
            self.circuit_menu.items.append(item)


    def populate_years(self):
        response = requests.get('http://ergast.com/api/f1/seasons.json')
        years = response.json().get('MRData', {}).get('SeasonTable', {}).get('Seasons', [])

        # Add items to the dropdown
        for year in years:
            item = {'text': year, 'viewclass': 'OneLineListItem', 'on_release': self.select_year}
            self.year_menu.items.append(item)


    def select_circuit(self, instance_menu_item, circuit):
        # Handle circuit selection
        print("Selected Circuit:", circuit)
        self.circuit_menu.dismiss()

    def select_year(self,  instance_menu_item, year):
        # Handle year selection
        print("Selected Year:", year)
        self.year_menu.dismiss()

    def on_api_button_press(self, instance):
        circuit_item = self.circuit_menu.current_item
        year_item = self.year_menu.current_item

        if circuit_item is not None and year_item is not None:
            circuit = circuit_item.text
            year = year_item.text

            # Make API request using the selected circuit and year
            api_url = f'http://ergast.com/api/f1/{year}/circuits/{circuit}/results.json'
            response = requests.get(api_url)

            # Process the API response (this depends on the actual Ergast API response structure)
            api_results = response.json()  # Adjust this based on the API response structure
            print(f"API Results for {year} at {circuit}:", api_results)

            # Add your logic to handle and display the results
            self.show_results_dialog()
        else:
            print("Please select a circuit and a year before making the API request.")

    def show_results_dialog(self):
        # Display a dialog with the API results (customize based on your API response)
        results_dialog = MDDialog(title="API Results", text="Dummy API Results")
        results_dialog.open()


#class Tracks(MDApp):
    #def build(self):
        #return TracksScreen()