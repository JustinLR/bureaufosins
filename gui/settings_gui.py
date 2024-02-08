from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label

class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.add_widget(self.layout)

        self.tabbed_panel = TabbedPanel(do_default_tab=False, tab_pos='left_top')
        self.layout.add_widget(self.tabbed_panel)

        api_tab = TabbedPanelItem(text='API Key')
        self.api_key_input = TextInput(hint_text='Enter your API Key here', multiline=False)
        api_tab.add_widget(self.api_key_input)
        self.tabbed_panel.add_widget(api_tab)

        general_tab = TabbedPanelItem(text='General')
        general_tab.add_widget(Label(text='General settings go here'))
        self.tabbed_panel.add_widget(general_tab)

        save_button = Button(text='Save Settings', size_hint=(1, None), height='50dp')
        save_button.bind(on_release=self.save_settings)
        self.layout.add_widget(save_button)

    def save_settings(self, instance):
        api_key = self.api_key_input.text
        print(f"API Key: {api_key}")

class ApiKeyScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10)
        layout.add_widget(Label(text="API Key"))
        self.api_key_input = TextInput(text='', multiline=False)
        layout.add_widget(self.api_key_input)
        self.add_widget(layout)

class OtherSettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10)
        layout.add_widget(Label(text="Other Settings"))
        self.add_widget(layout)
