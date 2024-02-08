import tkinter as tk
from tkinter import (
    ttk,
    scrolledtext,
    messagebox,
    filedialog,
    colorchooser,
    Checkbutton,
    IntVar,
)
from fpdf import FPDF
import datetime

entries = {}  # Define entries dictionary
distinguishing_features = {}  # Define distinguishing_features dictionary
date_entries = {}  # Define date_entries dictionary
color_values = {}  # Define color_values dictionary
color_labels = {}  # Define color_labels dictionary


def update_widget_colors(widget, bg_color, fg_color):
    try:
        widget.configure(bg=bg_color, fg=fg_color)
    except tk.TclError:
        pass  # Ignore widgets that do not support bg or fg

    if widget.winfo_children():
        for child in widget.winfo_children():
            update_widget_colors(child, bg_color, fg_color)


def get_character_details():
    character = {}
    for label, widget in entries.items():
        if label == "Distinguishing Features":
            features = [
                feature for feature, var in distinguishing_features.items() if var.get()
            ]
            character[label] = ", ".join(features)
        elif label == "Age & Birthdate":
            year, month, day = date_entries[label]
            character[label] = f"{year.get()}-{month.get()}-{day.get()}"
        elif isinstance(widget, ttk.Combobox):
            character[label] = widget.get()
        elif label in color_values:
            character[label] = color_values[label]
        elif isinstance(widget, scrolledtext.ScrolledText):
            character[label] = widget.get("1.0", "end-1c").strip()
        elif isinstance(widget, tk.Entry):
            character[label] = widget.get()  # Corrected line for Entry widgets
    return character


def export_to_pdf(character_profile):
    try:
        character_name = character_profile.get("Name", "Unnamed_Character").replace(
            " ", "_"
        )
        filename = filedialog.asksaveasfilename(
            initialdir="/",
            title="Select file",
            initialfile=f"{character_name}_profile.pdf",
            filetypes=(("PDF files", "*.pdf"), ("all files", "*.*")),
        )
        if filename:
            if not filename.endswith(".pdf"):
                filename += ".pdf"

            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            for key, value in character_profile.items():
                pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)

            pdf.output(filename)
            messagebox.showinfo(
                "Export Complete", f"Character profile saved to {filename}"
            )
        else:
            messagebox.showwarning(
                "Export Cancelled", "Export operation was cancelled."
            )
    except Exception as e:
        messagebox.showerror("Export Error", f"An error occurred: {e}")


def choose_color(label):  # Remove 'parent' argument
    color_code = colorchooser.askcolor(title="Choose color")[1]
    if color_code:
        color_labels[label].config(bg=color_code)
        color_values[label] = color_code


def on_submit():
    character_profile = get_character_details()
    export_to_pdf(character_profile)


def setup_character_creator(parent_frame):
    label = tk.Label(parent_frame, text="Character Creator")
    label.pack()

    # Create a frame within the parent_frame
    frame = tk.Frame(parent_frame)
    frame.pack(fill=tk.BOTH, expand=True)

    # Create a canvas within the frame
    canvas = tk.Canvas(frame)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Create a scrollbar within the frame
    scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Configure the canvas
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind(
        "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    # Create an inner frame inside the canvas
    inner_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=inner_frame, anchor="nw")

    labels = {
        "Name": "text",
        "Full Name": "text",
        "Nicknames/Aliases": "text",
        "Age & Birthdate": "date",
        "Zodiac Sign": "dropdown",
        "Place of Birth": "text",
        "Current Residence": "text",
        "Height (in inches)": "text",
        "Weight (in pounds)": "text",
        "Build": "dropdown",
        "Eye Color": "color",
        "Hair Color": "color",
        "Distinguishing Features": "checkbox",
        "Style of Dress": "dropdown",
        "Significant Physical Traits": "text",
        "Key Traits": "text",
        "Fears and Phobias": "text",
        "Hobbies and Interests": "text",
        "Habits or Behaviors": "text",
        "Strengths and Weaknesses": "text",
        "Mythological Influences on Personality": "text",
        "Moral Alignment": "text",
        "Communication Style": "text",
        "Family": "text",
        "Education and Training": "text",
        "Key Past Events": "text",
        "Social Status and Wealth": "dropdown",
        "Cultural Background & Mythological Lineage": "text",
        "Powers Specific to Greek Mythology": "text",
        "Limitations and Costs": "text",
        "Initial State": "text",
        "Evolution Throughout the Series": "text",
        "Goals and Motivations": "text",
        "Conflicts": "text",
        "Resolution": "text",
        "Ties to Mythological Themes": "text",
        "Destiny vs. Free Will": "text",
        "Key Relationships": "text",
        "Nature of Relationships": "text",
        "Changes Over Time": "text",
        "Mythological Alliances and Rivalries": "text",
        "Mentor Figures": "text",
        "Important Dialogue Quotations": "text",
        "Significant Moments or Scenes": "text",
        "Personal Belongings of Mythological Note": "text",
        "Prophecies or Oracles": "text",
        "Symbolism": "text",
        "Future Plot Ideas": "text"
        # Add other fields as needed
    }

    dropdown_options = {
        "Zodiac Sign": [
            "Aries",
            "Taurus",
            "Gemini",
            "Cancer",
            "Leo",
            "Virgo",
            "Libra",
            "Scorpio",
            "Sagittarius",
            "Capricorn",
            "Aquarius",
            "Pisces",
        ],
        "Build": ["Slender", "Muscular", "Average", "Heavyset", "Athletic"],
        "Style of Dress": ["Formal", "Casual", "Traditional", "Modern", "Athletic"],
        "Social Status and Wealth": [
            "Wealthy",
            "Middle class",
            "Poor",
            "Noble",
            "Royalty",
        ],
    }

    # For Distinguishing Features
    distinguishing_features_list = ["Scar", "Tattoo", "Freckles", "Birthmark"]
    distinguishing_features = {
        feature: IntVar() for feature in distinguishing_features_list
    }

    entries = {}
    color_labels = {}
    color_values = {}
    date_entries = {}  # Add this line to define date_entries

    for label, field_type in labels.items():
        tk.Label(inner_frame, text=label).pack()
        if field_type == "text":
            entry = tk.Entry(inner_frame, width=50)  # Adjust the width as needed
            entry.pack(anchor=tk.CENTER)
            entries[label] = entry
        elif field_type == "dropdown":
            combobox = ttk.Combobox(
                inner_frame, values=dropdown_options.get(label, []), width=47
            )  # Adjust the width
            combobox.pack(anchor=tk.CENTER)
            entries[label] = combobox
        elif field_type == "color":
            color_button = tk.Button(
                inner_frame,
                text=f"Choose {label}",
                command=lambda lbl=label: choose_color(lbl),
            )
            color_button.pack()
            color_label = tk.Label(inner_frame, text="     ", bg="white", width=20)
            color_label.pack()
            color_labels[label] = color_label
        elif field_type == "checkbox":
            for feature, var in distinguishing_features.items():
                cb = Checkbutton(inner_frame, text=feature, variable=var)
                cb.pack()
            entries[label] = distinguishing_features
        elif field_type == "date":
            year = ttk.Combobox(
                inner_frame, values=list(range(1900, datetime.datetime.now().year + 1))
            )
            month = ttk.Combobox(inner_frame, values=list(range(1, 13)))
            day = ttk.Combobox(inner_frame, values=list(range(1, 32)))
            year.pack()
            month.pack()
            day.pack()
            date_entries[label] = (year, month, day)

    # Create a "Submit" button to export character profile to PDF
    submit_button = tk.Button(parent_frame, text="Submit", command=on_submit)
    submit_button.pack()
