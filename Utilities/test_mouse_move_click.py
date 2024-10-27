import pyautogui
import random
import time

# Set the screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 832

# Disable pyautogui's fail-safe feature
pyautogui.FAILSAFE = False

# Function to move mouse to a random position and click
def random_move_and_click():
    x = random.randint(0, SCREEN_WIDTH)
    y = random.randint(0, SCREEN_HEIGHT)
    print(f"Moving to ({x}, {y})")
    pyautogui.moveTo(x, y, duration=2)  # Slow down the movement to 2 seconds
    print("Clicking!")
    pyautogui.click()
    print("Clicked!")
    current_pos = pyautogui.position()
    print(f"Current position after click: {current_pos}")

# Main loop
start_time = time.time()
duration = 30  # Run for 30 seconds

print("Starting mouse movement and click test...")
print("Press Ctrl+C to stop the script early.")

try:
    while time.time() - start_time < duration:
        random_move_and_click()
        time.sleep(3)  # Wait 3 seconds between actions

except KeyboardInterrupt:
    print("\nScript stopped by user.")

print("Test completed.")
