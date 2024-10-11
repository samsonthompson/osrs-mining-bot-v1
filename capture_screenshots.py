import pyautogui
import keyboard
import time
import os

def capture_screenshots(interval=10, output_dir='screenshots'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    count = 0
    print("Press 'q' to stop capturing screenshots.")
    while not keyboard.is_pressed('q'):
        screenshot = pyautogui.screenshot()
        screenshot.save(f"{output_dir}/screenshot_{count}.png")
        count += 1
        time.sleep(interval)

if __name__ == "__main__":
    capture_screenshots(interval=10)
