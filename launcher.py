
import tkinter as tk
from tkinter import messagebox
import subprocess
import sys

# Function to display info
def show_info():
    info_window = tk.Toplevel(root)
    info_window.title("How to Use the Whiteboard")
    info_window.geometry("500x400")  # Set a larger size for the info window
    info_window.configure(bg="#FFE5B4")  # Background color for the info window

    info_label = tk.Label(
        info_window,
        text="1. Use your hand to draw on the whiteboard.\n"
             "2. Select colors using the colored buttons at the top.\n"
             "3. Use 'CLEAR' to erase the board.\n"
             "4. Press 'q' to quit the application.\n"
             "\n"
             "Enjoy your whiteboard app!",
        font=("Arial", 14),
        bg="#FFE5B4",
        justify="left",
        wraplength=480  # Ensures text wraps properly within the window
    )
    info_label.pack(pady=20)

    ok_button = tk.Button(info_window, text="OK", command=info_window.destroy)
    ok_button.pack(pady=10)

# Function to start the whiteboard application
def start_whiteboard():
    try:
        # Open the whiteboard application in a non-blocking manner
        subprocess.Popen([sys.executable, "whiteboard.py"])
    except Exception as e:
        messagebox.showerror("Error", f"Failed to start whiteboard: {e}")

# Function to show developers information
def show_developers():
    developers_window = tk.Toplevel(root)
    developers_window.title("Developer")
    developers_window.geometry("500x400")  # Set a larger size for the developers window
    developers_window.configure(bg="#FFE5B4")  # Background color for the developers window

    # Developer names with IDs in the same format as required
    developers_info = (
        "Suryansh Singh Kushwah                        EN21CS301779\n"
    )

    developers_label = tk.Label(
        developers_window,
        text="Developers:\n\n" + developers_info,
        font=("Arial", 14),
        bg="#FFE5B4",
        justify="left",
        anchor="w"
    )
    developers_label.pack(pady=20)

    ok_button = tk.Button(developers_window, text="OK", command=developers_window.destroy)
    ok_button.pack(pady=10)

# Function to handle the "X" button close event
def on_close():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()

# Initialize the Tkinter GUI
root = tk.Tk()
root.title("Whiteboard Application")
root.geometry("600x400")
root.configure(bg="#FFE5B4")  # Background color for the launcher window

# Set the custom close button handler
root.protocol("WM_DELETE_WINDOW", on_close)

# Add a title label
title_label = tk.Label(
    root, text="Welcome to Our Whiteboard App", font=("Arial", 20, "bold"), bg="#FFE5B4"
)
title_label.pack(pady=20)

# Add buttons
btn_frame = tk.Frame(root, bg="#FFE5B4")
btn_frame.pack(pady=20)

# Start Button
start_button = tk.Button(
    btn_frame,
    text="START",
    font=("Arial", 16),
    command=start_whiteboard,
    bg="lightgreen",
    width=20
)
start_button.grid(row=0, column=0, padx=10, pady=10)

# Info Button
info_button = tk.Button(
    btn_frame, text="INFO", font=("Arial", 16), command=show_info, bg="lightblue", width=20
)
info_button.grid(row=1, column=0, padx=10, pady=10)

# Developers Button
developers_button = tk.Button(
    btn_frame,
    text="DEVELOPERS",
    font=("Arial", 16),
    command=show_developers,
    bg="lightyellow",








    width=20
)
developers_button.grid(row=2, column=0, padx=10, pady=10)

# Run the GUI event loop
root.mainloop()
