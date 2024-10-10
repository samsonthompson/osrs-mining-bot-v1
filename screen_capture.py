import pyautogui
from PIL import Image
import os

def Miner_Image_quick():
    # Get the screen size
    screen_width, screen_height = pyautogui.size()

    print(f"Screen size: {screen_width}x{screen_height}")

    # Ensure the images directory exists
    if not os.path.exists('images'):
        os.makedirs('images')

    # Capture the screen
    try:
        # Capture the entire screen
        im = pyautogui.screenshot()
        
        # Save the image
        im.save('images/miner_img.png')
        print("Screenshot saved as 'images/miner_img.png'")
        
        # Optional: You can crop the image here if needed
        # For example, to crop the top-left quarter of the screen:
        # cropped_im = im.crop((0, 0, screen_width // 2, screen_height // 2))
        # cropped_im.save('images/cropped_miner_img.png')
        
    except Exception as e:
        print(f"Error capturing or saving the image: {e}")

if __name__ == "__main__":
    # Test the screen capture
    Miner_Image_quick()