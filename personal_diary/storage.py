# storage.py
# -----------------------------------------
# Handles saving/loading entries to a file.
# -----------------------------------------

import json
import os
from diary import Entry


class StorageManager:
    FILE_NAME = "entries.json"

    def save(self, entries):
        data = [e.__dict__ for e in entries]
        with open(self.FILE_NAME, "w") as f:
            json.dump(data, f, indent=4)

    def load(self):
        if not os.path.exists(self.FILE_NAME):
            return []
        with open(self.FILE_NAME, "r") as f:
            data = json.load(f)
        return [Entry(**d) for d in data]
