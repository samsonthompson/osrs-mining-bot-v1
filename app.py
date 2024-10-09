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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=9420)