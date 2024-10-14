import numpy as np
from ultralytics import YOLO
import mss
import pyautogui
import time
import random
import cv2

# Load the YOLO model
model = YOLO("best.pt")

# Define the screen region to capture (adjust these values to match the RuneLite window)
monitor = {"top": 0, "left": 0, "width": 1280, "height": 832}

# Create an instance of mss
with mss.mss() as sct:
    successful_clicks = 0

    while successful_clicks < 5:  # Limit to 5 successful clicks
        # Capture the screen
        screenshot = sct.grab(monitor)
        
        # Convert the screenshot to a numpy array
        image = np.array(screenshot)

        # Convert RGBA to RGB
        image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)

        # Run inference
        results = model(image, verbose=False)  # Turn off verbose output

        best_tin_rock = None
        highest_conf = 0

        # Process results to find the highest confidence tin rock
        for result in results:
            for box in result.boxes:
                class_id = int(box.cls.item())
                conf = box.conf.item()
                if model.names[class_id] == "tin rocks" and conf > highest_conf:
                    x1, y1, x2, y2 = box.xyxy[0].tolist()
                    best_tin_rock = (x1, y1, x2, y2)
                    highest_conf = conf

        if best_tin_rock:
            x1, y1, x2, y2 = best_tin_rock
            
            # Calculate a random point within the center 50% of the bounding box
            center_x = int(x1 + (x2 - x1) * (0.25 + 0.5 * random.random()))
            center_y = int(y1 + (y2 - y1) * (0.25 + 0.5 * random.random()))

            screen_x = monitor["left"] + center_x
            screen_y = monitor["top"] + center_y

            print(f"Moving to tin rock at: ({screen_x}, {screen_y}) with confidence: {highest_conf:.2f}")

            # Move the mouse to the random point within the tin rock
            pyautogui.moveTo(screen_x, screen_y)
            
            # Short pause before clicking
            time.sleep(random.uniform(0.1, 0.3))
            
            # Click the tin rock
            pyautogui.click()

            successful_clicks += 1
            print(f"Successful clicks: {successful_clicks}")

            # Wait for a random time between 8 to 14 seconds
            wait_time = random.uniform(8, 14)
            print(f"Waiting for {wait_time:.2f} seconds...")
            time.sleep(wait_time)

        else:
            print("No tin rocks detected. Waiting 2 seconds before next scan.")
            time.sleep(2)

        # Optional: add a small delay to prevent the loop from running too fast
        time.sleep(0.1)

print("Program ended after 5 successful clicks.")
