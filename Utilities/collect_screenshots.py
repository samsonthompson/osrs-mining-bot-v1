import pyautogui
import time
import logging
import AppKit
from pynput.mouse import Controller, Button
from pynput.keyboard import Key, Controller as KeyboardController

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(asctime)s - %(message)s')

# Constants
ROTATIONS = 50  # Number of rotations to complete a 360-degree turn
DELAY_BETWEEN_ROTATIONS = 0.5  # Delay in seconds between each rotation
ZOOM_IN_KEY = '['
ZOOM_OUT_KEY = ']'
FULL_ZOOM_IN_TAPS = 16
FULL_ZOOM_OUT_TAPS = 16
ROTATION_TAPS = 3
SCREENSHOT_INTERVAL = 5  # Number of rotations between screenshots

mouse = Controller()
keyboard = KeyboardController()

def focus_runelite_window():
    logging.info("Attempting to focus RuneLite window")
    for app in AppKit.NSWorkspace.sharedWorkspace().runningApplications():
        if app.localizedName() == "RuneLite":
            app.activateWithOptions_(AppKit.NSApplicationActivateIgnoringOtherApps)
            time.sleep(1)  # Wait a bit for the window to come into focus
            logging.info("RuneLite window focused")
            return True
    logging.error("RuneLite window not found")
    return False

def zoom_in_full():
    logging.info("Zooming in fully")
    for _ in range(FULL_ZOOM_IN_TAPS):
        pyautogui.press(ZOOM_IN_KEY)
        time.sleep(0.1)

def rotate_and_capture():
    logging.info("Starting rotation and capture process")
    zoom_in_full()  # Zoom in fully before taking the first screenshot
    pyautogui.screenshot('screenshot_0.png')  # Take the first screenshot after zooming in fully
    logging.info("Taking first screenshot after zooming in fully")
    
    for rotation in range(0, ROTATIONS, ROTATION_TAPS):
        for _ in range(ROTATION_TAPS):
            pyautogui.press('right')  # Rotate clockwise
            time.sleep(DELAY_BETWEEN_ROTATIONS)
        
        if rotation % SCREENSHOT_INTERVAL == 0:
            logging.info(f"Taking screenshot at rotation {rotation}")
            pyautogui.screenshot(f'screenshot_{rotation}.png')
        
        if rotation + ROTATION_TAPS >= ROTATIONS:
            break

def main():
    logging.info("Starting camera control and zoom program")
    print("The program will attempt to focus the RuneLite window.")
    print("Please ensure RuneLite is running.")
    time.sleep(3)
    
    if focus_runelite_window():
        rotate_and_capture()
    else:
        print("Failed to focus RuneLite window. Please make sure it's running and try again.")
    
    logging.info("Program completed")

if __name__ == "__main__":
    main()
