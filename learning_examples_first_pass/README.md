# Learning Examples - Session 1: Async Fundamentals

Interactive Python scripts demonstrating async/await concepts through hands-on examples.

## 🎯 Learning Goals

After running these examples, you should understand:
- How event loops enable concurrent I/O operations
- When to use `await`, `asyncio.gather()`, and `asyncio.create_task()`
- Why async helps I/O-bound tasks but not CPU-bound tasks
- Async context managers and error handling patterns

## 🚀 Quick Start

### Run All Examples

```bash
cd learning_examples
python async_learning.py
```

### Run Individual Examples

Modify `async_learning.py` to comment out examples you don't want to run, or use Python's interactive mode:

```python
import asyncio
from async_learning import example_2_concurrent_gather

# Run one example
asyncio.run(example_2_concurrent_gather())
```

## 📊 What to Observe

### Example 1: Sequential Execution (~6 seconds)
```
▶ Watch the timestamps - each task waits for the previous one
▶ Total time = 2s + 2s + 2s = 6 seconds
▶ This mimics traditional synchronous code
```

**Key Insight**: Each `await` blocks until that operation completes.

---

### Example 2: Concurrent Execution (~2 seconds)
```
▶ All three tasks start at nearly the same time
▶ Total time = max(2s, 2s, 2s) = 2 seconds
▶ 3x speedup from concurrency!
```

**Key Insight**: The event loop switches between tasks during I/O waits. All tasks progress "simultaneously."

---

### Example 3: Manual Task Creation (~2.5 seconds)
```
▶ Tasks are created and start running immediately
▶ You can do other work before awaiting results
▶ Total time = max(2.0s, 1.5s, 2.5s) = 2.5 seconds
```

**Key Insight**: `create_task()` schedules work immediately. You control when to wait for results.

**When to use `create_task()` vs `gather()`:**
- Use `gather()`: When you have all coroutines ready and want results in a list
- Use `create_task()`: When you need fine-grained control or want to do work before awaiting

---

### Example 4: Async Context Managers (~1.3 seconds)
```
▶ Watch the setup → query → cleanup sequence
▶ Shows how async with handles resources properly
```

**Key Insight**: Real-world async code (aiohttp, asyncpg) uses this pattern for connection management.

**Real Examples:**
```python
# HTTP sessions
async with aiohttp.ClientSession() as session:
    await session.get('https://api.example.com')

# Database connections
async with asyncpg.create_pool(dsn) as pool:
    await pool.fetch('SELECT * FROM users')
```

---

### Example 5: Error Handling (~2 seconds)
```
▶ One task fails but others complete successfully
▶ return_exceptions=True returns errors as values
```

**Key Insight**: Partial failures don't crash your entire concurrent operation.

**Without `return_exceptions=True`:**
- First exception is raised immediately
- Other tasks may be cancelled
- Harder to handle granularly

**With `return_exceptions=True`:**
- All tasks run to completion
- Exceptions returned as results
- You decide how to handle each failure

## 🔬 Experiments to Try

### 1. Test Your Understanding

**Modify delays:**
```python
# Make one task much slower
await asyncio.gather(
    fetch_data("Fast", 0.5),
    fetch_data("Slow", 5.0),  # Changed from 2.0
    fetch_data("Medium", 1.0)
)
```
**Q**: How long will this take?  
**A**: ~5 seconds (the slowest task)

---

### 2. Break the Code (Learn from Errors)

**Forget to await:**
```python
# WRONG - This won't work!
result = fetch_data("Test", 1.0)  # Missing 'await'
```
**Error**: `RuntimeWarning: coroutine 'fetch_data' was never awaited`

**Lesson**: Async functions return coroutine objects. You must `await` them to execute.

---

### 3. Add More Tasks

```python
# What happens with 10 concurrent tasks?
tasks = [fetch_data(f"Service{i}", 2.0) for i in range(10)]
results = await asyncio.gather(*tasks)
```
**Q**: How long for 10 tasks?  
**A**: Still ~2 seconds! All run concurrently.

---

### 4. Mix Fast and Slow Tasks

```python
await asyncio.gather(
    fetch_data("InstantAPI", 0.1),
    fetch_data("SlowDB", 5.0),
    fetch_data("CacheHit", 0.2)
)
```
**Observe**: Fast tasks complete early, slow task determines total time.

## 🧠 Conceptual Deep Dives

### Event Loop Explained

```
┌─────────────────────────────────────────────┐
│           Event Loop (Single Thread)         │
│                                              │
│  Queue: [TaskA, TaskB, TaskC]                │
│                                              │
│  While tasks exist:                          │
│    1. Run TaskA until it hits 'await'        │
│    2. TaskA is waiting → switch to TaskB     │
│    3. TaskB is waiting → switch to TaskC     │
│    4. Check if anyone is ready → back to A   │
│    5. Repeat...                              │
└─────────────────────────────────────────────┘
```

**Key Points:**
- Single-threaded (no OS thread switching overhead)
- Cooperative multitasking (`await` = yield control)
- Tasks must cooperate (no blocking calls!)

---

### When Async DOESN'T Help

```python
# ❌ BAD: CPU-intensive work
async def calculate_primes(n):
    primes = []
    for num in range(2, n):
        # Heavy CPU work - blocks the event loop!
        if is_prime(num):
            primes.append(num)
    return primes
```

**Problem**: No I/O waits = no opportunity for event loop to switch tasks.

**Solution for CPU-bound work:**
- Use `multiprocessing` (parallel processing on multiple cores)
- Use `concurrent.futures.ProcessPoolExecutor`
- Don't use async

---

### Async vs Threads vs Multiprocessing

| Approach | Best For | Concurrency | Parallelism | Overhead |
|----------|----------|-------------|-------------|----------|
| **Async** | I/O-bound | ✅ High | ❌ No (single thread) | Low |
| **Threads** | I/O-bound | ✅ Good | ⚠️ Limited (GIL) | Medium |
| **Multiprocessing** | CPU-bound | ✅ Yes | ✅ True parallel | High |

**GIL (Global Interpreter Lock)**: Python's lock that prevents true parallel execution of Python bytecode in threads.

---

### Rails Developer Perspective

**Rails (Puma with threads):**
```ruby
# Multiple OS threads handle concurrent requests
puma -t 5:5  # 5 threads per worker
```
- Each request gets a thread
- OS preemptively switches between threads
- Can block on I/O without affecting other threads

**Python Async:**
```python
# Single thread, event loop switches cooperatively
async def handle_request():
    await db.query()  # Yield control during I/O
```
- Single thread handles many coroutines
- Event loop switches at `await` points
- Must explicitly yield control

**Both achieve concurrency, different mechanisms!**

## 📚 Next Steps

After mastering these concepts:

1. **Session 2**: Apply async to FastAPI endpoints
   - Use `httpx.AsyncClient` for external API calls
   - See how FastAPI handles concurrent requests
   
2. **Session 3**: Stream responses with async generators
   - Understand `async for` and async generators
   - Implement Server-Sent Events (SSE)

3. **Session 5**: Test async code
   - Learn `pytest-asyncio` patterns
   - Mock async operations

## 🎓 Self-Check Questions

Before moving on, make sure you can answer:

1. **What does the event loop do?**
   - Manages coroutines, switches between tasks at await points

2. **When should you use `asyncio.gather()` vs `create_task()`?**
   - `gather()`: Have all coroutines ready, want results together
   - `create_task()`: Need tasks to start immediately, await later

3. **Why doesn't async help with CPU-intensive calculations?**
   - No I/O waits = no opportunity to switch tasks
   - Event loop blocked by computation

4. **What would happen if you used `time.sleep(2)` instead of `await asyncio.sleep(2)`?**
   - Blocks entire event loop (no task switching possible)
   - Defeats the purpose of async

5. **How do async context managers differ from regular ones?**
   - Use `__aenter__`/`__aexit__` instead of `__enter__`/`__exit__`
   - Can perform async operations during setup/teardown

## 🐛 Troubleshooting

### "RuntimeWarning: coroutine was never awaited"
```python
# Wrong
result = my_async_func()

# Correct
result = await my_async_func()
```

### "RuntimeError: no running event loop"
```python
# Wrong - calling async function from sync code
result = asyncio.run(my_async_func())  # OK from main
result = await my_async_func()  # OK from inside async function

# Wrong
result = my_async_func()  # Not awaited!
```

### Tasks not running concurrently
```python
# Sequential (slow)
for task in tasks:
    await task  # Waits for each to finish

# Concurrent (fast)
await asyncio.gather(*tasks)  # All run together
```

## 📖 Additional Resources

- [Python asyncio documentation](https://docs.python.org/3/library/asyncio.html)
- [Real Python: Async IO](https://realpython.com/async-io-python/)
- [FastAPI async docs](https://fastapi.tiangolo.com/async/)
- [uvloop](https://github.com/MagicStack/uvloop) - Faster event loop implementation

---

**Happy learning! 🚀**

*Remember: The best way to learn async is to run code, break it, fix it, and observe the behavior.*
