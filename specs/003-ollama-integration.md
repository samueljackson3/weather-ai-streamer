# Spec: Ollama Integration — Local LLM Weather Summaries

**Session**: 3  
**Estimated Time**: 5.7 hours  
**Status**: 🔄 Not Started  
**Last Updated**: April 9, 2026

---

## Problem Statement

You have weather data. Now make it useful.

In this session, you'll connect your FastAPI weather endpoint to a locally-running Ollama LLM to generate human-readable weather summaries — and then stream those summaries token-by-token so users see results as they arrive, not after a multi-second wait.

This is where async Python stops being abstract: two external I/O operations (OpenWeather _then_ Ollama) chained together, with streaming output that makes the latency disappear. You'll reuse everything from Session 2 — `WeatherResponse`, `fetch_weather()`, and the `httpx.AsyncClient` — without touching them.

### What Makes This Different From Tutorials

Most LLM tutorials dump a full prompt into `ollama.chat()` and print the result. Here you'll understand:
- Why streaming exists (UX, not just performance)
- How the HTTP wire protocol actually works (newline-delimited JSON)
- What `async for` over a streaming HTTP response looks like under the hood
- Why error handling is harder with streams (you can't send a 503 after you've already started streaming)

---

## Learning Objectives

- [ ] Understand the Ollama HTTP API — what it accepts, what it streams back
- [ ] Write a clean `ollama_client.py` module with a single responsibility
- [ ] Build a prompt template that turns `WeatherResponse` fields into a useful LLM input
- [ ] Implement `GET /weather-ai/{city}` using Session 2's `fetch_weather()` as a building block
- [ ] Return a non-streaming JSON summary first (validate the full pipeline before adding streaming)
- [ ] Add streaming with FastAPI's `StreamingResponse` and `async for` over an httpx streaming response
- [ ] Handle Ollama being unreachable, model not found, and timeout gracefully
- [ ] Explain the difference between SSE and WebSockets and why SSE fits this use case
- [ ] Explain why you can't send an HTTP error code after streaming has started

---

## Technical Design

### File Structure (output of this session)

```
weather-ai-streamer/
├── src/
│   ├── config.py            # Already exists — ollama_url already set (no changes needed)
│   ├── models.py            # Already exists — import WeatherResponse (no changes needed)
│   ├── main.py              # Add GET /weather-ai/{city} route
│   └── ollama_client.py     # NEW: Ollama HTTP client, prompt builder, streaming generator
├── .env                     # Add OLLAMA_MODEL=llama3.2:3b (optional, can hardcode for now)
└── specs/
    └── 003-ollama-integration.md   # This file
```

> Note: `ollama_url` is already in `src/config.py` — it was planted in Session 2 for this moment.

---

### Request Lifecycle (Non-Streaming)

```
curl / browser
      │
      ▼
FastAPI Router (main.py)
      │  → Validates path param: city (string, required)
      │  → Injects httpx.AsyncClient via Depends()
      │
      ▼
fetch_weather(city, units="metric", client)   ← Session 2's function, unchanged
      │  → Calls OpenWeather API
      │  → Returns WeatherResponse (validated Pydantic model)
      │
      ▼
build_weather_prompt(weather: WeatherResponse) → str   ← New in ollama_client.py
      │  → Formats WeatherResponse fields into a natural language prompt
      │
      ▼
call_ollama(prompt, client)   ← New in ollama_client.py
      │  → POST to http://localhost:11434/api/generate
      │  → stream=false → waits for full response
      │  → Returns response text as a plain string
      │
      ▼
{"city": "Seattle", "summary": "A cool, overcast day..."}
      │
      ▼
HTTP 200 JSON response
```

---

### Request Lifecycle (Streaming)

```
Browser (EventSource or curl)
      │
      ▼
FastAPI: StreamingResponse(stream_ollama_summary(), media_type="text/event-stream")
      │
      ▼
stream_ollama_summary(weather, client) → AsyncGenerator[str, None]
      │  → POST to Ollama with stream=true
      │  → async for line in response.aiter_lines():
      │       → parse JSON token from each line
      │       → yield f"data: {token}\n\n"   ← SSE format
      │
      ▼
Client receives tokens as they are generated:
      data: The
      data:  weather
      data:  in
      data:  Seattle
      data:  is cool and overcast today.
```

---

### Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Ollama HTTP client | Reuse `lifespan` `httpx.AsyncClient` | Already managed; no new client lifecycle to handle |
| Non-streaming first | Step D before Step E | Validate full pipeline (weather → Ollama → response) before adding streaming complexity |
| Prompt placement | `ollama_client.py` | Prompt is LLM concern, not routing concern; keeps `main.py` clean |
| Streaming format | SSE (`text/event-stream`) | One-way server→client stream; simpler than WebSockets for this use case |
| Error strategy (non-streaming) | `HTTPException` (same as Session 2) | Works cleanly before any bytes are sent |
| Error strategy (streaming) | Yield `data: [ERROR] ...` as the last SSE event | Can't raise HTTP 503 once streaming has started; error lives in the stream |
| Model | `llama3.2:3b` | Fast on M4 Mac; confirmed working in your setup |
| No new route file | Flat `main.py` | Still early; no need for APIRouter yet |

---

## API Contract

### `GET /weather-ai/{city}` (Non-Streaming, Step D)

Returns a complete AI-generated weather summary as JSON.

**Path Parameters**:
- `city` (string, required): City name (e.g., `"Seattle"`)

**Query Parameters**:
- `units` (string, optional, default: `"metric"`): `"metric"` | `"imperial"` | `"standard"`
- `stream` (bool, optional, default: `false`): When `true`, returns SSE stream instead of JSON

**Response** (200, non-streaming):
```json
{
  "city": "Seattle",
  "summary": "Seattle is experiencing a cool, overcast day with temperatures around 15°C. With humidity at 80% and a light breeze, you might want to grab a light jacket."
}
```

**Error Responses**:

| Status | Condition | Detail |
|--------|-----------|--------|
| 404 | City not found (from OpenWeather) | `"City 'Atlantis' not found."` |
| 503 | OpenWeather unreachable | `"Weather service unavailable."` |
| 503 | Ollama not running | `"AI service unavailable. Is Ollama running?"` |
| 503 | Ollama model not found | `"Model 'llama3.2:3b' not found. Run: ollama pull llama3.2:3b"` |

---

### `GET /weather-ai/{city}?stream=true` (Streaming, Step E)

Returns tokens as Server-Sent Events.

**Response** (`200`, `Content-Type: text/event-stream`):
```
data: Seattle

data:  is

data:  experiencing

data:  overcast

data:  skies

data:  with

data:  mild

data:  temperatures.

data: [DONE]
```

**Error mid-stream**:
```
data: [ERROR] Ollama connection lost during generation.
```

> Why no HTTP status code on errors mid-stream? Once the first `data:` line is sent, the HTTP status code is already `200`. Errors have to be communicated in-band, in the stream itself.

---

## Code Contract

### `src/ollama_client.py` (New File)

```python
"""
Ollama integration: prompt building, HTTP calls, and streaming.

Single responsibility: everything LLM-related lives here.
main.py imports from here; doesn't know about Ollama's HTTP API details.
"""

import json
import httpx
from src.models import WeatherResponse
from src.config import settings
from typing import AsyncGenerator


def build_weather_prompt(weather: WeatherResponse) -> str:
    """
    Turn a WeatherResponse into a natural language prompt for the LLM.
    
    Key learning: Prompt engineering is domain-specific string formatting.
    The quality of this string directly impacts summary quality.
    Try different versions and compare outputs.
    """
    unit_label = {"metric": "°C", "imperial": "°F", "standard": "K"}[weather.units.value]
    return (
        f"The current weather in {weather.city}, {weather.country} is "
        f"{weather.temperature}{unit_label} (feels like {weather.feels_like}{unit_label}), "
        f"{weather.description}, humidity {weather.humidity}%, "
        f"wind speed {weather.wind_speed} m/s. "
        f"Write a 2-3 sentence friendly weather summary for someone deciding what to wear today. "
        f"Be specific and practical. Do not mention the city name in the first sentence."
    )


async def call_ollama(prompt: str, client: httpx.AsyncClient) -> str:
    """
    Call Ollama API and wait for the complete response (non-streaming).
    
    Use this first — validate the full pipeline before adding streaming.
    
    Raises:
        httpx.ConnectError: Ollama is not running
        httpx.TimeoutException: Model is taking too long
        ValueError: Unexpected response shape from Ollama
    """
    response = await client.post(
        f"{settings.ollama_url}/api/generate",
        json={"model": "llama3.2:3b", "prompt": prompt, "stream": False},
        timeout=30.0,
    )
    response.raise_for_status()
    data = response.json()
    return data["response"]


async def stream_ollama_summary(
    prompt: str,
    client: httpx.AsyncClient,
) -> AsyncGenerator[str, None]:
    """
    Stream Ollama response tokens as Server-Sent Events.
    
    Key learning: Ollama's streaming API sends newline-delimited JSON.
    Each line is: {"model":"...","response":"token","done":false}
    The last line has "done":true and an empty "response".
    
    We transform each token into SSE format: "data: {token}\\n\\n"
    
    Why AsyncGenerator? It lets FastAPI's StreamingResponse pull tokens
    one at a time without buffering the entire response in memory.
    """
    async with client.stream(
        "POST",
        f"{settings.ollama_url}/api/generate",
        json={"model": "llama3.2:3b", "prompt": prompt, "stream": True},
        timeout=60.0,
    ) as response:
        async for line in response.aiter_lines():
            if not line.strip():
                continue
            try:
                chunk = json.loads(line)
                token = chunk.get("response", "")
                if token:
                    yield f"data: {token}\n\n"
                if chunk.get("done"):
                    yield "data: [DONE]\n\n"
                    return
            except json.JSONDecodeError:
                continue
```

---

### `src/main.py` — New Route Only

Add this below the existing `GET /weather/{city}` route. **Do not restructure anything.**

```python
from fastapi.responses import StreamingResponse
from src.ollama_client import build_weather_prompt, call_ollama, stream_ollama_summary

@app.get("/weather-ai/{city}")
async def get_weather_ai(
    city: str,
    units: Units = Query(default=Units.metric),
    stream: bool = Query(default=False),
    client: httpx.AsyncClient = Depends(get_http_client),
):
    """
    Fetch weather data, then ask Ollama to summarize it.
    
    With stream=false (default): returns complete JSON summary.
    With stream=true: returns SSE token stream.
    """
    # Step 1: Get weather data (reuse Session 2's function unchanged)
    weather = await fetch_weather(city, units, client)
    
    # Step 2: Build the prompt
    prompt = build_weather_prompt(weather)
    
    if stream:
        # Step 3a: Stream tokens back as SSE
        return StreamingResponse(
            stream_ollama_summary(prompt, client),
            media_type="text/event-stream",
        )
    
    # Step 3b: Wait for complete response, return as JSON
    try:
        summary = await call_ollama(prompt, client)
    except httpx.ConnectError:
        raise HTTPException(
            status_code=503,
            detail="AI service unavailable. Is Ollama running? Try: ollama serve"
        )
    except httpx.TimeoutException:
        raise HTTPException(
            status_code=503,
            detail="AI service timed out. The model may be busy or too large."
        )
    
    return {"city": weather.city, "summary": summary}
```

---

## Success Criteria

### It Works

- [ ] `GET /weather-ai/Seattle` returns JSON: `{"city": "Seattle", "summary": "..."}`
- [ ] `GET /weather-ai/Seattle?stream=true` streams tokens to curl in real time
- [ ] `GET /weather-ai/FakeCityXyz` returns HTTP 404 (from OpenWeather, before Ollama is called)
- [ ] When Ollama is not running (`killall ollama`), non-streaming returns HTTP 503 with clear message
- [ ] `/docs` shows the new route with correct params (no manual work)

### You Understand It

- [ ] Can explain: "Why do we call `fetch_weather()` instead of rewriting the OpenWeather call inside `get_weather_ai()`?"
  - Expected: Separation of concerns; `fetch_weather()` is already tested/validated; DRY without coupling
- [ ] Can explain: "Why can't we raise `HTTPException(503)` after streaming has started?"
  - Expected: HTTP status code is sent with the first byte of the response; once `200 OK` is on the wire, you can't change it. Errors must be in-band (e.g., `data: [ERROR]...`).
- [ ] Can explain: "What is `AsyncGenerator` and why does `StreamingResponse` need one?"
  - Expected: It's a function that `yield`s values lazily; `StreamingResponse` pulls from it on demand without buffering the entire response in memory
- [ ] Can explain: "What's the difference between `client.post()` and `client.stream()`?"
  - Expected: `.post()` waits for the full response body; `.stream()` opens a connection and lets you read the body incrementally
- [ ] Can explain SSE vs WebSockets for this use case
  - Expected: SSE is one-way (server → client only), simpler, works over plain HTTP; WebSockets are bidirectional but overkill here

### Stretch (Optional)

- [ ] Try `GET /weather-ai/Seattle` with `llama3.2:1b` vs `llama3.2:3b` — measure response time and compare quality
- [ ] Modify `build_weather_prompt()` to accept a `style` param: `"formal"` | `"casual"` | `"poetic"` and pass it as a query param
- [ ] Add a `GET /weather-ai/batch?cities=Seattle,Tokyo,London&stream=true` that fetches all three cities with `asyncio.gather()` and streams all summaries

---

## Learning Progression (Micro-Steps)

Work through these in order. Don't skip E before validating D.

**Step A** (~20 min) — Understand Ollama's HTTP API directly  
Before writing any Python, understand what you're integrating with. Curl Ollama directly and read the raw response.
```bash
# Non-streaming — get one big response
curl http://localhost:11434/api/generate \
  -d '{"model": "llama3.2:3b", "prompt": "What is 2+2?", "stream": false}'

# Streaming — watch tokens arrive line by line
curl http://localhost:11434/api/generate \
  -d '{"model": "llama3.2:3b", "prompt": "What is 2+2?", "stream": true}'
```
Observe: What does each streaming line look like? What field holds the token? What does `"done": true` mean?

**Step B** (~20 min) — Create `ollama_client.py` with `build_weather_prompt()`  
Write the module with just the prompt builder. In a Python scratch file, create a fake `WeatherResponse` and call `build_weather_prompt()`. Read the output. Is it a good prompt? Would you answer it the way you want Ollama to?

**Step C** (~30 min) — Add `call_ollama()` (non-streaming)  
Add the non-streaming `call_ollama()` function. Test it in isolation: open a Python REPL or scratch file, call it with the prompt from Step B, and print the result. You should see a weather summary _before_ touching FastAPI.

**Step D** (~30 min) — Add `GET /weather-ai/{city}` (non-streaming)  
Wire the route into `main.py`. Import `build_weather_prompt` and `call_ollama`. Test the full end-to-end with curl:
```bash
curl http://localhost:8000/weather-ai/Seattle
```
You should get `{"city": "Seattle", "summary": "..."}`. This is the milestone: two APIs chained together.

**Step E** (~40 min) — Add streaming with `stream_ollama_summary()`  
Add the `stream_ollama_summary()` generator to `ollama_client.py`. Add the `?stream=true` path to the route. Test with curl and watch tokens arrive in your terminal in real time:
```bash
curl -N "http://localhost:8000/weather-ai/Seattle?stream=true"
```
The `-N` flag disables curl's output buffering so you see tokens as they arrive.

**Step F** (~30 min) — Error handling  
Kill Ollama (`killall ollama`). Test the non-streaming endpoint — verify you get a 503 with a useful message. Restart Ollama, test with a non-existent model name. Test with a city that doesn't exist — verify that error is caught before Ollama is called.

---

## Open Questions

- What happens if the user disconnects mid-stream (closes the browser)? Does Ollama keep generating?
- How would you add a timeout to the streaming case? (Hint: `timeout=httpx.Timeout(...)`)
- When would you switch from SSE to WebSockets? What would the client side look like?
- How does `async for line in response.aiter_lines()` work differently from reading a file line-by-line?
- What's the difference between `yield` in a regular function and `yield` in an `async def` function?
- If you wanted to log "LLM called for city X" on every request, where would that go? Middleware? The route? The client module?

---

## Testing Strategy

Manual testing first. pytest mocking in Session 5.

```bash
# 1. Confirm Ollama is running
curl http://localhost:11434/api/tags

# 2. Non-streaming summary
curl http://localhost:8000/weather-ai/Seattle

# 3. Imperial units
curl "http://localhost:8000/weather-ai/Tokyo?units=imperial"

# 4. Streaming (watch tokens arrive)
curl -N "http://localhost:8000/weather-ai/London?stream=true"

# 5. Bad city (should 404 before Ollama is called)
curl http://localhost:8000/weather-ai/FakeCityXyz

# 6. Ollama down (503 with helpful message)
killall ollama
curl http://localhost:8000/weather-ai/Seattle
ollama serve  # bring it back

# 7. Check /docs — new endpoint should appear automatically
open http://localhost:8000/docs
```

**Pytest preview** (don't write passing tests this session — just know the shape):
```python
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from src.ollama_client import build_weather_prompt, call_ollama
from src.models import WeatherResponse, Units

def test_build_weather_prompt_contains_city():
    weather = WeatherResponse(
        city="Seattle", country="US", temperature=15.5,
        feels_like=14.2, description="overcast clouds",
        humidity=80, wind_speed=3.1, units=Units.metric
    )
    prompt = build_weather_prompt(weather)
    assert "Seattle" in prompt
    assert "15.5°C" in prompt

@pytest.mark.asyncio
async def test_call_ollama_returns_string():
    mock_client = AsyncMock()
    mock_client.post.return_value.json.return_value = {
        "model": "llama3.2:3b",
        "response": "Seattle is cool and cloudy today.",
        "done": True
    }
    result = await call_ollama("some prompt", mock_client)
    assert isinstance(result, str)
    assert len(result) > 0
```

---

## Rails Developer Notes

| Concept | Rails Equivalent | Key Difference |
|---------|-----------------|----------------|
| `AsyncGenerator` | Enumerator / `lazy` | Python generators are first-class; streaming is a native pattern |
| `StreamingResponse` | `render plain: ..., stream: true` | FastAPI handles chunked transfer encoding automatically |
| `build_weather_prompt()` | A service object or view helper | No framework magic — just a function that returns a string |
| `call_ollama()` | An API wrapper gem (e.g., `ruby-openai`) | But you're writing it yourself; understand the HTTP directly |
| `data: {token}\n\n` SSE format | ActionController::Live + SSE | SSE is a browser-native standard; no framework needed on the client |
| `httpx.ConnectError` | `Faraday::ConnectionFailed` | Different libraries, same concept: catch network-level failures |
| `async for line in response.aiter_lines()` | `Net::HTTP` with a block | Ruby HTTP streaming exists but isn't idiomatic; Python makes it natural |

---

## Handoff Checklist (Ready for Session 4)

When this session is complete, Session 4 (Docker) should be able to:

- [ ] Run `docker-compose up` and have the FastAPI app and Ollama available as separate services
- [ ] See that `OLLAMA_URL` is already in `config.py` as a setting — easy to swap for a Docker service name (`http://ollama:11434`)
- [ ] Know that the `lifespan`-managed `httpx.AsyncClient` works correctly inside a container (no file system or process dependencies)
- [ ] Have a working `/weather-ai/{city}` endpoint to verify containerization succeeded

The architecture supports containerization without changes — the only thing that needs updating is `OLLAMA_URL` in `.env` to point to the Docker service name instead of `localhost`.
