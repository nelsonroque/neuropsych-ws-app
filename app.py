from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.websockets import WebSocketState
from typing import Dict, Set
from collections import defaultdict
from datetime import datetime
import random

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# In-memory state
sessions: Dict[str, Dict[str, WebSocket]] = {}
presence: Dict[str, Set[str]] = {}
user_colors: Dict[str, str] = {}
mouse_data: Dict[str, Dict[str, list]] = defaultdict(lambda: defaultdict(list))  # session -> user -> list of movements

# Color palette for cursors
def get_color_for_user(user_id: str):
    if user_id not in user_colors:
        palette = ['#FF3B30', '#34C759', '#007AFF', '#FF9500', '#AF52DE', '#5AC8FA', '#FFCC00']
        user_colors[user_id] = random.choice(palette)
    return user_colors[user_id]

@app.get("/canvas/{session_code}/{role}/{user_id}", response_class=HTMLResponse)
async def canvas_page(request: Request, session_code: str, role: str, user_id: str):
    return templates.TemplateResponse("canvas.html", {
        "request": request,
        "session_code": session_code,
        "role": role,
        "user_id": user_id
    })

@app.websocket("/ws/{session_code}/{role}/{user_id}")
async def websocket_endpoint(websocket: WebSocket, session_code: str, role: str, user_id: str):
    print(f"[CONNECT ATTEMPT] session={session_code}, role={role}, user={user_id}")
    await websocket.accept()
    print(f"[CONNECTED] session={session_code}, user={user_id}")

    sessions.setdefault(session_code, {})[user_id] = websocket
    presence.setdefault(session_code, set()).add(user_id)
    await broadcast_presence(session_code)

    try:
        while True:
            data = await websocket.receive_json()
            msg_type = data.get("type")

            if msg_type == "mousemove":
                mouse_data[session_code][user_id].append({
                    "x": data["x"],
                    "y": data["y"],
                    "image": data.get("image"),
                    "time": datetime.utcnow().isoformat()
                })

            for uid, ws in sessions[session_code].items():
                if uid != user_id and ws.application_state == WebSocketState.CONNECTED:
                    await ws.send_json({
                        "from": user_id,
                        "data": data,
                        "role": role,
                        "color": get_color_for_user(user_id)
                    })

    except WebSocketDisconnect:
        print(f"[DISCONNECTED] session={session_code}, user={user_id}")
        sessions[session_code].pop(user_id, None)
        presence[session_code].discard(user_id)
        if not sessions[session_code]:
            sessions.pop(session_code)
            presence.pop(session_code)
        await broadcast_presence(session_code)


async def broadcast_presence(session_code: str):
    user_list = list(presence.get(session_code, []))
    for ws in sessions.get(session_code, {}).values():
        if ws.application_state == WebSocketState.CONNECTED:
            await ws.send_json({
                "type": "presence_update",
                "users": user_list
            })