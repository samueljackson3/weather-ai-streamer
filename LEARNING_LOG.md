# Learning Log - Weather AI Streamer

**Start**: April 8, 2026 | **Budget**: 24-25h across 6 sessions | **Approach**: Spec-driven, incremental micro-steps

---

## Session 1: Async Fundamentals

**Date**: April 8, 2026  
**Time spent**: _____ hours (estimate: 3.7h)  
**Spec**: `specs/001-async-fundamentals.md`  
**Status**: ✅ Complete

### What I Built
- [x] `specs/001-async-fundamentals.md` - Detailed spec with learning objectives and success criteria
- [x] `learning_examples/async_learning.py` - 5 interactive examples demonstrating:
  - Example 1: Sequential execution baseline (~6s)
  - Example 2: Concurrent execution with `asyncio.gather()` (~2s - 3x faster!)
  - Example 3: Manual task creation with `create_task()`
  - Example 4: Async context managers for resource management
  - Example 5: Error handling with `return_exceptions=True`
- [x] `learning_examples/README.md` - Comprehensive guide with experiments and deep dives
- [x] All examples verified to run successfully with correct timing

### Key Concepts
1. **Event Loop**: Single-threaded loop that switches between tasks during `await` points (cooperative multitasking)
2. **Concurrent vs Sequential**: Sequential time = sum of delays (6s), Concurrent time = max delay (2s)
3. **When Async Helps**: I/O-bound operations (network, files, DB) - not CPU-bound calculations
4. **gather() vs create_task()**: gather() for batch operations, create_task() for fine-grained control
5. **Async Context Managers**: `__aenter__`/`__aexit__` for resources requiring async setup/teardown
6. **Error Handling**: `return_exceptions=True` prevents one failure from breaking all concurrent tasks

### Aha Moment
_Ready to fill in after running the examples hands-on:_
- Seeing the timestamps prove concurrent execution runs all tasks "simultaneously"
- Understanding that `await` is the key point where event loop can switch tasks
- Realizing async ≠ parallel (still single-threaded, just better I/O management)

### Still Confused About
_To explore during implementation:_
- How does the event loop decide which task to run next? (epoll/kqueue internals)
- What happens if you forget `await` on a long-running coroutine?
- Performance characteristics: How many concurrent tasks is too many?

---

## Session 2: FastAPI Basics + Weather API

**Date**: April 9, 2026  
**Time spent**: ~4.5 hours (estimate: 3.7h)  
**Spec**: `specs/002-fastapi-weather-api.md`  
**Status**: ✅ Complete — Commit [893c269](https://github.com/samueljackson/weather-ai-streamer/commit/893c269)  
**Git Commit**: `feat(session-2): Complete FastAPI weather API with real OpenWeather integration`

### What I Built
- [x] `src/config.py` - Settings from `.env` with validation (fail-fast principle)
  - `openweather_api_key`, `openweather_base_url`, `ollama_url`, `app_version`, `verify_ssl`
  - Pydantic validates types at startup (errors before app runs)

- [x] `src/models.py` - Type-safe request/response schemas
  - `HealthResponse` - Simple health check (status: string, version: string)
  - `Units` - Enum for temperature units (metric, imperial, standard)
  - `WeatherResponse` - Full weather data with 8 fields

- [x] `src/main.py` - Production-ready FastAPI application
  - `GET /health` - Liveness check, auto-docs
  - `GET /weather/{city}` - Real OpenWeather API integration
  - Business logic function `fetch_weather()` - Testable in isolation
  - Input validation - City name 2-50 chars, whitespace handled
  - Error handling - 400, 404, 401, 503 with clear messages
  - Async HTTP client (`httpx.AsyncClient`) - Non-blocking I/O

### Key Concepts Learned

1. **Type Hints as Contracts** 
   - Type hints → Pydantic validation (automatic)
   - Type hints → Auto-generated OpenAPI docs (free!)
   - Type hints → IDE autocomplete (better DX)

2. **Pydantic: Automatic Validation**
   - Define schema once → validates input & output automatically
   - Enums: FastAPI rejects invalid values in query params
   - `model_config` controls behavior (env_file, case_sensitive, etc.)

3. **Configuration Management**
   - `pydantic-settings` reads `.env` automatically
   - Validation happens at startup (fail-fast, not at first request)
   - Missing required fields → clear error at launch, not at runtime
   - Compare to Rails: `ENV['KEY']` returns nil silently; Pydantic fails loud

4. **Separation of Concerns**
   - Route handlers (`get_weather`) - HTTP concerns, validation
   - Business logic (`fetch_weather`) - Pure async, testable, reusable
   - Session 3 will import `fetch_weather` for Ollama integration

5. **Error Handling Hierarchy**
   - Input validation first (400 Bad Request)
   - API-specific errors (404 City not found, 401 Invalid key)
   - Network errors (503 Service unavailable, timeout)
   - Each error has helpful detail message for debugging

6. **Async HTTP Clients**
   - `httpx.AsyncClient` (not `requests`) for async context
   - Connection pooling for performance
   - `verify=settings.verify_ssl` - environment-aware SSL handling

### Aha Moments
- **`**data` unpacking**: Takes dict and turns into kwargs for Pydantic validation
- **Why separate business logic**: Testing without spinning up FastAPI app, reusable across routes
- **Why route handlers validate input**: Clearer error messages, early rejection, less API chatter
- **OpenAPI docs auto-generation**: Zero manual work; type hints + Pydantic = complete documentation

### Still Confused About / Questions for Next
- How to do lifespan management (create one client shared across requests)? → Session 3/4
- How to test this without hitting real OpenWeather API? → Session 5 (mocking with pytest)
- What's the difference between `Field()` and Query parameters in Pydantic? → Will explore in Step F+
- Environment variables: How do you handle secrets safely in production? → Beyond scope for now

### Improvements for Future Sessions
### Improvements Noted
- Split Step E: basic fetch first, then error handling separately
- Explain `**kwargs` unpacking before Pydantic models
- macOS SSL: document `VERIFY_SSL=false` upfront
- Add error scenario test list (empty city → 400, bad city → 404, bad enum → 422)

### What Worked / What To Improve
✅ Spec-driven approach, progressive steps, real API from day 1, concept checks  
⚠️ SSL cert issue, Step E too large, `**kwargs` not explained upfront

### Questions for Session 3
1. How does FastAPI handle async requests under the hood?
2. Difference between `httpx.AsyncClient` and `requests`?
3. Can you mix sync and async in the same FastAPI app?

---

## Session 3: Ollama Integration + Streaming API

**Date**: April 9-10, 2026  
**Time spent**: ~5-6 hours (estimate: 5.7h)  
**Spec**: `specs/003-ollama-integration.md`  
**Status**: ✅ Complete — Commits [df3c941](https://github.com/samueljackson/weather-ai-streamer/commit/df3c941), [32f8dad](https://github.com/samueljackson/weather-ai-streamer/commit/32f8dad)  
**Git Commits**: 
- `feat: streaming responses, location parameters, and capstone project spec`
- `feat(session-3): Add error handling for streaming failures (Capstone 1)`

### What I Built

**Core Implementation:**
- [x] `src/ollama_client.py` - Ollama HTTP client module
  - `build_weather_prompt()` - Formats WeatherResponse into natural language prompt for LLM
  - `call_ollama()` - Async non-streaming request to Ollama (wait for complete response)
  - `stream_ollama_summary()` - Async generator for streaming tokens as Server-Sent Events (SSE)
  - Error handling: ConnectError, TimeoutException, generic exceptions → yielded as SSE `data: [ERROR]...` events

- [x] `src/main.py` - Extended with new route
  - `GET /weather-ai/{city}` - New endpoint combining weather fetch + LLM summarization
  - `get_http_client()` - Dependency injector for httpx.AsyncClient (keeps client alive during response)
  - Query params: `units` (metric|imperial|standard), `stream` (boolean)
  - Non-streaming (default): Returns `{"city": "...", "summary": "..."}`  (HTTP 503 error handling)
  - Streaming: Returns `text/event-stream` with tokens as `data: token\n\n` (in-band error handling)

- [x] `specs/003-ollama-integration.md` - Detailed spec with micro-steps, knowledge checks, 5 capstone projects

**Bonus (User Initiative):**
- [x] `static/index.html` - Full HTML/CSS/JS UI
  - Cloud animations background
  - Form inputs: city name, units, stream checkbox
  - Real-time streaming display (EventSource API)
  - Error banner with dismiss button
  - Responsive design (mobile-friendly)
  - **Why this matters**: Turns spec validation into usable product. Shows feedback loops in real time.

### Key Concepts Learned

1. **Ollama HTTP API (Wire Protocol)**
   - Non-streaming: POST with `stream=false` → single JSON response with full text
   - Streaming: POST with `stream=true` → newline-delimited JSON, one token per line
   - Each line: `{"model":"...", "response":"token", "done":false}` until `"done":true`
   - Tokens are sub-word (e.g., `"2"`, `" +"`, not whole words)

2. **AsyncGenerator + StreamingResponse**
   - `async def` function with `yield` → lazy evaluation, pull-based
   - `StreamingResponse(async_gen)` → FastAPI pulls values on-demand without buffering
   - Memory efficient: doesn't load entire response into RAM
   - Compare: blocking generator would buffer, streaming wouldn't

3. **Error Handling: Request-Response vs Streaming**
   - **Request-Response**: Exception → HTTP 503 (sent BEFORE response starts) ✅ Clean
   - **Streaming**: Exception happens AFTER HTTP 200 sent → can't change status code ❌
   - **Solution**: Errors go in-band via SSE: `data: [ERROR] message\n\n`
   - **Key learning**: You can't send HTTP error codes after streaming starts. Headers are already sent.

4. **Dependency Injection for Resource Management**
   - `async def get_http_client()` with `yield` inside `async with` context manager
   - FastAPI calls this before route handler, cleans up after
   - For streaming: Client stays alive for entire response duration (not just route handler)
   - Why it works: FastAPI holds dependency alive through the full response lifecycle

5. **Prompt Engineering (Domain-Specific String Formatting)**
   - Good prompts: specific (actual temp/humidity), actionable (what to wear), practical (fabric types)
   - Testing: tried with hot day (Phoenix), cold day (Minneapolis) → adapts well
   - Bad prompts: vague ("nice day"), generic advice ("dress appropriately"), ignore facts
   - **Key insight**: Prompt quality directly impacts LLM output quality. Test early.

6. **Server-Sent Events (SSE) vs WebSockets**
   - **SSE**: One-way (server → client), uses regular HTTP, client-side `EventSource`, simple
   - **WebSockets**: Bidirectional, persistent TCP, more complex, better for real-time chat
   - For weather: SSE sufficient (uni-directional only), simpler to implement and deploy

7. **Capstone 1: Streaming Error Handling**
   - Bug: If Ollama dies, client sees silent connection close (no error message)
   - Fix: Wrap `stream_ollama_summary()` in try-except, yield errors via SSE format
   - Learning: Streaming error handling is fundamentally different from request-response
   - Impact: Users now see helpful error message instead of hanging connection

### Aha Moments
- **Why Ollama streaming works**: HTTP response body is just newline-delimited JSON. No special magic, just reading lines as they arrive.
- **The HTTP status code lock**: Once you send those first bytes (`HTTP/1.1 200`), you're committed to that status. Can't change it. Game-changing realization.
- **AsyncGenerator mental model**: Think of it as a "lazy list" that produces values on-demand. FastAPI pulls from it without knowing how many values there are.
- **Why `.stream()` not `.post()`**: `.post()` waits for entire body in memory. `.stream()` reads incrementally. For long responses, `.stream()` uses much less memory.

### Still Confused About / Open Questions
- What happens if client disconnects mid-stream? Does Ollama keep generating on the server? (Not tested, would need async signal handling)
- Could I use ngrok/proxy to test mid-stream Ollama failure without killing the actual process?
- How would you load-balance multiple Ollama instances behind this API? (Would need health checks, round-robin)

### Quiz Answers (Knowledge Checks from Spec)
1. ✅ Why reuse `fetch_weather()`? Separation of concerns + testable + DRY
2. ✅ Why can't raise HTTPException after streaming starts? HTTP status code sent on first byte
3. ⚠️ AsyncGenerator: lazy function with `yield`, StremingResponse pulls values on-demand without buffering
4. ✅ `.post()` waits for full body, `.stream()` reads incrementally
5. ⚠️ SSE: one-way (server→client), simpler, works over HTTP. WebSockets: bidirectional, persistent, better for chat
6. ✅ Tested: Streaming with Ollama down → connection closes. Fixed: now sends `data: [ERROR]...` instead
7. ✅ `Depends()` keeps client alive for entire respon**se lifecycle (request start → response end, including streaming duration)

### Capstone Projects Attempted
**Capstone 1: Error Handling in Streams** ✅ IMPLEMENTED
- Problem: Silent connection close when Ollama dies mid-stream
- Solution: Wrap generator in try-except, yield errors as SSE events
- Result: Users see `data: [ERROR] Failed to connect...` instead of silence
- Learning: Streams change the error handling game entirely

**Other Capstones** (not yet attempted, available for future depth):
- Capstone 2: Model selection (`?model=llama3.2:1b` vs `3b`)
- Capstone 3: Prompt styling (`?style=casual|formal|poetic`)
- Capstone 4: Batch weather-AI with `asyncio.gather()`
- Capstone 5: In-memory caching with TTL

### Model Performance Notes
- **Model Used**: `llama3.2:3b` (3.2 billion parameters, Q4_K_M quantization)
- **Speed**: ~1-2 seconds end-to-end (weather fetch + LLM generation)
- **Quality**: Very practical weather summaries (specific fabrics, accessories, not generic)
- **Resource**: Runs on M4 Mac without freezing system
- **Not tested**: `llama3.2:1b` vs `3b` speed/quality trade-off (future capstone)

### Spec Accuracy
- ✅ Spec matched implementation closely
- ✅ Micro-steps were well-ordered (A→B→C→D→E→F)
- ✅ Knowledge checks pushed real learning (not just reading)
- ⚠️ Mid-stream error testing is harder than listed; tested ConnectError instead
- 🎯 Updated spec: Removed answer keys, added 5 capstones, added UI note

### User Initiative Notes
**UI Beyond Spec**: 
- Built full HTML/CSS/JavaScript UI (`static/index.html`)
- Features: Cloud animations, form inputs, real-time streaming display via EventSource API, error banners
- Purpose: Test API through UI instead of just curl → much better feedback loop and usability
- **Why important**: Turns theoretical API into tangible product. Reveals UX issues curl doesn't (slow rendering, error visibility, form feedback)
- **Lesson**: Building a UI forces you to understand the API contract better (what fields matter, error cases users see, response times feeling)

### Questions for Session 4
1. How would you load-balance multiple Ollama instances? (health checks, round-robin, sticky sessions?)
2. What's the best way to test streaming endpoints with proper async mocking?
3. Should we add authentication to the `/weather-ai` endpoint?
4. How would you add request logging (LLM calls, response times, tokens generated)?

### Improvements for Future Sessions
- ✅ Knowledge checks without answers (user writes answers, we discuss)
- ✅ Capstone projects with varying difficulty (mini-tasks to deepen learning)
- ✅ Mix theory + hands-on early (not theory heavy) 
- ⚠️ Streaming error testing requires more setup; note that ConnectError is realistic, mid-stream is harder to replicate
- 🎯 Emphasize dependency injection pattern earlier (it's important for resource management)





---

## Session 4: Docker Containerization

**Date**: _____________  
**Time spent**: _____ hours (estimate: 4.7h)  
**Spec**: `specs/004-docker-deployment.md`

### What I Built
- [ ] `Dockerfile` - Multi-stage build
- [ ] `docker-compose.yml` - Service orchestration
- [ ] Successfully containerized application
- [ ] All services running in Docker

### Key Concepts
1.
2.
3.

### Aha Moment / Still Confused About / Questions for Next



---

## Session 4: Docker Containerization

**Date**: _____________  
**Time spent**: _____ hours (estimate: 4.7h)

### What I Built
- [ ] `Dockerfile` — Multi-stage build
- [ ] `docker-compose.yml` — Service orchestration
- [ ] All services running in Docker

### Key Concepts / Aha Moment / Still Confused About / Debugging Stories



---

## Session 5: Testing Async Code

**Date**: _____________  
**Time spent**: _____ hours (estimate: 3.7h)  
**Coverage**: ____% (target 80%+)

### What I Built
- [ ] `tests/test_weather.py`, `tests/test_streaming.py`, `tests/conftest.py`

### Key Concepts / Aha Moment / Still Confused About



---

## Session 6: Polish + Stretch Goal

**Date**: _____________  
**Time spent**: _____ hours (estimate: 2.5h)  
**Stretch goal**: _______________

### What I Built / Final Reflections



---

## Overall Reflection

**Total time**: _____ hours (estimate: 24-25h)

### Biggest Wins / Challenges / Top Learnings



### Did specs help or hinder? What would you do differently?



---

## Notes, Snippets & Mistakes

_Running log — add as you go_
