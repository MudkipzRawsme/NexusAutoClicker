'''
Python project by @MudkipzRawsme
Helps automate download process for NexusMods
Updated: Select Region + Move Away Logic
Before running, run the command below:
pip install pyautogui opencv-python pillow
***remember, using an autoclicker could get you banned***
'''

import pyautogui
import time
import random
import tkinter as tk
from tkinter import messagebox
from threading import Thread, Event
import os

# --- Global Variables ---
stop_event = Event()

# --- Helper Functions ---

def is_within_bounds(position, region):
    x, y = position
    left, top, width, height = region
    return left <= x <= left + width and top <= y <= top + height

def capture_screen_region(root_window):
    """
    Creates a semi-transparent overlay to let the user drag-select a region.
    """
    
    # Create a full-screen top-level window
    top = tk.Toplevel(root_window)
    top.attributes('-fullscreen', True)
    top.attributes('-alpha', 0.3)  # Transparency (0.3 = 30% visible)
    top.config(cursor="cross")

    # Canvas for drawing the selection rectangle
    canvas = tk.Canvas(top, bg="black", highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    # Variables to store coordinates
    start_x, start_y = 0, 0
    rect_id = None

    def on_mouse_down(event):
        nonlocal start_x, start_y, rect_id
        start_x, start_y = event.x, event.y
        # Create the rectangle
        rect_id = canvas.create_rectangle(start_x, start_y, start_x, start_y, outline='red', width=2)

    def on_mouse_drag(event):
        nonlocal rect_id
        # Update rectangle size as mouse moves
        canvas.coords(rect_id, start_x, start_y, event.x, event.y)

    def on_mouse_up(event):
        nonlocal start_x, start_y
        end_x, end_y = event.x, event.y
        
        # Calculate correct coordinates (handling drag in any direction)
        x = min(start_x, end_x)
        y = min(start_y, end_y)
        width = abs(end_x - start_x)
        height = abs(end_y - start_y)

        # Destroy overlay immediately so it doesn't appear in the screenshot
        top.destroy()
        
        # Slight delay to ensure overlay is fully gone
        root_window.update() 
        time.sleep(0.2)

        if width > 5 and height > 5:
            try:
                # Capture and save
                pyautogui.screenshot('button.png', region=(x, y, width, height))
                messagebox.showinfo("Success", "Button image saved as 'button.png'.\nYou can now press Start.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {e}")
        else:
            messagebox.showwarning("Warning", "Selection too small. Please try again.")

    # Bind events
    canvas.bind('<ButtonPress-1>', on_mouse_down)
    canvas.bind('<B1-Motion>', on_mouse_drag)
    canvas.bind('<ButtonRelease-1>', on_mouse_up)
    
    # Allow exit with Escape key
    top.bind('<Escape>', lambda e: top.destroy())

# --- Main Logic ---

def find_and_click():
    if not os.path.exists('button.png'):
        print("Error: button.png not found.")
        return

    # Get screen size once to ensure we don't move mouse off-screen later
    screen_w, screen_h = pyautogui.size()

    while not stop_event.is_set():
        try:
            # Locating button. grayscale=True is faster and often more accurate for UI elements
            button_location = pyautogui.locateOnScreen('button.png', confidence=0.8, grayscale=True)
            
            if button_location is not None:
                # --- 1. Calculate safe click spot ---
                w, h = button_location.width, button_location.height
                safe_x = int(w * 0.4) 
                safe_y = int(h * 0.4) 
                
                x_offset = random.randint(-safe_x, safe_x)
                y_offset = random.randint(-safe_y, safe_y)
                
                button_center = pyautogui.center(button_location)
                click_target = (button_center.x + x_offset, button_center.y + y_offset)

                # Anti-bot sleep before clicking
                time.sleep(random.uniform(0.5, 1.7))

                current_position = pyautogui.position()
                
                # Check bounds
                if not is_within_bounds(current_position, button_location):
                    pyautogui.moveTo(click_target, duration=random.uniform(0.4, 1.0))
                
                # Click
                pyautogui.click()
                print("Clicked button.")
                
                # --- 2. NEW: Move mouse AWAY to reset hover state ---
                # We pick a random direction and move 200-400 pixels away
                # This ensures the button stops glowing so we can find it again next time
                
                away_dist_x = random.randint(200, 400) * random.choice([-1, 1])
                away_dist_y = random.randint(200, 400) * random.choice([-1, 1])
                
                curr_x, curr_y = pyautogui.position()
                
                # Math to keep the mouse inside the screen (prevent crash)
                target_x = max(0, min(screen_w, curr_x + away_dist_x))
                target_y = max(0, min(screen_h, curr_y + away_dist_y))
                
                # Move away smoothly
                pyautogui.moveTo(target_x, target_y, duration=random.uniform(0.3, 0.7))

                # Wait after to make it less suspicious
                time.sleep(1.5)
            else:
                # Image not found this loop
                pass
                
        except pyautogui.ImageNotFoundException:
            # Expected if button isn't on screen yet
            time.sleep(1)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            time.sleep(1.5)

# --- GUI Logic ---

def show_termination_popup():
    messagebox.showinfo("Autoclicker Termination", "The autoclicker has been stopped.")

def start_autoclicker():
    if not os.path.exists('button.png'):
        messagebox.showerror("Error", "No 'button.png' found.\nPlease use 'Select Region' first.")
        return
        
    stop_event.clear()
    autoclicker_thread = Thread(target=find_and_click)
    autoclicker_thread.daemon = True # Kills thread if main app closes
    autoclicker_thread.start()
    print("Started")

def stop_autoclicker():
    stop_event.set()
    show_termination_popup()
    print("Stopped")

# --- GUI Setup ---
root = tk.Tk()
root.title("NexusMods Autoclicker")
root.geometry("300x200")

# Instruction Label
lbl_instr = tk.Label(root, text="1. Select the button region\n2. Press Start")
lbl_instr.pack(pady=5)

# Select Region Button
select_btn = tk.Button(root, text="Select Button Region", command=lambda: capture_screen_region(root), bg="#dddddd")
select_btn.pack(pady=5)

# Start Button
start_button = tk.Button(root, text="Start", width=15, command=lambda: [start_autoclicker(), start_button.config(state=tk.DISABLED), stop_button.config(state=tk.NORMAL), select_btn.config(state=tk.DISABLED)], bg="#90ee90")
start_button.pack(pady=5)

# Stop Button
stop_button = tk.Button(root, text="Stop", width=15, command=lambda: [stop_autoclicker(), start_button.config(state=tk.NORMAL), stop_button.config(state=tk.DISABLED), select_btn.config(state=tk.NORMAL)], bg="#ffcccb")
stop_button.pack(pady=5)
stop_button.config(state=tk.DISABLED)

root.mainloop()