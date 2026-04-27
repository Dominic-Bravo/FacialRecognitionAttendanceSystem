# API reference

Base URL when running locally: `http://127.0.0.1:8000` (adjust host/port if you changed them).

---

## HTTP

### `GET /health`

**Purpose:** Liveness check for load balancers, Kubernetes probes, or monitoring.

**Response:** `200 OK`

```json
{ "status": "ok" }
```

**Example (PowerShell):**

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:8000/health
```

**Example (curl):**

```bash
curl -s http://127.0.0.1:8000/health
```

---

## WebSocket — real-time messaging

### Connection

**URL pattern:** `ws://<host>:<port>/ws/<channel>`

**Channel rules:**

- 1–64 characters
- Allowed characters: letters, digits, `.`, `_`, `-`
- Examples: `lobby`, `room-1`, `team.alpha`

If the channel name is invalid, the server closes the socket with WebSocket close code **4400** before accepting the connection.

**Example URL:** `ws://127.0.0.1:8000/ws/lobby`

Use `wss://` when the app is served over HTTPS.

### Wire format

All messages are **text frames** containing **JSON objects**.

#### Client → server

| `type` | Required fields | Behavior |
|--------|-----------------|----------|
| `chat` | `text` (non-empty string after trim) | Broadcast a chat message to everyone in the same channel (including sender). |
| `ping` | — | Server replies with a `pong` to this connection only. |

**Chat example:**

```json
{ "type": "chat", "text": "Hello, channel!" }
```

**Ping example:**

```json
{ "type": "ping" }
```

#### Server → client

Every outbound message includes at least:

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | One of: `chat`, `pong`, `joined`, `left`, `error`, `system` |
| `channel` | string | Channel key |
| `sender_id` | string or omitted | Opaque id for the connection (Python `id(websocket)` as string) |
| `text` | string or null | Human-readable text when relevant |
| `payload` | object or null | Extra structured data |
| `ts` | string (ISO 8601) | UTC timestamp |
| `id` | string | Unique message id (UUID) |

**Lifecycle events:**

1. After a successful connect, the client receives **`system`** with `text: "connected"` and `payload.client_id`.
2. Other clients in the channel receive **`joined`** with `payload.members` = current member count (including the new connection).
3. On disconnect, remaining clients receive **`left`** with updated `payload.members`.

**Chat relay:** **`chat`** messages are broadcast to all sockets in the channel; `text` is the message body.

**Errors:** Invalid JSON, oversized payload, or validation failure yields **`error`** to that client only. Common `text` values: `invalid JSON`, `message too large`, `validation error` (with `payload.detail` from Pydantic when applicable).

**Size limit:** The UTF-8 byte length of each inbound text message must not exceed `WS_MAX_MESSAGE_BYTES` (default 65536).

### Client examples

#### Browser (JavaScript)

```javascript
const ws = new WebSocket("ws://127.0.0.1:8000/ws/lobby");

ws.onopen = () => {
  ws.send(JSON.stringify({ type: "chat", text: "Hi from the browser" }));
};

ws.onmessage = (event) => {
  const msg = JSON.parse(event.data);
  console.log(msg.type, msg);
};
```

#### Python (`websockets` library)

```bash
pip install websockets
```

```python
import asyncio
import json
import websockets

async def main():
    uri = "ws://127.0.0.1:8000/ws/lobby"
    async with websockets.connect(uri) as ws:
        await ws.send(json.dumps({"type": "chat", "text": "Hi from Python"}))
        async for raw in ws:
            print(json.loads(raw))

asyncio.run(main())
```

### OpenAPI / Swagger

REST endpoints appear under **Swagger UI** at `/docs`. WebSocket endpoints are not fully represented in OpenAPI; use this document for WebSocket URLs and payloads.

---

## Operational notes

- **Single process:** The in-memory `ChannelHub` only shares state inside one worker. For multiple workers or hosts, add a shared broker (for example Redis pub/sub) if you need cross-instance broadcast.
- **Identity:** `sender_id` is not authenticated; treat it as a session-local handle, not a user id.
