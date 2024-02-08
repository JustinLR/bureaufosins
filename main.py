from kivy.config import Config
Config.set('input', 'mouse', 'mouse,disable_multitouch')
Config.set('graphics', 'width', '1024')
Config.set('graphics', 'height', '768')

from gui.authors_toolbox_gui import AuthorsToolboxApp
# Import any necessary modules for initialization

def main():
    # Perform any pre-initialization if needed
    # e.g., setting up logging, loading configurations
    
    app = AuthorsToolboxApp()
    # You could pass any necessary backend services or configurations to the App here
    app.run()

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        # Handle top-level exceptions
        # Log the exception or display an error message
        print(f"Unhandled exception: {e}")
        # Optionally, perform any cleanup here
