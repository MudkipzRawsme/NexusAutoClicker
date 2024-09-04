'''
Python project by @MudkipzRawsme
Helps automate download process for NexusMods
Before running, run the command below
pip install pyautogui opencv-python pillow
Enjoy!
***remember, using a autoclicker could get you banned***
'''

import pyautogui
import time
import random
import tkinter as tk
from tkinter import messagebox

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
                # Randomizes the location for the click
                x_offset = random.randint(-10, 10)
                y_offset = random.randint(-5, 5)
                click_here = (button_center.x + x_offset, button_center.y + y_offset)
                # This is so that the API doesn't catch on
                # Picks a random number between 1-3 and waits
                time.sleep(random.uniform(1.0, 3.0))
                # Click the randomized location
                pyautogui.click(click_here)

        except pyautogui.ImageNotFoundException:
            # If the image is not found, print error and retry
            print("Cannot find the image")
            time.sleep(2)
        except Exception as e:
            # If anything else fucks over, print error and retry
            print(f"An unexpected error occurred: {e}")
            time.sleep(2)


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
