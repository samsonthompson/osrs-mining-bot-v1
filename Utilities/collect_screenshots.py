import pyautogui
import time
import logging
import AppKit
from pynput.mouse import Controller, Button
from pynput.keyboard import Key, Controller as KeyboardController

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
ROTATIONS = 50  # Number of rotations to complete a 360-degree turn
DELAY_BETWEEN_ROTATIONS = 0.5  # Delay in seconds between each rotation
ZOOM_LEVELS = 5  # Number of zoom levels
ZOOM_DELAY = 0.5  # Delay between zoom actions

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

def rotate_camera_clockwise():
    logging.info("Starting camera rotation")
    for i in range(ROTATIONS):
        pyautogui.press('right')
        logging.info(f"Rotation {i+1}/{ROTATIONS} completed")
        time.sleep(DELAY_BETWEEN_ROTATIONS)
    logging.info("Camera rotation complete")

def zoom_in():
    logging.info("Zooming in")
    mouse.press(Button.left)
    mouse.move(0, -10)  # Adjust this value to change zoom speed
    mouse.release(Button.left)
    time.sleep(ZOOM_DELAY)

def zoom_out():
    logging.info("Zooming out")
    mouse.press(Button.left)
    mouse.move(0, 10)  # Adjust this value to change zoom speed
    mouse.release(Button.left)
    time.sleep(ZOOM_DELAY)

def perform_zoom_cycle():
    logging.info("Starting zoom cycle")
    for _ in range(ZOOM_LEVELS):
        zoom_in()
    for _ in range(ZOOM_LEVELS):
        zoom_out()
    logging.info("Zoom cycle complete")

def main():
    logging.info("Starting camera control and zoom program")
    print("The program will attempt to focus the RuneLite window.")
    print("Please ensure RuneLite is running.")
    time.sleep(3)
    
    if focus_runelite_window():
        perform_zoom_cycle()
        rotate_camera_clockwise()
    else:
        print("Failed to focus RuneLite window. Please make sure it's running and try again.")
    
    logging.info("Program completed")

if __name__ == "__main__":
    main()
