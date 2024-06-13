import tkinter as tk
from tkinter import ttk
from datetime import datetime
import socket
import pytz

class NotesSystem:
    def __init__(self, master, person_name):
        self.master = master
        self.person_name = person_name
        
        self.master.title("Military Notes System")
        
        self.notes = []
        
        self.create_widgets()
        
    def create_widgets(self):
        self.notes_dropdown = ttk.Combobox(self.master, values=self.notes, width=30)
        self.notes_dropdown.grid(row=0, column=0, padx=10, pady=10)
        
        self.add_new_button = ttk.Button(self.master, text="Add New", command=self.add_new_note)
        self.add_new_button.grid(row=0, column=1, padx=10, pady=10)
        
        self.note_text = tk.Text(self.master, width=50, height=10)
        self.note_text.grid(row=1, columnspan=2, padx=10, pady=10)
        
    def add_new_note(self):
        current_time = datetime.now(pytz.timezone('UTC')).astimezone(pytz.timezone('US/Eastern')).strftime("%Y-%m-%d %H:%M:%S %Z")
        device_name = socket.gethostname()
        note_data = f"Date: {current_time}\nTime: {current_time.split()[1]}\nDevice: {device_name}\nPerson: {self.person_name}\n\n"
        self.note_text.insert(tk.END, note_data)

def main():
    person_name = "Agent X"
    root = tk.Tk()
    notes_system = NotesSystem(root, person_name)
    root.mainloop()

if __name__ == "__main__":
    main()
