import cv2 as cv
import numpy as np
import os

# Change the working directory to the folder this script is in.
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Load the haystack and needle images
haystack_img = cv.imread('mining-area.png', cv.IMREAD_UNCHANGED)  # Update with your haystack image
needle_img = cv.imread('ore.png', cv.IMREAD_UNCHANGED)  # Update with your needle image

if haystack_img is None:
    print("Error: Could not load haystack image.")
if needle_img is None:
    print("Error: Could not load needle image.")

# Perform template matching
result = cv.matchTemplate(haystack_img, needle_img, cv.TM_CCOEFF_NORMED)

# Get the best match position from the match result
min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
print('Best match top left position: %s' % str(max_loc))
print('Best match confidence: %s' % max_val)

# Set a threshold for a good match
threshold = 0.8
if max_val >= threshold:
    print('Found ore.')

    # Get the size of the needle image
    needle_w = needle_img.shape[1]
    needle_h = needle_img.shape[0]

    # Calculate the bottom right corner of the rectangle to draw
    top_left = max_loc
    bottom_right = (top_left[0] + needle_w, top_left[1] + needle_h)

    # Draw a rectangle on the haystack image
    cv.rectangle(haystack_img, top_left, bottom_right, color=(0, 255, 0), thickness=2, lineType=cv.LINE_4)

    # Save the result image
    cv.imwrite('ore_detection_result.jpg', haystack_img)
else:
    print('Ore not found.')






