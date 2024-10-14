import cv2
import numpy as np
from ultralytics import YOLO
import mss

# Load the YOLO model
model = YOLO("best.pt")

# Define the screen region to capture (adjust these values to match the RuneLite window)
monitor = {"top": 0, "left": 0, "width": 1280, "height": 832}

# Create an instance of mss
with mss.mss() as sct:
    while True:
        # Capture the screen
        screenshot = sct.grab(monitor)
        
        # Convert the screenshot to a numpy array
        image = np.array(screenshot)

        # Convert the image from BGRA to BGR
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)

        # Run inference
        results = model(image)

        # Process results
        for result in results:
            # Plot the results on the image
            annotated_image = result.plot()

            # Display the image
            cv2.imshow("YOLO Results", annotated_image)

            # Print detection information
            for box in result.boxes:
                class_id = box.cls.item()
                conf = box.conf.item()
                print(f"Detected class: {model.names[int(class_id)]}, Confidence: {conf:.2f}")

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
