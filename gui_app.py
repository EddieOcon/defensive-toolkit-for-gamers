# gui_app.py
import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
import getpass  # used for CLI only if needed

from safevault.core import SafeVault, VaultEntry, VaultAuthError, VaultError

VAULT_PATH = "vault.bin"

class VaultGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gamer SafeVault")
        self.geometry("520x340")

        self.vault = SafeVault(VAULT_PATH)
        self.master_password = None

        self.create_widgets()
        self.prompt_master_password(initial=True)

    def create_widgets(self):
        frame = ttk.Frame(self)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(frame, columns=("username",), show="headings")
        self.tree.heading("username", text="Username")
        self.tree.pack(fill="both", expand=True)

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x", pady=5)

        ttk.Button(btn_frame, text="Add Entry", command=self.add_entry).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="View Entry", command=self.view_entry).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Copy Password", command=self.copy_password).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Delete Entry", command=self.delete_entry).pack(side="right", padx=5)

    def prompt_master_password(self, initial=False):
        while True:
            mp = simpledialog.askstring("Master Password",
                                        "Enter master password:",
                                        show="*",
                                        parent=self)
            if mp is None:
                if initial:
                    self.destroy()
                return
            try:
                if self.vault.exists():
                    self.vault.load(mp)
                else:
                    # new vault
                    self.vault.create_new(mp)
                self.master_password = mp
                self.refresh_list()
                break
            except VaultAuthError:
                messagebox.showerror("Error", "Wrong master password.")
            except VaultError as e:
                messagebox.showerror("Error", str(e))
                break

    def refresh_list(self):
        self.tree.delete(*self.tree.get_children())
        for entry in self.vault.list_entries():
            self.tree.insert("", "end", iid=entry.name, values=(entry.username,))

    def add_entry(self):
        if not self.master_password:
            return
        name = simpledialog.askstring("New Entry", "Account name (e.g., steam):", parent=self)
        if not name:
            return
        user = simpledialog.askstring("Username", "Username / email:", parent=self)
        if not user:
            user = ""
        pwd = simpledialog.askstring("Password", "Password (leave blank to auto-generate):",
                                     show="*", parent=self)
        if not pwd:
            pwd = self.vault.generate_password(18)
            messagebox.showinfo("Generated Password", f"Generated: {pwd}")
        notes = simpledialog.askstring("Notes", "Notes (optional):", parent=self) or ""
        e = VaultEntry(name=name, username=user, password=pwd, notes=notes)
        self.vault.add_entry(e)
        self.vault.save(self.master_password)
        self.refresh_list()

    def _get_selected_name(self):
        sel = self.tree.selection()
        if not sel:
            return None
        return sel[0]

    def view_entry(self):
        name = self._get_selected_name()
        if not name:
            return
        entry = self.vault.get_entry(name)
        if not entry:
            return
        msg = f"Name: {entry.name}\nUsername: {entry.username}\nNotes: {entry.notes}"
        messagebox.showinfo("Entry Details", msg)

    def copy_password(self):
        import pyperclip, time, threading
        name = self._get_selected_name()
        if not name:
            return
        entry = self.vault.get_entry(name)
        if not entry:
            return
        pyperclip.copy(entry.password)
        messagebox.showinfo("Password Copied", "Password copied to clipboard for 10 seconds.")
        def clear_clip():
            time.sleep(10)
            pyperclip.copy("")
        threading.Thread(target=clear_clip, daemon=True).start()

    def delete_entry(self):
        name = self._get_selected_name()
        if not name:
            return
        if not messagebox.askyesno("Confirm", f"Delete entry '{name}'?"):
            return
        self.vault.delete_entry(name)
        self.vault.save(self.master_password)
        self.refresh_list()

if __name__ == "__main__":
    app = VaultGUI()
    app.mainloop()
