from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.filechooser import FileChooserListView
from kivy.graphics import Color, Rectangle, Line
from kivy.uix.widget import Widget
from kivy.clock import Clock

class DottedLineImagePlaceholder(Widget):
    """A custom widget to display a placeholder with dotted lines."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (200, 200)  # Specify the size of the widget
        Clock.schedule_once(lambda dt: self.draw_dotted_line(), 0.1)

    def draw_dotted_line(self, *args):
        """Draws dotted lines on the canvas to indicate a placeholder."""
        self.canvas.clear()
        with self.canvas:
            Color(1, 1, 1, 1)  # Set color to white for the dotted lines
            margin = 5
            # Draw a rectangle with dotted lines
            Line(rectangle=(self.x + margin, self.y + margin, self.width - 2*margin, self.height - 2*margin), dash_offset=2, dash_length=5)

    def on_size(self, *args):
        """Redraws the dotted line when the widget size changes."""
        self.draw_dotted_line()

    def on_pos(self, *args):
        """Redraws the dotted line when the widget position changes."""
        self.draw_dotted_line()


class FileChooser(Popup):
    """A popup for choosing files, customized for selecting book files."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (0.9, 0.9)
        self.title = 'Select a Book File'

        filechooser = FileChooserListView(path='.', size_hint=(1, 0.9))
        self.add_widget(filechooser)

        filechooser.bind(on_submit=self.selected)

    def selected(self, filechooser, selection, touch):
        """Handles the selection of a file and prints its path."""
        if selection:
            # Handle the selected file path. E.g., update the book's path in your data
            print("Selected path:", selection[0])
            self.dismiss()
            
# Sample data representing books in the application
books = [
    {'id': 1, 'title': 'Book Title 1', 'summary': 'Summary 1', 'image_path': 'path/to/image1.png'},
    {'id': 2, 'title': 'Book Title 2', 'summary': 'Summary 2', 'image_path': 'path/to/image2.png'},
    # Additional books can be added here
]

class EditBooksPopup(Popup):
    """A popup for editing the list of books."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (.8, .8)
        self.title = 'Edit Books'

        layout = BoxLayout(orientation='vertical')
        book_list = GridLayout(cols=1, spacing=10, size_hint_y=None)
        book_list.bind(minimum_height=book_list.setter('height'))

        # Dynamically create buttons for each book for editing
        for book in books:
            book_entry = Button(text=f"{book['title']}", size_hint_y=None, height=40)
            book_entry.bind(on_press=lambda x, book_id=book['id']: self.edit_book(book_id))
            book_list.add_widget(book_entry)

        scroll_view = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        scroll_view.add_widget(book_list)
        layout.add_widget(scroll_view)

        browse_button = Button(text="Browse Files", size_hint_y=None, height=50)
        browse_button.bind(on_press=self.open_file_chooser)
        layout.add_widget(browse_button)

        self.add_widget(layout)

    def open_file_chooser(self, instance):
        """Opens the file chooser popup."""
        popup = FileChooser()
        popup.open()

    def edit_book(self, book_id):
        """Placeholder for the book editing functionality."""
        print(f"Edit book with ID: {book_id}")
        self.dismiss()

class BookHubScreen(Screen):
    """Main screen for displaying and managing books."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        outer_layout = BoxLayout(orientation='vertical', size_hint_y=None)

        self.layout = GridLayout(cols=2, spacing=10, size_hint=(1, None), padding=10)
        self.layout.bind(minimum_height=self.layout.setter('height'))
        self.layout.row_force_default = True
        self.layout.row_default_height = 400

        scroll_view = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        scroll_view.add_widget(self.layout)
        outer_layout.add_widget(scroll_view)

        self.add_widget(outer_layout)

        # Populate the screen with book entries
        for book in books:
            self.add_book(book)

        # Edit button to modify the list of books
        bottom_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        edit_btn = Button(text='Edit Books', size_hint=(None, None), width=200, height=50)
        edit_btn.bind(on_press=self.open_edit_popup)
        bottom_layout.add_widget(edit_btn)
        self.add_widget(bottom_layout)

    def add_book(self, book):
        """Adds a book entry to the GridLayout."""
        book_layout = BoxLayout(orientation='vertical', size_hint=(None, None), spacing=5)
        book_layout.size = (200, 300)  # Set the size for each book entry

        # Use a placeholder image if a specific path is detected, otherwise display the actual image
        if book['image_path'] in ['path/to/image1.png', 'path/to/image2.png']:
            img = DottedLineImagePlaceholder()
        else:
            img = Image(source=book['image_path'], size_hint=(None, None), size=(200, 100))
        book_layout.add_widget(img)
        
        title = Label(text=book['title'], size_hint_y=None, height=20)
        book_layout.add_widget(title)
        
        summary = Label(text=book['summary'], size_hint_y=None, height=40)
        book_layout.add_widget(summary)
        
        open_btn = Button(text='Open', size_hint_y=None, height=40)
        # Here you might bind the button to a function to open/view the book details
        book_layout.add_widget(open_btn)

        self.layout.add_widget(book_layout)

    def open_edit_popup(self, instance):
        """Opens the popup for editing books."""
        popup = EditBooksPopup()
        popup.open()
