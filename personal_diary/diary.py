from datetime import datetime
from errors import DiaryLockedError, EntryNotFoundError

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

    def lock(self):
        self.locked = True

    def add_entry(self, entry):
        if self.locked:
            raise DiaryLockedError("Diary is locked!")
        self.entries.append(entry)

    def delete_entry(self, title):
        for e in self.entries:
            if e.title == title:
                self.entries.remove(e)
                return
        raise EntryNotFoundError(f"No entry found with title '{title}'")

    def search(self, keyword):
        return [e for e in self.entries if keyword.lower() in e.content.lower() or keyword.lower() in e.title.lower()]
