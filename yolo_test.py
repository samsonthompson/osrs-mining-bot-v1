import cv2
import numpy as np
import torch
import time
import random
import pyautogui
from mss import mss
import logging
from ultralytics import YOLO
import AppKit
import Quartz
import threading

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Load the YOLO model
logging.info("Loading YOLO model...")
model = YOLO("best.pt")
logging.info("Model loaded successfully")

# Define class names
class_names = ['tin rocks', 'copper rocks']

def print_all_windows():
    apps = AppKit.NSWorkspace.sharedWorkspace().runningApplications()
    for app in apps:
        print(f"Name: {app.localizedName()}, Bundle ID: {app.bundleIdentifier()}")

# Call this function before your main loop
print_all_windows()

# Find RuneLite window
def find_runelite_window():
    logging.info("Searching for RuneLite window...")
    runelite_app = None
    for app in AppKit.NSWorkspace.sharedWorkspace().runningApplications():
        if app.localizedName() == "RuneLite":
            runelite_app = app
            break
    
    if runelite_app:
        windows = Quartz.CGWindowListCopyWindowInfo(Quartz.kCGWindowListOptionOnScreenOnly, Quartz.kCGNullWindowID)
        for window in windows:
            if window.get(Quartz.kCGWindowOwnerName) == "RuneLite":
                bounds = window.get(Quartz.kCGWindowBounds)
                x, y, w, h = bounds["X"], bounds["Y"], bounds["Width"], bounds["Height"]
                logging.info(f"RuneLite window found at: ({x}, {y}, {w}, {h})")
                return (int(x), int(y), int(w), int(h))
    
    logging.warning("RuneLite window not found")
    return None

# Screen capture
def capture_screen(region):
    logging.debug(f"Capturing screen region: {region}")
    screenshot = pyautogui.screenshot(region=region)
    return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

# Object detection
def detect_objects_with_timeout(image, timeout=10):
    logging.debug("Starting object detection")
    result = []
    def detection_thread():
        nonlocal result
        try:
            result = model(image, verbose=False)
        except Exception as e:
            logging.error(f"Error during object detection: {e}")
    
    thread = threading.Thread(target=detection_thread)
    thread.start()
    thread.join(timeout)
    
    if thread.is_alive():
        logging.warning("Object detection timed out")
        return []
    
    logging.debug(f"Object detection completed, found {len(result)} results")
    return result[0].boxes.data.cpu().numpy() if result else []

# Click with randomness
def click():
    pyautogui.click()
    time.sleep(random.uniform(0.1, 0.3))
    logging.info("Clicked")

# Log detections
def log_detections(detections):
    if len(detections) == 0:
        logging.info("No rocks detected in this frame")
    else:
        for x1, y1, x2, y2, conf, cls in detections:
            rock_type = class_names[int(cls)]
            logging.info(f"Detected {rock_type} with confidence {conf:.2f} at position ({x1:.0f}, {y1:.0f})")
        logging.info(f"Total rocks detected: {len(detections)}")

# Main loop
def main():
    runelite_region = find_runelite_window()
    if not runelite_region:
        logging.error("RuneLite window not found. Please open RuneLite and try again.")
        return

    successful_clicks = 0

    while successful_clicks < 3:
        logging.info(f"Starting action {successful_clicks + 1} of 3")
        
        screen = capture_screen(runelite_region)
        logging.debug("Screen captured successfully")
        
        detections = detect_objects_with_timeout(screen)
        
        log_detections(detections)
        
        if len(detections) > 0:
            # Choose a random detection
            detection = random.choice(detections)
            x1, y1, x2, y2, conf, cls = detection
            
            # Calculate click position
            click_x = runelite_region[0] + int((x1 + x2) / 2)
            click_y = runelite_region[1] + int((y1 + y2) / 2)
            
            logging.info(f"Moving to detected object at: ({click_x}, {click_y}) with confidence: {conf:.2f}")
            
            # Move mouse and click
            pyautogui.moveTo(click_x, click_y, duration=0.5)
            pyautogui.click()
            
            successful_clicks += 1
            
            # Wait for a random time between 8 to 14 seconds
            wait_time = random.uniform(8, 14)
            logging.info(f"Waiting for {wait_time:.2f} seconds...")
            time.sleep(wait_time)
        else:
            logging.warning("No objects detected. Waiting 2 seconds before next scan.")
            time.sleep(2)

    logging.info("Program completed 3 actions. Exiting.")

if __name__ == "__main__":
    main()
