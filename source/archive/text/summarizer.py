from kivy.config import Config
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import ObjectProperty
from kivy.clock import Clock

# Define the layout and behavior of the SummarizerScreen using Kivy's Builder language
Builder.load_string("""
<SummarizerScreen>:
    BoxLayout:
        orientation: 'vertical'
        canvas.before:
            Color:
                rgba: 0.345, 0.345, 0.345, 1  # Light grey background for the entire layout
            Rectangle:
                pos: self.pos
                size: self.size
                
        TextInput:
            id: input_text
            hint_text: "Paste your text here"  # Placeholder text for input
            size_hint_y: 0.7  # Allocate 70% of the vertical space to the input field
            multiline: True  # Allow multiple lines of input

        # Horizontal layout for the 'Generate Summary' button and a progress bar
        BoxLayout:
            size_hint_y: 0.1  # Allocate 10% of the vertical space to this layout
            Button:
                text: "Generate Summary"
                size_hint_x: None  # Allow the width to be set explicitly
                width: 200  # Set the button width
                height: 150  # The height seems to be unusually large compared to typical UI elements
                on_release: root.generate_summary()  # Call generate_summary() when button is pressed
            ProgressBar:
                id: progress_bar
                max: 100  # Maximum value of the progress bar
                value: 0  # Initial progress bar value
                size_hint_x: 0.7  # Allocate 70% of the horizontal space to the progress bar 
     
        TextInput:
            id: output_text
            hint_text: "Summary will appear here"  # Placeholder text for output
            size_hint_y: 0.20  # Allocate 20% of the vertical space to the output field
            readonly: True  # Make the output field read-only
            multiline: True  # Allow multiple lines of output
""")

class SummarizerScreen(Screen):
    """Screen for a text summarization tool with input, progress, and output display."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # This initialization does not add additional widgets since the layout is defined in KV language
        layout = BoxLayout(orientation='vertical')  # Root layout for this screen's content
        self.add_widget(layout)  # In this case, adding widgets in Python is redundant due to KV layout

    def generate_summary(self):
        """Initiates the summarization process and updates the progress bar."""
        self.ids.progress_bar.value = 0  # Reset progress bar to 0
        Clock.schedule_interval(self.simulate_progress, 0.1)  # Schedule progress updates

    def simulate_progress(self, dt):
        """Simulates progress bar advancement and displays a dummy summary upon completion."""
        if self.ids.progress_bar.value >= 100:
            Clock.unschedule(self.simulate_progress)  # Stop updating the progress bar
            self.ids.output_text.text = "This is a dummy summary."  # Display placeholder summary text
        else:
            self.ids.progress_bar.value += 5  # Increment the progress bar value
