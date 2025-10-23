import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
from diary import Diary, Entry
from storage import StorageManager
from errors import DiaryLockedError, EntryNotFoundError

class DiaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Diary App 📝")

        self.storage = StorageManager()
        self.diary = Diary()
        self.diary.entries = self.storage.load()

        # Layout Frames
        self.left_frame = tk.Frame(root, padx=10, pady=10)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.right_frame = tk.Frame(root, padx=10, pady=10)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Left frame (Calendar/Entry List)
        tk.Label(self.left_frame, text="Entries", font=("Arial", 14, "bold")).pack()
        self.entry_listbox = tk.Listbox(self.left_frame, width=30)
        self.entry_listbox.pack(fill=tk.Y, expand=True)
        self.entry_listbox.bind("<<ListboxSelect>>", self.view_entry)

        # Right frame (Editor + Buttons)
        tk.Label(self.right_frame, text="Title:").pack(anchor="w")
        self.title_entry = tk.Entry(self.right_frame, width=50)
        self.title_entry.pack(anchor="w")

        tk.Label(self.right_frame, text="Content:").pack(anchor="w")
        self.content_text = scrolledtext.ScrolledText(self.right_frame, width=60, height=15)
        self.content_text.pack(fill=tk.BOTH, expand=True)

        self.search_box = tk.Entry(self.right_frame, width=30)
        self.search_box.pack(side=tk.LEFT)
        tk.Button(self.right_frame, text="Search", command=self.search_entry).pack(side=tk.LEFT, padx=5)

        tk.Button(self.right_frame, text="Add Entry", command=self.add_entry).pack(side=tk.LEFT, padx=5)
        tk.Button(self.right_frame, text="Delete", command=self.delete_entry).pack(side=tk.LEFT, padx=5)
        tk.Button(self.right_frame, text="Save", command=self.save_entries).pack(side=tk.LEFT, padx=5)

        self.refresh_listbox()

    def refresh_listbox(self):
        self.entry_listbox.delete(0, tk.END)
        for e in self.diary.entries:
            self.entry_listbox.insert(tk.END, f"{e.date} - {e.title}")

    def add_entry(self):
        title = self.title_entry.get().strip()
        content = self.content_text.get("1.0", tk.END).strip()
        if not title or not content:
            messagebox.showwarning("Input Error", "Please fill in both title and content!")
            return
        try:
            entry = Entry(title, content)
            self.diary.add_entry(entry)
            self.refresh_listbox()
            self.title_entry.delete(0, tk.END)
            self.content_text.delete("1.0", tk.END)
            messagebox.showinfo("Success", "Entry added successfully!")
        except DiaryLockedError as e:
            messagebox.showerror("Error", str(e))

    def view_entry(self, event):
        try:
            selected = self.entry_listbox.curselection()
            if not selected:
                return
            index = selected[0]
            entry = self.diary.entries[index]
            self.title_entry.delete(0, tk.END)
            self.title_entry.insert(0, entry.title)
            self.content_text.delete("1.0", tk.END)
            self.content_text.insert(tk.END, entry.content)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_entry(self):
        try:
            selected = self.entry_listbox.curselection()
            if not selected:
                messagebox.showinfo("Info", "Select an entry to delete.")
                return
            title = self.diary.entries[selected[0]].title
            self.diary.delete_entry(title)
            self.refresh_listbox()
            messagebox.showinfo("Deleted", "Entry deleted.")
        except EntryNotFoundError as e:
            messagebox.showerror("Error", str(e))

    def search_entry(self):
        keyword = self.search_box.get().strip()
        if not keyword:
            messagebox.showwarning("Warning", "Enter a keyword to search.")
            return
        results = self.diary.search(keyword)
        self.entry_listbox.delete(0, tk.END)
        for r in results:
            self.entry_listbox.insert(tk.END, f"{r.date} - {r.title}")

    def save_entries(self):
        self.storage.save(self.diary.entries)
        messagebox.showinfo("Saved", "All entries saved to file.")

def start_ui():
    root = tk.Tk()
    app = DiaryApp(root)
    root.mainloop()
