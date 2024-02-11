from kivy.config import Config
# Configure Kivy settings before importing any Kivy components
Config.set('input', 'mouse', 'mouse,disable_multitouch')
# Disable multitouch emulation through the mouse to prevent right-click from simulating touch.
Config.set('graphics', 'width', '1024')
# Set the default width of the application window.
Config.set('graphics', 'height', '768')
# Set the default height of the application window.

from source.authorstoolbox import AuthorsToolboxApp
# Import the main application class. Ensure this import comes after setting configurations to ensure they take effect.

# Define a main function as the entry point of the application.
def main():
    # This is where you can perform any pre-initialization tasks before the application starts.
    # For example, setting up logging, loading external configurations, or initializing services.

    app = AuthorsToolboxApp()  # Create an instance of the application.
    # Here, you could also pass any necessary backend services, configurations, or global state to the application.
    app.run()  # Start the Kivy application's main event loop.

if __name__ == '__main__':
    try:
        main()  # Try to run the main function.
    except Exception as e:
        # Catch any unhandled exceptions that occur during application startup or runtime.
        print(f"Unhandled exception: {e}")  # Print or log the exception for debugging purposes.
        # Here, you could also perform any necessary cleanup operations or display an error message to the user.
