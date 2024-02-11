from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.core.window import Window

# Importing custom screens for different functionalities
from gui.summarizer_gui import SummarizerScreen
from gui.book_hub_gui import BookHubScreen
from gui.character_creator_gui import CharacterCreatorScreen
from gui.settings_gui import SettingsScreen

class AuthorsToolboxApp(App):
    def build(self):
        self.screen_manager = ScreenManager(transition=FadeTransition(duration=0.1))
        
        # Register screens with the screen manager
        self.screen_manager.add_widget(Screen(name='homepage'))
        self.screen_manager.add_widget(SummarizerScreen(name='summarizer'))
        self.screen_manager.add_widget(BookHubScreen(name='book_hub'))
        self.screen_manager.add_widget(CharacterCreatorScreen(name='character_creator'))
        self.screen_manager.add_widget(SettingsScreen(name='settings'))
        
        Window.bind(on_request_close=self.on_request_close)
        return self.screen_manager

    def on_request_close(self, *args, **kwargs):
        print("Exit requested.")
        return False

if __name__ == '__main__':
    AuthorsToolboxApp().run()
