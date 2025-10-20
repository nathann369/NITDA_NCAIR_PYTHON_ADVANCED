# File Handling


# with open("day3.txt.txt", "r", encoding="utf-8") as file:
#     print(file.read())
#     # file.write("This is a test file.\n")

# with open("images.jfif", "rb") as fsrc, open("new.png", "wb") as fdst:
#     first_image = fsrc.read()
#     fdst.write(first_image)
#     print(first_image)


import os
from datetime import datetime, timedelta

# Custom exception for duplicate or early entries
class DuplicateVisitorError(Exception):
    """Raised when a duplicate visitor name is detected."""
    pass

class TooSoonError(Exception):
    """Raised when a new visitor tries to enter within 5 minutes."""
    pass

# File name
FILENAME = "visitors.txt"

def log_visitor():
    name = input("Enter your name: ").strip()

    # Create the file if it doesn't exist
    if not os.path.exists(FILENAME):
        with open(FILENAME, "w") as f:
            pass

    last_line = ""
    with open(FILENAME, "r") as f:
        lines = f.readlines()
        if lines:
            last_line = lines[-1].strip()

    if last_line:
        # Last line format: "Name - YYYY-MM-DD HH:MM:SS"
        last_name, last_time_str = last_line.split(" - ")
        last_time = datetime.strptime(last_time_str, "%Y-%m-%d %H:%M:%S")

        # Check if name is same
        if name.lower() == last_name.lower():
            raise DuplicateVisitorError(f"Duplicate visitor detected: {name}")

        # Check if 5 minutes have passed
        if datetime.now() - last_time < timedelta(minutes=5):
            raise TooSoonError("New visitor cannot enter yet. Please wait 5 minutes.")

    # Log new visitor
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(FILENAME, "a") as f:
        f.write(f"{name} - {timestamp}\n")

    print(f"Welcome, {name}! You have been logged successfully at {timestamp}.")

# Run the program
if __name__ == "__main__":
    try:
        log_visitor()
    except DuplicateVisitorError as e:
        print("Error:", e)
    except TooSoonError as e:
        print("Error:", e)
    except Exception as e:
        print("An unexpected error occurred:", e)
