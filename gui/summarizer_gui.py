from kivy.config import Config
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import ObjectProperty
from kivy.clock import Clock

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
            hint_text: "Paste your text here"
            size_hint_y: 0.7
            multiline: True

        # Horizontal layout for button and progress bar
        BoxLayout:
            size_hint_y: 0.1
            Button:
                text: "Generate Summary"
                # Adjust the size_hint_x to control the width relative to the progress bar
                size_hint_x: None
                width: 200
                height: 150
                on_release: root.generate_summary()
            ProgressBar:
                id: progress_bar
                max: 100
                value: 0
                # Adjust the size_hint_x to control the width relative to the button
                size_hint_x: 0.7         
     
        TextInput:
            id: output_text
            hint_text: "Summary will appear here"
            size_hint_y: 0.20
            readonly: True
            multiline: True
""")

class SummarizerScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')  # Root layout for this screen's content
        # [Add content to layout]
        self.add_widget(layout)

    def generate_summary(self):
        # Dummy function to simulate progress
        self.ids.progress_bar.value = 0  # Reset progress bar
        Clock.schedule_interval(self.simulate_progress, 0.1)

    def simulate_progress(self, dt):
        if self.ids.progress_bar.value >= 100:
            Clock.unschedule(self.simulate_progress)
            self.ids.output_text.text = "This is a dummy summary."  # Placeholder summary
        else:
            self.ids.progress_bar.value += 5
