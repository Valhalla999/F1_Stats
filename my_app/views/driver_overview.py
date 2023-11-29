from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
import requests

class DriverOverviewScreen(Screen):
    def __init__(self, **kwargs):
        super(DriverOverviewScreen, self).__init__(**kwargs)

        layout = BoxLayout(orientation='vertical',spacing=10)

        header_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=30)
        header_layout.add_widget(Label(text="Driver", size_hint_x=0.4))
        header_layout.add_widget(Label(text="Nationality", size_hint_x=0.2))
        header_layout.add_widget(Label(text="Date of Birth", size_hint_x=0.2))
        header_layout.add_widget(Label(text="Permanent Number", size_hint_x=0.2))
        layout.add_widget(header_layout)

        drivers_data = self.get_current_f1_drivers()
        for driver in drivers_data:
            row_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=30)
            row_layout.add_widget(Label(text=f"{driver['givenName']} {driver['familyName']}", size_hint_x=0.4))
            row_layout.add_widget(Label(text=driver['nationality'], size_hint_x=0.2))
            row_layout.add_widget(Label(text=driver['dateOfBirth'], size_hint_x=0.2))
            row_layout.add_widget(Label(text=driver['permanentNumber'], size_hint_x=0.2))
            layout.add_widget(row_layout)
                
        # Create a ScrollView and add the layout to it
        scroll_view = ScrollView(size_hint=(1, 1), do_scroll_x=False)
        scroll_view.add_widget(layout)

        back_button = Button(text="Back",
            size_hint=(1, 1), 
            bold=True, 
            background_color='#215974',
            background_normal='') 
        back_button.bind(on_press=self.switch_to_main)

        # Create a BoxLayout to contain the ScrollView and the back button
        container_layout = BoxLayout(orientation='vertical')
        container_layout.add_widget(scroll_view)
        container_layout.add_widget(back_button)

        self.add_widget(container_layout)

    def switch_to_main(self, instance):
        self.manager.current = 'main'



    def get_current_f1_drivers(self):
        #Request to Ergast API
        api_url = "https://ergast.com/api/f1/current/drivers.json"
        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()
            return data['MRData']['DriverTable']['Drivers']
        else:
            print(f"Error fetching data: {response.status_code}")
            return []