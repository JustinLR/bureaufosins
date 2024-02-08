from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.core.window import Window
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from gui.summarizer_gui import SummarizerScreen
from gui.book_hub_gui import BookHubScreen
from gui.character_creator_gui import CharacterCreatorScreen
from gui.settings_gui import SettingsScreen

# Homepage Screen
class HomepageScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        greeting = Label(text='Welcome to the Application!')
        layout.add_widget(greeting)
        self.add_widget(layout)

# Main Application Layout
class MainLayout(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'

        # Root layout for this screen
        root_layout = BoxLayout(orientation='horizontal')
        self.add_widget(root_layout)
         
        # Left bar with navigation buttons
        left_bar = BoxLayout(orientation='vertical', size_hint_x=None, width=200)  # Navigation bar
        root_layout.add_widget(left_bar)
        
        # Button to switch to Homepage
        homepage_btn = Button(text='Homepage')
        homepage_btn.bind(on_release=lambda x: self.switch_screen('homepage'))
        left_bar.add_widget(homepage_btn)

        # Button to switch to Summarizer tool
        summarizer_btn = Button(text='Summarizer')
        summarizer_btn.bind(on_release=lambda x: self.switch_screen('summarizer'))
        left_bar.add_widget(summarizer_btn)

        # Button to switch to Book Hub tool
        book_hub_btn = Button(text='Book Hub')
        book_hub_btn.bind(on_release=lambda x: self.switch_screen('book_hub'))
        left_bar.add_widget(book_hub_btn)

        # Button to switch to Character Creator tool
        character_creator_btn = Button(text='Character Creator')
        character_creator_btn.bind(on_release=lambda x: self.switch_screen('character_creator'))
        left_bar.add_widget(character_creator_btn)

        # Button to switch to Settings
        settings_btn = Button(text='Settings')
        settings_btn.bind(on_release=lambda x: self.switch_screen('settings'))
        left_bar.add_widget(settings_btn)

        exit_btn = Button(text='Exit')
        exit_btn.bind(on_release=lambda x: self.exit_application())
        left_bar.add_widget(exit_btn)

        # Screen manager to host the different tool screens
        self.screen_manager = ScreenManager(transition=FadeTransition(duration=0.1))
        root_layout.add_widget(self.screen_manager)
        
        # Add screens to the screen manager
        self.screen_manager.add_widget(HomepageScreen(name='homepage'))
        self.screen_manager.add_widget(SummarizerScreen(name='summarizer'))
        self.screen_manager.add_widget(BookHubScreen(name='book_hub'))
        self.screen_manager.add_widget(CharacterCreatorScreen(name='character_creator'))
        self.screen_manager.add_widget(SettingsScreen(name='settings'))

    def switch_screen(self, screen_name):
        self.screen_manager.current = screen_name
        
    def exit_application(self):
        App.get_running_app().stop()

# The Kivy App
class AuthorsToolboxApp(App):
    def build(self):
        # Bind the on_request_close event
        Window.bind(on_request_close=self.on_request_close)
        return MainLayout()
    
    def on_request_close(self, *args, **kwargs):
        # Handle the close request here (e.g., show a confirmation dialog)
        # Return False to allow the window to close, True to prevent it.
        print("Exit requested.")
        return False

if __name__ == '__main__':
    AuthorsToolboxApp().run()
