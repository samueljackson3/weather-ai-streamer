# Approach Updates

**Last updated**: April 8, 2026

## What Changed (and Why)

Session 1 completed in 45 min vs 3.7h estimate — code ran but understanding was shallow (no typing, no breaking, no building from scratch).

**Solution**: Switched to incremental micro-steps. New files created:

| File | Purpose |
|------|---------|
| `SESSION_WORKFLOW.md` | Per-step workflow with knowledge checks |
| `specs/001-async-fundamentals-rigorous.md` | Session 1 micro-steps |
| `specs/RIGOROUS_TEMPLATE.md` | Template for Sessions 2–6 |

## Core Principles

1. **Type code yourself** — no copy-paste
2. **Break it intentionally** — remove `await`, wrong types, skip steps
3. **Build without AI first** — spend 20-30 min on challenges before asking for review
4. **Answer knowledge checks** before asking AI to verify
5. **Match the time estimate** — if done in <40% of estimate, go deeper

## Time Estimates

| Session | Est. Time | Topic |
|---------|-----------|-------|
| 1 | 3.7h | Async fundamentals |
| 2 | 3.7h | FastAPI + Weather API |
| 3 | 5.7h | Ollama + Streaming |
| 4 | 4.7h | Docker |
| 5 | 3.7h | Testing |
| 6 | 2.5h | Polish + stretch goal |

Completing significantly faster than estimate = reading code, not learning it.

## Success Metrics

**Shallow** (avoid): Code runs, can't explain why, can't rebuild from scratch.  
**Deep** (target): Can explain every line, extend confidently, build similar without AI.
