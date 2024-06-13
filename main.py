import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import text_editor
import customtkinter as ctk

# Create the main window
root = ctk.CTk()

# Function to open the text editor
def open_text_editor():
    text_editor.TextEditorApp()
# Create a button to open the text editor
open_editor_button = ctk.CTkButton(root, text="Open Text Editor", command=open_text_editor)
open_editor_button.pack()

root.mainloop()
