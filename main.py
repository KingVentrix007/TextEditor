import tkinter as tk
from tkinter import filedialog, messagebox,simpledialog
import customtkinter as ctk
import encryption as enc
import decryption as decr
import base64
import sha
import os
import make_key as mk
import filename
users_password = None
user_name = None
MAX_ENCRYPTION_CYCLES = 25
def get_file_name_without_extension(file_path):
    file_name = os.path.basename(file_path)
    base_name, _ = os.path.splitext(file_name)
    return base_name
def save():
    global users_password
    global user_name
    # Get the text from the text input
    text_to_save = text_input.get("1.0", tk.END).strip()
    if not text_to_save:
        messagebox.showwarning("Warning", "Text box is empty. Nothing to save.")
        return

    # Use the global variable `users_password` as the user's password
    password = users_password
    if not password:
        messagebox.showwarning("Warning", "Password is required to save the file.")
        return

    # Generate a key from the user's password
    user_key = mk.generate_aes_key(user_name, users_password)

    # Generate a key for encrypting the data
    encryption_key = enc.generate_key()

    # Encrypt the text
    encrypted_text = enc.encrypt_string(text_to_save, encryption_key)
    # Cyclic encryption method

    # Encode the encryption key as Base64 to ensure it is a string
    encryption_key_str = base64.b64encode(encryption_key).decode('utf-8')

    # Encrypt the encryption key using the user's password
    encrypted_encryption_key = enc.encrypt_string(encryption_key_str, user_key)

    # Encode the encrypted text as Base64 to ensure it is a string
    encrypted_text_b64 = base64.b64encode(encrypted_text).decode('utf-8')
    encrypted_encryption_key_b64 = base64.b64encode(encrypted_encryption_key).decode('utf-8')

    # Save the encrypted text to a file
    file_path = filedialog.asksaveasfilename(defaultextension=".enc", filetypes=[("Encrypted File", "*.enc")])
    if file_path:
        with open(file_path, 'w') as file:
            file.write(encrypted_text_b64)

        # Save the encrypted encryption key to a separate file
        key_file_path = file_path + ".key"
        with open(key_file_path, 'w') as key_file:
            key_file.write(encrypted_encryption_key_b64)

        print("File saved successfully.")

def open_file():
    # Open the file dialog to select the encrypted file
    file_path = filedialog.askopenfilename(filetypes=[("Encrypted File", "*.enc")])
    if file_path:
        with open(file_path, 'r') as file:
            encrypted_text_b64 = file.read()
        
        # Decode the Base64 encoded string back to bytes
        encrypted_text = base64.b64decode(encrypted_text_b64)
        
        # Open the corresponding key file
        key_file_path = file_path + ".key"
        with open(key_file_path, 'r') as key_file:
            key_b64 = key_file.read()
        
        # Decode the Base64 encoded key back to bytes
        key = base64.b64decode(key_b64)
        
        # Generate the key to decrypt the encryption key using user_name and users_password
        user_key = mk.generate_aes_key(user_name, users_password)
        
        # Decrypt the encryption key using the generated key
        decrypted_key_str = decr.decrypt_string(key, user_key)
        
        # Decode the decrypted key from Base64 to bytes
        decrypted_key = base64.b64decode(decrypted_key_str)
        
        # Decrypt the text
        decrypted_text = decr.decrypt_string(encrypted_text, decrypted_key)
        
        # Insert the decrypted text into the text input
        text_input.delete("1.0", tk.END)
        text_input.insert("1.0", decrypted_text)
        
        print("File opened successfully.")


def login_screen():
    global users_password
    global user_name
    def load_password():
        if os.path.exists("shadow"):
            with open("shadow", "r") as shadow_file:
                return shadow_file.read().strip()
        return None

    def save_password(hashed_password):
        with open("shadow", "w") as shadow_file:
            shadow_file.write(hashed_password)

    def validate_login():
        global users_password
        global user_name
        # Function to validate the username and password
        username = username_entry.get()
        password = password_entry.get()

        # For simplicity, let's say valid username is "user" and password is "password"
        if username == "user" and sha.check_password(password, hashed_password):
            login_window.destroy()  # Close the login window
            root.deiconify()  # Show the main application window
            users_password = password
            user_name = username
        else:
            messagebox.showerror("Error", "Invalid username or password")

    # Create a new window for the login screen
    login_window = tk.Toplevel(root)
    login_window.title("Login")

    # Create and place labels and entry widgets for username and password
    tk.Label(login_window, text="Username:").pack()
    username_entry = tk.Entry(login_window)
    username_entry.pack()

    tk.Label(login_window, text="Password:").pack()
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack()

    # Create and place a login button
    login_button = tk.Button(login_window, text="Login", command=validate_login)
    login_button.pack()

    # Center the login window on the screen
    login_window.geometry("+{}+{}".format(
        int(login_window.winfo_screenwidth() / 2 - login_window.winfo_reqwidth() / 2),
        int(login_window.winfo_screenheight() / 2 - login_window.winfo_reqheight() / 2)))

    # Hide the main application window until login is successful
    root.withdraw()

    # Load hashed password from file
    hashed_password = load_password()

    # If no hashed password exists, prompt for a new one
    if not hashed_password:
        new_password = simpledialog.askstring("Create Password", "No password found. Please enter a new password:")
        hashed_password = sha.hash_password(new_password)
        save_password(hashed_password)

# Create the main application window
root = ctk.CTk()
root.geometry("600x400")  # Set the initial size of the window

# Create a menu bar
menu_bar = tk.Menu(root)

# Create a 'File' menu
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="New", command=lambda: text_input.delete("1.0", tk.END))
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)
menu_bar.add_cascade(label="File", menu=file_menu)

# Create an 'Edit' menu
edit_menu = tk.Menu(menu_bar, tearoff=0)
edit_menu.add_command(label="Undo", command=lambda: root.event_generate("<<Undo>>"))
edit_menu.add_command(label="Redo", command=lambda: root.event_generate("<<Redo>>"))
edit_menu.add_separator()
edit_menu.add_command(label="Cut", command=lambda: root.event_generate("<<Cut>>"))
edit_menu.add_command(label="Copy", command=lambda: root.event_generate("<<Copy>>"))
edit_menu.add_command(label="Paste", command=lambda: root.event_generate("<<Paste>>"))
menu_bar.add_cascade(label="Edit", menu=edit_menu)

# Create a 'Help' menu
help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="About", command=lambda: messagebox.showinfo("About", "This is a text editor with encryption capabilities."))
menu_bar.add_cascade(label="Help", menu=help_menu)

# Attach the menu bar to the root window
root.config(menu=menu_bar)

# Create a CTkTextbox for multiline input
text_input = ctk.CTkTextbox(root)
text_input.pack(fill=ctk.BOTH, expand=True)

# Display the login screen
login_screen()

# Run the application
root.mainloop()
