# Realtime API (FastAPI)

FastAPI service with **HTTP health checks** and **WebSocket channel messaging** (JSON protocol, validated with Pydantic).

## Quick start

```powershell
cd "path\to\Fastapi"
python -m venv .venv
.\.venv\Scripts\pip install -r requirements.txt
.\.venv\Scripts\uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- **Interactive REST docs (Swagger UI):** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Alternative OpenAPI UI (ReDoc):** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
- **OpenAPI JSON:** [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json)

WebSockets are not fully described by OpenAPI; see **[docs/API.md](docs/API.md)** for connection URLs, message shapes, and examples.

## Configuration

Environment variables (optional) map to `app/core/config.py` via `pydantic-settings`. You can also use a `.env` file in the project root.

| Variable | Default | Purpose |
|----------|---------|---------|
| `APP_NAME` | `Realtime API` | API title in OpenAPI |
| `DEBUG` | `false` | Verbose logging when `true` |
| `CORS_ORIGINS` | `["*"]` | Allowed browser origins (JSON array string in `.env`, e.g. `["http://localhost:5173"]`) |
| `WS_MAX_MESSAGE_BYTES` | `65536` | Max UTF-8 size of each inbound WebSocket text frame |

When `CORS_ORIGINS` is `["*"]`, cookie credentials are disabled for CORS (browser security rule).

## Project layout

| Path | Role |
|------|------|
| `app/main.py` | App factory, CORS, router mounting |
| `app/core/config.py` | Settings |
| `app/api/routes/health.py` | `GET /health` |
| `app/realtime/router.py` | WebSocket `/ws/{channel}` |
| `app/realtime/manager.py` | In-memory channel connection hub |
| `app/realtime/schemas.py` | Client/server message models |
| `docs/API.md` | Full API and WebSocket reference |

## Documentation

- **[docs/API.md](docs/API.md)** — HTTP and WebSocket API, message protocol, client examples, error behavior.
