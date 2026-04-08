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

## 📋 Step-by-Step Checklist

For EACH micro-step:

- [ ] Read the prompt in rigorous spec
- [ ] Ask AI to generate (keep it small!)
- [ ] **Review the generated code** - understand what it does
- [ ] Predict output before running
- [ ] Run and compare to prediction
- [ ] Break it (remove key part, wrong type, etc.)
- [ ] Fix it and understand why it broke
- [ ] Ask conceptual question about it
- [ ] Extend with your own variation
- [ ] Mark complete in progress tracker

**Time per step**: 10-45 min depending on complexity

---

## ⏱️ Time Expectations

| Session | Steps | Est. Time | Reality Check |
|---------|-------|-----------|---------------|
| 1 | 8 steps | 3.7h | If done in <2h, too shallow |
| 2 | 7-8 steps | 3.7h | Should feel substantial |
| 3 | 8-9 steps | 5.7h | Longest session - LLM integration |
| 4 | 6-7 steps | 4.7h | Docker can be tricky |
| 5 | 7-8 steps | 3.7h | Testing requires thinking |
| 6 | 5-6 steps | 2.5h | Polish & one stretch goal |

**If completing in 25% of time** → You're reading code, not learning it

---

## 🚫 Common Pitfalls

### Don't Do This
```
❌ "Do Session X"
❌ Copy-paste AI code
❌ Run only working code
❌ Skip challenges
❌ Rush through to "finish"
```

### Do This Instead
```
✅ "Step XA: Generate [small specific thing]"
✅ Type AI code yourself
✅ Intentionally break code
✅ Build challenges yourself first
✅ Take time to understand deeply
```

---

## 🎓 Success Indicators

### You're Learning Well If:
- Taking close to estimated time per session
- Can explain concepts without notes
- Successfully breaking and fixing code
- Building challenges without AI help (mostly)
- Asking "why" questions frequently
- Connecting concepts across sessions

### You Need to Slow Down If:
- Completing sessions in <50% of estimated time
- Can't explain why code works
- Haven't broken anything intentionally
- Relying fully on AI for every line
- Not asking questions
- Concepts feel disconnected

---

## 💡 When Stuck

### 1. Spend 5-10 Min Yourself
- Read error message carefully
- Check previous steps for patterns
- Try small experiments
- Google the specific error

### 2. Ask AI with Context
```
"I'm trying to [goal] based on [previous step].
I tried [what you tried].
Got error: [error message]
I think it's because [hypothesis].
Am I on right track?"
```

### 3. Break It Down Further
```
"This step is too big. Break it into 3 smaller steps."
```

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
