import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import StringVar
import webbrowser
import os
from datetime import datetime

# Sample data - replace with your actual book details
books = [
    {
        "title": "Book Title 1",
        "path": "path_or_url_2",
        "last_revised": datetime(2022, 1, 1),
        "info": "Summary of Book 1",
    },
    {
        "title": "Book Title 2",
        "path": "path_or_url_2",
        "last_revised": datetime(2021, 6, 15),
        "info": "Summary of Book 2",
    },
    # Add more books here
]


class AddBookDialog(tk.Toplevel):
    def __init__(self, parent, book=None, refresh_callback=None):
        super().__init__(parent)
        self.refresh_callback = refresh_callback
        self.book = book  # Store the book as an instance attribute
        self.title("Book Details")
        self.is_editing = (
            book is not None
        )  # Determine if we are adding or editing a book

        self.book_var = tk.StringVar()

        # Assuming these StringVars are connected to Entry widgets for title, path, and info
        self.book_title = tk.StringVar(self, value=book["title"] if self.is_editing else "")
        self.book_path = tk.StringVar(self, value=book["path"] if self.is_editing else "")
        self.book_info = tk.StringVar(self, value=book["info"] if self.is_editing else "")

        # Setup UI
        tk.Label(self, text="Title:").pack()
        tk.Entry(self, textvariable=self.book_title).pack()

        tk.Label(self, text="Info:").pack()
        tk.Entry(self, textvariable=self.book_info).pack()  # Corrected to use self.book_info

        tk.Label(self, text="Path:").pack()
        path_entry = tk.Entry(self, textvariable=self.book_path, state="readonly")
        path_entry.pack()
        tk.Button(self, text="Browse", command=self.browse_file).pack()

        # Button text changes based on whether adding a new book or editing an existing one
        button_text = "Confirm" if self.is_editing else "Add Book"
        tk.Button(self, text=button_text, command=self.add_or_edit_book).pack()

    def browse_file(self):
        path = filedialog.askopenfilename()
        print(f"Selected path: {path}")  # Debug print
        if path:
            self.book_path.set(path)
            if (
                not self.is_editing
            ):  # Optionally set title based on file name when adding new books
                title = os.path.splitext(os.path.basename(path))[0]
                if not self.is_editing:
                    file_size = os.path.getsize(path)
                    print(f"Setting title to: {title}")  # Debug print
                    print(f"Setting info to: Size: {file_size} bytes")  # Debug print
                    self.book_title.set(title)
                    self.book_info.set(f"Size: {file_size} bytes")

    def add_or_edit_book(self):
        # Make sure to declare 'books' as global if it's not part of a class or passed in some other way
        global books

        # Extract details from the dialog's inputs
        book_details = {
            "title": self.book_title.get(),
            "path": self.book_path.get(),
            "info": self.book_info.get(),
        }

        if self.is_editing:
            # Assuming 'book' has a unique way to identify it; for simplicity, let's use title here
            # You might need to adjust this logic to use a more robust identification method
            for i, existing_book in enumerate(books):
                if existing_book.get("title") == self.book.get("title"):  # Check if "title" exists
                    # This assumes title is unique
                    books[i] = book_details
                    break
        else:
            # Append new book to the global list
            books.append(book_details)

        # Refresh the book list in the main UI and close the dialog
        if callable(self.refresh_callback):
            self.refresh_callback()
        self.destroy()


def open_book(path_or_url):
    try:
        if path_or_url.startswith("http"):
            # Attempt to open a web URL
            webbrowser.open(path_or_url)
        else:
            # Attempt to open a local file
            os.startfile(path_or_url)
    except Exception as e:
        # Handle the error by showing an error message to the user
        # Here, you would need a reference to the root Tk window if this code is not in the same scope
        messagebox.showerror("Open Failed", f"Failed to open the book: {e}")

        # If 'root' is not accessible directly (e.g., in a different module or class), you might need to pass
        # a reference to the Tk root window to this function or use another method to display the error.

def edit_book(book, parent, refresh_books):
    # Instantiate the AddBookDialog; it will be shown automatically
    edit_dialog = AddBookDialog(parent, book=book, refresh_callback=refresh_books)
    # No need to call edit_dialog.show()

def create_book_buttons(parent, book_list, refresh_books):
    # Clear existing widgets and recreate them with the current book list
    for widget in parent.winfo_children():
        widget.destroy()

    # Create new widgets for each book in the book list
    for book in book_list:
        # Create a frame for each book to organize its display
        book_frame = tk.Frame(parent)
        book_frame.pack(fill=tk.X, pady=5)

        # Display the book title as a button
        title_button = tk.Button(
            book_frame, text=book["title"], command=lambda p=book["path"]: open_book(p)
        )
        title_button.pack(side=tk.LEFT)

        # Display the book info
        info_label = tk.Label(book_frame, text=book["info"])
        info_label.pack(side=tk.LEFT)

        # Display the last revised date, handling books without a 'last_revised' key
        last_revised_str = "Unknown"
        if 'last_revised' in book and book['last_revised']:
            last_revised_str = book["last_revised"].strftime("%Y-%m-%d")
        last_revised_label = tk.Label(book_frame, text="Last Revised: " + last_revised_str)
        last_revised_label.pack(side=tk.LEFT)

        # Display the path; formatting or abbreviation might be needed for readability
        path_label = tk.Label(book_frame, text="Path: " + book["path"])
        path_label.pack(side=tk.LEFT)

        # Add an "Edit" button for each book, ensuring lambda captures book correctly
        edit_button = tk.Button(
            book_frame,
            text="Edit",
            # Use a default argument to capture the current book's state in the lambda
            command=lambda book=book: edit_book(book, parent, refresh_books)
        )
        edit_button.pack(side=tk.RIGHT)

def sort_books(parent, book_list, sort_by, refresh_books, search_query=""):
    filtered_books = [
        book for book in book_list if search_query.lower() in book["title"].lower()
    ]

    if sort_by == "Name":
        sorted_books = sorted(filtered_books, key=lambda x: x["title"].lower())
    elif sort_by == "Date Last Revised":
        sorted_books = sorted(
            filtered_books, key=lambda x: x["last_revised"], reverse=True
        )
    else:
        sorted_books = filtered_books  # Default sorting

    # Make sure this 'parent' is the widget where you want to display the books
    create_book_buttons(parent, sorted_books, refresh_books)


def on_search(window, sorting, search_entry):
    query = search_entry.get()
    sort_books(window, books, sorting.get(), search_query=query)


def setup_book_hub(parent):
    # Define sorting options before defining refresh_books
    sorting = ttk.Combobox(
        parent, values=["Name", "Date Last Revised"], state="readonly"
    )
    sorting.pack(fill=tk.X)
    sorting.set("Name")  # Default sorting criteria

    def refresh_books():
        # Assumes 'sorting' and 'search_entry' are defined in setup_book_hub
        current_sorting = sorting.get()
        current_search_query = (
            search_entry.get()
        )  # Fetch the search query from a search box or similar
        sort_books(parent, books, current_sorting, current_search_query)

    # Add a button to add a new book, correctly passing refresh_books
    add_book_button = tk.Button(
        parent,
        text="Add Book",
        command=lambda: AddBookDialog(parent, refresh_callback=refresh_books),
    )
    add_book_button.pack()

    # Bind the sorting combobox selection to refresh_books instead of sort_books directly
    sorting.bind("<<ComboboxSelected>>", lambda e: refresh_books())

    # Define search_entry and its search button
    search_entry = tk.Entry(parent)
    search_entry.pack(fill=tk.X)
    search_button = tk.Button(parent, text="Search", command=refresh_books)
    search_button.pack(fill=tk.X)

    # Call refresh_books to initialize the book list display
    refresh_books()
