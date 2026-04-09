# Learning Log - Weather AI Streamer

**Project Start Date**: April 8, 2026  
**Learning Approach**: Spec-driven development with AI assistance  
**Total Budget**: 24-25 hours across 6 sessions

---

## How to Use This Log

After each session, record:
1. **Time spent**: Actual hours (compare to estimate)
2. **What I built**: Concrete deliverables
3. **Key concepts**: Main ideas learned
4. **Aha moment**: Most interesting insight
5. **Still confused about**: Honest assessment of what's unclear
6. **Questions for next session**: Carry-forward topics

**Be honest**: This is for you, not for grading. Only through honesty can you identify real gaps.

---

## Session 1: Async Fundamentals

**Date**: April 8, 2026  
**Time spent**: _____ hours (estimate: 3.7h)  
**Spec**: `specs/001-async-fundamentals.md`  
**Status**: ✅ Spec created, Implementation complete and verified

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
1. **Better Step Progression**: Break Steps A-F into finer granularity (A-H perhaps)
   - Step A: Health endpoint only (already good)
   - Step B: Pydantic models (good)
   - Step C: Config (good)
   - Step D: Hardcoded response (good - let them test routing first)
   - Step E: Real API call (SPLIT THIS)
     - E1: Simple fetch without error handling
     - E2: Add error handling for 404, 401, 500s
   - Step F: Input validation (good)
   - Future: Add Step G for async context managers / lifespan

2. **Teach `**kwargs` Unpacking**: Before Pydantic validation, explain what `**data` means
   - Show the equivalence: `HealthResponse(**data) == HealthResponse(status="ok", version="0.1.0")`
   - This helps understand Pydantic's magic

3. **Better Error Testing**: Add explicit section for "test these error scenarios"
   - Empty city name → 400
   - Non-existent city → 404
   - Invalid units enum → 422
   - Include expected response bodies in examples

4. **Production Readiness Earlier**: SSL verification, environment variables weren't emphasized enough
   - Move to Step C or create Step C.5 for environment-aware config
   - Show how `VERIFY_SSL=false` in dev, `VERIFY_SSL=true` in prod

5. **Concept Checks with Explanations**: Great to ask questions, but when user answer is incomplete:
   - Explain WHY the full answer matters
   - Show what goes wrong with the incomplete understanding
   - Example: "SSL verification disabled is a security risk because..."

6. **Code Comments**: Add more inline explanations of FastAPI magic
   - Why `response_model=WeatherResponse` (validates output, powers docs)
   - Why `-> WeatherResponse` return type hint (helps IDE, helps type checker)
   - Why separate `fetch_weather()` function (testable, reusable)

7. **Testing Preview**: Add note about pytest-asyncio patterns early
   - Shows how the business logic is designed to be testable
   - Motivates the separation of concerns

### What Worked Well
✅ Spec-driven approach - knowing where we were going helped prioritize
✅ Progressive steps - each step built on previous, clear learning
✅ Real API integration - not just mocks, actual OpenWeather calls
✅ Error handling from day 1 - made it feel production-ready
✅ Concept checks - forced understanding, not just typing code
✅ Config as part of core - showed best practices early
✅ Pydantic's auto-docs - magic moment when `/docs` worked perfectly

### What To Improve
⚠️ SSL certificate issue - wasted time on macOS SSL verification
  → Document this upfront: "On macOS, you may need `VERIFY_SSL=false` in .env"
⚠️ Step E too large - combining real API call + error handling at once
  → Split into E1 (basic fetch), E2 (error handling)
⚠️ Didn't explain `**kwargs` unpacking before using it
  → Add 2-minute explanation before Pydantic models
⚠️ Didn't emphasize lifespan/dependency injection until end
  → Move Step F note about `Depends()` earlier as preview

### Questions for Next Session
1. How does FastAPI use async under the hood for handling requests?
2. What's the difference between `httpx.AsyncClient` and regular `requests` library?
3. Can you mix sync and async code in the same FastAPI app? 

### Spec Accuracy
- [ ] Spec matched implementation closely
- [ ] Spec needed significant revision
- [ ] Spec was helpful for AI code generation
- [ ] Spec was too rigid/detailed
- [ ] Spec was too vague

### Notes
_Any other observations, struggles, or wins_


---

## Session 2: FastAPI + Weather API

**Date**: _____________  
**Time spent**: _____ hours (estimate: 3.7h)  
**Spec**: `specs/002-fastapi-weather-api.md`

### What I Built
- [ ] `main.py` - FastAPI application
- [ ] `models.py` - Pydantic schemas
- [ ] `config.py` - Environment configuration
- [ ] Weather endpoint with OpenWeather API

### Key Concepts
1. 
2. 
3. 

### Aha Moment



### Still Confused About



### Questions for Next Session
1. 
2. 

### Spec Accuracy
- [ ] Spec matched implementation closely
- [ ] Spec needed significant revision
- [ ] Spec was helpful for AI code generation

### Comparison to Rails
_How does this compare to Rails patterns I know?_


### Notes



---

## Session 3: Ollama + Streaming

**Date**: _____________  
**Time spent**: _____ hours (estimate: 5.7h)  
**Spec**: `specs/003-ollama-streaming.md`

### What I Built
- [ ] `ollama_client.py` - LLM integration
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

### Aha Moment



### Still Confused About



### Debugging Stories
_What broke? How did you fix it?_


### Spec Accuracy
- [ ] Spec matched implementation closely
- [ ] Spec needed significant revision

### Notes



---

## Session 5: Testing Async Code

**Date**: _____________  
**Time spent**: _____ hours (estimate: 3.7h)  
**Spec**: `specs/005-testing-strategy.md`

### What I Built
- [ ] `tests/test_weather.py` - API tests
- [ ] `tests/test_streaming.py` - SSE tests
- [ ] `tests/conftest.py` - Fixtures
- [ ] All tests passing

### Test Coverage
**Coverage**: _____%  
**Target**: 80%+

### Key Concepts
1. 
2. 
3. 

### Aha Moment



### Still Confused About



### Spec Accuracy
- [ ] Spec matched implementation closely
- [ ] Spec needed significant revision

### Notes



---

## Session 6: Polish + Stretch Goal

**Date**: _____________  
**Time spent**: _____ hours (estimate: 2.5h)  
**Stretch goal chosen**: _______________

### What I Built
- [ ] Completed stretch goal
- [ ] Production patterns added
- [ ] Final polish and cleanup

### Key Concepts
1. 
2. 
3. 

### Aha Moment



### Final Reflections
_What would you do differently? What surprised you most?_


---

## Overall Project Reflection

**Total time spent**: _____ hours (estimate: 24-25h)  
**Completion date**: _____________

### Biggest Wins
1. 
2. 
3. 

### Biggest Challenges
1. 
2. 
3. 

### Top 3 Learnings
1. 
2. 
3. 

### Spec-Driven Development Assessment

**Did specs help or hinder?**


**Would you use specs again?**


**What would you change about the spec process?**


### What's Next?
_Future projects or topics to explore_

1. 
2. 
3. 

### Advice to Past Self
_What would you tell yourself at the start?_


---

## Running Log of Questions & Answers

_Use this section to track questions that arise and get answered throughout the project_

**Q**: 
**A**: 
**When**: 

---

**Q**: 
**A**: 
**When**: 

---

**Q**: 
**A**: 
**When**: 

---

## Resources That Helped

_Keep track of useful docs, tutorials, Stack Overflow posts, etc._

- **Topic**: [Link or description]
  - Why it helped: 

---

## Code Snippets Worth Remembering

_Patterns or techniques you want to reuse_

```python
# Description
# Code
```

---

## Mistakes & Lessons

_Document errors and what you learned from them_

**Mistake**: 
**Lesson**: 
**Fix**: 

---

**Mistake**: 
**Lesson**: 
**Fix**: 
