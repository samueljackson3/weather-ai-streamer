# Updated Session 1: Rigorous Async Fundamentals

**IMPORTANT**: This replaces the Session 1 section in plan.md  
**Time**: 3.7 hours  
**Approach**: Incremental micro-steps, hands-on building

---

## 🎯 Philosophy Change

### What Was Wrong
```
Old: "Do Session 1" → AI generates everything → Run it → Done (45 min, shallow)
```

### What's Better
```
New: 8 micro-steps → Type each yourself → Break it → Fix it → Extend (3.7h, deep)
```

**Key difference**: You build incrementally, make mistakes, and learn through doing.

---

## 📋 Rigorous Step-by-Step Workflow

### Before You Start

**Delete or rename** the existing `learning_examples/` folder:
```bash
mv learning_examples learning_examples_old
mkdir learning_examples
cd learning_examples
```

**Create progress tracker**:
```bash
touch session1_progress.md
```

---

### Step 1A: Simplest Async Function (10 min)

**Prompt**:
```
Generate the simplest async function that:
- Uses asyncio.sleep(1) to simulate I/O
- Prints "Starting", does sleep, prints "Done"
- Returns a string "Task complete"
- Includes timing with time.perf_counter()

Keep it under 15 lines total. Include comments explaining async, await, and asyncio.run().
```

**Your Tasks**:
1. Read the generated code carefully
2. **Type it yourself** into `step_1a.py` (don't copy-paste!)
3. Before running: predict what order things will print
4. Run: `python step_1a.py`
5. Observe: timing, print order

**Break It Challenge**:
```
Ask AI: "Show me what happens if I:"
1. Remove the `await` before asyncio.sleep()
2. Call `simple_async()` directly instead of asyncio.run()
3. Don't use `asyncio.run()` at all

Try each one. Read the error. Understand why.
```

**Concept Check** (ask yourself, then verify with AI):
- What does `await` actually do?
- Why can't I just call `simple_async()` like a normal function?
- What is asyncio.run() doing?

**Mark complete**: `[x] Step 1A` in progress tracker

---

### Step 1B: Sync vs Async Comparison (15 min)

**Prompt**:
```
Create two versions that each call a simulated fetch 3 times:

Version 1: Synchronous (using time.sleep - blocking)
Version 2: Async sequential (using await asyncio.sleep sequentially)

Each fetch takes 1 second. Show timing for both.
Keep under 35 lines total.
```

**Your Tasks**:
1. Type the code into `step_1b.py`
2. Predict: Will there be a timing difference? Why/why not?
3. Run it and compare your prediction
4. Observation: Both should take ~3 seconds - why is async not faster here?

**Extend Challenge**:
```
Modify the code yourself:
- Change delays to 0.5s, 1s, 2s (different for each call)
- Add a 4th fetch in sequence
- Print timestamps to see execution order

Don't ask AI - try it yourself first.
```

**Concept Check**:
- Why is async still "sequential" here (~3 seconds)?
- What's the difference between time.sleep (sync) and asyncio.sleep (async)?
- Predict: What would make async faster?

**Mark complete**: `[x] Step 1B`

---

### Step 1C: Concurrent Execution with gather() (20 min)

**Prompt**:
```
Add a third version to step_1b.py that uses asyncio.gather() 
to run the 3 fetches concurrently.

Include:
- Print statement showing when each fetch starts
- Timing comparison
- Clear labels for each version

Show ONLY the new function, I'll integrate it myself.
```

**Your Tasks**:
1. Add the concurrent version to your file
2. Before running: predict the timing
3. Run all three versions
4. **Observe execution order** - which fetch starts first? Is it always the same?

**Experiment**:
```bash
# Run it multiple times
for i in {1..5}; do python step_1b.py; done

# Does the order change?
# Are timings consistent?
```

**Break It Challenge**:
```
Modify your code:
1. What if you await each fetch before calling gather()?
   Like: await fetch(), await fetch(), await fetch() in gather()
   
2. What if you forget to await gather()?

3. What if you use gather(*[fetch() for _ in range(3)])?
   Does this work? Why/why not?

Try each. Debug the errors yourself first.
```

**Concept Check**:
- How does gather() make this ~1 second instead of ~3?
- Are the tasks running "in parallel"? (Trick question!)
- What's the event loop doing during asyncio.sleep()?

**Mark complete**: `[x] Step 1C`

---

### Step 1D: Manual Task Creation (20 min)

**Prompt**:
```
Create a new file step_1d.py that demonstrates asyncio.create_task().

Show:
1. Creating 3 tasks explicitly
2. Doing some work BETWEEN creating tasks and awaiting them
3. Collecting results

Include timing and comments explaining when tasks start vs when we await them.
Keep under 25 lines.
```

**Your Tasks**:
1. Type the code into `step_1d.py`
2. Add a print statement between task creation and awaiting
3. Run it - when do tasks actually start?

**Deep Dive**:
```
Ask AI: "Explain the difference between:

Option A:
  results = await asyncio.gather(fetch(), fetch(), fetch())

Option B:
  task1 = asyncio.create_task(fetch())
  task2 = asyncio.create_task(fetch())
  result1 = await task1
  result2 = await task2

When would I use each?"
```

**Experiment Yourself**:
```python
# Try this:
task1 = create_task(fetch("A", 2))
task2 = create_task(fetch("B", 1))

# Do 3 seconds of work here
time.sleep(3)  # Simulate CPU work

# Now await them
result1 = await task1
result2 = await task2

# How long does this take total?
# Why?
```

**Concept Check**:
- When does a task start running?
- Can tasks run while I'm doing CPU work?
- Why use create_task() vs just calling gather()?

**Mark complete**: `[x] Step 1D`

---

### Step 1E: Error Handling (20 min)

**Prompt**:
```
Create step_1e.py demonstrating error handling in async code.

Show two approaches:
1. Try/except around await gather()
2. gather() with return_exceptions=True

Make one of the fetch calls randomly fail.
Keep under 40 lines total.
```

**Your Tasks**:
1. Type code into `step_1e.py`
2. Run multiple times - observe different error scenarios
3. Compare output of both approaches

**Break It Challenge**:
```
Modify to test edge cases:
- All tasks fail - what happens?
- First task fails vs last task fails - different?
- Catch specific exception types (ValueError vs Exception)
```

**Real-World Connection**:
```
Ask AI: "In a real API that calls 10 external services:
- Some might timeout
- Some might return 404
- Some might succeed

How would I handle partial failures with gather()?"
```

**Concept Check**:
- When should I use return_exceptions=True?
- How do I handle errors for individual tasks vs all tasks?
- What happens if I don't handle errors at all?

**Mark complete**: `[x] Step 1E`

---

### Step 1F: Build Your Own Challenge (30 min)

**Challenge** (Do this YOURSELF first - no AI help yet):
```
Create step_1f_weather_sim.py that simulates fetching weather from 5 cities:

Requirements:
- Each city takes a random delay (0.5s - 3s)
- Use gather() to fetch all concurrently
- Print results as they come in (hint: use asyncio.as_completed)
- Handle at least one city failing realistically
- Show total time vs sequential time calculation

Build incrementally:
1. Random delays first
2. Basic gather()
3. Switch to as_completed() 
4. Add error handling for one failure
```

**Your Tasks**:
1. Write code yourself - refer to earlier steps if needed
2. Test it - does it work?
3. If stuck after 15 min, ask AI for hints (not full solution)

**After You Build It**:
```
Ask AI: "Review my code. What could be improved for:
- Readability
- Error handling
- Performance
- Real-world usage

[Paste your code]"
```

**Concept Check**:
- Can you build this without AI help?
- Can you explain each line?
- Could you add new features (caching, retries, etc.)?

**Mark complete**: `[x] Step 1F`

---

### Step 1G: Real-World Patterns (20 min)

**Prompt**:
```
Show me how the async patterns from steps 1A-1F would work with:

1. Real HTTP requests (httpx.AsyncClient)
2. Async file I/O (aiofiles)
3. Database queries (asyncpg pool)

For each: 10-15 line example showing the pattern.
Don't generate complete implementations - just show the structure.
```

**Your Tasks**:
1. Compare to your simulated examples
2. Identify what's the same (gather, create_task, error handling)
3. Note what's new (context managers, connection pools)

**Code Reading Exercise**:
```
Ask AI: "Find a real open-source project using FastAPI.
Show me an example of their async API endpoint.
Explain how they use the patterns I learned."
```

**Concept Check**:
- What real libraries use async?
- How does httpx.AsyncClient differ from requests?
- Why use connection pools with databases?

**Mark complete**: `[x] Step 1G`

---

### Step 1H: Concept Self-Test (20 min)

**Test Yourself** (answer BEFORE asking AI):

1. **What's the difference between concurrent and parallel execution?**
   Your answer:
   
2. **When does async NOT help?**
   Your answer:
   
3. **Why use async context managers (async with)?**
   Your answer:
   
4. **gather() vs create_task() vs as_completed() - when to use each?**
   Your answer:
   
5. **What happens in the event loop during await asyncio.sleep(1)?**
   Your answer:

**After Answering**:
```
Ask AI: "I answered these async concept questions:
1. [Your answer]
2. [Your answer]
...

Critique my understanding. What am I missing? What's incorrect?"
```

**Code Challenge** (Do without AI):
```python
# Can you write this from scratch?
# No looking at previous examples!

async def fetch_multiple_apis(urls: list[str]) -> dict:
    """Fetch all URLs concurrently, handle errors gracefully."""
    # Your implementation here
    pass

# Test it with:
urls = ["api1", "api2", "api3"]  # Simulated
results = asyncio.run(fetch_multiple_apis(urls))
```

**Concept Check**:
- Could you rebuild all of Session 1 from memory?
- Can you explain async to a colleague?
- Ready to use async in a real project?

**Mark complete**: `[x] Step 1H`

---

## 🎯 Session 1 Completion Checklist

### Code Quality
- [ ] All 8 steps completed and working
- [ ] Typed code yourself (didn't just copy-paste)
- [ ] Broke and fixed code in each step
- [ ] Added your own experiments/variations
- [ ] Can run any example and explain what happens

### Conceptual Understanding
- [ ] Can explain event loop without notes
- [ ] Know when async helps vs doesn't help
- [ ] Understand gather() vs create_task() trade-offs
- [ ] Can debug "coroutine was never awaited" error
- [ ] Can write async code from scratch

### Application
- [ ] Completed step 1F challenge independently
- [ ] Reviewed real-world async code
- [ ] Connected patterns to Rails knowledge
- [ ] Ready to build FastAPI endpoints (Session 2)

### Reflection
- [ ] Updated LEARNING_LOG.md with honest assessment
- [ ] Documented "aha moments" and confusions
- [ ] Listed questions for deeper exploration
- [ ] Estimated time spent (compare to 3.7h)

---

## ⏱️ Time Tracking

| Step | Estimated | Your Actual | Notes |
|------|-----------|-------------|-------|
| 1A | 10 min | _____ | |
| 1B | 15 min | _____ | |
| 1C | 20 min | _____ | |
| 1D | 20 min | _____ | |
| 1E | 20 min | _____ | |
| 1F | 30 min | _____ | |
| 1G | 20 min | _____ | |
| 1H | 20 min | _____ | |
| Breaks/Debug | 45 min | _____ | |
| **Total** | **3.7h** | **_____** | |

---

## 🚀 Ready for Session 2?

**You're ready when**:
- Completed 7/8 steps (1F is the hardest)
- Can explain 4/5 concept questions correctly
- Feel comfortable writing async functions
- Excited to build real APIs with FastAPI

**Not ready yet?**
- Spend more time on steps that were confusing
- Build more variations of 1F
- Read async Python articles
- Come back to Session 2 tomorrow

---

## 📝 Update Plan.md

Replace the Session 1 section in plan.md with:

```markdown
### Session 1: Async Fundamentals (3.7 hours)

**Spec**: `specs/001-async-fundamentals.md`  
**Rigorous Workflow**: `specs/001-async-fundamentals-rigorous.md` (this file)

**IMPORTANT**: Don't ask AI to "do Session 1" - follow the 8-step workflow:

| Step | Focus | Time |
|------|-------|------|
| 1A | Simplest async | 10 min |
| 1B | Sync comparison | 15 min |
| 1C | Introduce gather() | 20 min |
| 1D | Manual tasks | 20 min |
| 1E | Error handling | 20 min |
| 1F | Build your own | 30 min |
| 1G | Real patterns | 20 min |
| 1H | Concept check | 20 min |

See rigorous workflow doc for detailed prompts and challenges.
```
