import numpy as np
from ultralytics import YOLO
import mss
import pyautogui
import time
import random
import cv2

# Load the YOLO model
model = YOLO("best.pt")

# Define the screen region to capture (full screen)
monitor = {"top": 0, "left": 0, "width": 1280, "height": 832}

# Define the inner boundary (1/8 from each edge)
BOUNDARY_RATIO = 1/8
inner_left = int(monitor["width"] * BOUNDARY_RATIO)
inner_top = int(monitor["height"] * BOUNDARY_RATIO)
inner_right = int(monitor["width"] * (1 - BOUNDARY_RATIO))
inner_bottom = int(monitor["height"] * (1 - BOUNDARY_RATIO))

print(f"Boundary: Left={inner_left}, Top={inner_top}, Right={inner_right}, Bottom={inner_bottom}")

# Lower the confidence threshold
CONFIDENCE_THRESHOLD = 0.3

# Create an instance of mss
with mss.mss() as sct:
    successful_clicks = 0

    while successful_clicks < 5:  # Limit to 5 successful clicks
        # Capture the screen
        screenshot = sct.grab(monitor)
        
        # Convert the screenshot to a numpy array
        image = np.array(screenshot)

        # Convert BGRA to RGB (mss captures in BGRA format)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGRA2RGB)

        # Run inference
        results = model(image_rgb, verbose=True)  # Turn on verbose output

        # Create a copy of the image for annotation
        annotated_image = image_rgb.copy()

        # Process results to find the top 3 confidence tin rocks within the boundary
        tin_rocks = []
        for result in results:
            for box in result.boxes:
                class_id = int(box.cls.item())
                conf = box.conf.item()
                if model.names[class_id] == "tin rocks":
                    x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                    print(f"Detected tin rock: ({x1}, {y1}, {x2}, {y2}) with confidence {conf:.2f}")
                    if conf > CONFIDENCE_THRESHOLD:
                        # Check if the rock is within the inner boundary
                        if inner_left < x1 < x2 < inner_right and inner_top < y1 < y2 < inner_bottom:
                            tin_rocks.append((conf, (x1, y1, x2, y2)))
                            print(f"Rock within boundary: ({x1}, {y1}, {x2}, {y2}) with confidence {conf:.2f}")
                            cv2.rectangle(annotated_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        else:
                            print(f"Rock outside boundary: ({x1}, {y1}, {x2}, {y2}) with confidence {conf:.2f}")
                            cv2.rectangle(annotated_image, (x1, y1), (x2, y2), (0, 0, 255), 2)
        
        # Sort by confidence and take top 3
        tin_rocks.sort(reverse=True, key=lambda x: x[0])
        top_rocks = tin_rocks[:3]

        print(f"Detected {len(tin_rocks)} suitable tin rocks")

        if top_rocks:
            # Choose a random rock from the top 3
            chosen_rock = random.choice(top_rocks)
            conf, (x1, y1, x2, y2) = chosen_rock
            
            # Calculate a random point within the center 50% of the bounding box
            center_x = int(x1 + (x2 - x1) * (0.25 + 0.5 * random.random()))
            center_y = int(y1 + (y2 - y1) * (0.25 + 0.5 * random.random()))

            # Draw the click point on the annotated image
            cv2.circle(annotated_image, (center_x, center_y), 5, (255, 0, 0), -1)

            # Save the annotated screenshot
            cv2.imwrite(f"annotated_screenshot_{successful_clicks}.png", cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR))

            # Calculate screen coordinates
            screen_x = monitor["left"] + center_x
            screen_y = monitor["top"] + center_y

            print(f"Moving to tin rock at: ({screen_x}, {screen_y}) with confidence: {conf:.2f}")

            # Move the mouse to the random point within the tin rock
            pyautogui.moveTo(screen_x, screen_y, duration=0.5)  # Added duration for smoother movement
            
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
            print("No suitable tin rocks detected. Waiting 2 seconds before next scan.")
            cv2.imwrite(f"no_detection_screenshot_{successful_clicks}.png", cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR))
            time.sleep(2)

        # Optional: add a small delay to prevent the loop from running too fast
        time.sleep(0.1)

print("Program ended after 5 successful clicks.")
