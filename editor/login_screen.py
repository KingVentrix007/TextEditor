import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
global username,password
def login():
    def authenticate():
        global username,password
        username = entry_username.get()
        password = entry_password.get()
        print(f"Username: {username}, Password: {password}")
        # 
        # Dummy authentication for demonstration
        root.destroy()
        

    root = ctk.CTkToplevel()
    root.title("Login Screen")
    root.geometry("300x200")

    frame = ctk.CTkFrame(root)
    frame.pack(pady=20, padx=60, fill="both", expand=True)

    label = ctk.CTkLabel(frame, text="Login", font=ctk.CTkFont(size=20, weight="bold"))
    label.pack(pady=12, padx=10)

    entry_username = ctk.CTkEntry(frame, placeholder_text="Username")
    entry_username.pack(pady=12, padx=10)

    entry_password = ctk.CTkEntry(frame, placeholder_text="Password", show="*")
    entry_password.pack(pady=12, padx=10)
    
    button = ctk.CTkButton(frame, text="Login", command=authenticate)
    button.pack(pady=12, padx=10)

    root.mainloop()
    return username, password

# Call the login function
# username_u, password_u = login()
# print(f"Username: {username_u}, Password: {password_u}")
