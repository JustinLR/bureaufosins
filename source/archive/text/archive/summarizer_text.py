import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, Menu
import time
from tkinter import re
import requests
from typing import List
import openai

class ProgressBar:
    def __init__(self, total: int, parent):
        self.total = total
        self.progress = 0
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(parent, variable=self.progress_var, maximum=total)
        self.progress_bar.pack()

    def update(self):
        self.progress += 1
        self.progress_var.set(self.progress)
        print(f"Progress: {(self.progress / self.total) * 100:.2f}%")
        time.sleep(0.1)  # Simulate work being done

def split_text_into_chunks(text: str, sentences_per_chunk: int = 5) -> List[str]:
    # Split the text into sentences
    sentences = re.split(r'(?<=[.!?]) +', text)
    chunks = [' '.join(sentences[i:i+sentences_per_chunk]) for i in range(0, len(sentences), sentences_per_chunk)]
    return chunks

def generate_summary(api_key, text):
    # API endpoint URL
    url = "https://api.openai.com/v1/completions"

    # Headers with Authorization including the API key
    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    # Data payload for the API request, tailored to the API you're using
    data = {
        "model": "davinci-002",  # Adjust model as needed
        "prompt": text,
        "max_tokens": 50,  # Example parameter, adjust as needed
    }

    # Making the POST request to the API
    response = requests.post(url, headers=headers, json=data)

    # Error handling for response status
    if response.status_code == 200:
        # Process successful response
        response_data = response.json()
        summary = response_data.get("choices")[0].get("text").strip()
        return summary
    else:
        # Handle errors or unsuccessful response
        print(f"Error: Received status code {response.status_code}")
        return None

def summarize_text(text, api_key, parent):
    # Split the text into chunks for more accurate summaries
    chunks = split_text_into_chunks(text)

    # Initialize the progress bar
    progress_bar = ProgressBar(len(chunks), parent)

    # Generate summaries for each chunk
    summaries = [generate_summary(api_key, chunk) for chunk in chunks]
    for summary in summaries:  # Assuming you want to update progress per summary
        progress_bar.update()

    # Combine the summaries into a single text
    final_summary = "\n".join(filter(None, summaries))

    return final_summary

def setup_summarizer(parent, api_key):
    tk.Label(parent, text="Text to Summarize:").pack()
    text_input = scrolledtext.ScrolledText(parent, height=10)
    text_input.pack()
    tk.Label(parent, text="Summary:").pack()
    summary_output = scrolledtext.ScrolledText(parent, height=5)
    summary_output.pack()
    summary_output.configure(state='disabled')  # Prevent user from editing the summary

    def summarize():
        text = text_input.get("1.0", tk.END)
        # Now passing api_key to the summarize_text function
        summary = summarize_text(text, api_key, parent)  # Adjust summarize_text to accept api_key
        summary_output.configure(state='normal')
        summary_output.delete("1.0", tk.END)
        summary_output.insert("1.0", summary)
        summary_output.configure(state='disabled')

    summarize_button = tk.Button(parent, text="Summarize", command=summarize)
    summarize_button.pack()