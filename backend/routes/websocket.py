"""WebSocket endpoints for real-time trip updates."""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter(tags=["websocket"])


class ConnectionManager:
    def __init__(self) -> None:
        self.active: dict[int, list[WebSocket]] = {}

    async def connect(self, trip_id: int, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active.setdefault(trip_id, []).append(websocket)

    def disconnect(self, trip_id: int, websocket: WebSocket) -> None:
        connections = self.active.get(trip_id, [])
        if websocket in connections:
            connections.remove(websocket)

    async def broadcast(self, trip_id: int, message: dict) -> None:
        for connection in list(self.active.get(trip_id, [])):
            await connection.send_json(message)


manager = ConnectionManager()


@router.websocket("/ws/trips/{trip_id}")
async def trip_socket(websocket: WebSocket, trip_id: int):
    await manager.connect(trip_id, websocket)
    await manager.broadcast(
        trip_id, {"type": "presence", "message": "A planner joined", "trip_id": trip_id}
    )
    try:
        while True:
            payload = await websocket.receive_json()
            await manager.broadcast(
                trip_id, {"type": "update", "trip_id": trip_id, "payload": payload}
            )
    except WebSocketDisconnect:
        manager.disconnect(trip_id, websocket)
        await manager.broadcast(
            trip_id,
            {"type": "presence", "message": "A planner left", "trip_id": trip_id},
        )
