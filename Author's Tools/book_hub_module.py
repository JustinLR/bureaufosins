import tkinter as tk
from tkinter import ttk
import webbrowser
import os
from datetime import datetime

# Sample data - replace with your actual book details
books = [
    {"title": "Book Title 1", "path": "path_or_url_1", "last_revised": datetime(2022, 1, 1), "info": "Summary of Book 1"},
    {"title": "Book Title 2", "path": "path_or_url_2", "last_revised": datetime(2021, 6, 15), "info": "Summary of Book 2"},
    # Add more books here
]

def open_book(path_or_url):
    if path_or_url.startswith("http"):
        webbrowser.open(path_or_url)
    else:
        os.startfile(path_or_url)

def create_book_buttons(window, book_list):
    for widget in window.winfo_children():
        widget.destroy()
    
    for book in book_list:
        button = tk.Button(window, text=book["title"], command=lambda p=book["path"]: open_book(p))
        button.pack()
        info_label = tk.Label(window, text=book["info"])
        info_label.pack()

def sort_books(window, book_list, sort_by, search_query=""):
    filtered_books = [book for book in book_list if search_query.lower() in book["title"].lower()]

    if sort_by == "Name":
        sorted_books = sorted(filtered_books, key=lambda x: x['title'].lower())
    elif sort_by == "Date Last Revised":
        sorted_books = sorted(filtered_books, key=lambda x: x['last_revised'], reverse=True)
    else:
        sorted_books = filtered_books  # Default sorting
    
    create_book_buttons(window, sorted_books)

def on_search(window, sorting, search_entry):
    query = search_entry.get()
    sort_books(window, books, sorting.get(), search_query=query)

def setup_book_hub(parent):
    # Sorting options
    sort_options = ["Name", "Date Last Revised"]
    sorting = ttk.Combobox(parent, values=sort_options, state="readonly")
    sorting.set("Sort By")
    sorting.bind("<<ComboboxSelected>>", lambda e: sort_books(parent, books, sorting.get()))
    sorting.pack()

    # Search bar
    search_entry = tk.Entry(parent)
    search_entry.pack()
    search_button = tk.Button(parent, text="Search", command=lambda: on_search(parent, sorting, search_entry))
    search_button.pack()

    # Initialize the interface with all books
    sort_books(parent, books, sorting.get())  # Call sort_books to display all books initially

# Example usage in your main script:
# book_hub_module.setup_book_hub(character_creator_frame)  # Add Book Hub to the character_creator_frame
