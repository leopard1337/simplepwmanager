import tkinter as tk
from tkinter import simpledialog, messagebox
from cryptography.fernet import Fernet, InvalidToken
import os

class SecurePasswordManager:
    def __init__(self, master_password, data_file):
        self.master_password = master_password
        self.data_file = data_file
        self.cipher_suite = self._create_cipher_suite()

    def _create_cipher_suite(self):
        key = Fernet.generate_key()
        return Fernet(key)

    def _load_data(self):
        try:
            with open(self.data_file, 'rb') as file:
                encrypted_data = file.read()
                decrypted_data = self.cipher_suite.decrypt(encrypted_data)
                return eval(decrypted_data)
        except (InvalidToken, FileNotFoundError, SyntaxError):
            return {}

    def _save_data(self, data):
        encrypted_data = self.cipher_suite.encrypt(str(data).encode())
        with open(self.data_file, 'wb') as file:
            file.write(encrypted_data)

    def add_password(self, account, password, website):
        data = self._load_data()
        if website not in data:
            data[website] = []
        data[website].append({"account": account, "password": password})
        self._save_data(data)

    def get_password(self, website, account):
        data = self._load_data()
        if website in data:
            for entry in data[website]:
                if entry["account"] == account:
                    return entry["password"]
        return "Account not found"

    def list_accounts(self):
        data = self._load_data()
        return data

class PasswordManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("𝓟𝓪𝓼𝓼𝔀𝓸𝓻𝓭 𝓜𝓪𝓷𝓪𝓰𝓮𝓻")
        self.root.configure(bg='black')  # Set background color to black
        
        self.master_password = get_master_password()
        self.password_manager = SecurePasswordManager(self.master_password, "password_data.bin")
        
        self.create_ui()

    def create_ui(self):
        title_label = tk.Label(self.root, text="𝓟𝓪𝓼𝓼𝔀𝓸𝓻𝓭 𝓜𝓪𝓷𝓪𝓰𝓮𝓻", font=('Arial', 16, 'bold'), fg='red', bg='black')
        title_label.pack(pady=10)
        
        self.website_label = tk.Label(self.root, text="Website:", fg='white', bg='black')
        self.website_label.pack()

        self.website_entry = tk.Entry(self.root)
        self.website_entry.pack()

        self.account_label = tk.Label(self.root, text="Account:", fg='white', bg='black')
        self.account_label.pack()
        
        self.account_entry = tk.Entry(self.root)
        self.account_entry.pack()

        self.password_label = tk.Label(self.root, text="Password:", fg='white', bg='black')
        self.password_label.pack()
        
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack()

        self.add_button = tk.Button(self.root, text="Add Password", command=self.add_password, bg='dark grey', fg='black')
        self.add_button.pack(pady=5)

        self.get_button = tk.Button(self.root, text="Get Password", command=self.get_password, bg='dark grey', fg='black')
        self.get_button.pack(pady=5)

        self.list_button = tk.Button(self.root, text="List Accounts", command=self.list_accounts, bg='dark grey', fg='black')
        self.list_button.pack(pady=5)

    def add_password(self):
        website = self.website_entry.get()
        account = self.account_entry.get()
        password = self.password_entry.get()

        if website and account and password:
            self.password_manager.add_password(account, password, website)
            messagebox.showinfo("Success", "Password added!")
        else:
            messagebox.showerror("Error", "Please enter website, account, and password.")

    def get_password(self):
        website = self.website_entry.get()
        account = self.account_entry.get()
        password = self.password_manager.get_password(website, account)

        if password != "Account not found":
            messagebox.showinfo("Password", f"Password for {account} on {website}: {password}")
        else:
            messagebox.showerror("Error", "Account not found.")

    def list_accounts(self):
        data = self.password_manager.list_accounts()
        
        if data:
            accounts = "\n".join([f"Website: {website}, Account: {entry['account']}, Password: {entry['password']}" for website, entries in data.items() for entry in entries])
            messagebox.showinfo("Accounts", f"Accounts:\n{accounts}")
        else:
            messagebox.showinfo("Accounts", "No accounts stored.")

def get_master_password():
    root = tk.Tk()
    root.withdraw()

    while True:
        master_password = simpledialog.askstring("Master Password", "Enter master password:", show='*')
        confirm_password = simpledialog.askstring("Master Password", "Confirm master password:", show='*')

        if master_password == confirm_password:
            root.destroy()
            return master_password
        else:
            messagebox.showerror("Error", "Passwords do not match. Please try again.")

def main():
    root = tk.Tk()
    app = PasswordManagerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
