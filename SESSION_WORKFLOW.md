# Rigorous Session Workflow

**Rule**: Never say "Do Session X." Work through micro-steps: generate → type yourself → run → break → fix → extend.

---

## 📋 Session Structure

### Phase 1: Foundation (30-45 min)
1. Generate minimal example
2. Run and observe
3. Break it intentionally → fix it → understand why
4. Ask conceptual question, extend with your own variation

**Knowledge check** (after each micro-step): What didn't you predict? Why did that error appear? Can you explain each line without comments?

### Phase 2: Core Learning (1-2 hours)
- Add one piece of complexity at a time, run tests after each
- Compare against previous version

**Knowledge check**: What changed in behavior and why? What breaks if you remove what you just added?

### Phase 3: Experimentation (45-60 min)
- Modify behavior, debug broken examples, combine patterns

**Knowledge check** (before): What's your hypothesis? (after): Was it right? What surprised you?

### Phase 4: Integration (30-45 min)
- Build something not in the spec, refactor earlier code

**Phase 4 Knowledge Check** (mid-integration and at end):
- Can you describe what you're building without referencing the earlier examples?
- What decision did you make differently than the provided examples? Why?
- Where did you reach for AI help? What does that reveal?

### Phase 5: Reflection (15-20 min)
**Solidify understanding**:
- Update learning log
- Write explanations in own words
- List remaining questions

**Knowledge check** (final gate — no notes):
1. Explain the session's core concept in 2-3 sentences.
2. What's the most common mistake someone new to this would make?
3. What would you apply in real code tomorrow?
4. Rate each learning objective (1–5). Any below 3 → revisit before next session.
5. What question do you want answered next session?

---

## Prompt Templates

**Generate snippet** (keep small):
```
Generate [specific thing] that:
- [Requirement 1]
- [Requirement 2]
Keep under [N] lines. I'll type it myself.
```

**Break it** (learn from errors):
```
Show me what happens if I: [remove/modify X], [wrong type for Y], [skip step Z].
For each, what error and why?
```

**Concept check** (test your understanding):
```
I think [concept] works like this: [your explanation]. Am I right? What am I missing?
```

**Code review** (after building yourself):
```
Review my code for correctness, best practices, performance, production readiness.
[Paste code]
```

---

---

## Session 1: Async Fundamentals

**Spec**: `specs/001-async-fundamentals-rigorous.md` | **Prompts**: `PROMPTS.md` → Session 1

| Step | Time | Topic |
|------|------|-------|
| 1A | 10 min | Simplest async function |
| 1B | 15 min | Sync vs async comparison |
| 1C | 20 min | `gather()` concurrent execution |
| 1D | 20 min | `create_task()` manual control |
| 1E | 20 min | Error handling |
| 1F | 30 min | Build your own (weather sim) |
| 1G | 20 min | Real-world patterns (httpx, aiofiles) |
| 1H | 20 min | Concept self-test |
| Buffer | 45 min | Debug time, re-runs |
| **Total** | **3.7h** | |

**Final confidence table** (fill after 1H):
| Concept | Rating (1–5) | Gap |
|---------|-------------|-----|
| async/await mechanics | | |
| gather() vs create_task() | | |
| When async helps (and doesn't) | | |
| Event loop mental model | | |
| Error handling in async | | |

Any rating below 3 → revisit that step before Session 2.

---

## Per-Step Quality Checklist

After each step:
- [ ] Typed the code myself (no copy-paste)
- [ ] Ran it and observed output
- [ ] Broke it intentionally and fixed it
- [ ] Answered the knowledge check before asking AI
- [ ] Can explain this to someone without notes

If 2+ are "no" → slow down, engage more deeply.

---

## When Stuck

1. Spend 5 min debugging yourself first
2. Read the error message carefully
3. Check your changes vs the working version
4. Ask AI with context:

```
I modified X to Y because I wanted Z.
Got error: [paste]
I think it's because [hypothesis]. Am I on the right track?
```
