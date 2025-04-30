import tkinter as tk
from tkinter import ttk, messagebox
import datetime

# --- Global Styling Variables ---
BACKGROUND_COLOR = "#111827"
BUTTON_BG = "#374151"
BUTTON_FG = "#F9FAFB"
OPERATOR_BG = "#EF4444"
OPERATOR_ACTIVE_BG = "#DC2626"
EQUAL_BG = "#10B981"
EQUAL_ACTIVE_BG = "#059669"
CLEAR_BG = "#FCD34D"
CLEAR_ACTIVE_BG = "#F87171"
BACKSPACE_BG = "#8B5CF6"
BACKSPACE_ACTIVE_BG = "#6D28D9"
ENTRY_BG = "#1F2937"
ENTRY_FG = "#FFFFFF"
FONT_NORMAL = ("Inter", 16)
BUTTON_ACTIVE_BG = "#D1D5DB"
BUTTON_ACTIVE_FG = "#FFFFFF"

# --- Logging Function ---
def log_error(error_message):
    """Logs an error message with a timestamp to error_log.txt."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("error_log.txt", "a") as log_file:
        log_file.write(f"[{timestamp}] Error: {error_message}\n")

# --- Calculator Logic ---
def button_click(number):
    entry.insert(tk.END, str(number))

def button_clear():
    entry.delete(0, tk.END)

def button_operation(operator):
    global first_number, math_operation
    math_operation = operator
    first_number = entry.get()
    entry.delete(0, tk.END)

def button_equal():
    try:
        num1 = float(first_number)
        num2 = float(entry.get())
        result = {
            "+": num1 + num2,
            "-": num1 - num2,
            "*": num1 * num2,
            "/": "Error!" if num2 == 0 else num1 / num2,
            "**": num1 ** num2
        }[math_operation]
        entry.delete(0, tk.END)
        entry.insert(tk.END, str(result))
    except Exception as e:
        log_error(f"Error in calculation: {e}")
        entry.delete(0, tk.END)
        entry.insert(tk.END, "Error")

def button_backspace():
    entry.delete(len(entry.get())-1, tk.END)

# --- GUI Creation ---
def main():
    global entry
    window = tk.Tk()
    window.title("Calculator X")
    window.configure(bg=BACKGROUND_COLOR)
    window.geometry("280x380")  # Reduced size for a compact layout

    # **Remove default Tkinter window icon**
    window.iconbitmap("calculator.ico")  

    # Apply Modern Theme
    style = ttk.Style()
    style.configure("TButton", font=FONT_NORMAL, padding=10, relief="flat")
    style.map("TButton",
              background=[("active", OPERATOR_ACTIVE_BG)],
              foreground=[("active", BUTTON_FG)])

    # Entry field
    entry = ttk.Entry(window, font=("Inter", 20), justify="right")
    entry.grid(row=0, column=0, columnspan=4, padx=15, pady=15)

    # Buttons with hover effects
    buttons_data = [
        ("7", BUTTON_BG), ("8", BUTTON_BG), ("9", OPERATOR_BG), ("/", OPERATOR_BG),
        ("4", BUTTON_BG), ("5", BUTTON_BG), ("6", OPERATOR_BG), ("*", OPERATOR_BG),
        ("1", BUTTON_BG), ("2", BUTTON_BG), ("3", OPERATOR_BG), ("-", OPERATOR_BG),
        ("0", BUTTON_BG), (".", BUTTON_BG), ("**", OPERATOR_BG), ("+", OPERATOR_BG)
    ]

    row_val, col_val = 1, 0
    global buttons
    buttons = {}

    for text, bg_color in buttons_data:
        button = tk.Button(window, text=text, padx=20, pady=15, 
                           font=(FONT_NORMAL[0], 18), bg=bg_color, fg=BUTTON_FG,
                           activebackground=OPERATOR_ACTIVE_BG if bg_color in [OPERATOR_BG, EQUAL_BG, CLEAR_BG, BACKSPACE_BG] else BUTTON_ACTIVE_BG,
                           activeforeground=BUTTON_ACTIVE_FG,
                           relief="flat",
                           command=lambda b=text: on_click(b))
        buttons[text] = button
        buttons[text].grid(row=row_val, column=col_val, padx=6, pady=6)
        col_val += 1
        if col_val > 3:
            col_val = 0
            row_val += 1

    # Special Buttons
    buttons["C"] = tk.Button(window, text="C", padx=20, pady=15, font=(FONT_NORMAL[0], 18),
                             bg=CLEAR_BG, fg=BUTTON_FG, activebackground=CLEAR_ACTIVE_BG, activeforeground=BUTTON_ACTIVE_FG,
                             relief="flat",
                             command=lambda: on_click("C"))
    buttons["C"].grid(row=row_val, column=col_val, padx=6, pady=6)

    buttons["<-"] = tk.Button(window, text="<-", padx=20, pady=15, font=(FONT_NORMAL[0], 18),
                              bg=BACKSPACE_BG, fg=BUTTON_FG, activebackground=BACKSPACE_ACTIVE_BG, activeforeground=BUTTON_ACTIVE_FG,
                              relief="flat",
                              command=lambda: on_click("<-"))
    buttons["<-"].grid(row=row_val + 1, column=0, padx=6, pady=6)

    buttons["="] = tk.Button(window, text="=", padx=20, pady=15, font=(FONT_NORMAL[0], 18),
                             bg=EQUAL_BG, fg=BUTTON_FG, activebackground=EQUAL_ACTIVE_BG, activeforeground=BUTTON_ACTIVE_FG,
                             relief="flat",
                             command=lambda: on_click("="))
    buttons["="].grid(row=row_val + 1, column=1, columnspan=3, padx=6, pady=6)

    window.mainloop()

# --- Button Click Handler ---
def on_click(button_text):
    """Handles button clicks with animation."""
    button = buttons.get(button_text)
    if button:
        original_bg, original_fg = button["bg"], button["fg"]

        button.config(bg=OPERATOR_ACTIVE_BG if original_bg in [OPERATOR_BG, EQUAL_BG, CLEAR_BG, BACKSPACE_BG] else BUTTON_ACTIVE_BG, fg=BUTTON_ACTIVE_FG)
        button.after(150, lambda: button.config(bg=original_bg, fg=original_fg))

        if button_text.isdigit() or button_text == ".":
            button_click(button_text)
        elif button_text in ["+", "-", "*", "/", "**"]:
            button_operation(button_text)
        elif button_text == "=":
            button_equal()
        elif button_text == "C":
            button_clear()
        elif button_text == "<-":
            button_backspace()

if __name__ == "__main__":
    main()
