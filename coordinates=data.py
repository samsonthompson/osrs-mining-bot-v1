from fastapi import FastAPI, Request
from typing import Dict, Any, List, Tuple
import pyautogui
import time
import random
import math

app = FastAPI()

# In-memory storage for temporary data
player_status_data: Dict[str, Any] = {}
last_position: Dict[str, int] = {}

# Constants for coordinate translation
PIXELS_PER_TILE = 4  # You might need to adjust this based on your game's zoom level

# Screen center coordinates (adjusted for 1280x832 resolution)
SCREEN_CENTER_X = 640  # Half of 1280
SCREEN_CENTER_Y = 416  # Half of 832

# Define absolute rock locations
ROCK_LOCATIONS: List[Tuple[int, int]] = [
    (3223, 3148),  # One tile north of the reference point
    (3222, 3147),  # One tile west of the reference point
    (3223, 3146),  # One tile south of the reference point
]

def game_to_screen(player_x: int, player_y: int, target_x: int, target_y: int) -> tuple:
    """Convert game coordinates to screen coordinates relative to player position."""
    dx = target_x - player_x
    dy = player_y - target_y  # Invert y-axis because screen coordinates increase downwards
    screen_x = SCREEN_CENTER_X + (dx * PIXELS_PER_TILE)
    screen_y = SCREEN_CENTER_Y + (dy * PIXELS_PER_TILE)
    return (int(screen_x), int(screen_y))

def bezier_curve(start, end, control1, control2, t):
    """Calculate point on a Bézier curve at parameter t."""
    x = (1-t)**3 * start[0] + 3*(1-t)**2 * t * control1[0] + 3*(1-t) * t**2 * control2[0] + t**3 * end[0]
    y = (1-t)**3 * start[1] + 3*(1-t)**2 * t * control1[1] + 3*(1-t) * t**2 * control2[1] + t**3 * end[1]
    return (int(x), int(y))

def human_like_mouse_move(start_x, start_y, end_x, end_y, duration=1):
    """Move the mouse in a human-like manner using a Bézier curve."""
    start = (start_x, start_y)
    end = (end_x, end_y)
    
    # Generate two random control points
    control1 = (random.randint(min(start_x, end_x), max(start_x, end_x)),
                random.randint(min(start_y, end_y), max(start_y, end_y)))
    control2 = (random.randint(min(start_x, end_x), max(start_x, end_x)),
                random.randint(min(start_y, end_y), max(start_y, end_y)))
    
    steps = int(duration * 60)  # 60 movements per second
    for i in range(steps):
        t = i / steps
        x, y = bezier_curve(start, end, control1, control2, t)
        pyautogui.moveTo(x, y)
        time.sleep(duration / steps)

def click_at_game_coords(player_x: int, player_y: int, target_x: int, target_y: int):
    """Move mouse to game coordinates relative to player position and click."""
    start_x, start_y = pyautogui.position()
    screen_x, screen_y = game_to_screen(player_x, player_y, target_x, target_y)
    
    # Use human-like mouse movement
    human_like_mouse_move(start_x, start_y, screen_x, screen_y, duration=random.uniform(0.5, 1.5))
    
    # Add a small random delay before clicking
    time.sleep(random.uniform(0.1, 0.3))
    
    # Click with a random duration
    pyautogui.click(duration=random.uniform(0.05, 0.15))

def interpret_movement(current: Dict[str, int], last: Dict[str, int]) -> str:
    dx = current['x'] - last['x']
    dy = current['y'] - last['y']
    
    movement = []
    if dx > 0:
        movement.append(f"{abs(dx)} step(s) east")
    elif dx < 0:
        movement.append(f"{abs(dx)} step(s) west")
    
    if dy > 0:
        movement.append(f"{abs(dy)} step(s) north")
    elif dy < 0:
        movement.append(f"{abs(dy)} step(s) south")
    
    return " and ".join(movement) if movement else "No movement"

@app.post("/api/player_status/")
async def player_status(request: Request):
    global player_status_data, last_position
    data = await request.json()
    world_point = data.get('data', {}).get('worldPoint', {})
    
    movement = "Initial position"
    if last_position:
        movement = interpret_movement(world_point, last_position)
    
    print(f"Player location: {world_point}")
    print(f"Movement: {movement}")
    
    last_position = world_point
    player_status_data = data
    return {"status": "success", "message": "Player status received"}

def mine_random_rock():
    """Function to initiate mining at a random rock location."""
    if last_position:
        target_rock = random.choice(ROCK_LOCATIONS)
        click_at_game_coords(last_position['x'], last_position['y'], target_rock[0], target_rock[1])
        print(f"Clicked at rock coordinates ({target_rock[0]}, {target_rock[1]}) relative to player position ({last_position['x']}, {last_position['y']})")
    else:
        print("Error: Player position unknown")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=9420)
