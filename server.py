from fastapi import FastAPI, HTTPException
import requests
import asyncio
import sys

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
    asyncio.create_task(send_ping())
    return "pong"

async def send_ping():
    await asyncio.sleep(pong_time_ms / 1000)
    try:
        response = requests.get(f"{other_server_url}/ping")
        if response.status_code == 200:
            print("ping")
        else:
            print(f"Bad request: {response.status_code}")
    except requests.RequestException as e:
        print(f"Failed to ping: {e}")

def start_game(pong_time, other_url):
    global pong_time_ms, other_server_url, is_running
    pong_time_ms = pong_time
    other_server_url = other_url
    is_running = True

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


# Extend the FastAPI server to handle game control commands

from fastapi import Body

@app.post("/start")
async def start(pong_time_ms: int = Body(...), other_server_url: str = Body(...)):
    start_game(pong_time_ms, other_server_url)
    return {"status": "started"}

@app.post("/pause")
async def pause():
    pause_game()
    return {"status": "paused"}

@app.post("/resume")
async def resume():
    resume_game()
    return {"status": "resumed"}

@app.post("/stop")
async def stop():
    stop_game()
    return {"status": "stopped"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=int(sys.argv[1]))
