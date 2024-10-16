import cv2
import torch
from ultralytics import YOLO
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

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
    
    for r in results:
        logging.info(f"Detections: {r.boxes}")
        
except Exception as e:
    logging.error(f"An error occurred: {str(e)}", exc_info=True)
