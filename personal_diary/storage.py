import json
from diary import Entry

class StorageManager:
    def __init__(self, file_path="diary_data.json"):
        self.file_path = file_path

    def save(self, entries):
        data = [e.__dict__ for e in entries]
        with open(self.file_path, "w") as f:
            json.dump(data, f, indent=4)

    def load(self):
        try:
            with open(self.file_path, "r") as f:
                data = json.load(f)
                return [Entry(**item) for item in data]
        except FileNotFoundError:
            return []
