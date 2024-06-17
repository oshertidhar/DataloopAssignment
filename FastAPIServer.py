# server.py
from fastapi import FastAPI, HTTPException
import requests
import asyncio

app = FastAPI()
pong_time_ms = 1000
is_running = False
other_server_url = None

@app.on_event("startup")
async def startup_event():
    global is_running, other_server_url
    is_running = False

@app.get("/ping")
async def ping():
    if not is_running:
        raise HTTPException(status_code=400, detail="Game is not running")
    return "pong"

async def send_ping():
    global is_running
    while is_running:
        try:
            response = requests.get(f"{other_server_url}/ping")
            if response.status_code == 200 and response.text == "pong":
                await asyncio.sleep(pong_time_ms / 1000.0)
        except requests.RequestException as e:
            print(f"Failed to ping: {e}")

def start_game(pong_time, other_url):
    global pong_time_ms, other_server_url, is_running
    pong_time_ms = pong_time
    other_server_url = other_url
    is_running = True
    asyncio.create_task(send_ping())

def pause_game():
    global is_running
    is_running = False

def resume_game():
    global is_running
    is_running = True
    asyncio.create_task(send_ping())

def stop_game():
    global is_running
    is_running = False

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)  # Change port for the second server
