import pyautogui
import time
import random
import os
from datetime import datetime

# Constants
SCREENSHOT_DIR = "screenshots"
ZOOM_LEVELS = [0, 25, 50, 75, 100]  # Adjust these values based on RuneScape's zoom levels
CAMERA_ROTATIONS = [0, 45, 90, 135, 180, 225, 270, 315]  # 8 directions

def setup_screenshot_directory():
    if not os.path.exists(SCREENSHOT_DIR):
        os.makedirs(SCREENSHOT_DIR)

def take_screenshot(zoom, rotation):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"screenshot_zoom{zoom}_rot{rotation}_{timestamp}.png"
    filepath = os.path.join(SCREENSHOT_DIR, filename)
    pyautogui.screenshot(filepath)
    print(f"Screenshot saved: {filepath}")

def set_zoom_level(level):
    # Implement zoom control here
    # This might involve pressing a key or clicking a UI element
    print(f"Setting zoom level to {level}")
    # Example: pyautogui.press('up')  # Adjust based on RuneScape's controls

def rotate_camera(angle):
    # Implement camera rotation here
    # This might involve pressing arrow keys or using the mouse
    print(f"Rotating camera to {angle} degrees")
    # Example: pyautogui.keyDown('right')
    # time.sleep(angle / 360 * 2)  # Adjust timing based on rotation speed
    # pyautogui.keyUp('right')

def collect_screenshots():
    setup_screenshot_directory()
    
    for zoom in ZOOM_LEVELS:
        set_zoom_level(zoom)
        for rotation in CAMERA_ROTATIONS:
            rotate_camera(rotation)
            time.sleep(1)  # Wait for camera movement to settle
            take_screenshot(zoom, rotation)
            time.sleep(random.uniform(0.5, 1.5))  # Random delay between screenshots

if __name__ == "__main__":
    print("Starting screenshot collection...")
    time.sleep(5)  # Give user time to switch to RuneScape window
    collect_screenshots()
    print("Screenshot collection complete.")
