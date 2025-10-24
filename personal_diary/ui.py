# ui.py
# -----------------------------------------
# Handles GUI for Personal Diary App
# -----------------------------------------

import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
from tkcalendar import Calendar
from diary import Diary, Entry
from storage import StorageManager
from utils import parse_date, hash_password, verify_password
from errors import DiaryLockedError, EntryNotFoundError


class DiaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Diary 🗓️")

        self.storage = StorageManager()
        self.diary = Diary()
        self.diary.entries = self.storage.load()

        # Ask for or set a password (only once)
        self._init_password()

        # -------------------------------
        # UI Layout
        # -------------------------------
        self.left = tk.Frame(root, padx=10, pady=10)
        self.left.pack(side=tk.LEFT, fill=tk.Y)

        self.right = tk.Frame(root, padx=10, pady=10)
        self.right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Left Sidebar: Calendar + Entry List
        try:
            self.cal = Calendar(self.left)
        except TypeError:
            self.cal = Calendar(self.left)
        self.cal.pack(pady=5)

        tk.Button(self.left, text="View by Date", command=self.view_by_date).pack(pady=5)

        self.listbox = tk.Listbox(self.left, width=30, height=15)
        self.listbox.pack(pady=10)
        self.listbox.bind("<<ListboxSelect>>", self.view_entry)

        # Right Pane: Editor
        tk.Label(self.right, text="Title:").pack(anchor="w")
        self.title_entry = tk.Entry(self.right, width=50)
        self.title_entry.pack(anchor="w")

        tk.Label(self.right, text="Content:").pack(anchor="w")
        self.content_text = scrolledtext.ScrolledText(self.right, width=60, height=15)
        self.content_text.pack(fill=tk.BOTH, expand=True)

        # Controls
        self.search_box = tk.Entry(self.right, width=20)
        self.search_box.pack(side=tk.LEFT, padx=5)

        tk.Button(self.right, text="Search", command=self.search_entries).pack(side=tk.LEFT, padx=5)
        tk.Button(self.right, text="Add", command=self.add_entry).pack(side=tk.LEFT, padx=5)
        tk.Button(self.right, text="Edit", command=self.edit_entry).pack(side=tk.LEFT, padx=5)
        tk.Button(self.right, text="Delete", command=self.delete_entry).pack(side=tk.LEFT, padx=5)
        tk.Button(self.right, text="Save", command=self.save_entries).pack(side=tk.LEFT, padx=5)

        # Lock/Unlock feature
        tk.Button(self.right, text="Lock", command=self.lock_diary).pack(side=tk.LEFT, padx=5)
        tk.Button(self.right, text="Unlock", command=self.unlock_diary).pack(side=tk.LEFT, padx=5)

        self.refresh_list()

    # -------------------------------
    # Password Setup
    # -------------------------------
    def _init_password(self):
        """Set up or verify password."""
        try:
            with open("password.txt", "r") as f:
                stored_hash = f.read().strip()
        except FileNotFoundError:
            pw = simpledialog.askstring("Set Password", "Create a password for your diary:", show="*")
            if not pw:
                pw = "1234"  # default if empty
            with open("password.txt", "w") as f:
                f.write(hash_password(pw))
            stored_hash = hash_password(pw)
        self.diary.password_hash = stored_hash

    # -------------------------------
    # Diary Actions
    # -------------------------------
    def refresh_list(self, entries=None):
        self.listbox.delete(0, tk.END)
        for e in (entries or self.diary.entries):
            self.listbox.insert(tk.END, f"{e.date} - {e.title}")

    def add_entry(self):
        title = self.title_entry.get().strip()
        content = self.content_text.get("1.0", tk.END).strip()
        if not title or not content:
            messagebox.showwarning("Error", "Both title and content required.")
            return
        try:
            self.diary.add_entry(Entry(title, content))
            self.refresh_list()
        except DiaryLockedError as e:
            messagebox.showerror("Locked", str(e))

    def edit_entry(self):
        try:
            index = self.listbox.curselection()[0]
            entry = self.diary.entries[index]
            new_content = self.content_text.get("1.0", tk.END).strip()
            self.diary.edit_entry(entry.title, new_content)
            messagebox.showinfo("Success", "Entry updated.")
        except (DiaryLockedError, IndexError, EntryNotFoundError) as e:
            messagebox.showerror("Error", str(e))

    def delete_entry(self):
        try:
            index = self.listbox.curselection()[0]
            title = self.diary.entries[index].title
            self.diary.delete_entry(title)
            self.refresh_list()
            messagebox.showinfo("Deleted", "Entry removed.")
        except (DiaryLockedError, IndexError, EntryNotFoundError) as e:
            messagebox.showerror("Error", str(e))

    def view_entry(self, event):
        try:
            index = self.listbox.curselection()[0]
            e = self.diary.entries[index]
            self.title_entry.delete(0, tk.END)
            self.title_entry.insert(0, e.title)
            self.content_text.delete("1.0", tk.END)
            self.content_text.insert(tk.END, e.content)
        except IndexError:
            pass

    def view_by_date(self):
        date_selected = self.cal.get_date()
        results = [e for e in self.diary.entries if e.date.startswith(date_selected)]
        self.refresh_list(results)

    def search_entries(self):
        keyword = self.search_box.get().strip()
        start = simpledialog.askstring("Start Date", "Enter start date (YYYY-MM-DD):")
        end = simpledialog.askstring("End Date", "Enter end date (YYYY-MM-DD):")
        try:
            s = parse_date(start) if start else None
            e = parse_date(end) if end else None
            results = self.diary.search(keyword, s, e)
            self.refresh_list(results)
        except ValueError as err:
            messagebox.showerror("Error", str(err))

    def save_entries(self):
        self.storage.save(self.diary.entries)
        messagebox.showinfo("Saved", "All entries saved!")

    # -------------------------------
    # Lock & Unlock Functions
    # -------------------------------
    def lock_diary(self):
        self.diary.lock()
        messagebox.showinfo("Locked", "Diary is now locked.")

    def unlock_diary(self):
        password = simpledialog.askstring("Unlock", "Enter your diary password:", show="*")
        if self.diary.unlock(password, lambda p: verify_password(self.diary.password_hash, p)):
            messagebox.showinfo("Unlocked", "Diary unlocked successfully!")
        else:
            messagebox.showerror("Error", "Incorrect password.")


def start_ui():
    root = tk.Tk()
    app = DiaryApp(root)
    root.mainloop()
