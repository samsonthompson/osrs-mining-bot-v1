from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/api/")
async def receive_data(request: Request):
       data = await request.json()
       print("Received data:", data)
       return {"status": "success", "message": "Data received"}

@app.post("/api/player_status/")
async def player_status(request: Request):
       data = await request.json()
       print("Player status data:", data)
       return {"status": "success", "message": "Player status received"}

@app.post("/api/inventory_items/")
async def inventory_items(request: Request):
       data = await request.json()
       print("Inventory items data:", data)
       return {"status": "success", "message": "Inventory items received"}

@app.post("/api/login_state/")
async def login_state(request: Request):
    data = await request.json()
    print("Login state data:", data)
    return {"status": "success", "message": "Login state received"}

@app.post("/api/level_change/")
async def level_change(request: Request):
    data = await request.json()
    print("Level change data:", data)
    return {"status": "success", "message": "Level change received"}

@app.post("/api/quest_change/")
async def quest_change(request: Request):
    data = await request.json()
    print("Quest change data:", data)
    return {"status": "success", "message": "Quest change received"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=9420)