import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from tkinter import PhotoImage
from tkinter import Menu, Toplevel
import configparser
import webbrowser
from character_creator_module import setup_character_creator
from book_hub_module import setup_book_hub
from summarizer_module import setup_summarizer
import configparser
import os
import openai
from cryptography.fernet import Fernet

def load_encryption_key():
    # Example: Load the encryption key from an environment variable
    key = os.environ.get("ENCRYPTION_KEY")
    if not key:
        raise ValueError("Encryption key not found.")
    return key.encode()  # Ensure the key is in bytes format

# Then, before you use `encryption_key` in `encrypt_message` or `decrypt_message`, load it:
encryption_key = load_encryption_key()

# Encrypt a message
def encrypt_message(message, key):
    f = Fernet(key)
    encrypted_message = f.encrypt(message.encode())
    return encrypted_message

# Decrypt a message
def decrypt_message(encrypted_message, key):
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message).decode()
    return decrypted_message

# Function to save API key to config.ini
def save_api_key(api_key):
    encrypted_key = encrypt_message(api_key, encryption_key)
    config = configparser.ConfigParser()
    config['DEFAULT'] = {'ChatGPT_API_Key': encrypted_key}  # Use encrypted_key instead of api_key
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    messagebox.showinfo("API Key", "API Key saved successfully!")

def read_config():
    config = configparser.ConfigParser()
    config.read(r"C:\Users\justi\Dropbox\Scrivener\Macros\Instruction Sets\Author's Toolbox\config.ini")
    return config['DEFAULT'].get('ChatGPT_API_Key', None)

# Obtain the API key from config
api_key = read_config()

# Function to show the selected tab's content
def show_tab(tab_frame, content_func=None):
    # Hide all tab frames
    for frame in (
        homepage_frame,
        character_creator_frame,
        book_hub_frame,
        summarizer_frame,
    ):
        frame.pack_forget()

    # Show the selected tab frame
    tab_frame.pack(fill=tk.BOTH, expand=True)

    # Call the function to configure the tab's content if provided
    if content_func:
        content_func(tab_frame)

# Modify the summarizer_content function to pass api_key
def summarizer_content(tab_frame):
    for widget in tab_frame.winfo_children():
        widget.destroy()
    setup_summarizer(tab_frame, api_key)  # Pass the api_key here

def character_creator_content(tab_frame):
    # Clear the frame before setting it up again
    for widget in tab_frame.winfo_children():
        widget.destroy()

    # Call the setup_character_creator function to set up the frame again
    setup_character_creator(tab_frame)

def book_hub_content(tab_frame):
    # Clear the book_hub_canvas_frame
    for widget in book_hub_canvas_frame.winfo_children():
        widget.destroy()

    # Call the setup_book_hub function for the book_hub_canvas_frame
    setup_book_hub(book_hub_canvas_frame)

def homepage_content(tab_frame):
    # Clear the homepage_frame
    for widget in tab_frame.winfo_children():
        widget.destroy()

    # Load the background image
    background_image = PhotoImage(
        file=r"C:\Users\justi\Dropbox\Scrivener\Macros\Instruction Sets\Author's Toolbox\Images\Homepage.png"
    )  # Update path as needed

    # Create a label to hold the background image
    background_label = tk.Label(tab_frame, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Keep a reference to the image to prevent garbage collection
    background_label.image = background_image

    # Create other content on top of the background
    homepage_label = tk.Label(
        tab_frame, text="Welcome to the Author's Toolbox!", bg="white"
    )
    homepage_label.pack(pady=20)  # Adjust positioning as needed

def close_application():
    root.destroy()

def open_website(event):
    webbrowser.open("http://www.bureauofsins.com")

def about():
    # Create a new window for the About information
    about_window = tk.Toplevel(root)
    about_window.title("About")
    about_label = tk.Label(
        about_window, text="Author's Toolbox - Version 1.0\n© 2024 J. L. Richards"
    )
    about_label.pack(padx=20, pady=10)

    # Add your website address as a clickable hyperlink
    website_label = tk.Label(
        about_window, text="Website: www.bureauofsins.com", cursor="hand2"
    )
    website_label.pack(padx=20, pady=10)
    website_label.bind("<Button-1>", open_website)

# Create the main application window
root = tk.Tk()
root.title("Author's Toolbox")
root.geometry("800x600+300+120")

# Create a Menu Bar
menu_bar = Menu(root)
root.config(menu=menu_bar)

# Create File Menu
file_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)

def open_settings_window():
    settings_window = Toplevel(root)
    settings_window.title("Settings")
    settings_window.geometry("600x400")

    tabs_frame = tk.Frame(settings_window)
    tabs_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

    content_frame = tk.Frame(settings_window)
    content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    tabs = ["General", "Appearance", "Network", "API Key"]
    frames = {tab: tk.Frame(content_frame) for tab in tabs}

    def show_tab(tab):
        for frame in frames.values():
            frame.pack_forget()
        frames[tab].pack(fill=tk.BOTH, expand=True)

    for tab in tabs:
        tab_button = tk.Button(tabs_frame, text=tab, command=lambda t=tab: show_tab(t))
        tab_button.pack(fill=tk.X)

        if tab == "API Key":
            tk.Label(frames[tab], text="Enter your API Key:").pack(pady=(20, 5))
            api_key_entry = tk.Entry(frames[tab])
            api_key_entry.pack(pady=(0, 20))

            def on_save_api_key():
                api_key = api_key_entry.get()
                save_api_key(api_key)  # Call the function to save the API key

            save_button = tk.Button(frames[tab], text="Save", command=on_save_api_key)
            save_button.pack()

    show_tab(tabs[0])

menu_bar = tk.Menu(root)
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Settings", command=open_settings_window)
menu_bar.add_cascade(label="File", menu=file_menu)
root.config(menu=menu_bar)

# Create other menu items under File
file_menu.add_command(label="Close", command=root.destroy)  # Example for closing the app

# Create Help Menu
help_menu = Menu(menu_bar, tearoff=0)
help_menu.add_command(label="About", command=about)
menu_bar.add_cascade(label="Help", menu=help_menu)

# Create a Frame to hold the Notebook with tabs on the left
frame = ttk.Frame(root)
frame.pack(side=tk.LEFT, fill=tk.Y, expand=False)

# Create custom tab buttons on the left side
# Creating buttons with a specified width
homepage_button = tk.Button(
    frame,
    text="Homepage",
    width=20,
    height=5,
    command=lambda: show_tab(homepage_frame, homepage_content),
)
character_creator_button = tk.Button(
    frame,
    text="Character Creator",
    width=20,
    height=5,
    command=lambda: show_tab(character_creator_frame, character_creator_content),
)
book_hub_button = tk.Button(
    frame,
    text="Book Hub",
    width=20,
    height=5,
    command=lambda: show_tab(book_hub_frame, book_hub_content),
)
summarizer_button = tk.Button(
    frame,
    text="Summarizer",
    width=20,
    height=5,
    command=lambda: show_tab(summarizer_frame, summarizer_content),
)

homepage_button.pack(anchor="nw")
character_creator_button.pack(anchor="nw")
book_hub_button.pack(anchor="nw")
summarizer_button.pack(anchor="nw")

# Create frames for the content of each tab
homepage_frame = tk.Frame(root)
character_creator_frame = tk.Frame(root)
book_hub_frame = tk.Frame(root)
summarizer_frame = tk.Frame(root)

# Create a Canvas widget with a scrollbar for each tab
homepage_canvas_frame = tk.Frame(homepage_frame)
homepage_canvas_frame.pack(fill=tk.BOTH, expand=True)

homepage_canvas = tk.Canvas(homepage_canvas_frame, height=200)
homepage_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

homepage_scrollbar = ttk.Scrollbar(
    homepage_canvas_frame, orient="vertical", command=homepage_canvas.yview
)
homepage_scrollbar.pack(side=tk.RIGHT, fill="y")

homepage_canvas.configure(yscrollcommand=homepage_scrollbar.set)

# Configure the canvas to scroll
homepage_canvas.bind(
    "<Configure>",
    lambda event, canvas=homepage_canvas: canvas.configure(
        scrollregion=canvas.bbox("all")
    ),
)

# Create a new frame to be the content of the canvas
homepage_canvas_inner_frame = tk.Frame(homepage_canvas)
homepage_canvas.create_window((0, 0), window=homepage_canvas_inner_frame, anchor="nw")

# Create a Canvas widget for the Character Creator tab (similar to Homepage tab)
character_creator_canvas = tk.Canvas(character_creator_frame, height=200)
character_creator_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

character_creator_scrollbar = ttk.Scrollbar(
    character_creator_frame, orient="vertical", command=character_creator_canvas.yview
)
character_creator_scrollbar.pack(side=tk.RIGHT, fill="y")
character_creator_canvas.configure(yscrollcommand=character_creator_scrollbar.set)
character_creator_canvas_frame = tk.Frame(character_creator_canvas)
character_creator_canvas.create_window(
    (0, 0), window=character_creator_canvas_frame, anchor="nw"
)

# Create a Canvas widget for the Book Hub tab (similar to Character Creator tab)
book_hub_canvas = tk.Canvas(book_hub_frame, height=200)
book_hub_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

book_hub_scrollbar = ttk.Scrollbar(
    book_hub_frame, orient="vertical", command=book_hub_canvas.yview
)
book_hub_scrollbar.pack(side=tk.RIGHT, fill="y")
book_hub_canvas.configure(yscrollcommand=book_hub_scrollbar.set)
book_hub_canvas_frame = tk.Frame(book_hub_canvas)
book_hub_canvas.create_window((0, 0), window=book_hub_canvas_frame, anchor="nw")

# Configure the canvas to scroll
book_hub_canvas.bind(
    "<Configure>",
    lambda event, canvas=book_hub_canvas: canvas.configure(
        scrollregion=canvas.bbox("all")
    ),
)

# Show the homepage frame first
show_tab(homepage_frame, homepage_content)

# Start the main application loop
root.mainloop()
