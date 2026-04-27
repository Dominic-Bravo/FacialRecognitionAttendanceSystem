from __future__ import annotations

import json
import logging
import re
from typing import Annotated

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from pydantic import ValidationError

from app.core.config import Settings, get_settings
from app.realtime.manager import hub
from app.realtime.schemas import (
    ClientMessage,
    ClientMessageType,
    ServerMessage,
    ServerMessageType,
)

logger = logging.getLogger(__name__)

router = APIRouter(tags=["realtime"])

_CHANNEL_PATTERN = re.compile(r"^[a-zA-Z0-9._-]{1,64}$")


def _normalize_channel(raw: str) -> str | None:
    raw = raw.strip()
    if not _CHANNEL_PATTERN.fullmatch(raw):
        return None
    return raw


@router.websocket(
    "/ws/{channel}",
    name="websocket_channel",
)
async def websocket_channel(
    websocket: WebSocket,
    channel: str,
    settings: Annotated[Settings, Depends(get_settings)],
) -> None:
    """Join a named channel; exchange JSON text frames per docs/API.md."""
    channel_key = _normalize_channel(channel)
    if channel_key is None:
        await websocket.close(code=4400)
        return

    await websocket.accept()
    client_id = id(websocket)

    await hub.connect(channel_key, websocket)
    await hub.broadcast(
        channel_key,
        ServerMessage(
            type=ServerMessageType.JOINED,
            channel=channel_key,
            sender_id=str(client_id),
            text=None,
            payload={"members": hub.channel_count(channel_key)},
        ),
        exclude=websocket,
    )
    await hub.send_personal(
        websocket,
        ServerMessage(
            type=ServerMessageType.SYSTEM,
            channel=channel_key,
            text="connected",
            payload={"client_id": str(client_id)},
        ),
    )

    try:
        while True:
            raw = await websocket.receive_text()
            if len(raw.encode("utf-8")) > settings.ws_max_message_bytes:
                await hub.send_personal(
                    websocket,
                    ServerMessage(
                        type=ServerMessageType.ERROR,
                        channel=channel_key,
                        text="message too large",
                    ),
                )
                continue
            try:
                data = json.loads(raw)
            except json.JSONDecodeError:
                await hub.send_personal(
                    websocket,
                    ServerMessage(
                        type=ServerMessageType.ERROR,
                        channel=channel_key,
                        text="invalid JSON",
                    ),
                )
                continue
            try:
                msg = ClientMessage.model_validate(data)
            except ValidationError as e:
                await hub.send_personal(
                    websocket,
                    ServerMessage(
                        type=ServerMessageType.ERROR,
                        channel=channel_key,
                        text="validation error",
                        payload={"detail": e.errors()},
                    ),
                )
                continue

            if msg.type == ClientMessageType.PING:
                await hub.send_personal(
                    websocket,
                    ServerMessage(
                        type=ServerMessageType.PONG,
                        channel=channel_key,
                    ),
                )
                continue

            if msg.type == ClientMessageType.CHAT and msg.text:
                await hub.broadcast(
                    channel_key,
                    ServerMessage(
                        type=ServerMessageType.CHAT,
                        channel=channel_key,
                        sender_id=str(client_id),
                        text=msg.text,
                    ),
                )
    except WebSocketDisconnect:
        pass
    finally:
        await hub.disconnect(channel_key, websocket)
        await hub.broadcast(
            channel_key,
            ServerMessage(
                type=ServerMessageType.LEFT,
                channel=channel_key,
                sender_id=str(client_id),
                payload={"members": hub.channel_count(channel_key)},
            ),
        )
