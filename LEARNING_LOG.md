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

## Session 4: Docker Containerization + Corporate SSL

**Date**: April 10-13, 2026  
**Time spent**: ~6-7 hours (estimate: 4.7h)  
**Status**: ✅ Complete — Commit [abc123](https://github.com/samueljackson/weather-ai-streamer) (llama3.2:3b upgrade)

### What I Built
- [x] `Dockerfile` - Multi-stage build (builder + runtime stages)
- [x] `Dockerfile.ollama` - Custom Ollama image with Zscaler cert injection
- [x] `docker-compose.yml` - Service orchestration without version field (avoids deprecation)
- [x] `scripts/ollama-entrypoint.sh` - Startup orchestration for model pull
- [x] Both services running in Docker with health checks and dependency ordering

### Problems Encountered & Solutions

**Problem 1: Zscaler Corporate SSL Certificate Verification**
- **Symptom**: Ollama binary inside container fails to pull models with `x509: certificate signed by unknown authority`
- **Root Cause**: Colima VM (Docker engine on macOS) doesn't have corporate Zscaler CA bundle; Zscaler proxy intercepts HTTPS traffic and re-signs with corporate cert
- **Attempted Solutions**:
  - Mount cert as volume: `/certs/zscaler.pem:/certs/zscaler.pem` — Failed because Docker creates destination as directory, not file
  - Environment variables: `HTTPS_PROXY`, `HTTP_PROXY` — Still failed because cert wasn't trusted
- **Solution Implemented**: Bake certificate into Docker image at build time
  - Extract system cert bundle from macOS: `/tmp/system-certs.pem`
  - Append into `Dockerfile.ollama`: `RUN cat /tmp/zscaler.pem >> /etc/ssl/certs/ca-certificates.crt`
  - Go's crypto/tls runtime reads this file automatically
  - Result: Ollama trusts corporate proxy during model pull ✅
- **Key Learning**: Docker volume mounts require destination path to pre-exist or be a directory parent. For single files, bake into image instead.

**Problem 2: Docker Variable Interpolation in YAML**
- **Symptom**: Shell variables `$!` and `$SERVER_PID` being interpolated by Docker Compose YAML before bash sees them
- **Attempted Solutions**:
  - Escape as `$$!` and `$$SERVER_PID` — Still didn't work because YAML block scalar `-c` flag still processed by Compose
  - Complex quoting — Made it worse
- **Solution Implemented**: Move startup logic to external shell script mounted as `ENTRYPOINT`
  - `scripts/ollama-entrypoint.sh` — Eliminates YAML interpolation entirely
  - `ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]` — Docker runs script directly
  - Result: Shell variables work correctly ✅
- **Key Learning**: Docker Compose processes YAML before any shell runs. If you need shell variables, use external scripts.

**Problem 3: Inference Timeout (30s deadline)**
- **Symptom**: API returns 503 "AI service timed out" after exactly 30 seconds, but Ollama logs show inference completing
- **Root Cause**: Initial model (phi:2.7b, 3B parameters) takes ~30+ seconds for CPU-only inference on 2-core system
- **Solution**: Increased timeout from 30.0s to 120.0s (non-streaming) and 180.0s (streaming) ✅
- **Key Learning**: CPU-only LLM inference is dramatically slower than expected (~30s for 3B model on 2 cores)

**Problem 4: Memory Exhaustion with Large Model**
- **Symptom**: phi:2.7b crashes during inference with OOM: `requested="2.3 GiB" available="1.8 GiB"`
- **Root Cause**: Model was too large; even with container memory set to 5G, Ollama's internal resource tracking prevented loading
- **Solution Implemented**: Switched to tinyllama model
  - phi:2.7b → tinyllama (1.1 billion parameters, ~800MB)
  - Context window: 2048 → 512 (adequate for weather summaries)
  - Container memory: 5G → 2G (tinyllama needs less)
  - Result: Model loads and inference completes in ~5-10s ✅
- **Key Learning**: Model selection matters more than memory allocation. Smaller models are practical for learning projects.

**Problem 5: Model Not Updating After Code Changes**
- **Symptom**: Changed `ollama-entrypoint.sh` to pull `tinyllama` but it still pulled `phi:2.7b` (old model)
- **Root Cause**: Docker layer caching — rebuilt container used cached layers from previous build
- **Solution**: `docker-compose up --build` forces fresh image build
- **Key Learning**: Docker caches layers aggressively. When you change script files, `--build` is required.

### Key Concepts
1. **Multi-stage Dockerfile** - Builder stage compiles dependencies, runtime stage has only application + runtime (smaller image)
2. **Docker Compose Services & Health Checks** - `depends_on` with condition `service_healthy` ensures ordering (API waits for Ollama)
3. **Volume Mounts vs Baked Artifacts** - Mounts are runtime flexible but require pre-existing paths; baking is inflexible but reliable
4. **Shell Script Entrypoints** - Solves variable interpolation issues while keeping orchestration logic centralized
5. **Model Performance Tradeoffs** - Smaller models (800MB tinyllama vs 3GB phi) dramatically impact user experience
6. **Container Resource Limits** - Memory limits on deploy config control what Ollama can access

### Aha Moments
- **Zscaler is transparent SSL inspection**: Rewrites certs on the fly. The proxy isn't a problem; the app just needs to trust the proxy's cert.
- **YAML processes before shell**: This was a major gotcha. Docker Compose reads all variables before bash runs.
- **CPU inference is slow**: 30 seconds isn't a bug; it's expected on 2-core CPU. Accepting this reality led to better model choice.
- **Layer caching helps and hurts**: Great for iterating (build time), terrible when you forget `--build` (confusing behavior).

### Still Confused About / Questions for Next
- **Answered**: Colima memory allocation — The 2G container limit was Docker's own `deploy.resources.limits.memory`. Colima's VM was provisioned at 10GiB total, but the container was capped at 2G by the compose config. These are independent constraints: Colima sets the VM ceiling, Docker `deploy` sets per-container limits.
- Could we use GPU acceleration on Apple silicon within Colima? (Likely no — Metal is not exposed to the Colima VM)
- How would you monitor Ollama's actual memory usage vs allocated limits?

---

## Session 5: Model Quality Upgrade — tinyllama → llama3.2:3b

**Date**: April 13, 2026  
**Time spent**: ~1-2 hours  
**Status**: ✅ Complete

### Context
Session 4 ended with tinyllama working but producing poor-quality summaries — ignoring prompt constraints like "don't mention the city name in the first sentence" and generating generic, unhelpful output. This session upgraded to a model with meaningfully better instruction-following.

### What I Built
- [x] Switched model: tinyllama (1.1B) → llama3.2:3b (3B, Meta's latest small model)
- [x] Raised Colima VM memory: 10GiB → 16GiB to give the larger model headroom
- [x] Raised container memory limit: 2G → 6G
- [x] Raised context window: 512 → 2048 tokens (tinyllama was cutting off its own output at 512)
- [x] Made model config-driven: `settings.ollama_model` instead of hardcoded string in both call sites
- [x] Updated healthcheck to match new model name

### Model Comparison

| Model | Params | Size | Instruction-following | Context | Verdict |
|---|---|---|---|---|---|
| tinyllama | 1.1B | 637MB | Poor — ignores constraints | 512 | Too small |
| phi:2.7b | 2.7B | 1.6GB | Decent — but inconsistent | 2048 | OOM'd at 2G limit |
| llama3.2:3b | 3B | 2.0GB | Good — Meta tuned for instructions | 8192 | ✅ Chosen |
| mistral:7b | 7B | ~4.7GB | Very good | 8192 | Overkill for summaries |

### Infrastructure Changes

**Colima** (the macOS VM running Docker): `colima stop && colima start --memory 16 --cpu 4`
- Host has 48GB RAM; leaving ~32GB for macOS + other work applications
- Colima VM ceiling and Docker container `deploy.resources.limits` are independent constraints — both must be sized

**docker-compose.yml**:
- `OLLAMA_MODEL=llama3.2:3b` passed as env var to API service
- Container memory: `2G → 6G` (model needs ~2.5GB, rest is OS/Ollama overhead)
- Context window: `512 → 2048` (prevents mid-sentence truncation)

**src/config.py**: Added `ollama_model: str = "llama3.2:3b"` — model is now overridable via env var without code changes

### Key Concepts

**1. Model Selection Framework**

The right question isn't "what's the biggest model I can fit?" — it's "what's the minimum capability needed for the task?"

For structured summarization (fixed format, constrained output, deterministic style), the key capability is **instruction-following**, not reasoning depth. Factors to evaluate:

| Factor | Why it matters |
|---|---|
| Fine-tuning type | Instruction-tuned models (llama3.2, mistral-instruct) follow prompt constraints. Base models don't. |
| Parameter count | More params ≠ better at your task. A 3B instruction-tuned model beats a 7B base model for prompts. |
| Quantization | Q4 models are ~4x smaller with ~5% quality loss. Fine for summaries, bad for code generation. |
| Context window | Must be larger than your prompt + expected output. 512 tokens caused truncation mid-sentence. |
| RAM footprint | Rule of thumb: model file size × 1.2 for runtime overhead (KV cache, activations). |

**2. Resource Allocation: Three Independent Layers**

When running LLMs in Docker on macOS, there are three separate memory ceilings — a common source of confusion:

```
macOS Host (48GB)
  └── Colima VM  ← colima start --memory 16    (VM ceiling, hard limit)
        └── Docker Engine
              └── ollama container  ← deploy.resources.limits.memory: 6G  (container ceiling)
                    └── Ollama process  ← OLLAMA_NUM_CTX, model size  (model footprint)
```

- Raising only the container limit without raising Colima does nothing — Docker can't allocate beyond the VM.
- Raising Colima without raising the container limit also does nothing — Docker enforces the lower bound.
- Both must be sized correctly. Always size: `model_size × 1.2 ≤ container_limit ≤ Colima_memory - 2GB (OS overhead)`.

**3. Context Window vs. Model Quality**

A context window that's too small silently degrades output — the model doesn't error, it just truncates its own generation mid-thought. Signs of context starvation:
- Summaries that end abruptly or trail off
- Model repeating itself (attention degrading near window boundary)
- Output that ignores later lines of the prompt (if prompt + output exceeds context)

For weather summaries: prompt is ~80 tokens, expected output ~60 tokens. 512 was marginal. 2048 gives safe headroom.

**4. Config-Driven Model Selection**

Hardcoding a model name in application code is the same anti-pattern as hardcoding an API URL. Correct approach:
- Default in `config.py`: `ollama_model: str = "llama3.2:3b"`
- Override via env var: `OLLAMA_MODEL=mistral:7b` in `.env` or `docker-compose.yml`
- No code changes needed to swap models in different environments

### Key Learning
**Instruction-following quality is not linear with model size.** tinyllama at 1.1B cannot reliably follow multi-constraint prompts ("2-3 sentences", "don't start with city name", "be practical"). llama3.2:3b was specifically fine-tuned by Meta for instruction-following, which is what structured summarization tasks need — not raw intelligence.

### DebugStories (carried forward from Session 4)
- **Issue**: `docker-compose up` took 7+ minutes. Thought Zscaler proxy was slow.
  - **Root cause**: Image layer caching — old Dockerfile still pulled phi:2.7b
  - **Fix**: One flag (`--build`) solved everything
  - **Learning**: Always `--build` when you change Dockerfile or scripts



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
