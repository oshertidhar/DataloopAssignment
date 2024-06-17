# server.py (continued)
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
