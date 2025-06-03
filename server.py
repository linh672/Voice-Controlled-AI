from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
import asyncio

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

connected_clients = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    try:
        while True:
            # keep connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        connected_clients.remove(websocket)

async def send_pulse_event():
    # Broadcast 'pulse' message to all connected clients
    for client in connected_clients:
        try:
            await client.send_text("pulse")
        except:
            connected_clients.remove(client)
