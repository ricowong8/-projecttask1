import ttkbootstrap as tb
from tkinter import messagebox
from gui import InventoryApp

USERS = {
    "admin": {"password": "1234", "role": "admin"},
    "user": {"password": "5678", "role": "viewer"},
}
MAX_ATTEMPTS = 3


class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Login - Bcry UI")
        self.attempts = 0

        frame = tb.Frame(root, padding=20)
        frame.pack(fill="both", expand=True)

        tb.Label(frame, text="Username", bootstyle="primary").grid(
            row=0, column=0, padx=10, pady=10
        )
        tb.Label(frame, text="Password", bootstyle="primary").grid(
            row=1, column=0, padx=10, pady=10
        )

        self.entry_user = tb.Entry(frame, bootstyle="info")
        self.entry_pass = tb.Entry(frame, show="*", bootstyle="info")

        self.entry_user.grid(row=0, column=1, padx=10, pady=10)
        self.entry_pass.grid(row=1, column=1, padx=10, pady=10)

        tb.Button(
            frame, text="Login", bootstyle="success", command=self.check_login
        ).grid(row=2, column=0, columnspan=2, pady=15)

    def check_login(self):
        username = self.entry_user.get()
        password = self.entry_pass.get()

        if username in USERS and USERS[username]["password"] == password:
            role = USERS[username]["role"]
            messagebox.showinfo("Success", f"Welcome {username} ({role})!")
            self.root.destroy()
            main_app(username, role)
        else:
            self.attempts += 1
            remaining = MAX_ATTEMPTS - self.attempts
            if remaining > 0:
                messagebox.showerror(
                    "Error", f"Invalid login! {remaining} attempts left."
                )
            else:
                messagebox.showerror("Error", "Too many failed attempts. Exiting...")
                self.root.destroy()


def main_app(username, role):
    root = tb.Window(themename="darkly")
    InventoryApp(
        root, username=username, role=role, logout_callback=lambda: logout(root)
    )
    root.mainloop()


def logout(root):
    root.destroy()
    login_root = tb.Window(themename="darkly")
    LoginWindow(login_root)
    login_root.mainloop()


if __name__ == "__main__":
    login_root = tb.Window(themename="darkly")
    LoginWindow(login_root)
    login_root.mainloop()
