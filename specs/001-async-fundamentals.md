# Spec: Async Fundamentals

**Session**: 1  
**Estimated Time**: 3.7 hours  
**Status**: Draft  
**Last Updated**: April 8, 2026

---

## Problem Statement

Learn Python async fundamentals by building interactive examples that demonstrate event loops, coroutines, and concurrent execution. This provides the foundation for understanding FastAPI's async capabilities and modern Python I/O patterns.

---

## Learning Objectives

- [ ] Understand how event loops manage concurrent tasks (vs traditional threading)
- [ ] Know when to use `await` vs `asyncio.gather()` vs `asyncio.create_task()`
- [ ] Compare concurrent vs parallel vs sequential execution patterns
- [ ] Explain why async helps with I/O-bound work but not CPU-intensive tasks
- [ ] Recognize async context managers and their purpose
- [ ] Can write basic async functions with proper error handling

---

## Technical Design

**Components**:
- `async_learning.py`: Standalone Python script with 5 progressive examples
- Uses `asyncio.sleep()` to simulate I/O operations (network calls, file I/O, etc.)
- Print statements to trace execution order and timing

**Learning Progression**:
```
Example 1: Synchronous Baseline (slow)
    ↓
Example 2: Concurrent with asyncio.gather() (fast)
    ↓
Example 3: Task creation with create_task()
    ↓
Example 4: Async context managers
    ↓
Example 5: Error handling in async code
```

**Key Decisions**:
| Decision | Choice | Rationale |
|----------|--------|-----------|
| Simulation method | `asyncio.sleep()` | Safe, predictable timing vs real network calls |
| Execution model | Single-threaded event loop | Core Python async pattern |
| Examples format | Standalone functions | Can run individually to observe behavior |
| Timing mechanism | `time.perf_counter()` | High-resolution timing for comparisons |

---

## API / Code Contract

### Core Functions

```python
async def fetch_data(source: str, delay: float) -> dict:
    """
    Simulates an async I/O operation (API call, database query, etc.)
    
    Args:
        source: Human-readable identifier (e.g., "WeatherAPI", "UserDB")
        delay: Simulated I/O time in seconds
        
    Returns:
        dict with source name and timestamp
    """
    pass

async def example_1_synchronous() -> None:
    """
    Baseline: Sequential execution of 3 tasks.
    Expected time: sum of all delays (~6 seconds)
    """
    pass

async def example_2_concurrent_gather() -> None:
    """
    Concurrent execution using asyncio.gather().
    Expected time: max of all delays (~2 seconds)
    Demonstrates: All tasks run "simultaneously" during I/O waits
    """
    pass

async def example_3_create_task() -> None:
    """
    Manual task creation for more control.
    Demonstrates: Difference between creating tasks and awaiting them
    """
    pass

async def example_4_async_context_manager() -> None:
    """
    Shows async with statement for resource management.
    Demonstrates: __aenter__ and __aexit__ patterns
    """
    pass

async def example_5_error_handling() -> None:
    """
    Handling exceptions in concurrent async code.
    Demonstrates: One failure doesn't crash all tasks
    """
    pass
```

### Data Structures

```python
# Simple return structure for fetch operations
{
    "source": "WeatherAPI",
    "timestamp": 1712550123.456,
    "data": "Sample data"
}
```

---

## Success Criteria

**Code Works**:
- [ ] Example 1 takes ~6 seconds (sequential: 2+2+2)
- [ ] Example 2 takes ~2 seconds (concurrent: max(2,2,2))
- [ ] Example 3 demonstrates task scheduling vs immediate execution
- [ ] Example 4 shows async context manager enter/exit order
- [ ] Example 5 catches and handles exceptions without crashing other tasks
- [ ] All examples include timing output and execution traces

**Conceptual Understanding**:
- [ ] Can explain in own words: "The event loop switches between tasks during I/O waits"
- [ ] Can answer: "When would async NOT help performance?"
  - Expected: CPU-bound work, no I/O waits, single operation
- [ ] Can explain difference between `await gather(a, b, c)` vs creating 3 tasks manually
- [ ] Understand why `await asyncio.sleep(2)` is non-blocking but `time.sleep(2)` would block

**Rails Developer Notes**:
- [ ] Can compare: Rails Puma thread pool vs Python async event loop
- [ ] Understand: Both achieve concurrency, but different mechanisms
  - Rails: Multiple threads, preemptive multitasking, OS-scheduled
  - Python async: Single thread, cooperative multitasking, event loop scheduled

---

## Open Questions

- How does the event loop actually work under the hood? (epoll/kqueue/IOCP)
- When would you use `asyncio.create_task()` over `asyncio.gather()`?
- How do you debug async code when tasks are interleaved?
- What are the performance characteristics on different platforms?

---

## Testing Strategy

**Manual Testing** (sufficient for learning):
- Run each example function individually
- Observe and verify timing output
- Modify delays and counts to test understanding
- Intentionally break code:
  - Remove `await` to see "coroutine never awaited" warning
  - Make delays longer/shorter to understand concurrency
  - Add more tasks to see scaling behavior

**Validation Checks**:
- Timing assertions (e.g., concurrent should be < sequential)
- Print output shows correct execution order
- Error handling example doesn't crash on exception

**No pytest required** - this is exploratory learning code, not production

---

## Implementation Files

```
learning_examples/
  async_learning.py          # Main implementation
  README.md                  # How to run and what to observe
```

---

## References for Deeper Learning

- Python asyncio docs: https://docs.python.org/3/library/asyncio.html
- Real Python async tutorial: https://realpython.com/async-io-python/
- Event loop implementations: uvloop, asyncio
- Comparison with other concurrency models (threads, multiprocessing)

---

## Notes

This spec focuses on **learning through observation** rather than production code. Each example should:
- Print what it's doing (trace execution)
- Show timing to demonstrate performance
- Be simple enough to understand at a glance
- Build on previous examples incrementally

Expected "aha moments":
1. "Concurrent execution only takes as long as the slowest task!"
2. "The event loop switches between tasks automatically during awaits"
3. "Async is about concurrency, not parallelism"
4. "I/O-bound tasks benefit, CPU-bound tasks don't"
