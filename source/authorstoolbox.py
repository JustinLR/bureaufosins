from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.core.window import Window
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label

# Importing custom screens for different functionalities
from source.summarizer import SummarizerScreen
from source.bookhub import BookHubScreen
from source.charactercreator import CharacterCreatorScreen
from source.settings import SettingsScreen

class HomepageScreen(Screen):
    """Defines the homepage screen layout and components."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Main layout for the homepage
        layout = BoxLayout(orientation='vertical')
        # Greeting label displayed on the homepage
        greeting = Label(text='Welcome to the Application!')
        layout.add_widget(greeting)
        self.add_widget(layout)

class MainLayout(Screen):
    """Main application layout hosting the navigation and screen manager."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Root layout configuration
        root_layout = BoxLayout(orientation='horizontal')
        self.add_widget(root_layout)
         
        # Side bar for navigation between screens
        left_bar = BoxLayout(orientation='vertical', size_hint_x=None, width=200)
        root_layout.add_widget(left_bar)
        
        # Navigation buttons for each application screen
        # Button to navigate to the Homepage
        homepage_btn = Button(text='Homepage')
        homepage_btn.bind(on_release=lambda x: self.switch_screen('homepage'))
        left_bar.add_widget(homepage_btn)

        # Button to navigate to the Summarizer tool
        summarizer_btn = Button(text='Summarizer')
        summarizer_btn.bind(on_release=lambda x: self.switch_screen('summarizer'))
        left_bar.add_widget(summarizer_btn)

        # Button to navigate to the Book Hub
        book_hub_btn = Button(text='Book Hub')
        book_hub_btn.bind(on_release=lambda x: self.switch_screen('book_hub'))
        left_bar.add_widget(book_hub_btn)

        # Button to navigate to the Character Creator
        character_creator_btn = Button(text='Character Creator')
        character_creator_btn.bind(on_release=lambda x: self.switch_screen('character_creator'))
        left_bar.add_widget(character_creator_btn)

        # Button to navigate to the Settings
        settings_btn = Button(text='Settings')
        settings_btn.bind(on_release=lambda x: self.switch_screen('settings'))
        left_bar.add_widget(settings_btn)

        # Button to exit the application
        exit_btn = Button(text='Exit')
        exit_btn.bind(on_release=lambda x: self.exit_application())
        left_bar.add_widget(exit_btn)

        # Screen manager for handling screen transitions
        self.screen_manager = ScreenManager(transition=FadeTransition(duration=0.1))
        root_layout.add_widget(self.screen_manager)
        
        # Adding the individual screens to the screen manager
        self.screen_manager.add_widget(HomepageScreen(name='homepage'))
        self.screen_manager.add_widget(SummarizerScreen(name='summarizer'))
        self.screen_manager.add_widget(BookHubScreen(name='book_hub'))
        self.screen_manager.add_widget(CharacterCreatorScreen(name='character_creator'))
        self.screen_manager.add_widget(SettingsScreen(name='settings'))

    def switch_screen(self, screen_name):
        """Switches the current screen based on the screen name."""
        self.screen_manager.current = screen_name
        
    def exit_application(self):
        """Closes the application."""
        App.get_running_app().stop()

class AuthorsToolboxApp(App):
    """The main Kivy application class."""
    def build(self):
        # Binding the close event to enable custom close handling
        Window.bind(on_request_close=self.on_request_close)
        return MainLayout()
    
    def on_request_close(self, *args, **kwargs):
        # Custom handler for the window close request
        # Implement confirmation dialog or cleanup here if necessary
        print("Exit requested.")
        return False
