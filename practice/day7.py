import tkinter
from tkinter import messagebox

window = tkinter.Tk()
window.title("Reg_Form")
window.geometry('640x450')
window.configure(bg='#333333')
frame = tkinter.Frame(window, bg='#333333')
frame.pack()


def registration():
    username = "Ace"
    password = "pass"
    # if username_entry.get()==username.strip().lower() and password_entry.get()==password.strip().lower():
    #     messagebox.showinfo(title="Access", message=f"Welcome agent {username}")
    # else:
    #     messagebox.showerror(title="ERror", message="No Access Try agaiin")

# Added Widgets
reg_label = tkinter.Label(frame, text="Registration", bg='#333333', fg='#3D5C45', font=("Arial", 30))
name_label = tkinter.Label(frame, text="name", bg='#333333', fg='#ffffff',font=("Arial", 16))
name_entry = tkinter.Entry(frame, font=("Arial", 16),)
email_label = tkinter.Label(frame, text="email", bg='#333333', fg='#ffffff',font=("Arial", 16))
email_entry = tkinter.Entry(frame, font=("Arial", 16),)
phone_label = tkinter.Label(frame, text="phone", bg='#333333', fg='#ffffff',font=("Arial", 16))
phone_entry = tkinter.Entry(frame, font=("Arial", 16),)
comment_label = tkinter.Label(frame, text="comment", bg='#333333', fg='#ffffff',font=("Arial", 16))
comment_entry = tkinter.Text(frame, font=("Arial", 16), height=3)
reg_button = tkinter.Button(frame, text="Register", bg="#3D5C45", fg='#ffffff',font=("Arial", 16) , command=registration)

# Arranegment/ display on screen
reg_label.grid(row=0, column=0, columnspan=2, sticky='news', pady=40)
name_label.grid(row=1, column=0)
name_entry.grid(row=1, column=1, pady=5)
email_label.grid(row=2, column=0)
email_entry.grid(row=2, column=1, pady=5)
phone_label.grid(row=3, column=0)
phone_entry.grid(row=3, column=1, pady=5)
comment_label.grid(row=4, column=0)
comment_entry.grid(row=4, column=1, pady=5,)
reg_button.grid(row=5, column=0, columnspan=2, pady=30)

window.mainloop()