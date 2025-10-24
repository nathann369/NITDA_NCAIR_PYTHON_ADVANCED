# diary.py
# -----------------------------------------
# Core business logic of the Diary
# -----------------------------------------

from datetime import datetime
from errors import DiaryLockedError, EntryNotFoundError


class Entry:
    """Represents a single diary entry."""
    def __init__(self, title, content, date=None):
        self.title = title
        self.content = content
        self.date = date or datetime.now().strftime("%Y-%m-%d")

    def __repr__(self):
        return f"<Entry: {self.title} ({self.date})>"


class Diary:
    """Manages diary entries and lock state."""
    def __init__(self):
        self.entries = []
        self.locked = False
        self.password_hash = None  # set via utils.hash_password()

    def add_entry(self, entry: Entry):
        if self.locked:
            raise DiaryLockedError("Diary is locked! Unlock to add entries.")
        self.entries.append(entry)

    def edit_entry(self, title, new_content):
        if self.locked:
            raise DiaryLockedError("Diary is locked! Unlock to edit entries.")
        for e in self.entries:
            if e.title == title:
                e.content = new_content
                return
        raise EntryNotFoundError(f"Entry '{title}' not found.")

    def delete_entry(self, title):
        if self.locked:
            raise DiaryLockedError("Diary is locked! Unlock to delete entries.")
        for e in self.entries:
            if e.title == title:
                self.entries.remove(e)
                return
        raise EntryNotFoundError(f"Entry '{title}' not found.")

    def search(self, keyword="", start_date=None, end_date=None):
        """Search entries by keyword or date range."""
        results = []
        for e in self.entries:
            if keyword.lower() in e.title.lower() or keyword.lower() in e.content.lower():
                results.append(e)
            elif start_date and end_date and start_date <= e.date <= end_date:
                results.append(e)
        return results

    def lock(self):
        self.locked = True

    def unlock(self, password, verify_func):
        """Unlock diary if password is correct."""
        if verify_func(password):
            self.locked = False
            return True
        return False
