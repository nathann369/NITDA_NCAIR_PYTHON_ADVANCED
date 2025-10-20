import tkinter as tk
from tkinter import messagebox


root = tk.Tk()
root.title("Registration Form")
root.geometry("500x350")
# root.geometry("WxH")
root.config(bg="#333333")  

# Function to handle button click
def submit_form():
    pass
    # name = name_entry.get().strip()
    # email = email_entry.get().strip()
    # phone = phone_entry.get().strip()
    # comments = comments_text.get("1.0", tk.END).strip()

    # if not name or not email or not phone:
    #     messagebox.showwarning("Incomplete", "Please fill in all fields.")
    # else:
    #     messagebox.showinfo("Success", f"Thank you {name}, your form has been submitted!")
    #     # You could also save to file or database here if needed

# Labels
tk.Label(root, text="Register", bg="#333333",fg="white", font=("Arial", 20, "bold")).place(x=150, y=10)
tk.Label(root, text="Name:", bg="#333333",fg="white", font=("Arial", 10, "bold")).place(x=50, y=50)
tk.Label(root, text="Email:", bg="#333333",fg="white", font=("Arial", 10, "bold")).place(x=50, y=90)
tk.Label(root, text="Phone:", bg="#333333",fg="white", font=("Arial", 10, "bold")).place(x=50, y=130)
tk.Label(root, text="Comments:", bg="#333333",fg="white", font=("Arial", 10, "bold")).place(x=50, y=170)

# Entry fields
name_entry = tk.Entry(root, width=30)
email_entry = tk.Entry(root, width=30)
phone_entry = tk.Entry(root, width=30)
comments_text = tk.Text(root, width=30, height=3)

# Place the input fields
name_entry.place(x=150, y=50)
email_entry.place(x=150, y=90)
phone_entry.place(x=150, y=130)
comments_text.place(x=150, y=170)

# Submit button
submit_btn = tk.Button(root, text="Register", bg="#383B38", fg="white", font=("Arial", 13, "bold"), command=submit_form)
submit_btn.place(x=150, y=240)

# Run the Tkinter event loop
root.mainloop()
