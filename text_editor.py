import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import customtkinter as ctk
import encryption as enc
import decryption as decr
import base64
import sha
import os
import make_key as mk
import filename
import login_screen as lg
import passowrd as ps

class TextEditorApp:
    def __init__(self):
        self.users_password = None
        self.user_name = None
        self.MAX_ENCRYPTION_CYCLES = 25
        self.root = None
        self.menu_bar = None
        self.text_input = None
        self.create_main_window()

    def create_main_window(self):
        self.root = ctk.CTk()
        self.root.geometry("600x400")  # Set the initial size of the window

        # Create a menu bar
        self.menu_bar = tk.Menu(self.root)

        # Create a 'File' menu
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="New", command=lambda: self.text_input.delete("1.0", tk.END))
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        self.menu_bar.add_cascade(label="File", menu=file_menu)

        # Create an 'Edit' menu
        edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        edit_menu.add_command(label="Undo", command=lambda: self.root.event_generate("<<Undo>>"))
        edit_menu.add_command(label="Redo", command=lambda: self.root.event_generate("<<Redo>>"))
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", command=lambda: self.root.event_generate("<<Cut>>"))
        edit_menu.add_command(label="Copy", command=lambda: self.root.event_generate("<<Copy>>"))
        edit_menu.add_command(label="Paste", command=lambda: self.root.event_generate("<<Paste>>"))
        self.menu_bar.add_cascade(label="Edit", menu=edit_menu)

        # Create a 'Help' menu
        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label="About", command=lambda: messagebox.showinfo("About", "This is a text editor with encryption capabilities."))
        self.menu_bar.add_cascade(label="Help", menu=help_menu)

        # Attach the menu bar to the root window
        self.root.config(menu=self.menu_bar)

        # Create a CTkTextbox for multiline input
        self.text_input = ctk.CTkTextbox(self.root)
        self.text_input.pack(fill=ctk.BOTH, expand=True)

        # Display the login screen
        self.login_screen()

        # Run the application
        self.root.mainloop()

    def save(self):
        global users_password
        global user_name
        # Get the text from the text input
        text_to_save = self.text_input.get("1.0", tk.END).strip()
        if not text_to_save:
            messagebox.showwarning("Warning", "Text box is empty. Nothing to save.")
            return

        # Use the global variable `users_password` as the user's password
        password = self.users_password
        if not password:
            messagebox.showwarning("Warning", "Password is required to save the file.")
            return

        # Generate a key from the user's password
        user_key = mk.generate_aes_key(self.user_name, self.users_password)

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
            self.text_input.delete("1.0", tk.END)

    def open_file(self):
        global users_password
        global user_name
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
            user_key = mk.generate_aes_key(self.user_name, self.users_password)
            
            # Decrypt the encryption key using the generated key
            decrypted_key_str = decr.decrypt_string(key, user_key)
            
            # Decode the decrypted key from Base64 to bytes
            decrypted_key = base64.b64decode(decrypted_key_str)
            
            # Decrypt the text
            decrypted_text = decr.decrypt_string(encrypted_text, decrypted_key)
            
            # Insert the decrypted text into the text input
            self.text_input.delete("1.0", tk.END)
            self.text_input.insert("1.0", decrypted_text)
            
            print("File opened successfully.")

    def login_screen(self):
        def load_credentials():
            if os.path.exists("shadow"):
                with open("shadow", "r") as shadow_file:
                    return shadow_file.read().strip().split(':')
            return None

        def save_credentials(username, hashed_password):
            with open("shadow", "w") as shadow_file:
                shadow_file.write(f"{username}:{hashed_password}")

        def validate_login():
            # Function to validate the username and password
            username = username_entry.get()
            password = password_entry.get()
            # print
            # print(f"Username: {username}, Password: {password}")

            if username == stored_username and sha.check_password(password, stored_hashed_password):
                print("Login successful")
                login_window.destroy()  # Close the login window
                self.root.deiconify()  # Show the main application window
                self.users_password = password
                self.user_name = username
            else:
                messagebox.showerror("Error", "Invalid username or password")

        def create_credentials():
            nonlocal stored_username
            nonlocal stored_hashed_password

            new_username = new_username_entry.get()
            new_password = new_password_entry.get()
            confirm_password = confirm_password_entry.get()
            
            if new_password != confirm_password:
                messagebox.showerror("Error", "Passwords do not match")
                return
            if(ps.test_password(new_password) == False):
                messagebox.showerror("Error", "Your password is too weak")
                return
            stored_hashed_password = sha.hash_password(new_password)
            save_credentials(new_username, stored_hashed_password)
            stored_username = new_username
            create_window.destroy()
            self.login_screen()

        # Load stored credentials
        credentials = load_credentials()
        if credentials:
            stored_username, stored_hashed_password = credentials
        else:
            create_window = ctk.CTkToplevel(self.root)
            create_window.title("Create Credentials")

            ctk.CTkLabel(create_window, text="Create Username:").pack()
            new_username_entry = ctk.CTkEntry(create_window)
            new_username_entry.pack()

            ctk.CTkLabel(create_window, text="Create Password:").pack()
            new_password_entry = ctk.CTkEntry(create_window, show="*")
            new_password_entry.pack()

            ctk.CTkLabel(create_window, text="Confirm Password:").pack()
            confirm_password_entry = ctk.CTkEntry(create_window, show="*")
            confirm_password_entry.pack()

            create_button = ctk.CTkButton(create_window, text="Create", command=create_credentials)
            create_button.pack()

            # Center the create window on the screen
            create_window.geometry("+{}+{}".format(
                int(create_window.winfo_screenwidth() / 2 - create_window.winfo_reqwidth() / 2),
                int(create_window.winfo_screenheight() / 2 - create_window.winfo_reqheight() / 2)))

            self.root.withdraw()
            return

        # Create a new window for the login screen
        login_window = ctk.CTkToplevel(self.root)
        login_window.title("Login")

        # Create and place labels and entry widgets for username and password
        ctk.CTkLabel(login_window, text="Username:").pack()
        username_entry = ctk.CTkEntry(login_window)
        username_entry.pack()

        ctk.CTkLabel(login_window, text="Password:").pack()
        password_entry = ctk.CTkEntry(login_window, show="*")
        password_entry.pack()

        # Create and place a login button
        login_button = ctk.CTkButton(login_window, text="Login", command=validate_login)
        login_button.pack()

        # Center the login window on the screen
        login_window.geometry("+{}+{}".format(
            int(login_window.winfo_screenwidth() / 2 - login_window.winfo_reqwidth() / 2),
            int(login_window.winfo_screenheight() / 2 - login_window.winfo_reqheight() / 2)))

        # Hide the main application window until login is successful
        self.root.withdraw()



if __name__ == "__main__":
    TextEditorApp()
