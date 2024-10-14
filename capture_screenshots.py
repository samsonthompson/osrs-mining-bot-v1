import time
import pyscreenshot as ImageGrab

def capture_screenshots(interval):
    while True:
        # Capture the entire screen
        screenshot = ImageGrab.grab()
        
        # Save the screenshot
        screenshot.save(f"screenshot_{int(time.time())}.png")
        print(f"Screenshot saved at {time.ctime()}")
        
        time.sleep(interval)

# Example usage
capture_screenshots(interval=10)
