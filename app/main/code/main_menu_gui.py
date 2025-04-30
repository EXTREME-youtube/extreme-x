# main_menu_gui.py
import tkinter as tk
from tkinter import ttk
import subprocess
import platform
import datetime
import time
import tkinter.messagebox

# --- Cool Colors ---
BACKGROUND_COLOR = "#34495e"
BUTTON_COLOR = "#2ecc71"
BUTTON_HOVER_COLOR = "#27ae60"
TEXT_COLOR = "#ffffff"
ACCENT_COLOR = "#f39c12"

def log_message(message, log_type="INFO"):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("error_log.txt", "a") as log_file:
        log_file.write(f"[{timestamp}] {log_type}: {message}\n")

def launch_application(app_name, script_name):
    print(f"Console: Attempting to launch {app_name}...")
    log_message(f"Launching {app_name} application...", "INFO")
    try:
        if platform.system() == "Windows":
            subprocess.Popen(["python", script_name])
        else:
            subprocess.Popen(["python3", script_name])
        print(f"Console: {app_name} launched (hopefully!).")
        log_message(f"{app_name} application launched successfully.", "INFO")
    except FileNotFoundError as e:
        print(f"Console Error: {script_name} not found!")
        error_message = f"FileNotFoundError: {script_name} not found. Make sure it's in the same directory. Error Details: {e}"
        log_message(error_message, "ERROR")
        tk.messagebox.showerror("Error", f"{app_name} application not found!")
    except Exception as e:
        print(f"Console Error: Failed to launch {app_name}: {e}")
        error_message = f"Error launching {app_name} application: {e}"
        log_message(error_message, "ERROR")
        tk.messagebox.showerror("Error", f"Failed to launch {app_name} application: {e}")

def launch_calculator():
    print("Console: Calculator button clicked.")
    launch_application("calculator", "calculator_gui.py")

def launch_notes():
    print("Console: Notes button clicked.")
    launch_application("notes", "notes_app.py")

def launch_drawing():
    print("Console: Drawing button clicked.")
    launch_application("drawing", "drawing_app.py")

def launch_prank_cli():
    print("Console: Surprise Utility button clicked.")
    print("Console: Error pc info not found")
    time.sleep(2)
    print("Extreme: why did you do it")
    time.sleep(2)
    print("Extreme: just why you have to stop the app now")
    time.sleep(4)
    print("Console: getting pc info.")
    time.sleep(0.1)
    print("Console: getting pc info..")
    time.sleep(0.1)
    print("Console: getting pc info...")
    time.sleep(0.1)
    print("Console: getting pc info.")
    time.sleep(0.1)
    print("Console: getting pc info..")
    time.sleep(0.1)
    print("Console: getting pc info...")
    time.sleep(0.1)
    print("Console: getting pc info.")
    time.sleep(0.1)
    print("Console: pc info")
    time.sleep(2)
    print("Console: found")
    print("Extreme: turn it off")
    time.sleep(1)
    print("Console: Error")
    print("Console: Error")
    print("Console: Error")
    print("Console: Error")
    print("Console: Error")
    print("Console: Error")
    print("Console: Error")
    print("Console: Error")
    print("Console: Error")
    print("Console: Error")
    print("Console: Error")
    print("Console: Error")
    print("Console: Error")
    print("Console: Error")
    print("Console: Error")
    print("Console: Error")
    print("Console: Error")
    print("Console: Error")
    print("Console: Error")
    print("Console: Error")
    print("Console: Error")
    print("Console: Error")
    print("Console: Error")
    print("Console: Error")
    print("Console: Error")
    print("Console: Error")
    print("Console: Error")
    print("Console: Error")
    print("Console: Error")
    print("Console: Error")
    print("Console: Error")
    print("Console: Error")
    print("Console: Error")
    print("Console: Error")
    print("Console: Error")
    print("Console: Error")
    print("Console: Error")
    print("Console: Error")
    print("Console: Error")
    print("Console: Error")
    print("Console: Error")
    print("Console: Error")
    print("Console: Error")
    print("Console: Error")
    print("Console: Error")
    print("Console: Error")
    print("Console: Error")
    print("Console: Error")
    print("Console: Error")
    print("Console: Error")
    print("Console: Error")
    print("Console: Error")
    print("Console: Error")
    print("Console: Error")
    print("Console: Error")
    print("Console: Error")
    print("Console: Error")
    print("Console: Error")
    print("Console: Error")
    print("Console: Error")
    print("Console: Error")
    print("Console: Error")
    print("Console: Error")
    print("Console: Error")
    print("Console: Error")
    print("Console: Error")
    print("Console: Error")
    print("Console: Error")
    print("Console: Error")
    print("Console: Error")
    print("Console: Error")
    print("Console: Error")
    print("Console: Error")
    print("Console: Error")
    print("Console: Error")
    time.sleep(2)
    print("NUKER ON")
    print("Console: Starting the Launcher...")
    time.sleep(2)
    print("Console: Starting the NUKER...")
    time.sleep(2)
    print("Console: RUN")
    
    try:
        script_path = 'NUKER.PY'
        result = subprocess.run(['python', script_path], check=True, capture_output=True, text=True)
        print(f"Script '{script_path}' executed successfully.")
        print("Stdout:", result.stdout)
        print("Stderr:", result.stderr)
        return result.returncode
    except subprocess.CalledProcessError as e:
        print(f"Error running script '{script_path}':")
        print("Stdout:", e.stdout)
        print("Stderr:", e.stderr)
        return e.returncode
    except FileNotFoundError:
        print(f"Error: Script '{script_path}' not found.")
        return 1
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return 1




def main():
    print("Console: Starting the Cool App Launcher...")
    window = tk.Tk()
    try:
        window.title("🚀 Cool App Launcher")
        window.geometry("380x320")
        window.configure(bg=BACKGROUND_COLOR)

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("ButtonFrame.TFrame", background=BACKGROUND_COLOR)
        style.configure("TButton",
                        padding=(20, 12),
                        font=("Segoe UI", 14),
                        background=BUTTON_COLOR,
                        foreground=TEXT_COLOR,
                        relief="flat",
                        borderwidth=0)
        style.map("TButton",
                  background=[('active', BUTTON_HOVER_COLOR), ('!active', BUTTON_COLOR)],
                  foreground=[('active', TEXT_COLOR), ('!active', TEXT_COLOR)],
                  relief=[('active', 'sunken'), ('!active', 'flat')])

        title_label = ttk.Label(window,
                                text="🚀 Application Hub",
                                font=("Segoe UI", 20, "bold"),
                                foreground=ACCENT_COLOR,
                                background=BACKGROUND_COLOR,
                                padding=(20, 20))
        title_label.pack(pady=(0, 15))

        button_frame = ttk.Frame(window, padding=(20, 0), style="ButtonFrame.TFrame")
        button_frame.pack(expand=True, fill='both')

        calc_button = ttk.Button(button_frame, text="🧮 Calculator", command=launch_calculator, style="TButton")
        calc_button.pack(pady=10, fill='x', padx=10)

        notes_button = ttk.Button(button_frame, text="📝 Notes", command=launch_notes, style="TButton")
        notes_button.pack(pady=10, fill='x', padx=10)

        draw_button = ttk.Button(button_frame, text="🎨 Drawing", command=launch_drawing, style="TButton")
        draw_button.pack(pady=10, fill='x', padx=10)

        prank_button = ttk.Button(button_frame, text="😈 Surprise Utility", command=launch_prank_cli, style="TButton")
        prank_button.pack(pady=10, fill='x', padx=10)

    except Exception as e:
        print(f"An error occurred during GUI setup: {e}")
    finally:
        window.mainloop()
        print("Console: Cool App Launcher closed.")

if __name__ == "__main__":
    main()
