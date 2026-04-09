# Quick Reference - Rigorous Learning Workflow

**Updated**: April 8, 2026 | **For**: Weather AI Streamer Learning Project

---

## 📁 File Navigation

| File | Use When |
|------|----------|
| **PROMPTS.md** ⭐ | Copy-paste prompts for each micro-step |
| **UPDATES.md** | Understanding what changed and why |
| **SESSION_WORKFLOW.md** | Understanding the philosophy of rigorous learning |
| **plan.md** | Getting overview of all 6 sessions |
| **LEARNING_LOG.md** | Recording progress after each session |
| **specs/001-async-fundamentals-rigorous.md** | Working through Session 1 step-by-step |
| **specs/RIGOROUS_TEMPLATE.md** | Structuring Sessions 2-6 |
| **specs/README.md** | Understanding spec-driven development |

---

## ⚡ Quick Start Commands

### Redo Session 1 Rigorously
```bash
cd /Users/samueljackson/dev-ghec/local-projects/weather-ai-streamer
mv learning_examples learning_examples_first_pass
mkdir learning_examples
cd learning_examples
```

**Then prompt**:
```
"Session 1, Step 1A from specs/001-async-fundamentals-rigorous.md:
Generate the simplest async function with asyncio.sleep(1), 
prints before/after, timing. Under 15 lines."
```

### Start Session 2 Rigorously
```bash
mkdir session2_work
cd session2_work
```

**Then prompt**:
```
"Session 2, Step 2A: Generate simplest FastAPI endpoint:
- One GET route /hello
- Returns JSON
- Under 12 lines
I'll type it myself."
```

---

## 🎯 Prompt Templates

### Generate Code (Small Snippet)
```
"Generate [specific thing] that:
- [Requirement 1]
- [Requirement 2]
Keep under [N] lines. I'll type it myself."
```

### Break Code (Learn from Errors)
```
"Show me what happens if I:
1. [Remove/modify X]
2. [Use wrong type for Y]
3. [Skip step Z]

For each, what error and why?"
```

### Concept Check (Test Understanding)
```
"I think [concept] works like this: [your explanation]

Am I right? What am I missing?"
```

### Code Review (After Building Yourself)
```
"Review my code for:
- Correctness
- Best practices
- Performance
- Production readiness

[Paste your code]"
```

### Extend Code (Your Own Experiment)
```
"I want to add [feature] to this code.
Give me hints, not full solution.

[Paste current code]"
```

---

## ⏱️ Time Expectations

| Session | Est. Time | Note |
|---------|-----------|------|
| 1 | 3.7h | Async fundamentals |
| 2 | 3.7h | FastAPI + Weather API |
| 3 | 5.7h | Ollama + Streaming (longest) |
| 4 | 4.7h | Docker |
| 5 | 3.7h | Testing |
| 6 | 2.5h | Polish + stretch goal |

Done in <40% of estimate = reading code, not learning it.

---

## When Stuck

1. Spend 5–10 min yourself — read the error, google it, try small experiments
2. Ask AI with context:
```
"I'm trying to [goal] from [step].
Tried [what you tried]. Got: [error].
I think it's [hypothesis]. Am I right?"
```
3. If step is too big: "Break this step into 3 smaller steps."

### 4. Take a Break
- 5-minute walk
- Come back with fresh eyes
- Often the answer becomes obvious

---

## 📊 Progress Tracking

### Create Per-Session
```bash
# In each session folder
touch progress.md
```

**Format**:
```markdown
# Session X Progress

## Step XA: [Topic] ⏳
- [ ] Generated code
- [ ] Typed it myself
- [ ] Ran successfully
- [ ] Broke and fixed
- [ ] Extended it
- [ ] Understand concept

## Step XB: [Topic] ⏳
...
```

Update as you go - visual progress helps motivation!

---

## 🔄 Iteration Workflow

```
┌─ Read prompt in spec
│
├─ Ask AI for small snippet
│
├─ Type code yourself (no copy-paste!)
│
├─ Predict output
│
├─ Run and observe
│
├─ Compare to prediction
│
├─ Break intentionally
│  └─ Remove await, wrong type, etc.
│
├─ Debug error yourself (5-10 min)
│
├─ Fix and understand
│
├─ Ask conceptual question
│
├─ Extend with variation
│
├─ Mark complete
│
└─ Next step ──┐
               │
               └─ Repeat
```

---

## 📞 Quick Help

**Philosophy questions**: Read SESSION_WORKFLOW.md  
**Session 1 steps**: Read 001-async-fundamentals-rigorous.md  
**Session 2-6 structure**: Use RIGOROUS_TEMPLATE.md  
**Overall goals**: Review plan.md  
**Progress tracking**: Update LEARNING_LOG.md  
**What changed**: Read UPDATES.md  

---

## 🚀 Next Action

**If starting fresh**:
```
Read UPDATES.md → Understand changes
Read SESSION_WORKFLOW.md → Understand why
Start Step 1A from 001-async-fundamentals-rigorous.md
```

**If continuing**:
```
Review what you learned in Session 1
Do steps 1F, 1G, 1H if you haven't
Create Session 2 structure from RIGOROUS_TEMPLATE.md
```

---

**Remember**: The goal isn't to finish fast. The goal is to learn deeply.

**24 hours with understanding >> 8 hours with confusion**
