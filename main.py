'''
Python project by @MudkipzRawsme
Helps automate download process for NexusMods
Before running, run the command below
pip install pyautogui opencv-python pillow
Enjoy!
***remember, using an  autoclicker could get you banned***
'''

import pyautogui
import time
import random
import tkinter as tk
from tkinter import messagebox

# Helper function to test if current_position is within the bounds of button_location
def is_within_bounds(position, region):
    x, y = position
    left, top, width, height = region
    return left <= x <= left + width and top <= y <= top + height

# Main function
def find_and_click():
    while True:
        try:
            # Locating center. Edit confidence as needed
            button_location = pyautogui.locateOnScreen('button.png', confidence=0.9)
            if button_location is not None:
                # Getting center of button
                button_center = pyautogui.center(button_location)
                # This is a just in case they can detect button press location kinda thing
                # Randomizes the location for the mouse
                x_offset = random.randint(-80, 80)
                y_offset = random.randint(-20, 20)
                move_here = (button_center.x + x_offset, button_center.y + y_offset)
                # This is so that the API doesn't catch on
                # Picks a random number between 0.5-1.7 and waits
                time.sleep(random.uniform(0.5, 1.7))
                current_position = pyautogui.position()
                if not is_within_bounds(current_position, button_location):
                    # Going to make it move instead of teleport just in case. Clicks if already within bounds
                    pyautogui.moveTo(move_here, duration=random.uniform(0.4, 1.0))
                # Click
                pyautogui.click()
                # Sleep to make it less suspicious
                time.sleep(1.5)
        except pyautogui.ImageNotFoundException:
            # If the image is not found, print error and retry
            print("Cannot find the image")
            time.sleep(1.5)
        except Exception as e:
            # If anything else fucks over, print error and retry
            print(f"An unexpected error occurred: {e}")
            time.sleep(1.5)


# Dunno why I did this and dont know how it work well. Just felt like it'd be prettier
def show_termination_popup():
    # Create a Tkinter window and hides it
    root = tk.Tk()
    root.withdraw()
    # Shows termination window and closes the hidden root window
    messagebox.showinfo("Autoclicker Termination", "The autoclicker has been terminated.")
    root.destroy()

# Running the project
try:
    # Running the main function
    find_and_click()
except KeyboardInterrupt:
    # Terminates and shows a popup
    show_termination_popup()
