from __future__ import annotations

import asyncio
import json
import logging
from collections import defaultdict
from fastapi import WebSocket

from app.realtime.schemas import ServerMessage

logger = logging.getLogger(__name__)


class ChannelHub:
    """Tracks WebSockets per channel and broadcasts JSON server messages."""

    def __init__(self) -> None:
        self._lock = asyncio.Lock()
        self._channel_clients: dict[str, set[WebSocket]] = defaultdict(set)

    async def connect(self, channel: str, websocket: WebSocket) -> None:
        async with self._lock:
            self._channel_clients[channel].add(websocket)

    async def disconnect(self, channel: str, websocket: WebSocket) -> None:
        async with self._lock:
            clients = self._channel_clients.get(channel)
            if not clients:
                return
            clients.discard(websocket)
            if not clients:
                del self._channel_clients[channel]

    def channel_count(self, channel: str) -> int:
        return len(self._channel_clients.get(channel, ()))

    async def broadcast(
        self,
        channel: str,
        message: ServerMessage,
        *,
        exclude: WebSocket | None = None,
    ) -> None:
        payload = message.model_dump(mode="json")
        text = json.dumps(payload, default=str)
        async with self._lock:
            clients = list(self._channel_clients.get(channel, ()))
        dead: list[WebSocket] = []
        for ws in clients:
            if ws is exclude:
                continue
            try:
                await ws.send_text(text)
            except Exception:
                dead.append(ws)
        for ws in dead:
            await self.disconnect(channel, ws)
            logger.debug("Removed dead websocket from channel %s", channel)

    async def send_personal(self, websocket: WebSocket, message: ServerMessage) -> None:
        text = json.dumps(message.model_dump(mode="json"), default=str)
        await websocket.send_text(text)


hub = ChannelHub()
