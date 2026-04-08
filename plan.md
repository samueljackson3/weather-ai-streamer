# Weather AI Streamer - Spec-Driven Learning Project

**Project Type**: Educational | Spec-Driven Development + Python Learning  
**Total Time Budget**: 24-25 hours  
**Learning Approach**: Write lightweight specs → AI generates code → Hands-on refinement  
**Tech Stack**: Python 3.12 • FastAPI • Ollama • Docker • pytest  
**Platform**: M4 MacBook Pro (48GB RAM)  
**Created**: April 8, 2026

---

## 🎯 Project Goals & Requirements

### Primary Learning Objectives

1. **Python Async/Await Fundamentals**
   - Event loops and coroutines
   - Concurrent I/O operations
   - When to use async vs threads vs multiprocessing
   - `asyncio.gather()`, `asyncio.create_task()`, async context managers

2. **FastAPI Framework & Modern API Development**
   - Type hints driving validation and documentation
   - Dependency injection patterns
   - Auto-generated OpenAPI documentation
   - Async HTTP clients (httpx)
   - Error handling and status codes

3. **LLM Streaming & Local Model Deployment**
   - Ollama architecture and local model hosting
   - Streaming responses for better UX
   - Server-Sent Events (SSE) protocol
   - Prompt engineering basics

4. **Docker Containerization**
   - Container vs VM concepts
   - Dockerfile layer optimization
   - Multi-stage builds
   - docker-compose multi-service orchestration
   - ARM64 considerations (M4 Mac)

5. **Testing Async Applications**
   - pytest-asyncio patterns
   - Mocking external APIs
   - Testing streaming endpoints
   - Test fixtures and setup

6. **Spec-Driven Development** (NEW)
   - Design before implementation
   - API contract definition
   - Success criteria specification
   - Using specs as AI prompts

### Secondary Goals

- Production-ready patterns (logging, error handling, configuration)
- Backend development best practices
- AI-assisted development workflows
- Portfolio-worthy documentation

### Non-Goals (Explicitly Out of Scope)

- ❌ Kafka (too complex for 25-hour timeline)
- ❌ Redis/PostgreSQL (not core to learning objectives)
- ❌ React frontend (vanilla JS sufficient for learning)
- ❌ WebSockets (SSE simpler for one-way streaming)
- ❌ Cloud deployment (can be added post-completion)

---

## 🏗️ Application Architecture

### System Design

```
┌─────────────────┐
│  OpenWeather    │ (External API - weather data)
│      API        │
└────────┬────────┘
         │ HTTP Request
         ▼
┌────────────────────────────────────────┐
│      FastAPI Application               │
│  ┌──────────────────────────────────┐  │
│  │  GET /weather-ai/{city}          │  │
│  │  ┌────────────────────────────┐  │  │
│  │  │ 1. Fetch weather data      │  │  │
│  │  │ 2. Format prompt           │  │  │
│  │  │ 3. Call Ollama             │  │  │
│  │  │ 4. Stream LLM response     │  │  │
│  │  └────────────────────────────┘  │  │
│  └──────────────────────────────────┘  │
│                                        │
│  Additional Endpoints:                 │
│  - GET /weather/{city} (raw data)      │
│  - GET /health (service status)        │
│  - GET /docs (auto-generated)          │
└────────┬───────────────────────────────┘
         │ Server-Sent Events (SSE)
         ▼
   ┌─────────────┐
   │  Browser    │ Simple HTML + Vanilla JavaScript
   │  Frontend   │ EventSource API for streaming
   └─────────────┘

  ┌──────────────┐
  │   Ollama     │ (Local LLM Server)
  │ Llama 3.2 3B │ Running on http://localhost:11434
  └──────────────┘
```

### Key Technical Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Framework | FastAPI | Modern async, type hints, auto-docs |
| LLM Provider | Ollama (local) | Free, no rate limits, privacy, learning opportunity |
| Model | Llama 3.2 3B | Fast iteration on M4 Mac, good quality |
| Streaming | Server-Sent Events | Simpler than WebSockets for one-way |
| Frontend | Vanilla JS | Keep focus on backend learning |
| Weather API | OpenWeather | Free tier, simple REST API |
| Testing | pytest-asyncio | Standard for async Python |
| Containerization | Docker + compose | Industry standard, portable |

---

## 📋 Spec-Driven Development Workflow

### Philosophy

**Traditional Learning**: Code first → Debug → Maybe document  
**Spec-Driven Learning**: Design → Spec → AI generates → Refine → Update spec

### Benefits for AI-Assisted Development

1. **Better Prompts**: Detailed specs = better generated code from Copilot
2. **Design Thinking**: Forces consideration of errors, edge cases upfront
3. **Learning Reinforcement**: Writing spec = explaining concepts to yourself
4. **Professional Practice**: Mirrors real-world engineering workflows
5. **Iterative Refinement**: Specs evolve as understanding deepens

### Lightweight Spec Template

Each session includes a ~1-page spec with:

```markdown
# Spec: [Feature/Module Name]

## Problem Statement
[What you're trying to learn/build and why]

## Learning Objectives
- [Specific concept to understand]
- [Pattern to apply]
- [Comparison to make]

## Technical Design
[Simple architecture diagram or bullet points]
[Key components and their interactions]

## API/Code Contract
[Endpoints, function signatures, data structures]
[Inputs, outputs, error cases]

## Success Criteria
- [ ] [Concrete, testable outcome]
- [ ] [Another outcome]
- [ ] [Can explain concept in own words]

## Open Questions
- [Things you're unsure about - research during implementation]

## Testing Strategy
[What to test and how]
```

### Session Workflow (Per Topic)

**Phase 1: Design & Spec** (20-30 min)
- Read concept overview
- Draft lightweight spec
- Define success criteria

**Phase 2: Spec Review** (10 min)
- Prompt AI: "Review this spec - what am I missing?"
- Discuss trade-offs and alternatives
- Refine spec based on feedback

**Phase 3: Implementation** (main session time)
- Provide spec to Copilot as detailed prompt
- Review and understand generated code
- Test against success criteria
- Iterate and refine

**Phase 4: Reflection** (5-10 min)
- Update spec if design changed
- Document learnings
- Note what would be specified differently next time

---

## 🗓️ Course Plan: 6-Session Structure

### Overview Timeline

| Session | Topic | Original | +Spec | Total | Focus |
|---------|-------|----------|-------|-------|-------|
| 1 | Async Fundamentals | 3h | +0.7h | 3.7h | Event loops, coroutines |
| 2 | FastAPI + Weather API | 3h | +0.7h | 3.7h | Type hints, async HTTP |
| 3 | Ollama + Streaming | 5h | +0.7h | 5.7h | LLM integration, SSE |
| 4 | Docker Containerization | 4h | +0.7h | 4.7h | Multi-stage builds, compose |
| 5 | Testing Async Code | 3h | +0.7h | 3.7h | pytest-asyncio, mocking |
| 6 | Polish + Stretch Goal | 2h | +0.5h | 2.5h | Production patterns |
| **TOTAL** | | **20h** | **+4h** | **24h** | |

---

### Session 1: Async Fundamentals (3.7 hours)

**Spec**: `specs/001-async-fundamentals.md`

#### Learning Objectives
- Understand event loops vs traditional threading
- Master `await`, `async def`, `asyncio.gather()`
- Compare concurrent vs parallel vs sequential execution
- Recognize when async provides benefits (I/O bound vs CPU bound)

#### What You'll Build
- `async_learning.py` - Interactive examples demonstrating:
  - Sequential execution (slow)
  - Concurrent execution with `asyncio.gather()` (fast for I/O)
  - Task creation with `asyncio.create_task()`
  - Async context managers

#### Key Concepts
1. **Synchronous blocking** (Rails-style): Each operation waits for I/O
2. **Asynchronous non-blocking**: Event loop juggles multiple paused tasks
3. **When to use async**: Network I/O, file I/O, database queries
4. **When NOT to use async**: CPU-intensive calculations

#### Hands-On Activities
- Run sync vs async examples, observe timing
- Modify delays and task counts
- Intentionally break code (remove `await`) to understand errors
- Trace execution order with print statements

#### Success Criteria
- [ ] Can explain event loop in own words
- [ ] Understand difference between `await` and `asyncio.gather()`
- [ ] Know when async helps vs hurts performance
- [ ] Can write basic async functions

#### Rails Developer Notes
Rails uses threads for concurrency (Thread pools in Puma). Python async is different - single-threaded event loop that switches between tasks during I/O waits. Similar to JavaScript's event loop.

---

### Session 2: FastAPI Basics + Weather API (3.7 hours)

**Spec**: `specs/002-fastapi-weather-api.md`

#### Learning Objectives
- Understand type hints → automatic validation & docs
- Use async HTTP clients (httpx)
- Handle path/query parameters
- Implement error handling with HTTP exceptions
- Explore auto-generated OpenAPI documentation

#### What You'll Build
- `main.py` - FastAPI application with:
  - `GET /weather/{city}` - Fetch raw weather data
  - `GET /` - Health check endpoint
- `models.py` - Pydantic schemas for validation
- `config.py` - Environment-based configuration

#### API Contract

**Endpoint**: `GET /weather/{city}`

**Parameters**:
- `city` (path, string): City name (e.g., "Seattle")
- `units` (query, optional): "metric" | "imperial" (default: metric)

**Response** (200):
```json
{
  "city": "Seattle",
  "temperature": 15.5,
  "description": "cloudy",
  "feels_like": 14.2,
  "humidity": 80
}
```

**Errors**:
- 404: City not found
- 500: Weather API unavailable
- 401: Invalid API key

#### Hands-On Activities
- Test endpoints in auto-generated docs (http://localhost:8000/docs)
- Send invalid requests, observe validation errors
- Compare Pydantic models to Rails strong parameters
- Add new query parameter (language support)

#### Success Criteria
- [ ] Weather endpoint returns valid data
- [ ] Type validation works (try sending wrong types)
- [ ] Error handling graceful for missing city
- [ ] Can explain how Pydantic generates OpenAPI schema

#### Setup Requirements
```bash
# Get OpenWeather API key
# https://openweathermap.org/api (free tier)

pip install "fastapi[standard]" httpx python-dotenv pydantic-settings
echo "OPENWEATHER_API_KEY=your_key_here" > .env
```

---

### Session 3: Ollama Integration + Streaming (5.7 hours)

**Spec**: `specs/003-ollama-streaming.md`

#### Learning Objectives
- Understand local LLM deployment vs cloud APIs
- Implement streaming responses with Server-Sent Events
- Use async context managers for resource management
- Apply prompt engineering for weather summaries
- Handle streaming errors and client disconnects

#### What You'll Build
- `ollama_client.py` - LLM integration module
- `GET /weather-ai/{city}` - Streaming weather + AI summary
- `static/index.html` - Frontend with EventSource API
- Prompt templates for weather summarization

#### Technical Design

**Flow**:
1. Receive city request
2. Fetch weather data from OpenWeather API (async)
3. Format prompt: "Weather in {city}: {temp}°C, {description}. Summarize in friendly way."
4. Stream to Ollama API
5. Yield LLM tokens as Server-Sent Events
6. Client displays tokens as they arrive

**SSE Format**:
```
data: The weather
data:  in Seattle
data:  is quite
data:  pleasant today
```

#### Hands-On Activities
- Test different models (3B vs 7B) and compare speed
- Experiment with prompt styles (formal, casual, poetic)
- Toggle streaming on/off to feel UX difference
- Handle client disconnect mid-stream

#### Success Criteria
- [ ] Ollama installed and running (http://localhost:11434)
- [ ] Streaming endpoint works in browser
- [ ] Can explain SSE protocol vs WebSockets
- [ ] Understand async streaming with `async for`

#### Manual Setup
```bash
# Install Ollama
brew install ollama

# Start server (keep running)
ollama serve

# Download model
ollama pull llama3.2:3b  # ~2GB, 5 min

# Test
ollama run llama3.2:3b "Hello"
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.2:3b",
  "prompt": "Test",
  "stream": true
}'
```

#### Model Recommendations

| Model | Size | Speed (M4) | Quality | Use Case |
|-------|------|------------|---------|----------|
| llama3.2:1b | 1GB | Very fast | Basic | Quick testing |
| llama3.2:3b | 2GB | Fast | Good | **Recommended for learning** |
| llama3.1:8b | 4.7GB | Medium | Great | After basics work |
| mistral:7b | 4GB | Medium | Excellent | Alternative to Llama |

---

### Session 4: Docker Containerization (4.7 hours)

**Spec**: `specs/004-docker-deployment.md`

#### Learning Objectives
- Understand containers vs VMs
- Write multi-stage Dockerfiles for optimization
- Orchestrate multiple services with docker-compose
- Handle environment variables and secrets
- Debug containerized applications

#### What You'll Build
- `Dockerfile` - Multi-stage build for FastAPI app
- `docker-compose.yml` - FastAPI + Ollama services
- `.dockerignore` - Exclude unnecessary files
- `requirements.txt` - Python dependencies

#### Technical Design

**Multi-Stage Build**:
```
Stage 1 (builder): Install dependencies
Stage 2 (runtime): Copy only needed artifacts
Result: Smaller image, faster builds
```

**Services**:
- `api`: FastAPI application (port 8000)
- `ollama`: Ollama server (port 11434)

**Volumes**:
- `ollama_data`: Persist downloaded models

#### Hands-On Activities
- Build image: `docker build -t weather-ai .`
- Observe layer caching (modify code, rebuild)
- Run with compose: `docker-compose up`
- Debug with logs: `docker-compose logs -f api`
- Shell into container: `docker exec -it weather-ai_api_1 /bin/bash`

#### Success Criteria
- [ ] Application runs in container
- [ ] docker-compose starts all services
- [ ] Environment variables passed correctly
- [ ] Can explain layer caching benefits

#### M4 Mac Considerations
```dockerfile
# If needed, specify platform
FROM --platform=linux/arm64 python:3.12-slim

# Ollama automatically uses Metal acceleration on Apple Silicon
```

---

### Session 5: Testing Async Code (3.7 hours)

**Spec**: `specs/005-testing-strategy.md`

#### Learning Objectives
- Test async functions with pytest-asyncio
- Mock external APIs (httpx, Ollama)
- Test streaming endpoints
- Use fixtures for test setup
- Measure test coverage

#### What You'll Build
- `tests/test_weather.py` - Weather endpoint tests
- `tests/test_streaming.py` - SSE streaming tests
- `tests/conftest.py` - Shared fixtures
- `tests/test_async_basics.py` - Async concept tests

#### Testing Strategy

**Unit Tests**:
- Mock all external calls (OpenWeather, Ollama)
- Test individual functions (format_prompt, parse_weather)

**Integration Tests** (Optional):
- Test actual API calls (with rate limiting)
- Test full request flow

**Key Test Cases**:
1. Valid city returns weather data
2. Invalid city returns 404
3. API timeout handled gracefully
4. Streaming interrupted mid-response
5. Environment variables missing

#### Hands-On Activities
- Write test, watch it fail, make it pass (TDD)
- Intentionally break code, verify tests catch it
- Run coverage: `pytest --cov=. --cov-report=html`
- Mock Ollama streaming response

#### Success Criteria
- [ ] All tests pass
- [ ] Can mock async httpx calls
- [ ] Understand `@pytest.mark.asyncio`
- [ ] Test coverage > 80%

#### Setup
```bash
pip install pytest pytest-asyncio pytest-cov pytest-mock

# Run tests
pytest -v

# With coverage
pytest --cov=. --cov-report=html
open htmlcov/index.html
```

---

### Session 6: Polish + Stretch Goal (2.5 hours)

**Choose ONE stretch goal based on interest**

#### Option A: Advanced Async Patterns

**Learn**: Different concurrency primitives

- `asyncio.gather()` vs `asyncio.as_completed()`
- FastAPI background tasks
- Async generators for custom streaming
- Semaphores for rate limiting

**Project**: Fetch weather for multiple cities concurrently

#### Option B: Production Patterns

**Learn**: Production-ready code practices

- Structured logging (JSON logs)
- Health check endpoint (check Ollama availability)
- Environment-based configuration (dev/staging/prod)
- Graceful shutdown

**Project**: Add observability and reliability

#### Option C: Error Handling & Resilience

**Learn**: Building fault-tolerant systems

- Custom exception handlers
- Request/response middleware
- Retry logic with exponential backoff (tenacity)
- Circuit breaker pattern

**Project**: Make system resilient to API failures

#### Success Criteria
- [ ] Completed one stretch goal
- [ ] Can explain trade-offs of chosen approach
- [ ] Documented learnings in README

---

## 📁 Final Project Structure

```
weather-ai-streamer/
├── specs/                          # Spec-driven development docs
│   ├── README.md                   # Spec index + learnings
│   ├── 001-async-fundamentals.md   # Session 1 spec
│   ├── 002-fastapi-weather-api.md  # Session 2 spec
│   ├── 003-ollama-streaming.md     # Session 3 spec
│   ├── 004-docker-deployment.md    # Session 4 spec
│   └── 005-testing-strategy.md     # Session 5 spec
│
├── src/                            # Or flat structure - your choice
│   ├── main.py                     # FastAPI app (~150 lines)
│   ├── ollama_client.py            # LLM integration (~50 lines)
│   ├── models.py                   # Pydantic schemas (~30 lines)
│   └── config.py                   # Settings (~20 lines)
│
├── tests/
│   ├── conftest.py                 # Shared fixtures (~30 lines)
│   ├── test_weather.py             # API tests (~80 lines)
│   ├── test_streaming.py           # SSE tests (~60 lines)
│   └── test_async_basics.py        # Concept tests (~40 lines)
│
├── static/
│   └── index.html                  # Frontend (~100 lines)
│
├── Dockerfile                      # Multi-stage build (~25 lines)
├── docker-compose.yml              # Service orchestration (~30 lines)
├── .dockerignore
├── requirements.txt                # ~10 dependencies
├── .env.example                    # Template for secrets
├── .env                            # Actual secrets (gitignored)
├── .gitignore
├── pytest.ini                      # Test configuration
├── README.md                       # Project overview + learnings
├── LEARNING_LOG.md                 # Session reflections
└── plan.md                         # This file

Total code: ~580 lines (AI writes ~90%, you review/refine)
Total specs: ~6 markdown docs (~1 page each)
```

---

## 🚀 Getting Started

### Prerequisites

**System Requirements**:
- macOS (M4 MacBook Pro)
- 48GB RAM (excellent for running models up to 30B)
- ~20GB disk space (models + Docker images)

**Accounts Needed**:
- GitHub (for version control)
- OpenWeather API account (free tier)

### Initial Setup (30 minutes)

**1. Python Environment**
```bash
cd /Users/samueljackson/dev-ghec/local-projects/weather-ai-streamer

# Install Python 3.12 with pyenv (if not already done)
pyenv install 3.12.0
pyenv local 3.12.0

# Verify
python --version  # Should show 3.12.0

# Create virtual environment
python -m venv venv
source venv/bin/activate
```

**2. Install Ollama** (if not already done)
```bash
# Already ran: brew install ollama

# Start Ollama server (keep terminal open)
ollama serve

# In new terminal: download model
ollama pull llama3.2:3b  # ~2GB, 5 min
ollama list  # Verify

# Test
ollama run llama3.2:3b "Explain async in one sentence"
```

**3. Install Dependencies**
```bash
pip install --upgrade pip
pip install \
  "fastapi[standard]" \
  httpx \
  pytest \
  pytest-asyncio \
  pytest-cov \
  python-dotenv \
  pydantic-settings

# Save to file
pip freeze > requirements.txt
```

**4. Get API Key**
```bash
# 1. Visit: https://openweathermap.org/api
# 2. Sign up (free)
# 3. Generate API key (takes ~10 min to activate)

# Create .env file
echo "OPENWEATHER_API_KEY=your_key_here" > .env
echo "OLLAMA_URL=http://localhost:11434" >> .env

# Create template
cp .env .env.example
# Edit .env.example to remove actual key
```

**5. Initialize Git**
```bash
git init
curl -o .gitignore https://raw.githubusercontent.com/github/gitignore/main/Python.gitignore
echo ".env" >> .gitignore
echo "venv/" >> .gitignore

git add .
git commit -m "Initial commit: Project structure and plan"
```

**6. Verify Setup**
```bash
# Check Python
python --version

# Check FastAPI
python -c "import fastapi; print(fastapi.__version__)"

# Check Ollama
curl http://localhost:11434/api/tags

# Check OpenWeather (replace YOUR_KEY)
curl "https://api.openweathermap.org/data/2.5/weather?q=Seattle&appid=YOUR_KEY"
```

### Ready to Start!

**Next Step**: Create your first spec

```bash
# Option 1: Let AI generate it
# Prompt: "Create spec 001-async-fundamentals.md using the template"

# Option 2: Copy template and fill in
cp specs/template.md specs/001-async-fundamentals.md
# Edit with your understanding
```

---

## 💡 Self-Guided Learning Tips

### Working with AI/Copilot for Spec-Driven Dev

**Phase 1: Design**
```
Prompt: "I'm learning async Python. Help me write a spec for exploring
event loops, coroutines, and concurrent execution. Use the spec template
and include 3-5 concrete examples to build."
```

**Phase 2: Review**
```
Prompt: "Review this spec for Session 1. What concepts am I missing?
What edge cases should I consider? Suggest improvements to the API contract."
```

**Phase 3: Implementation**
```
Prompt: "Implement this design spec: [paste spec]. Generate code with
inline comments explaining each concept. Include timing comparisons."
```

**Phase 4: Understanding**
```
Prompt: "Explain this generated code line-by-line. Why did you use
asyncio.gather() here instead of sequential await?"
```

### Learning Checkpoints

**After Each Session**:
1. ✍️ Update `LEARNING_LOG.md` with 3-sentence summary
2. 🤔 Note one confusing concept to research
3. 💡 Document one "aha!" moment
4. 📊 Update spec with what actually happened vs planned
5. 🔨 Commit with message: `[Session X] Implement {feature} per spec #001`

**Mid-Project (After Session 3)**:
- Review first 3 specs - how did reality diverge?
- Assess: Are specs helping or hindering?
- Adjust template if needed

**End of Project**:
- Compare final code to specs
- Write `specs/README.md` with lessons learned
- Document: "What I'd spec differently next time"

### Iteration Pattern (Per Session)

1. **Read** concept overview (10 min)
2. **Write** lightweight spec (20-30 min)
3. **Review** with AI, refine (10 min)
4. **Generate** code from spec (20 min)
5. **Run** and observe behavior (15 min)
6. **Break** intentionally - test edge cases (20 min)
7. **Fix** and understand why it broke (15 min)
8. **Extend** - add your own twist (30 min)
9. **Update** spec with learnings (10 min)
10. **Reflect** - write log entry (5 min)

### When You Get Stuck

**15-Minute Rule**:
1. Spend 15 min debugging yourself
2. Ask AI with context: "I'm trying X per spec, getting error Y"
3. If still stuck after 30 min total, move on
4. Mark in spec as "Open Question" to return to

**Good Questions to Ask**:
- "Compare my code to the spec - where did I diverge?"
- "Show me 3 ways to solve this spec requirement"
- "This spec assumes X, but what if Y happens?"
- "How would a senior engineer implement this spec?"

### Spec Quality Checks

**Good Specs Are**:
- ✅ Concrete (testable success criteria)
- ✅ Flexible (can evolve as you learn)
- ✅ Concise (1 page, not 10)
- ✅ Honest (includes "Open Questions")

**Bad Specs Are**:
- ❌ Perfect (you're learning, not building production)
- ❌ Rigid (don't get blocked by spec)
- ❌ Vague ("make it work" isn't testable)
- ❌ Exhaustive (don't enumerate every edge case)

---

## 📚 Resources

### Official Documentation
- **FastAPI Tutorial**: https://fastapi.tiangolo.com/tutorial/ (best async Python resource)
- **Ollama Docs**: https://ollama.ai/docs
- **Python asyncio**: https://docs.python.org/3/library/asyncio.html
- **Docker Docs**: https://docs.docker.com/get-started/

### Books
- "Python Concurrency with asyncio" (Manning) - Chapters 1-5 essential
- "Designing Data-Intensive Applications" - Chapter 1 (streams/batching)

### Video Tutorials
- ArjanCodes (YouTube): FastAPI deep dives
- mCoding (YouTube): Python async explained
- freeCodeCamp: FastAPI full course

### Community
- FastAPI Discord: https://discord.com/invite/VQjSZaeJmf
- Python Discord: https://discord.gg/python
- r/FastAPI and r/learnpython subreddits

### Tools
- **httpie**: Better curl for testing APIs (`brew install httpie`)
- **Thunder Client**: VS Code extension for API testing
- **Docker Desktop**: GUI for container management

---

## 🎓 Expected Outcomes

### Technical Skills Acquired

**By Session 3** (12 hours in):
- Write async Python functions confidently
- Build REST APIs with FastAPI
- Integrate local LLMs with streaming
- Understand Server-Sent Events

**By Session 6** (24 hours total):
- Containerize applications with Docker
- Test async code thoroughly
- Design APIs before coding (spec-first)
- Deploy multi-service applications
- Debug production-like issues

### Professional Skills Developed

1. **Spec-Driven Development**: Design → Review → Implement → Iterate
2. **AI-Assisted Coding**: Effective prompting for code generation
3. **Technical Communication**: Writing clear API contracts
4. **Systems Thinking**: Understanding distributed service interactions

### Portfolio Artifacts

1. **Working Application**: Streaming weather AI with local LLM
2. **Spec Documentation**: 6 well-written design specs
3. **Learning Log**: Documented journey and insights
4. **GitHub Repository**: Clean code with good commit history
5. **README with Architecture Diagrams**: Portfolio-ready documentation

### Transferable Knowledge

This project teaches patterns applicable to:
- **Node.js/Deno**: Similar async models
- **Go**: Goroutines conceptually similar to coroutines
- **Rust**: async/await syntax nearly identical
- **Any API development**: REST patterns, error handling
- **Microservices**: Service orchestration, containerization

---

## 🔄 Going Beyond 25 Hours

### Natural Next Steps

**If you enjoyed this** (10-20 more hours):

**Phase 2 Projects**:
1. **Add Kafka**: Event-driven architecture
   - Weather fetcher publishes to topic
   - LLM processor consumes from topic
   - Learn message brokers, pub/sub patterns

2. **Add PostgreSQL**: Persistence layer
   - Store request/response history
   - Learn async ORMs (SQLAlchemy async)
   - Implement rate limiting with DB

3. **Upgrade Frontend**: React + WebSockets
   - Real-time bidirectional communication
   - Learn React hooks for async data
   - Build proper UI components

4. **Cloud Deployment**:
   - Deploy to Railway.app or Render.com
   - Learn CI/CD with GitHub Actions
   - Add monitoring (Prometheus, Grafana)

**Spec-Driven Development Practice**:
- Apply to existing projects (spec your Rails apps!)
- Before building features, write specs first
- Use specs as team communication tool

---

## ✅ Pre-Flight Checklist

Before starting Session 1:

**Environment**:
- [ ] Python 3.12 installed (`python --version`)
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip list`)
- [ ] Ollama running (`curl http://localhost:11434/api/tags`)
- [ ] Llama 3.2 3B downloaded (`ollama list`)
- [ ] OpenWeather API key obtained and in `.env`

**Project Setup**:
- [ ] Git repository initialized
- [ ] `.gitignore` configured
- [ ] Project structure created
- [ ] This plan.md read and understood

**Mindset**:
- [ ] Ready to learn, not just copy code
- [ ] Comfortable asking "why" questions
- [ ] Willing to break things intentionally
- [ ] Excited about spec-driven development

---

## 📞 Getting Help

**Stuck on concepts?**
- Read the "Rails Developer Notes" in each session
- Ask AI to compare to Rails patterns you know
- Search for "Python async explained for Rails developers"

**Spec writing unclear?**
- Look at Session 2 example spec in this plan
- Ask AI: "Convert this code idea to a lightweight spec"
- Start simple - specs improve with practice

**Code not working?**
- Check error message carefully (Python errors are helpful!)
- Verify environment (`.env` loaded, Ollama running)
- Test components individually (weather API, then Ollama, then combined)
- Ask AI: "Debug this error: [paste error + relevant code]"

**Behind schedule?**
- Skip stretch goals (Session 6)
- Use more AI generation, less manual coding
- Focus on understanding over perfection
- Remember: 25 hours is estimate, not deadline

---

## 🎯 Success Metrics

**You've successfully completed this project when**:

- [ ] Can explain async/await to another developer
- [ ] Built working streaming weather AI application
- [ ] Written 6 design specs (doesn't have to be perfect)
- [ ] All tests pass
- [ ] Application runs in Docker
- [ ] Committed code to GitHub with good history
- [ ] Documented learnings in LEARNING_LOG.md
- [ ] Feel confident starting next async Python project
- [ ] Understand how to use specs for AI code generation

**Bonus achievements**:
- [ ] Deployed to cloud (Railway, Render, etc.)
- [ ] Added one stretch goal feature
- [ ] Wrote blog post about learnings
- [ ] Helped someone else learn async Python

---

## 🚦 Ready to Begin?

### Next Immediate Steps

**Right now (5 min)**:
1. Read through this plan fully ✓
2. Verify all tools installed (checklist above)
3. Create `LEARNING_LOG.md` file

**Today (30 min)**:
1. Read Session 1 overview
2. Research: What is an event loop?
3. Draft `specs/001-async-fundamentals.md`

**This session (3.7 hours)**:
1. Complete Session 1: Async Fundamentals
2. Update learning log
3. Commit progress

**Ask your AI assistant**:
- "Let's start Session 1. Create the spec for async fundamentals."
- "Generate async learning examples with timing comparisons."
- "Explain why async is about efficiency, not speed."

---

**Good luck with your learning journey!** 🚀

Remember: Specs are guides, not shackles. If you discover a better approach while coding, update the spec and keep moving. The goal is learning, not perfect documentation.

**Most important**: Have fun! You're learning valuable skills that transfer across the entire modern development ecosystem.
