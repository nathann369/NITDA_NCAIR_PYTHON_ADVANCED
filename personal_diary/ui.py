from calendar import Calendar
import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
# from  tkcalendar import Calendar
from datetime import datetime
from diary import Diary, Entry
from storage import StorageManager
from errors import DiaryLockedError, EntryNotFoundError
from utils import parse_date
from security import verify_password

class DiaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Diary 🗓️")
        self.storage = StorageManager()
        self.diary = Diary()
        self.diary.entries = self.storage.load()

        # Password prompt
        if not verify_password(simpledialog.askstring("Password", "Enter master password:", show="*")):
            messagebox.showerror("Error", "Invalid password. Exiting.")
            root.destroy()
            return

        # Layout
        self.left_frame = tk.Frame(root, padx=10, pady=10)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.right_frame = tk.Frame(root, padx=10, pady=10)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Calendar
       # Calendar sidebar
        try:
            self.cal = Calendar(self.left_frame, selectmode="day")
        except TypeError:
            # fallback if the installed tkcalendar doesn’t support selectmode
            self.cal = Calendar(self.left_frame)

        self.cal.pack(pady=5)
        tk.Button(self.left_frame, text="View Date Entries", command=self.view_by_date).pack()

        # Entry list
        self.entry_listbox = tk.Listbox(self.left_frame, width=30, height=15)
        self.entry_listbox.pack(pady=10, fill=tk.Y)
        self.entry_listbox.bind("<<ListboxSelect>>", self.view_entry)

        # Right Pane - Editor
        tk.Label(self.right_frame, text="Title:").pack(anchor="w")
        self.title_entry = tk.Entry(self.right_frame, width=50)
        self.title_entry.pack(anchor="w")

        tk.Label(self.right_frame, text="Content:").pack(anchor="w")
        self.content_text = scrolledtext.ScrolledText(self.right_frame, width=60, height=15)
        self.content_text.pack(fill=tk.BOTH, expand=True)

        # Search bar
        self.search_box = tk.Entry(self.right_frame, width=20)
        self.search_box.pack(side=tk.LEFT, padx=5)
        tk.Button(self.right_frame, text="Search", command=self.search_entries).pack(side=tk.LEFT, padx=5)

        tk.Button(self.right_frame, text="Add", command=self.add_entry).pack(side=tk.LEFT, padx=5)
        tk.Button(self.right_frame, text="Edit", command=self.edit_entry).pack(side=tk.LEFT, padx=5)
        tk.Button(self.right_frame, text="Delete", command=self.delete_entry).pack(side=tk.LEFT, padx=5)
        tk.Button(self.right_frame, text="Save", command=self.save_entries).pack(side=tk.LEFT, padx=5)

        self.refresh_list()

    def refresh_list(self, entries=None):
        self.entry_listbox.delete(0, tk.END)
        for e in (entries or self.diary.entries):
            self.entry_listbox.insert(tk.END, f"{e.date} - {e.title}")

    def add_entry(self):
        title = self.title_entry.get().strip()
        content = self.content_text.get("1.0", tk.END).strip()
        if not title or not content:
            messagebox.showwarning("Input Error", "Please fill both title and content!")
            return
        entry = Entry(title, content)
        self.diary.add_entry(entry)
        self.refresh_list()
        messagebox.showinfo("Added", "Entry added successfully.")

    def edit_entry(self):
        selected = self.entry_listbox.curselection()
        if not selected:
            messagebox.showwarning("Select Entry", "Select an entry to edit.")
            return
        title = self.diary.entries[selected[0]].title
        new_content = self.content_text.get("1.0", tk.END).strip()
        self.diary.edit_entry(title, new_content)
        self.refresh_list()
        messagebox.showinfo("Updated", "Entry updated successfully.")

    def delete_entry(self):
        selected = self.entry_listbox.curselection()
        if not selected:
            messagebox.showwarning("Select Entry", "Select an entry to delete.")
            return
        title = self.diary.entries[selected[0]].title
        self.diary.delete_entry(title)
        self.refresh_list()
        messagebox.showinfo("Deleted", "Entry deleted successfully.")

    def view_entry(self, event):
        try:
            selected = self.entry_listbox.curselection()
            if not selected:
                return
            entry = self.diary.entries[selected[0]]
            self.title_entry.delete(0, tk.END)
            self.title_entry.insert(0, entry.title)
            self.content_text.delete("1.0", tk.END)
            self.content_text.insert(tk.END, entry.content)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def search_entries(self):
        keyword = self.search_box.get().strip()
        start_date = simpledialog.askstring("Start Date", "Enter start date (YYYY-MM-DD):")
        end_date = simpledialog.askstring("End Date", "Enter end date (YYYY-MM-DD):")

        start = parse_date(start_date) if start_date else None
        end = parse_date(end_date) if end_date else None
        results = self.diary.search(keyword, start, end)
        self.refresh_list(results)

    def view_by_date(self):
        date_selected = self.cal.get_date()
        results = [e for e in self.diary.entries if e.date.startswith(date_selected)]
        self.refresh_list(results)

    def save_entries(self):
        self.storage.save(self.diary.entries)
        messagebox.showinfo("Saved", "All entries saved!")

def start_ui():
    root = tk.Tk()
    app = DiaryApp(root)
    root.mainloop()
