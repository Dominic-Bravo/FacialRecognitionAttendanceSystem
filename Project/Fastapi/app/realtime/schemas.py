from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field, model_validator


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class ClientMessageType(StrEnum):
    CHAT = "chat"
    PING = "ping"


class ServerMessageType(StrEnum):
    CHAT = "chat"
    PONG = "pong"
    JOINED = "joined"
    LEFT = "left"
    ERROR = "error"
    SYSTEM = "system"


class ClientMessage(BaseModel):
    type: ClientMessageType
    text: str | None = None

    @model_validator(mode="after")
    def validate_chat_text(self) -> ClientMessage:
        if self.type == ClientMessageType.CHAT:
            if self.text is None or not self.text.strip():
                raise ValueError("chat messages require non-empty text")
            self.text = self.text.strip()
        return self


class ServerMessage(BaseModel):
    type: ServerMessageType
    channel: str
    sender_id: str | None = None
    text: str | None = None
    payload: dict[str, Any] | None = None
    ts: datetime = Field(default_factory=utc_now)
    id: str = Field(default_factory=lambda: str(uuid4()))
