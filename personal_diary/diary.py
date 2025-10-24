from datetime import datetime
from errors import DiaryLockedError, EntryNotFoundError
from utils import within_date_range

class Entry:
    def __init__(self, title, content, date=None):
        self.title = title
        self.content = content
        self.date = date or datetime.now().strftime("%Y-%m-%d %H:%M")

    def __repr__(self):
        return f"[{self.date}] {self.title}"

class Diary:
    def __init__(self, password=None):
        self.entries = []
        self.locked = bool(password)
        self.password = password

    def unlock(self, password):
        if not self.locked:
            return True
        if password == self.password:
            self.locked = False
            return True
        raise DiaryLockedError("Incorrect password")

    def add_entry(self, entry):
        if self.locked:
            raise DiaryLockedError("Diary is locked!")
        self.entries.append(entry)

    def edit_entry(self, title, new_content):
        for e in self.entries:
            if e.title == title:
                e.content = new_content
                return
        raise EntryNotFoundError(f"No entry found with title '{title}'")

    def delete_entry(self, title):
        for e in self.entries:
            if e.title == title:
                self.entries.remove(e)
                return
        raise EntryNotFoundError(f"No entry found with title '{title}'")

    def search(self, keyword=None, start_date=None, end_date=None):
        results = self.entries
        if keyword:
            results = [e for e in results if keyword.lower() in e.title.lower() or keyword.lower() in e.content.lower()]
        if start_date and end_date:
            results = [e for e in results if within_date_range(e.date, start_date, end_date)]
        return results
