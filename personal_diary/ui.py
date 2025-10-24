# ui.py
# -----------------------------------------
# GUI for Personal Diary App
# Features:
#   - Create, edit, delete diary entries
#   - Calendar sidebar navigation
#   - Keyword/date search
#   - Basic password lock/unlock
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
        # -------------------------------
        # WINDOW CONFIGURATION
        # -------------------------------
        self.root = root
        self.root.title("Personal Diary")
        self.root.config(bg="#333333")  # Set dark theme background

        self.storage = StorageManager()
        self.diary = Diary()
        self.diary.entries = self.storage.load()

        # Password setup or verification
        self._init_password()

        # -------------------------------
        # UI LAYOUT
        # -------------------------------

        # LEFT PANEL — Calendar + Entry List
        self.left = tk.Frame(root, bg="#333333", padx=10, pady=10)
        self.left.pack(side=tk.LEFT, fill=tk.Y)

        # RIGHT PANEL — Editor + Controls
        self.right = tk.Frame(root, bg="#333333", padx=10, pady=10)
        self.right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Calendar widget
        try:
            self.cal = Calendar(self.left)
        except TypeError:
            self.cal = Calendar(self.left)
        self.cal.pack(pady=5)

        tk.Button(self.left, text="View by Date", command=self.view_by_date, bg="#555555", fg="white").pack(pady=5)

        # Entry listbox
        self.listbox = tk.Listbox(self.left, width=30, height=15, bg="#868383", fg="white")
        self.listbox.pack(pady=10)
        self.listbox.bind("<<ListboxSelect>>", self.view_entry)

        # -------------------------------
        # RIGHT PANEL — Editor
        # -------------------------------
        tk.Label(self.right, text="Title:", bg="#333333", fg="white").pack(anchor="w")
        self.title_entry = tk.Entry(self.right, width=50, bg="#444444", fg="white", insertbackground="white")
        self.title_entry.pack(anchor="w")

        tk.Label(self.right, text="Content:", bg="#333333", fg="white").pack(anchor="w")
        self.content_text = scrolledtext.ScrolledText(self.right, width=60, height=15, bg="#928F8F", fg="white", insertbackground="white")
        self.content_text.pack(fill=tk.BOTH, expand=True)

        # -------------------------------
        # CONTROL BUTTONS
        # -------------------------------
        self.search_box = tk.Entry(self.right, width=20, bg="#8B8787", fg="white", insertbackground="white")
        self.search_box.pack(side=tk.LEFT, padx=5)

        tk.Button(self.right, text="Search", command=self.search_entries, bg="#555555", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(self.right, text="Add", command=self.add_entry, bg="#609C60", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(self.right, text="Edit", command=self.edit_entry, bg="#525296", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(self.right, text="Delete", command=self.delete_entry, bg="#834444", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(self.right, text="Save", command=self.save_entries, bg="#444444", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(self.right, text="Lock", command=self.lock_diary, bg="#333333", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(self.right, text="Unlock", command=self.unlock_diary, bg="#333333", fg="white").pack(side=tk.LEFT, padx=5)

        self.refresh_list()

    # -------------------------------
    # PASSWORD SETUP
    # -------------------------------
    def _init_password(self):
        """Set or verify password (first time setup uses a default if none)."""
        try:
            with open("password.txt", "r") as f:
                stored_hash = f.read().strip()
        except FileNotFoundError:
            pw = simpledialog.askstring("Set Password", "Create a password for your diary:", show="*")
            if not pw:
                pw = "1234"  # Default fallback
            with open("password.txt", "w") as f:
                f.write(hash_password(pw))
            stored_hash = hash_password(pw)
        self.diary.password_hash = stored_hash

    # -------------------------------
    # ENTRY MANAGEMENT FUNCTIONS
    # -------------------------------
    def refresh_list(self, entries=None):
        """Refresh entry list display."""
        self.listbox.delete(0, tk.END)
        for e in (entries or self.diary.entries):
            self.listbox.insert(tk.END, f"{e.date} - {e.title}")

    def clear_fields(self):
        """Clear the title and content fields."""
        self.title_entry.delete(0, tk.END)
        self.content_text.delete("1.0", tk.END)

    def add_entry(self):
        """Add a new diary entry."""
        title = self.title_entry.get().strip()
        content = self.content_text.get("1.0", tk.END).strip()
        if not title or not content:
            messagebox.showwarning("Error", "Both title and content required.")
            return
        try:
            self.diary.add_entry(Entry(title, content))
            self.refresh_list()
            self.clear_fields()  # Clear after add
        except DiaryLockedError as e:
            messagebox.showerror("Locked", str(e))

    def edit_entry(self):
        """Edit the selected diary entry."""
        try:
            index = self.listbox.curselection()[0]
            entry = self.diary.entries[index]
            new_title = self.title_entry.get().strip()
            new_content = self.content_text.get("1.0", tk.END).strip()
            entry.title = new_title
            entry.content = new_content
            messagebox.showinfo("Success", "Entry updated successfully.")
            self.refresh_list()
            self.clear_fields()  # Clear after edit
        except (DiaryLockedError, IndexError, EntryNotFoundError) as e:
            messagebox.showerror("Error", str(e))

    def delete_entry(self):
        """Delete selected diary entry."""
        try:
            index = self.listbox.curselection()[0]
            title = self.diary.entries[index].title
            self.diary.delete_entry(title)
            self.refresh_list()
            messagebox.showinfo("Deleted", "Entry removed.")
            self.clear_fields()
        except (DiaryLockedError, IndexError, EntryNotFoundError) as e:
            messagebox.showerror("Error", str(e))

    def view_entry(self, event):
        """Display selected entry in editor."""
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
        """Filter entries by selected date on the calendar."""
        date_selected = self.cal.get_date()
        results = [e for e in self.diary.entries if e.date.startswith(date_selected)]
        self.refresh_list(results)

    def search_entries(self):
        """Search entries by keyword or date range."""
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
        """Save all entries to storage."""
        self.storage.save(self.diary.entries)
        messagebox.showinfo("Saved", "All entries saved!")

    # -------------------------------
    # LOCK / UNLOCK DIARY
    # -------------------------------
    def lock_diary(self):
        """Lock the diary."""
        self.diary.lock()
        messagebox.showinfo("Locked", "Diary is now locked.")

    def unlock_diary(self):
        """Unlock the diary."""
        password = simpledialog.askstring("Unlock", "Enter your diary password:", show="*")
        if self.diary.unlock(password, lambda p: verify_password(self.diary.password_hash, p)):
            messagebox.showinfo("Unlocked", "Diary unlocked successfully!")
        else:
            messagebox.showerror("Error", "Incorrect password.")


def start_ui():
    root = tk.Tk()
    app = DiaryApp(root)
    root.mainloop()
