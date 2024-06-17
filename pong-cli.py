import requests
import sys

def start_game(pong_time_ms):
    requests.post(f"http://localhost:8000/start", json={"pong_time_ms": pong_time_ms, "other_server_url": "http://localhost:8001"})
    requests.post(f"http://localhost:8001/start", json={"pong_time_ms": pong_time_ms, "other_server_url": "http://localhost:8000"})
    requests.get(f"http://localhost:8000/ping")

def pause_game():
    requests.post(f"http://localhost:8000/pause")
    requests.post(f"http://localhost:8001/pause")

def resume_game():
    requests.post(f"http://localhost:8000/resume")
    requests.post(f"http://localhost:8001/resume")

def stop_game():
    requests.post(f"http://localhost:8000/stop")
    requests.post(f"http://localhost:8001/stop")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: pong-cli.py <command> <param>")
        sys.exit(1)

    command = sys.argv[1]

    if command == "start" and len(sys.argv) == 3:
        pong_time_ms = int(sys.argv[2])
        start_game(pong_time_ms)
    elif command == "pause":
        pause_game()
    elif command == "resume":
        resume_game()
    elif command == "stop":
        stop_game()
    else:
        print("Unknown command or missing parameter.")
