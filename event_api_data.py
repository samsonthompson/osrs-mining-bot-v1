from fastapi import FastAPI, Request
from typing import Dict, Any

app = FastAPI()

# In-memory storage for temporary data
player_status_data: Dict[str, Any] = {}
inventory_items_data: Dict[str, Any] = {}
login_state_data: Dict[str, Any] = {}
level_change_data: Dict[str, Any] = {}
quest_change_data: Dict[str, Any] = {}

@app.post("/api/player_status/")
async def player_status(request: Request):
    global player_status_data
    data = await request.json()
    print("Player status data:", data)
    player_status_data = data  # Store the latest player status data
    return {"status": "success", "message": "Player status received"}

@app.post("/api/inventory_items/")
async def inventory_items(request: Request):
    global inventory_items_data
    data = await request.json()
    print("Inventory items data:", data)
    inventory_items_data = data  # Store the latest inventory items data
    return {"status": "success", "message": "Inventory items received"}

@app.post("/api/login_state/")
async def login_state(request: Request):
    global login_state_data
    data = await request.json()
    print("Login state data:", data)
    login_state_data = data  # Store the latest login state data
    return {"status": "success", "message": "Login state received"}

@app.post("/api/level_change/")
async def level_change(request: Request):
    global level_change_data
    data = await request.json()
    print("Level change data:", data)
    level_change_data = data  # Store the latest level change data
    return {"status": "success", "message": "Level change received"}

@app.post("/api/quest_change/")
async def quest_change(request: Request):
    global quest_change_data
    data = await request.json()
    print("Quest change data:", data)
    quest_change_data = data  # Store the latest quest change data
    return {"status": "success", "message": "Quest change received"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=9420)