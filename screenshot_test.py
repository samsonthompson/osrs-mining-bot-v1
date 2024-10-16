import cv2
import numpy as np
from ultralytics import YOLO
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load the YOLO model
logging.info("Loading YOLO model...")
model = YOLO("best.pt")
logging.info("Model loaded successfully")

# Directory containing the screenshots
screenshot_dir = "screenshots"

# List of screenshot files
screenshot_files = [
    "Screenshot 2024-10-16 at 14.33.16.png",
    "Screenshot 2024-10-16 at 14.33.21.png",
    "Screenshot 2024-10-16 at 14.33.25.png",
    "Screenshot 2024-10-16 at 14.33.28.png"
]

def process_screenshot(image_path):
    logging.info(f"Processing {image_path}")
    
    # Read the image
    image = cv2.imread(image_path)
    if image is None:
        logging.error(f"Failed to load image: {image_path}")
        return
    
    # Convert BGR to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Run inference
    results = model(image_rgb, verbose=True)
    
    # Process results
    for result in results:
        for box in result.boxes:
            class_id = int(box.cls.item())
            conf = box.conf.item()
            if model.names[class_id] == "tin rocks":
                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                logging.info(f"Tin rock detected: ({x1}, {y1}, {x2}, {y2}) with confidence {conf:.2f}")
                
                # Draw bounding box on the image
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(image, f"Tin rock: {conf:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    
    # Save the annotated image
    output_path = os.path.join("output", f"annotated_{os.path.basename(image_path)}")
    cv2.imwrite(output_path, image)
    logging.info(f"Annotated screenshot saved as '{output_path}'")

def main():
    # Create output directory if it doesn't exist
    os.makedirs("output", exist_ok=True)
    
    for screenshot in screenshot_files:
        image_path = os.path.join(screenshot_dir, screenshot)
        process_screenshot(image_path)

if __name__ == "__main__":
    main()
