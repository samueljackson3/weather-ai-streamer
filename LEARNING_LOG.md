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

## Session 3: Ollama + Streaming

**Date**: _____________  
**Time spent**: _____ hours (estimate: 5.7h)  
**Spec**: `specs/003-ollama-streaming.md`

### What I Built
- [ ] Ollama client integration
- [ ] Streaming endpoint with SSE
- [ ] Frontend with EventSource API
- [ ] Prompt engineering for weather

### Key Concepts
1. 
2. 
3. 

### Aha Moment



### Still Confused About



### Questions for Next Session
1. 
2. 

### Model Performance Notes
_Which models did you try? Speed/quality trade-offs?_


### Spec Accuracy
- [ ] Spec matched implementation closely
- [ ] Spec needed significant revision

### Notes



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
