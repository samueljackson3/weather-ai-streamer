# Rigorous Session Workflow

**Problem**: Asking AI to "do Session X" generates all code at once → minimal learning  
**Solution**: Break each session into small, hands-on incremental steps

---

## 🎯 Learning Philosophy

**Bad workflow** (what happened):
```
You: "Do Session 1"
AI: [Generates complete code]
You: [Read it, run it, done in 45 min]
Result: Code works, but shallow understanding
```

**Good workflow** (what we want):
```
You: "Generate Step 1A: Basic async function"
AI: [Generates 10-line snippet]
You: [Review it, understand it, run it]
You: "What if I remove await?" → Break it → Fix it
You: "Add timing to compare sync vs async"
AI: [Shows modification]
You: [Review, test it]
You: "Explain why this is faster"
AI: [Conceptual explanation]
Repeat for steps 1B, 1C, 1D...
Result: Deep understanding through iteration
```

---

## 📋 Session Structure Template

### Phase 1: Foundation (30-45 min)
**Micro-steps** (5-10 min each):
1. Generate minimal example
2. Run and observe
3. Break it intentionally
4. Fix it and understand why
5. Ask conceptual question
6. Extend with your own variation

### Phase 2: Core Learning (1-2 hours)
**Incremental building**:
- Add complexity one piece at a time
- Run tests after each addition
- Compare against previous version
- Document observations

### Phase 3: Experimentation (45-60 min)
**Hands-on challenges**:
- Modify behavior to meet specs
- Debug broken examples
- Optimize performance
- Combine patterns

### Phase 4: Integration (30-45 min)
**Apply learnings**:
- Build something not in the spec
- Refactor earlier code
- Write your own examples

### Phase 5: Reflection (15-20 min)
**Solidify understanding**:
- Update learning log
- Write explanations in own words
- List remaining questions

---

## 🔧 Granular Prompt Templates

### Step 1: Generate Minimal Code
```
Generate a minimal async function that [does X].
Requirements:
- 10-15 lines max
- Include print statements showing execution
- Add comments explaining [key concept]
- No extra features - keep it simple
```

### Step 2: Run & Observe
```bash
python snippet.py
# Look at output - what do you notice?
# What order did things execute?
# What were the timings?
```

### Step 3: Break It
```
Show me what happens if I:
1. Remove the `await` keyword
2. Don't use `asyncio.run()`
3. Call the async function directly without await

For each: what error appears and why?
```

### Step 4: Fix & Understand
```
I got error: [paste error]
Explain why this happens and how to fix it.
Compare with [Rails pattern] if applicable.
```

### Step 5: Conceptual Deep Dive
```
Now that I've run this code, explain:
- Why is [specific line] necessary?
- What's happening in the event loop?
- When would I use this pattern in real code?
```

### Step 6: Extend & Experiment
```
Modify this code to:
- [Add variation 1]
- [Try different parameters]
- [Combine with another pattern]

Show me the modified code with clear comments on what changed.
```

---

## 📝 Example: Session 1 Rigorous Workflow

### Step 1A: Simplest Async Function (10 min)

**Prompt**:
```
Generate the simplest possible async function that:
1. Uses asyncio.sleep(1) to simulate I/O
2. Prints before and after the sleep
3. Returns a string

Keep it under 10 lines. Include timing with time.perf_counter().
```

**Your Actions**:
1. Read generated code
2. Review and understand pattern
3. Run it: `python step_1a.py`
4. Observe timing and print order

**Challenge**: Predict the output before running!

---

### Step 1B: Compare Sync vs Async (15 min)

**Prompt**:
```
Create TWO versions of calling fetch_data() three times:
1. Sequential (one await after another)
2. Using time.sleep() instead (blocking)

Show timing difference. Keep under 30 lines total.
```

**Your Actions**:
1. Review the generated code
2. Run both versions
3. Note timing difference
4. Ask: "Why is async not faster if it's single-threaded?"

**Experiment**:
```
Modify delays: try 0.1s, 1s, 5s
What changes? What stays the same?
```

---

### Step 1C: Introduce gather() (20 min)

**Prompt**:
```
Add a third version using asyncio.gather() for concurrent execution.
Include print statements showing when each task starts and finishes.
Max 20 new lines.
```

**Your Actions**:
1. Before running: predict which will print first
2. Run and compare to prediction
3. Run it 3 times - does order change?

**Break It**:
```
What happens if I:
1. await each fetch_data() before passing to gather()?
2. Don't await gather()?
3. Use a regular list comprehension with await?
```

**Fix It**: Debug each error

---

### Step 1D: Manual Task Creation (20 min)

**Prompt**:
```
Refactor the gather() example to use asyncio.create_task() instead.
Show how you can do work BETWEEN creating tasks and awaiting them.
```

**Your Actions**:
1. Identify the key difference from gather()
2. Add a print statement between task creation and awaiting
3. Experiment: create 5 tasks but only await 3 - what happens?

---

### Step 1E: Error Handling (20 min)

**Prompt**:
```
Modify one of the fetch_data() calls to raise an exception.
Show two approaches:
1. Try/except around gather()
2. gather() with return_exceptions=True

Keep it minimal - just demonstrate the difference.
```

**Your Actions**:
1. Run both versions
2. Compare output
3. Ask: "When would I use each approach in production?"

---

### Step 1F: Build Your Own (30 min)

**Challenge** (do this yourself first, then ask AI for feedback):
```
Create an async function that:
- Fetches weather from 5 different "cities" (simulated)
- Each city takes a random delay (0.5s - 3s)
- Uses gather() to fetch all concurrently
- Prints results as they arrive (use as_completed)
- Handles errors gracefully

Build it incrementally:
1. Random delays
2. Basic gather()
3. Switch to as_completed()
4. Add error handling
```

**Ask AI**: "Review my code. What could be improved?"

---

### Step 1G: Real-World Application (20 min)

**Prompt**:
```
Show me how this async pattern would work with:
1. Real HTTP requests (using httpx)
2. Database queries (conceptual)
3. File I/O (aiofiles)

Just show the structure, not complete implementations (10 lines each).
```

**Your Actions**:
1. Compare to your simulated examples
2. Identify the pattern that's the same
3. Note what's different

---

### Step 1H: Concept Check (20 min)

**Self-test** (answer these yourself, then ask AI):
1. What's the difference between concurrent and parallel?
2. When does async NOT help?
3. Why use async context managers?
4. gather() vs create_task() vs as_completed() - when each?

**Prompt**: 
```
I answered:
1. [Your answer]
2. [Your answer]
...

Critique my understanding. What am I missing?
```

---

## ⏱️ Time Breakdown

| Phase | Time | Activities |
|-------|------|------------|
| **1A-1C** | 45 min | Basics: async, sync comparison, gather() |
| **1D-1E** | 40 min | Advanced: create_task(), error handling |
| **1F** | 30 min | Build your own challenge |
| **1G** | 20 min | Real-world patterns |
| **1H** | 20 min | Concept check & reflection |
| **Break/Buffer** | 45 min | Debug time, re-runs, questions |
| **Total** | **3.7h** | Rigorous, hands-on learning |

---

## ✅ Quality Checks

After each step, ask yourself:

- [ ] Did I **type** the code myself (not just copy-paste)?
- [ ] Did I **run** it and observe the output?
- [ ] Did I **break** it intentionally and fix it?
- [ ] Did I **ask** a conceptual question and get it answered?
- [ ] Can I **explain** this concept to someone else?

If you answered "no" to 2+, slow down and engage more deeply.

---

## 🎓 Success Metrics

**Shallow learning** (what we're avoiding):
- Code runs ✅
- Don't know why it works ❌
- Can't modify without breaking ❌
- Couldn't recreate from scratch ❌

**Deep learning** (what we're aiming for):
- Code runs ✅
- Can explain every line ✅
- Can modify and extend ✅
- Could build similar from scratch ✅

---

## 🔄 Iteration Protocol

When something doesn't work:

1. **Don't immediately ask AI** - spend 5 min debugging yourself
2. **Read the error message** carefully - Python errors are helpful
3. **Check your changes** - diff against working version
4. **Google it** - build research skills
5. **Ask AI with context** - after trying yourself

**Good question**:
```
I modified X to Y because I wanted Z.
I got error: [paste]
I think it's because of [hypothesis].
Am I on the right track?
```

**Bad question**:
```
It doesn't work. Fix it.
```

---

## 📊 Progress Tracking

Create a checklist file for each session:

```markdown
# Session 1 Progress

## Step 1A: Basic Async ⏳
- [ ] Generated code
- [ ] Typed it myself
- [ ] Ran successfully
- [ ] Broke it (removed await)
- [ ] Fixed and understood error
- [ ] Can explain in own words

## Step 1B: Sync vs Async ⏳
- [ ] ...
```

Update as you go. This shows real progress vs. just "AI generated code."

---

## 🚀 Next Steps

**Ready for rigorous Session 1?**

Use this workflow:
1. Don't ask for full examples
2. Request small, incremental steps
3. Type code yourself
4. Break and fix everything
5. Ask conceptual questions throughout
6. Build your own variations

**Start with**:
```
"Session 1, Step 1A: Generate the simplest async function that 
demonstrates await with asyncio.sleep(). Under 10 lines, include 
timing. I want to type it myself, so keep it minimal."
```

Then work through steps 1B, 1C, etc. following this guide.
