import cv2
import numpy as np
from ultralytics import YOLO

# Load the YOLO model
model = YOLO("best.pt")

# Load the screenshot
image_path = "screenshot.png"  # Make sure this matches your screenshot filename
image = cv2.imread(image_path)

# Convert BGR to RGB (cv2 loads images in BGR format)
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Run inference
results = model(image_rgb, verbose=True)  # Set verbose to True for detailed output

# Process results
for result in results:
    for box in result.boxes:
        class_id = int(box.cls.item())
        conf = box.conf.item()
        if model.names[class_id] == "tin rocks":
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            print(f"Tin rock detected: ({x1}, {y1}, {x2}, {y2}) with confidence {conf:.2f}")
            
            # Draw bounding box on the image
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(image, f"Tin rock: {conf:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

# Save the annotated image
cv2.imwrite("annotated_screenshot.png", image)

print("Annotated screenshot saved as 'annotated_screenshot.png'")
