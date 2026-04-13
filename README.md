# Weather AI Streamer

A learning project combining Python async/await, FastAPI, local LLM streaming (Ollama), and Docker containerization.

**Status**: 🚧 In Progress  
**Learning Approach**: **Rigorous, incremental, hands-on** with AI assistance  
**Time Budget**: 24-25 hours across 6 sessions  
**Updated**: April 8, 2026 - Enhanced with step-by-step rigorous workflow

---

## ⚡ Quick Start

**New to this project?** Start here:
1. Read [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Navigation & commands
2. Read [PROMPTS.md](PROMPTS.md) ⭐ - **Copy-paste prompts for each step**
3. Read [UPDATES.md](UPDATES.md) - Why rigorous approach matters
4. Read [SESSION_WORKFLOW.md](SESSION_WORKFLOW.md) - Learning philosophy
5. Start Session 1: [specs/001-async-fundamentals-rigorous.md](specs/001-async-fundamentals-rigorous.md)

**Important**: 
- Don't ask AI to "do Session X" - work through micro-steps incrementally
- Use prompts from PROMPTS.md - ready to copy-paste into fresh chat windows
- Review generated code carefully before running and experimenting

---

## What This Project Teaches

- **Python async/await fundamentals** - Event loops, coroutines, concurrent I/O
- **FastAPI** - Modern async API development with type hints
- **Local LLM integration** - Ollama streaming responses
- **Server-Sent Events** - Real-time streaming to browser
- **Docker** - Containerization and multi-service orchestration
- **Testing async code** - pytest-asyncio, mocking, fixtures
- **Spec-driven development** - Design before implementation
- **Rigorous learning methodology** - Build, break, fix, understand

## What It Does

Fetches weather data for a city and streams an AI-generated friendly summary using a locally-run LLM (tinyllama).

```
User enters "Seattle" → FastAPI fetches weather → Ollama generates summary → Streams to browser
```

### Architecture Notes
- **LLM Model**: `tinyllama` (1.1B parameters, ~800MB, 5-10s inference on CPU)
- **Containerization**: Docker Compose with custom Ollama image for corporate SSL support
- **Corporate Zscaler Support**: Bakes CA certificate into Ollama image at build time (required for environments with SSL inspection)
- **Performance**: End-to-end latency ~5-10 seconds (suitable for learning project)

---

## 📚 Documentation Structure

### Core Learning Files
- **[PROMPTS.md](PROMPTS.md)** ⭐⭐ - **Copy-paste prompts for each micro-step**
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** ⭐ - Commands, navigation, workflow
- **[plan.md](plan.md)** - Complete 24-hour learning plan
- **[LEARNING_LOG.md](LEARNING_LOG.md)** - Track your progress after each session
- **[SESSION_WORKFLOW.md](SESSION_WORKFLOW.md)** - Why rigorous approach works

### Updates & Changes
- **[UPDATES.md](UPDATES.md)** - Recent improvements to learning methodology
- **[specs/README.md](specs/README.md)** - Spec-driven development guide

### Session-Specific
- **[specs/001-async-fundamentals-rigorous.md](specs/001-async-fundamentals-rigorous.md)** - Session 1 step-by-step
- **[specs/RIGOROUS_TEMPLATE.md](specs/RIGOROUS_TEMPLATE.md)** - Template for Sessions 2-6
- **[specs/template.md](specs/template.md)** - Original spec template

---

## Project Structure

```
weather-ai-streamer/
├── PROMPTS.md              # ⭐⭐ Copy-paste prompts for each step
├── QUICK_REFERENCE.md      # ⭐ Start here - commands & navigation
├── UPDATES.md              # What changed and why
├── SESSION_WORKFLOW.md     # Learning philosophy
├── plan.md                 # Complete learning plan
├── LEARNING_LOG.md         # Your progress journal
├── README.md               # This file
├── specs/                  # Design specifications
│   ├── README.md           # Spec-driven workflow guide
│   ├── template.md         # Spec template
│   ├── RIGOROUS_TEMPLATE.md # Session structure template
│   └── 001-async-fundamentals-rigorous.md # Session 1 steps
├── learning_examples/      # Session 1 code (if completed)
├── src/                    # Application code (Sessions 2-6)
├── tests/                  # Test suite (Session 5)
└── static/                 # Frontend (Session 3)
```

---

## Learning Progress

Track progress in [LEARNING_LOG.md](LEARNING_LOG.md)

- [x] Session 1: Async Fundamentals (3.7h) - Complete
- [x] Session 2: FastAPI + Weather API (3.7h) - Complete
- [x] Session 3: Ollama + Streaming (5.7h) - Complete
- [x] Session 4: Docker + Zscaler SSL (6-7h) - Complete
- [x] Session 5: Performance Optimization (1-2h) - Complete
- [ ] Session 5: Testing (3.7h) - 7-8 steps
- [ ] Session 6: Polish + Stretch Goal (2.5h) - 5-6 steps

**Important**: Each session broken into small incremental steps. Don't rush!

---

## Tech Stack

- **Language**: Python 3.12
- **Web Framework**: FastAPI
- **LLM**: Ollama (Llama 3.2 3B)
- **Async HTTP**: httpx
- **Testing**: pytest + pytest-asyncio
- **Containerization**: Docker + docker-compose
- **Weather API**: OpenWeather (free tier)

---

## Running the Application

_Instructions will be added as the project develops_

---

## Resources

- [Complete Learning Plan](plan.md)
- [Spec Template](specs/template.md)
- [Learning Log](LEARNING_LOG.md)

### External Docs
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [Ollama Documentation](https://ollama.ai/docs)
- [Python asyncio](https://docs.python.org/3/library/asyncio.html)

---

## License

MIT - This is a learning project, feel free to use for your own education.

## Acknowledgments

Built as a personal learning initiative to explore modern Python async patterns, local LLM deployment, and spec-driven development workflows.
