import cv2
import torch
from ultralytics import YOLO
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Define class names
class_names = ['copper rocks', 'tin rocks']

try:
    # Load the YOLO model
    logging.info("Loading YOLO model...")
    model = YOLO("best.pt").to('cpu')
    logging.info("Model loaded successfully")

    # Load the screenshot
    image_path = "Screenshot 2024-10-16 at 14.33.16.png"
    logging.info(f"Loading image from: {image_path}")
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Failed to load image: {image_path}")
    
    # Run inference
    logging.info("Running inference...")
    results = model(image, verbose=True)
    
    logging.info(f"Inference complete. Detections: {len(results[0])}")
    
    # Draw bounding boxes on the image
    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            conf = box.conf[0]
            cls = int(box.cls[0])
            
            # Convert tensor values to integers
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            
            # Draw rectangle
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            # Add label
            label = f"{class_names[cls]} {conf:.2f}"
            cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    
    # Save the annotated image
    output_path = "annotated_screenshot.png"
    cv2.imwrite(output_path, image)
    logging.info(f"Annotated image saved as '{output_path}'")
    
    # Log detections
    for r in results:
        logging.info(f"Detections: {r.boxes}")
        
except Exception as e:
    logging.error(f"An error occurred: {str(e)}", exc_info=True)
