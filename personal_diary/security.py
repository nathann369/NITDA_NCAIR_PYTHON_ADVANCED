import hashlib, json, os

PASSWORD_FILE = "password.json"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def save_password(password):
    with open(PASSWORD_FILE, "w") as f:
        json.dump({"hash": hash_password(password)}, f)

def verify_password(password):
    if not os.path.exists(PASSWORD_FILE):
        save_password(password)  # First-time setup
        return True
    with open(PASSWORD_FILE, "r") as f:
        data = json.load(f)
    return data["hash"] == hash_password(password)
