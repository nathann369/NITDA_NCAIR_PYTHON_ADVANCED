# utils.py
# -----------------------------------------
# Utility functions: password hashing,
# regex date parsing, etc.
# -----------------------------------------

import re
import hashlib

def hash_password(password: str):
    """Hash a password using SHA256."""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(stored_hash, entered_password):
    """Compare a stored hash and an entered password."""
    return stored_hash == hash_password(entered_password)

def parse_date(date_str: str):
    """Parse and validate date format YYYY-MM-DD using regex."""
    pattern = r"^\d{4}-\d{2}-\d{2}$"
    if re.match(pattern, date_str):
        return date_str
    raise ValueError("Invalid date format. Use YYYY-MM-DD.")
