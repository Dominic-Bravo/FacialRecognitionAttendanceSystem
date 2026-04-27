import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.health import router as health_router
from app.core.config import get_settings
from app.realtime.router import router as ws_router

OPENAPI_DESCRIPTION = """
## Overview

This service exposes a **health** endpoint over HTTP and **real-time messaging** over WebSockets.

## WebSockets

Clients connect to **`/ws/{channel}`** (see the **realtime** tag). The wire format is JSON text frames; invalid channel names are rejected with close code **4400**.

For full message schemas, lifecycle events, limits, and client examples, see **`docs/API.md`** in the repository.
"""

OPENAPI_TAGS_METADATA = [
    {
        "name": "health",
        "description": "HTTP endpoints for health and orchestration probes.",
    },
    {
        "name": "realtime",
        "description": (
            "WebSocket endpoint `/ws/{channel}` for channel-scoped messaging. "
            "OpenAPI does not fully describe WebSockets; refer to **docs/API.md**."
        ),
    },
]


def create_app() -> FastAPI:
    settings = get_settings()
    logging.basicConfig(
        level=logging.DEBUG if settings.debug else logging.INFO,
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    )

    app = FastAPI(
        title=settings.app_name,
        description=OPENAPI_DESCRIPTION,
        openapi_tags=OPENAPI_TAGS_METADATA,
        debug=settings.debug,
    )
    wildcard_origin = settings.cors_origins == ["*"] or "*" in settings.cors_origins
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=not wildcard_origin,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health_router)
    app.include_router(ws_router)
    return app


app = create_app()
