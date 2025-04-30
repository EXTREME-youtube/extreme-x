import tkinter as tk
from tkinter import messagebox

def show_messageboxes():
    root = tk.Tk()
    root.withdraw()

    messagebox.showinfo("Message 1", "This is the first message.")
    messagebox.showinfo("Message 2", "This is the second message.")

    root.destroy()

if __name__ == "__main__":
    show_messageboxes()
