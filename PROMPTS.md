# Hands-On Learning: Build First, Learn From Mistakes

**Purpose**: Practical, incremental projects with clear requirements  
**Format**: Requirements → You Build → Test → Iterate → Review  
**Updated**: April 8, 2026

---

## 📋 How to Use This Guide

1. **Read the requirements** in each step
2. **Build the solution yourself** (don't copy-paste generated code first)
3. **Test it** - see what breaks and why
4. **Check your understanding** with review questions
5. **Move to next step** when solid

**Key principle**: Building code (even buggy code) teaches you more than reading perfect examples.

---

## Session 1: Async Fundamentals

### Step 1A: Simplest Async Function (10 min)

```
I'm learning Python async fundamentals from /Users/samueljackson/dev-ghec/local-projects/weather-ai-streamer/plan.md

Session 1, Step 1A: Generate the SIMPLEST async function that:
- Uses asyncio.sleep(1) to simulate I/O
- Prints "Starting task", sleeps, prints "Task complete"
- Returns a string "Task complete"
- Includes timing with time.perf_counter()
- Has a main block that runs it with asyncio.run()

Requirements:
- Keep under 15 lines total
- Add comments explaining: async, await, asyncio.run()
- Show timing output
- Keep it minimal and clear
```

---

### Step 1B: Sync vs Async Comparison (15 min)

```
I'm learning Python async fundamentals (Session 1, Step 1B).

Create two versions that each call a simulated fetch_data() function 3 times:

Version 1: Synchronous using time.sleep() (blocking)
Version 2: Async using await asyncio.sleep() (sequential, not concurrent yet)

Requirements:
- Each fetch takes 1 second
- Show timing for both versions using time.perf_counter()
- Include print statements showing execution order
- Keep under 35 lines total
- Add comments explaining why both take ~3 seconds

Save as step_1b.py

Keep it clean and minimal with clear comments.
```

---

### Step 1C: Concurrent Execution with gather() (20 min)

```
I'm learning Python async fundamentals (Session 1, Step 1C).

I have sync and sequential async versions in step_1b.py. Now add a THIRD version that uses asyncio.gather() to run the 3 fetches concurrently.

Requirements:
- Show when each fetch starts (print statements with timestamps)
- Compare timing: sequential (~3s) vs concurrent (~1s)
- Clear labels for each version
- Comments explaining why gather() is faster

Generate ONLY the new concurrent function - I'll integrate it into my file.

Keep the function under 15 lines.
```

---

### Step 1D: Manual Task Creation (20 min)

```
I'm learning Python async fundamentals (Session 1, Step 1D).

Create a new example (step_1d.py) that demonstrates asyncio.create_task() instead of gather().

Show:
1. Creating 3 tasks explicitly with create_task()
2. Doing some print/work BETWEEN creating tasks and awaiting them
3. Awaiting tasks and collecting results
4. Timing the whole operation

Requirements:
- Include comments explaining when tasks actually start vs when we await
- Show that tasks run even before we await them
- Keep under 25 lines
- Compare to gather() approach in comments
```

---

### Step 1E: Error Handling (20 min)

```
I'm learning Python async fundamentals (Session 1, Step 1E).

Create step_1e.py demonstrating TWO approaches to error handling in async code:

Approach 1: try/except around await asyncio.gather()
Approach 2: asyncio.gather() with return_exceptions=True

Requirements:
- Make one of the fetch calls raise a random exception (50% chance)
- Show output difference between both approaches
- Include comments explaining when to use each
- Keep under 40 lines total
```

---

### Step 1F: Build Your Own Challenge (30 min)

```
I'm learning Python async fundamentals (Session 1, Step 1F).

After I build my own weather simulator, I need you to REVIEW it (not write it).

I will create step_1f_weather_sim.py that:
- Simulates fetching weather from 5 cities
- Each city has random delay (0.5s - 3s) using random.uniform()
- Uses asyncio.as_completed() to print results as they arrive
- Handles one city failing gracefully
- Shows total time vs calculated sequential time

DO NOT generate code yet. Just tell me:
1. What imports I'll need
2. What the function signature should look like
3. Hints for using as_completed()

I'll build it myself first, then ask for review.
```

---

### Step 1G: Real-World Patterns (20 min)

```
I'm learning Python async fundamentals (Session 1, Step 1G).

Show me how the async patterns I learned (gather, create_task, error handling) work with REAL libraries:

1. HTTP requests with httpx.AsyncClient
2. File I/O with aiofiles
3. Database queries with asyncpg (connection pool)

For each:
- 10-15 line example showing the pattern
- Don't generate complete implementation - just show the structure
- Include comments connecting to the patterns I learned (gather, etc.)

Focus on showing what's SIMILAR to my learning examples and what's NEW (context managers, pools, etc.).
```

---

### Step 1H: Concept Self-Test (20 min)

```
I'm learning Python async fundamentals (Session 1, Step 1H).

I will answer these 5 questions about async Python. AFTER I answer, critique my understanding:

1. What's the difference between concurrent and parallel execution?
2. When does async NOT help performance?
3. Why use async context managers (async with)?
4. gather() vs create_task() vs as_completed() - when to use each?
5. What happens in the event loop during await asyncio.sleep(1)?

DO NOT answer yet - wait for my answers, then critique them.

Also: After my answers, show me a code challenge to build from scratch (no hints) that tests if I really understand async.
```

---

## Session 2: FastAPI + Weather API

**Format for every step**: Requirements → You build → Paste code → Get review

---

### Step 2A: Your First FastAPI App (15 min)

**Concept**: FastAPI uses Python decorators and type hints to define endpoints. The framework handles request parsing, validation, and response serialization automatically.

**Build** `learning_examples/step_2a.py`:
- `GET /hello` → returns `{"message": "Hello, World!"}`
- `GET /hello/{name}` → returns `{"message": "Hello, {name}!"}`
- `POST /echo` → accepts JSON body `{"text": "..."}` and returns it back
- Main block that runs uvicorn

**Hints:**
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

Build it. Test each endpoint with `curl` or the auto-generated docs at `http://localhost:8000/docs`. Then paste your code for review.

---

### Step 2B: Pydantic Models + Validation (20 min)

**Concept**: Pydantic models define the shape of your data. FastAPI uses them to validate inputs and serialize outputs automatically — wrong types get a 422 error before your code even runs.

**Build** `learning_examples/step_2b.py`:
- `WeatherRequest` model: `city: str`, `units: str = "metric"`
- `WeatherResponse` model: `city: str`, `temperature: float`, `description: str`, `units: str`
- `POST /weather` → accepts `WeatherRequest`, returns a hardcoded `WeatherResponse` (fake data is fine)
- Deliberately test a bad request: send `{"city": 123}` and observe the automatic error

**Hints:**
```python
from pydantic import BaseModel

class MyModel(BaseModel):
    field: str
    optional_field: int = 0

@app.post("/endpoint", response_model=ResponseModel)
async def endpoint(body: RequestModel):
    ...
```

Build it. Intentionally break the input and read the 422 error. Then paste for review.

---

### Step 2C: Async HTTP with httpx (25 min)

**Concept**: `httpx.AsyncClient` is the async equivalent of the `requests` library. The `async with` context manager ensures the connection is properly closed even if an error occurs.

**Build** `learning_examples/step_2c.py`:
- `GET /post/{id}` → fetches from `https://jsonplaceholder.typicode.com/posts/{id}`
- Handle 404 (post not found) → return HTTP 404
- Handle timeout → return HTTP 503
- Add `elapsed_ms` field to the response showing how long the fetch took

**Hints:**
```python
import httpx
from fastapi import HTTPException
import time

async with httpx.AsyncClient(timeout=5.0) as client:
    response = await client.get(url)
    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="Not found")
```

Build it. Test with a valid ID, an invalid ID (9999), and try reducing the timeout to trigger a 503. Then paste for review.

---

### Step 2D: Real Weather API (30 min)

**Concept**: Using environment variables keeps secrets out of code. `os.getenv()` reads them at runtime.

**Build** `learning_examples/step_2d.py`:
- `GET /weather/{city}?units=metric` → fetches real data from OpenWeather API
- Load `OPENWEATHER_API_KEY` from environment (use `python-dotenv` or export it in terminal)
- Return a typed `WeatherResponse` Pydantic model
- Handle: invalid city → 404, missing API key → 500, API down → 503
- Create `.env.example` with `OPENWEATHER_API_KEY=your_key_here`

**OpenWeather URL:**
```
https://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}&units={units}
```

**Response fields you'll need:** `main.temp`, `weather[0].description`, `name`, `sys.country`

**Hints:**
```python
import os
api_key = os.getenv("OPENWEATHER_API_KEY")
if not api_key:
    raise HTTPException(status_code=500, detail="API key not configured")
```

Build it. Test with real cities and a fake one. Then paste for review.

---

### Step 2E: Project — Multi-City Comparison (45 min)

**This is your Session 2 capstone. No hints.**

**Build** `learning_examples/step_2e_compare.py`:
- `GET /weather/compare?cities=Seattle,Portland,Vancouver`
  - Parse comma-separated city list from query param
  - Fetch all cities **concurrently** using `asyncio.gather()` (from Session 1!)
  - Return results sorted coldest → warmest
  - Handle partial failures: if one city is invalid, include an error for it but return the rest
  - Include `total_time_ms` and `cities_requested` in the response
- `GET /health` → returns `{"status": "ok", "timestamp": "..."}`

You have everything you need: async patterns from Session 1, FastAPI from 2A-2B, httpx from 2C-2D.

Build it, run it, break it. When done, paste your code for review.

---

## Session 3: Ollama + Streaming

**Format for every step**: Requirements → You build → Paste code → Get review

---

### Step 3A: Talk to Ollama Directly (15 min)

**Concept**: Before wrapping a service in FastAPI, always understand its raw API first. Ollama exposes a simple REST API.

**Build** `learning_examples/step_3a_ollama.py` (plain Python, no FastAPI):
- POST to `http://localhost:11434/api/generate` with `{"model": "llama3.2:3b", "prompt": "...", "stream": false}`
- Print the response text
- Time the full request
- Try a few different prompts

**Hints:**
```python
# Response JSON has a "response" key
# Use timeout=60.0 — LLM inference takes time
async with httpx.AsyncClient(timeout=60.0) as client:
    response = await client.post(url, json=payload)
    data = response.json()
    print(data["response"])
```

Build it. Confirm it works before moving on. Then paste for review.

---

### Step 3B: Streaming from Ollama (25 min)

**Concept**: With `stream: true`, Ollama sends back one JSON object per token (newline-delimited). You process them as they arrive instead of waiting for the whole response.

**Build** `learning_examples/step_3b_stream.py`:
- Same Ollama call but `"stream": true`
- Print each token to the terminal **as it arrives** (not all at once at the end)
- Stop when you see `"done": true` in the JSON
- Time how long the first token takes vs total time

**Hints:**
```python
async with client.stream("POST", url, json=payload) as response:
    async for line in response.aiter_lines():
        if line:
            data = json.loads(line)
            print(data["response"], end="", flush=True)
            if data.get("done"):
                break
```

Notice the difference in experience vs 3A. Then paste for review.

---

### Step 3C: FastAPI + StreamingResponse (25 min)

**Concept**: `StreamingResponse` lets you yield data from an async generator, sending each chunk to the client immediately instead of buffering the whole response.

**Build** `learning_examples/step_3c_api.py`:
- `GET /generate?prompt=your+text`
- Returns `StreamingResponse` that streams tokens from Ollama as plain text
- Test with: `curl "http://localhost:8000/generate?prompt=hello+world"`
- You should see tokens appearing one at a time in the terminal

**Hints:**
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

Build it. Test with curl. Then paste for review.

---

### Step 3D: Server-Sent Events Format (30 min)

**Concept**: SSE is a browser-native protocol for one-way streaming. It's just text with a specific format: `data: {content}\n\n`. Browsers handle reconnection automatically.

**Build** `learning_examples/step_3d_sse.py` extending 3C:
- Same `/generate` endpoint but format output as SSE
- Each token: `f"data: {token}\n\n"`
- When Ollama signals `done: true`, yield `data: [DONE]\n\n` then stop
- Media type: `text/event-stream`
- Handle exceptions: yield `data: [ERROR] {message}\n\n` before closing

**Hints:**
```python
# SSE is just a text format — no special library needed
yield f"data: {token}\n\n"  # Two newlines = end of event

# Test with curl:
# curl -N "http://localhost:8000/generate?prompt=hello"
# The -N flag disables buffering so you see output live
```

Build it. Test with curl `-N`. Then paste for review.

---

### Step 3E: Project — Weather AI Streamer (45 min)

**This is the main feature of the whole project. No hints.**

**Build** `learning_examples/step_3e_weather_ai.py`:

- `GET /weather-ai/{city}`
  1. Fetch real weather from OpenWeather (reuse your Session 2 code)
  2. Build a prompt: `f"Weather in {city}: {temp}°C, {description}. Write a friendly 2-sentence summary."`
  3. Stream the Ollama response as SSE
  4. Handle failures from either API gracefully

- `GET /weather-ai/compare?cities=Seattle,Portland`
  1. Fetch weather for all cities concurrently with `gather()`
  2. Build a comparison prompt with all the data
  3. Stream the AI summary as SSE

You've built every piece of this separately. Now combine them.

Build it. Get it working end-to-end. Then paste for review.

---

### Step 3F: Frontend (25 min)

**Concept**: The browser's `EventSource` API is the client-side counterpart to your SSE endpoint. It handles reconnection and message parsing automatically.

**Build** `static/index.html` with vanilla JavaScript:
- Input field for city name + Submit button
- Text area where streamed tokens appear one by one as they arrive
- Loading indicator while waiting for first token
- Error display if the request fails
- "Clear" button to reset

**Hints:**
```javascript
// EventSource connects to your SSE endpoint
const source = new EventSource(`/weather-ai/${city}`);

source.onmessage = (event) => {
    if (event.data === "[DONE]") { source.close(); return; }
    if (event.data.startsWith("[ERROR]")) { /* handle */ return; }
    outputDiv.textContent += event.data;
};

source.onerror = () => { source.close(); };
```

Build it. Serve it through FastAPI's `StaticFiles`. Test the full flow. Then paste for review.

---

## Session 4: Docker Containerization

**Format for every step**: Requirements → You build → Run it → Debug → Paste for review

---

### Step 4A: Dockerfile From Scratch (20 min)

**Concept**: A Dockerfile is a recipe for building a reproducible environment. Layer order matters — Docker caches layers, so put things that change less often (dependencies) before things that change more often (your code).

**Build** `Dockerfile` for the FastAPI app:
- Base: `python:3.12-slim`
- Copy `requirements.txt` first, install dependencies, THEN copy app code (why this order?)
- Expose port 8000
- CMD that runs uvicorn

**Hints:**
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build it: `docker build -t weather-ai .`  
Run it: `docker run -p 8000:8000 weather-ai`  
Then break it intentionally: change your code, rebuild, and notice which layers get cached.

---

### Step 4B: Multi-Stage Build (20 min)

**Concept**: Production images should be small. The build stage needs compilers and build tools; the runtime stage needs only the installed packages. Multi-stage builds let you discard the heavy build stuff.

**Build** a 2-stage `Dockerfile`:
- Stage 1 (`builder`): Install dependencies
- Stage 2 (`runtime`): Copy only installed packages from builder, not the build tools

No hints — research `FROM ... AS builder` and `COPY --from=builder`.

Compare sizes with `docker images` before and after. The difference might surprise you. Paste both Dockerfiles for review.

---

### Step 4C: docker-compose.yml (25 min)

**Concept**: Compose lets services find each other by **service name** as the hostname. Your `api` service doesn't reach Ollama at `localhost` — it reaches it at `http://ollama:11434`.

**Build** `docker-compose.yml`:
- `api` service: built from your Dockerfile, port 8000 exposed
- `ollama` service: `ollama/ollama` image, port 11434
- `api` passes `OPENWEATHER_API_KEY` loaded from a `.env` file
- Volume for ollama models so they persist between `docker-compose down` restarts

**Hints:**
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

Get it running with `docker-compose up`. Confirm `api` can reach `ollama`. Then paste for review.

---

### Step 4D: Project — Full Stack in Docker (45 min)

**The capstone. No hints.**

Get the entire project running in containers end-to-end:

- `docker-compose up` starts everything
- `http://localhost:8000/docs` shows the FastAPI docs
- `http://localhost:8000` serves the HTML frontend
- Weather AI streaming works through containers (frontend → api → ollama + openweather)
- `docker-compose logs -f api` shows live logs
- After `docker-compose down` and `docker-compose up` again, Ollama models are still there

Figure out what breaks and debug it. Common issues to solve:
- The `api` starts before `ollama` is ready (hint: `depends_on` + healthcheck)
- Static files not served (hint: FastAPI `StaticFiles` mount)
- Environment variables not reaching the container
- Ollama model not downloaded inside the container

Document what broke and how you fixed it. Then show the final setup for review.

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
