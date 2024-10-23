import os
import cv2
from ultralytics import YOLO
import matplotlib.pyplot as plt
import numpy as np
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
SCREENSHOT_DIR = "screenshots"
OUTPUT_DIR = "analysis_results"
CLASS_NAMES = ['copper rocks', 'tin rocks']

def setup_output_directory():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

def analyze_screenshots():
    model = YOLO("best.pt")
    
    zoom_levels = {}
    rotations = {}
    class_counts = {cls: 0 for cls in CLASS_NAMES}
    confidence_scores = []

    for filename in os.listdir(SCREENSHOT_DIR):
        if filename.endswith(".png"):
            logging.info(f"Analyzing {filename}")
            
            # Extract zoom and rotation from filename
            parts = filename.split('_')
            zoom = int(parts[1][4:])
            rotation = int(parts[2][3:])
            
            # Update zoom and rotation counts
            zoom_levels[zoom] = zoom_levels.get(zoom, 0) + 1
            rotations[rotation] = rotations.get(rotation, 0) + 1
            
            # Perform inference
            image_path = os.path.join(SCREENSHOT_DIR, filename)
            results = model(image_path)
            
            for r in results:
                for box in r.boxes:
                    cls = int(box.cls)
                    conf = float(box.conf)
                    class_counts[CLASS_NAMES[cls]] += 1
                    confidence_scores.append(conf)

    # Generate plots
    plt.figure(figsize=(15, 5))
    
    plt.subplot(131)
    plt.bar(zoom_levels.keys(), zoom_levels.values())
    plt.title("Distribution of Zoom Levels")
    plt.xlabel("Zoom Level")
    plt.ylabel("Count")

    plt.subplot(132)
    plt.bar(rotations.keys(), rotations.values())
    plt.title("Distribution of Camera Rotations")
    plt.xlabel("Rotation Angle")
    plt.ylabel("Count")

    plt.subplot(133)
    plt.bar(class_counts.keys(), class_counts.values())
    plt.title("Distribution of Rock Types")
    plt.xlabel("Rock Type")
    plt.ylabel("Count")

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "analysis_plots.png"))

    # Generate summary report
    with open(os.path.join(OUTPUT_DIR, "analysis_report.txt"), "w") as f:
        f.write("Screenshot Analysis Report\n")
        f.write("==========================\n\n")
        f.write(f"Total screenshots analyzed: {len(os.listdir(SCREENSHOT_DIR))}\n\n")
        f.write("Zoom Level Distribution:\n")
        for zoom, count in zoom_levels.items():
            f.write(f"  Zoom {zoom}: {count}\n")
        f.write("\nCamera Rotation Distribution:\n")
        for rotation, count in rotations.items():
            f.write(f"  Rotation {rotation}: {count}\n")
        f.write("\nRock Type Distribution:\n")
        for cls, count in class_counts.items():
            f.write(f"  {cls}: {count}\n")
        f.write(f"\nAverage Confidence Score: {np.mean(confidence_scores):.2f}\n")

    logging.info("Analysis complete. Results saved in the 'analysis_results' directory.")

if __name__ == "__main__":
    setup_output_directory()
    analyze_screenshots()
