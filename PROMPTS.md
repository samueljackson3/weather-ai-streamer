# Hands-On Learning Prompts

**Format**: Requirements → You Build → Test → Iterate → Review  
**Key principle**: Build it yourself (even buggy code) before asking for review.

---

## Session 1: Async Fundamentals

### Step 1A: Simplest Async Function (10 min)

```
Session 1, Step 1A: Generate the SIMPLEST async function that:
- Uses asyncio.sleep(1) to simulate I/O
- Prints "Starting task", sleeps, prints "Task complete"
- Returns a string "Task complete"
- Includes timing with time.perf_counter()
- Has a main block that runs it with asyncio.run()

Keep under 15 lines. Add comments explaining: async, await, asyncio.run().
```

---

### Step 1B: Sync vs Async Comparison (15 min)

```
Session 1, Step 1B: Create two versions that each call fetch_data() 3 times:

Version 1: Synchronous using time.sleep() (blocking)
Version 2: Async using await asyncio.sleep() (sequential, not concurrent yet)

- Each fetch takes 1 second
- Show timing for both with time.perf_counter()
- Print execution order
- Keep under 35 lines, add comments explaining why both take ~3 seconds

Save as step_1b.py
```

---

### Step 1C: Concurrent Execution with gather() (20 min)

```
Session 1, Step 1C: Add a THIRD version to step_1b.py using asyncio.gather()
to run 3 fetches concurrently.

- Show when each fetch starts (timestamps)
- Compare timing: sequential (~3s) vs concurrent (~1s)
- Clear labels for each version
- Comments explaining why gather() is faster

Generate ONLY the new concurrent function — I'll integrate it.
Keep under 15 lines.
```

---

### Step 1D: Manual Task Creation (20 min)

```
Session 1, Step 1D: Create step_1d.py demonstrating asyncio.create_task().

Show:
1. Creating 3 tasks explicitly with create_task()
2. Doing print/work BETWEEN creating tasks and awaiting them
3. Awaiting tasks and collecting results
4. Timing the operation

- Comments explaining when tasks start vs when we await them
- Show tasks run before we await them
- Keep under 25 lines, compare to gather() in comments
```

---

### Step 1E: Error Handling (20 min)

```
Session 1, Step 1E: Create step_1e.py with TWO error handling approaches:

Approach 1: try/except around await asyncio.gather()
Approach 2: asyncio.gather() with return_exceptions=True

- Make one fetch raise randomly (50% chance)
- Show output difference between approaches
- Comments explaining when to use each
- Keep under 40 lines
```

---

### Step 1F: Build Your Own Challenge (30 min)

```
Session 1, Step 1F: After I build my own weather simulator, REVIEW it (don't write it yet).

I will create step_1f_weather_sim.py that:
- Simulates fetching weather from 5 cities
- Each with random delay (0.5s-3s)
- Uses asyncio.as_completed() to print results as they arrive
- Handles one city failing gracefully
- Shows total time vs calculated sequential time

DO NOT generate code yet. Tell me:
1. What imports I'll need
2. What the function signature should look like
3. Hints for using as_completed()

I'll build it myself first, then ask for review.
```

---

### Step 1G: Real-World Patterns (20 min)

```
Session 1, Step 1G: Show how async patterns (gather, create_task, error handling)
work with real libraries:

1. HTTP requests with httpx.AsyncClient
2. File I/O with aiofiles
3. Database queries with asyncpg

For each: 10-15 line example showing the pattern.
Don't generate complete implementation — show the structure.
Comments connecting to patterns I learned (gather, etc.).
```

---

### Step 1H: Concept Self-Test (20 min)

```
Session 1, Step 1H: I will answer 5 questions. AFTER I answer, critique my understanding.

1. What's the difference between concurrent and parallel execution?
2. When does async NOT help performance?
3. Why use async context managers (async with)?
4. gather() vs create_task() vs as_completed() — when to use each?
5. What happens in the event loop during await asyncio.sleep(1)?

DO NOT answer yet — wait for my answers, then critique them.

After feedback, give me a code challenge to build from scratch (no hints) to test real understanding.
```

---

## Session 2: FastAPI + Weather API

---

### Step 2A: Your First FastAPI App (15 min)

**Build** `learning_examples/step_2a.py`:
- `GET /hello` → `{"message": "Hello, World!"}`
- `GET /hello/{name}` → `{"message": "Hello, {name}!"}`
- `POST /echo` → accepts `{"text": "..."}`, returns it back
- Main block that runs uvicorn

```python
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()

@app.get("/path")
async def my_endpoint():
    return {"key": "value"}

# Run with: uvicorn step_2a:app --reload
```

Test with `curl` or `http://localhost:8000/docs`. Then paste for review.

---

### Step 2B: Pydantic Models + Validation (20 min)

**Build** `learning_examples/step_2b.py`:
- `WeatherRequest`: `city: str`, `units: str = "metric"`
- `WeatherResponse`: `city: str`, `temperature: float`, `description: str`, `units: str`
- `POST /weather` → accepts request, returns hardcoded response (fake data OK)
- Test bad input: `{"city": 123}` — observe the automatic 422 error

```python
from pydantic import BaseModel

class MyModel(BaseModel):
    field: str
    optional_field: int = 0

@app.post("/endpoint", response_model=ResponseModel)
async def endpoint(body: RequestModel):
    ...
```

Break the input intentionally and read the 422. Then paste for review.

---

### Step 2C: Async HTTP with httpx (25 min)

**Build** `learning_examples/step_2c.py`:
- `GET /post/{id}` → fetches from `https://jsonplaceholder.typicode.com/posts/{id}`
- 404 → return HTTP 404; timeout → return HTTP 503
- Add `elapsed_ms` field showing how long the fetch took

```python
import httpx
from fastapi import HTTPException

async with httpx.AsyncClient(timeout=5.0) as client:
    response = await client.get(url)
    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="Not found")
```

Test valid ID, invalid ID (9999), and reduce timeout to trigger 503. Then paste for review.

---

### Step 2D: Real Weather API (30 min)

**Build** `learning_examples/step_2d.py`:
- `GET /weather/{city}?units=metric` → real OpenWeather API
- Load `OPENWEATHER_API_KEY` from env; create `.env.example`
- Return typed `WeatherResponse` Pydantic model
- Handle: invalid city → 404, missing key → 500, API down → 503

**OpenWeather URL**: `https://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}&units={units}`  
**Fields**: `main.temp`, `weather[0].description`, `name`, `sys.country`

```python
import os
api_key = os.getenv("OPENWEATHER_API_KEY")
if not api_key:
    raise HTTPException(status_code=500, detail="API key not configured")
```

Test with real cities and a fake one. Then paste for review.

---

### Step 2E: Project — Multi-City Comparison (45 min)

**This is your Session 2 capstone. No hints.**

**Build** `learning_examples/step_2e_compare.py`:
- `GET /weather/compare?cities=Seattle,Portland,Vancouver`
  - Parse comma-separated city list from query param
  - Fetch all cities **concurrently** using `asyncio.gather()` (from Session 1!)
  - Return results sorted coldest to warmest
  - Handle partial failures: if one city is invalid, include an error for it but return the rest
  - Include `total_time_ms` and `cities_requested` in the response
- `GET /health` → returns `{"status": "ok", "timestamp": "..."}`

You have everything you need: async patterns from Session 1, FastAPI from 2A-2B, httpx from 2C-2D.

Build it, run it, break it. When done, paste your code for review.

---

## Session 3: Ollama + Streaming

---

### Step 3A: Talk to Ollama Directly (15 min)

**Build** `learning_examples/step_3a_ollama.py` (plain Python, no FastAPI):
- POST to `http://localhost:11434/api/generate` with `{"model": "llama3.2:3b", "prompt": "...", "stream": false}`
- Print the response text
- Time the full request
- Try a few different prompts

```python
# Response JSON has a "response" key; use timeout=60.0 — LLM inference takes time
async with httpx.AsyncClient(timeout=60.0) as client:
    response = await client.post(url, json=payload)
    print(response.json()["response"])
```

Confirm it works before moving on. Then paste for review.

---

### Step 3B: Streaming from Ollama (25 min)

**Build** `learning_examples/step_3b_stream.py`:
- Same Ollama call but `"stream": true`
- Print each token to the terminal as it arrives (not all at once)
- Stop when you see `"done": true` in the JSON
- Time how long the first token takes vs total time

```python
async with client.stream("POST", url, json=payload) as response:
    async for line in response.aiter_lines():
        if line:
            data = json.loads(line)
            print(data["response"], end="", flush=True)
            if data.get("done"):
                break
```

Notice the experience difference vs 3A. Then paste for review.

---

### Step 3C: FastAPI + StreamingResponse (25 min)

**Build** `learning_examples/step_3c_api.py`:
- `GET /generate?prompt=your+text`
- Returns `StreamingResponse` that streams tokens from Ollama as plain text
- Test with: `curl "http://localhost:8000/generate?prompt=hello+world"`

```python
from fastapi.responses import StreamingResponse

async def stream_tokens(prompt: str):
    async with httpx.AsyncClient(timeout=60.0) as client:
        async with client.stream("POST", ...) as response:
            async for line in response.aiter_lines():
                if line:
                    data = json.loads(line)
                    yield data["response"]

@app.get("/generate")
async def generate(prompt: str):
    return StreamingResponse(stream_tokens(prompt), media_type="text/plain")
```

Test with curl. Then paste for review.

---

### Step 3D: Server-Sent Events Format (30 min)

**Build** `learning_examples/step_3d_sse.py` extending 3C:  
*(SSE: `data: {content}\n\n` — browsers handle reconnection automatically)*
- Same `/generate` endpoint but format output as SSE
- Each token: `f"data: {token}\n\n"`
- When Ollama signals `done: true`, yield `data: [DONE]\n\n` then stop
- Media type: `text/event-stream`
- Handle exceptions: yield `data: [ERROR] {message}\n\n` before closing

```python
yield f"data: {token}\n\n"  # Two newlines = end of event
# Test: curl -N "http://localhost:8000/generate?prompt=hello"
```

Test with `curl -N`. Then paste for review.

---

### Step 3E: Project — Weather AI Streamer (45 min)

**This is the main feature of the whole project. No hints.**

**Build** `learning_examples/step_3e_weather_ai.py`:

- `GET /weather-ai/{city}`
  1. Fetch real weather from OpenWeather (reuse Session 2 code)
  2. Build prompt: `f"Weather in {city}: {temp}C, {description}. Write a friendly 2-sentence summary."`
  3. Stream Ollama response as SSE
  4. Handle failures from either API gracefully

- `GET /weather-ai/compare?cities=Seattle,Portland`
  1. Fetch weather for all cities concurrently with `gather()`
  2. Build a comparison prompt with all the data
  3. Stream the AI summary as SSE

You've built every piece separately. Now combine them. Then paste for review.

---

### Step 3F: Frontend (25 min)

**Build** `static/index.html` with vanilla JavaScript:
- Input field for city name + Submit button
- Text area where streamed tokens appear one by one
- Loading indicator while waiting for first token
- Error display if the request fails
- "Clear" button to reset

```javascript
const source = new EventSource(`/weather-ai/${city}`);

source.onmessage = (event) => {
    if (event.data === "[DONE]") { source.close(); return; }
    if (event.data.startsWith("[ERROR]")) { /* handle */ return; }
    outputDiv.textContent += event.data;
};

source.onerror = () => { source.close(); };
```

Serve through FastAPI's `StaticFiles`. Test the full flow. Then paste for review.

---

## Session 4: Docker Containerization

---

### Step 4A: Dockerfile From Scratch (20 min)

**Build** `Dockerfile` for the FastAPI app:  
*(Layer order: dependencies before code — Docker caches layers)*
- Base: `python:3.12-slim`
- Copy `requirements.txt` first, install, THEN copy app code
- Expose port 8000; CMD runs uvicorn

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build: `docker build -t weather-ai .` / Run: `docker run -p 8000:8000 weather-ai`  
Change code, rebuild, and observe which layers get cached.

---

### Step 4B: Multi-Stage Build (20 min)

**Build** a 2-stage `Dockerfile`:  
*(Build stage installs deps; runtime stage copies only installed packages — keeps image small)*
- Stage 1 (`builder`): Install dependencies
- Stage 2 (`runtime`): Copy only installed packages from builder

No hints — research `FROM ... AS builder` and `COPY --from=builder`.

Compare sizes with `docker images`. Paste both Dockerfiles for review.

---

### Step 4C: docker-compose.yml (25 min)

**Build** `docker-compose.yml`:  
*(Services reach each other by service name — `api` reaches Ollama at `http://ollama:11434`, not `localhost`)*
- `api` service: built from Dockerfile, port 8000
- `ollama` service: `ollama/ollama` image, port 11434
- `api` loads `OPENWEATHER_API_KEY` from `.env`
- Volume for ollama models (persists across `down`/`up`)

```yaml
services:
  api:
    build: .
    env_file: .env
    environment:
      - OLLAMA_URL=http://ollama:11434
  ollama:
    image: ollama/ollama
    volumes:
      - ollama_models:/root/.ollama

volumes:
  ollama_models:
```

Run `docker-compose up`. Confirm `api` can reach `ollama`. Then paste for review.

---

### Step 4D: Project — Full Stack in Docker (45 min)

**The capstone. No hints.**

Get the entire project running in containers end-to-end:

- `docker-compose up` starts everything
- `http://localhost:8000/docs` shows FastAPI docs
- `http://localhost:8000` serves the HTML frontend
- Weather AI streaming works: frontend → api → ollama + openweather
- After `docker-compose down` and `up` again, Ollama models still there

Debug what breaks. Common issues:
- `api` starts before `ollama` is ready → `depends_on` + healthcheck
- Static files not served → FastAPI `StaticFiles` mount
- Env vars not reaching container
- Ollama model not downloaded inside container

Document what broke and how you fixed it. Then show the final setup for review.

---

## Session 5: Testing Async Applications

---

### Step 5A: pytest-asyncio Basics (20 min)

**Build** `tests/test_health.py`:
- Install `pytest-asyncio` and `httpx` test client
- Write async test for `GET /health`
- Use FastAPI's `TestClient` and `AsyncClient`
- Run with `pytest tests/`

```python
import pytest
from httpx import AsyncClient, ASGITransport
from src.main import app

@pytest.mark.asyncio
async def test_health():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/health")
    assert response.status_code == 200
```

Run the test. Then paste for review.

---

### Step 5B: Mocking External APIs (30 min)

**Build** `tests/test_weather.py`:
- Mock `httpx.AsyncClient` so no real HTTP calls are made
- Test `GET /weather/{city}` returns correct shape
- Test 404 when city not found
- Test 500 when API key missing

```python
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_weather_success():
    mock_response = AsyncMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "main": {"temp": 20.0, "feels_like": 19.0, "humidity": 80},
        "weather": [{"description": "clear sky"}],
        "name": "Tokyo",
        "sys": {"country": "JP"},
        "wind": {"speed": 5.0}
    }
    with patch("httpx.AsyncClient.get", return_value=mock_response):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.get("/weather/Tokyo")
    assert response.status_code == 200
    assert response.json()["city"] == "Tokyo"
```

Test both happy path and error cases. Then paste for review.

---

### Step 5C: Testing SSE Streaming Endpoints (30 min)

**Build** `tests/test_streaming.py`:
- Test `GET /weather-ai/{city}` returns SSE stream
- Collect all `data:` lines and assert `[DONE]` appears
- Mock both OpenWeather AND Ollama calls

```python
@pytest.mark.asyncio
async def test_weather_ai_streams():
    # Mock weather fetch and ollama stream
    # Collect SSE events from response
    # Assert structure: data: tokens..., data: [DONE]
    ...
```

This is harder — figure out how to collect streaming response lines. Then paste for review.

---

### Step 5D: Fixtures and conftest.py (20 min)

**Build** `tests/conftest.py`:
- Create reusable `async_client` fixture
- Create `mock_weather_response` fixture (fake OpenWeather payload)
- Create `mock_ollama_response` fixture
- Refactor tests to use fixtures

```python
# conftest.py
import pytest
from httpx import AsyncClient, ASGITransport
from src.main import app

@pytest.fixture
async def async_client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client
```

Refactor all existing tests to use conftest fixtures. Then paste for review.

---

### Step 5E: Capstone — Full Test Suite (45 min)

**No hints. Build a complete test suite covering the whole app.**

`tests/` should include:
- `conftest.py` — shared fixtures
- `test_health.py` — health endpoint
- `test_weather.py` — weather endpoint (success, city not found, missing key, timeout)
- `test_weather_ai.py` — streaming endpoint (tokens arrive, [DONE] sent, errors handled)
- All tests pass with `pytest tests/ -v`
- No real HTTP calls (fully mocked)
- Coverage: `pytest tests/ --cov=src`

Target: **>80% coverage** on `src/`.

When done, paste coverage report for review.

---

## When Stuck

```
I'm on Step XY and getting this error:

[paste error]

Here's my code:

[paste code]

My hypothesis: [your guess at the cause]

Am I on the right track? Give me a hint, not the full solution.
```
