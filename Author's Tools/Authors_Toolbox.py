import tkinter as tk
from tkinter import ttk
from tkinter import Menu
from character_creator_module import setup_character_creator  # Import the Character Creator module function

def show_tab(tab_frame):
    # Hide all tab frames
    character_creator_frame.pack_forget()
    book_hub_frame.pack_forget()
    
    # Show the selected tab frame
    tab_frame.pack(fill=tk.BOTH, expand=True)

# Define functions to display module contents
def character_creator_content():
    for widget in character_creator_frame.winfo_children():
        widget.destroy()

    character_creator_canvas = tk.Canvas(character_creator_frame, height=200)
    character_creator_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    character_creator_scrollbar = ttk.Scrollbar(character_creator_frame, orient="vertical", command=character_creator_canvas.yview)
    character_creator_scrollbar.pack(side=tk.RIGHT, fill="y")

    character_creator_canvas.configure(yscrollcommand=character_creator_scrollbar.set)
    character_creator_canvas_frame = tk.Frame(character_creator_canvas)
    character_creator_canvas.create_window((0, 0), window=character_creator_canvas_frame, anchor="nw")

    def configure_canvas(event):
        character_creator_canvas.configure(scrollregion=character_creator_canvas.bbox("all"))
    
    character_creator_canvas.bind("<Configure>", configure_canvas)

    content = tk.Label(character_creator_canvas_frame, text="Character Creator Module Content")
    content.pack()

    setup_character_creator(character_creator_canvas_frame)

def book_hub_content():
    content = tk.Label(book_hub_frame, text="Book Hub Module Content")
    content.pack()

def close_application():
    root.destroy()

def about():
    about_window = tk.Toplevel(root)
    about_window.title("About")
    about_label = tk.Label(about_window, text="Author's Toolbox - Version 1.0\n© 2024 Your Name")
    about_label.pack(padx=20, pady=20)

# Create the main application window
root = tk.Tk()
root.title("Main Program Launcher")

# Create a Menu Bar
menu_bar = Menu(root)
root.config(menu=menu_bar)

# Create File Menu
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Close", command=close_application)
menu_bar.add_cascade(label="File", menu=file_menu)

# Create Help Menu
help_menu = Menu(menu_bar, tearoff=0)
help_menu.add_command(label="About", command=about)
menu_bar.add_cascade(label="Help", menu=help_menu)

# Create a Frame to hold the Notebook with tabs on the left
frame = ttk.Frame(root)
frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Create custom tab buttons on the left side
character_creator_button = tk.Button(frame, text="Character Creator", command=lambda: show_tab(character_creator_frame))
book_hub_button = tk.Button(frame, text="Book Hub", command=lambda: show_tab(book_hub_frame))
character_creator_button.pack(fill=tk.X)
book_hub_button.pack(fill=tk.X)

# Create a Notebook widget to hold the tabs with tabs on top
notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH, expand=True)

# Create frames for the content of each tab
character_creator_frame = tk.Frame(root)
book_hub_frame = tk.Frame(root)

# Add the frames to the Notebook
notebook.add(character_creator_frame, text="Character Creator")
notebook.add(book_hub_frame, text="Book Hub")

# Create a Canvas widget with a scrollbar for each tab
character_creator_canvas_frame = tk.Frame(character_creator_frame)
character_creator_canvas_frame.pack(fill=tk.BOTH, expand=True)

character_creator_canvas = tk.Canvas(character_creator_canvas_frame, height=200)
character_creator_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

character_creator_scrollbar = ttk.Scrollbar(character_creator_canvas_frame, orient="vertical", command=character_creator_canvas.yview)
character_creator_scrollbar.pack(side=tk.RIGHT, fill="y")

character_creator_canvas.configure(yscrollcommand=character_creator_scrollbar.set)
character_creator_canvas.create_window((0, 0), window=character_creator_canvas_frame, anchor="nw")

# Add content to the canvas_frame here (Character Creator tab)
character_creator_content()

# Configure the canvas to scroll
character_creator_canvas.bind("<Configure>", lambda event, canvas=character_creator_canvas: canvas.configure(scrollregion=canvas.bbox("all")))

# Create a Canvas widget for the Book Hub tab (similar to Character Creator tab)
book_hub_canvas = tk.Canvas(book_hub_frame, height=200)
book_hub_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

book_hub_scrollbar = ttk.Scrollbar(book_hub_frame, orient="vertical", command=book_hub_canvas.yview)
book_hub_scrollbar.pack(side=tk.RIGHT, fill="y")

book_hub_canvas.configure(yscrollcommand=book_hub_scrollbar.set)
book_hub_canvas_frame = tk.Frame(book_hub_canvas)
book_hub_canvas.create_window((0, 0), window=book_hub_canvas_frame, anchor="nw")

# Add content to the canvas_frame here (Book Hub tab)
book_hub_content()

# Configure the canvas to scroll
book_hub_canvas.bind("<Configure>", lambda event, canvas=book_hub_canvas: canvas.configure(scrollregion=canvas.bbox("all")))

# Function to show the selected tab's content
def show_tab(tab_frame):
    # Hide all tab frames
    character_creator_frame.pack_forget()
    book_hub_frame.pack_forget()
    
    # Show the selected tab frame
    tab_frame.pack(fill=tk.BOTH, expand=True)

# Initially show the Character Creator tab
show_tab(character_creator_frame)

# Start the main application loop
root.mainloop()
