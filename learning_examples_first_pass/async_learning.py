#!/usr/bin/env python3
"""
Async Fundamentals Learning Examples

Session 1: Understanding async/await, event loops, and concurrent execution
Run each example individually to observe behavior and timing.
"""

import asyncio
import time
from typing import Dict, Any


# =============================================================================
# CORE SIMULATION FUNCTION
# =============================================================================

async def fetch_data(source: str, delay: float) -> Dict[str, Any]:
    """
    Simulates an async I/O operation (API call, database query, file read, etc.)
    
    In a real application, this would be:
    - HTTP request to external API
    - Database query
    - File I/O operation
    - Any operation that waits for external resources
    
    Args:
        source: Human-readable identifier (e.g., "WeatherAPI", "UserDB")
        delay: Simulated I/O time in seconds
        
    Returns:
        dict with source name, timestamp, and sample data
    """
    print(f"  [{time.strftime('%H:%M:%S')}] Starting fetch from {source} (will take {delay}s)...")
    await asyncio.sleep(delay)  # Simulate I/O wait - this is non-blocking!
    print(f"  [{time.strftime('%H:%M:%S')}] ✓ Completed fetch from {source}")
    
    return {
        "source": source,
        "timestamp": time.time(),
        "data": f"Sample data from {source}"
    }


# =============================================================================
# EXAMPLE 1: SEQUENTIAL (SYNCHRONOUS) EXECUTION - THE SLOW WAY
# =============================================================================

async def example_1_sequential():
    """
    Baseline: Sequential execution of 3 tasks.
    
    Each task waits for the previous one to complete.
    Expected time: sum of all delays (2 + 2 + 2 = ~6 seconds)
    
    This is what happens when you DON'T use async concurrency features.
    """
    print("\n" + "="*70)
    print("EXAMPLE 1: Sequential Execution (The Slow Way)")
    print("="*70)
    print("Fetching data one at a time, waiting for each to complete...\n")
    
    start = time.perf_counter()
    
    # Each await blocks until that operation completes
    result1 = await fetch_data("WeatherAPI", 2.0)
    result2 = await fetch_data("UserDatabase", 2.0)
    result3 = await fetch_data("PaymentService", 2.0)
    
    elapsed = time.perf_counter() - start
    
    print(f"\n⏱️  Total time: {elapsed:.2f}s")
    print(f"📊 Expected: ~6s (2+2+2)")
    print(f"💡 Learning: Sequential execution = sum of all wait times\n")
    
    return [result1, result2, result3]


# =============================================================================
# EXAMPLE 2: CONCURRENT WITH asyncio.gather() - THE FAST WAY
# =============================================================================

async def example_2_concurrent_gather():
    """
    Concurrent execution using asyncio.gather().
    
    All tasks start "simultaneously" and run concurrently.
    The event loop switches between tasks during I/O waits.
    Expected time: max of all delays (~2 seconds)
    
    This is the power of async - I/O operations don't block each other!
    """
    print("\n" + "="*70)
    print("EXAMPLE 2: Concurrent Execution with asyncio.gather()")
    print("="*70)
    print("Fetching all data concurrently...\n")
    
    start = time.perf_counter()
    
    # gather() runs all coroutines concurrently and waits for all to complete
    results = await asyncio.gather(
        fetch_data("WeatherAPI", 2.0),
        fetch_data("UserDatabase", 2.0),
        fetch_data("PaymentService", 2.0)
    )
    
    elapsed = time.perf_counter() - start
    
    print(f"\n⏱️  Total time: {elapsed:.2f}s")
    print(f"📊 Expected: ~2s (max of 2, 2, 2)")
    print(f"💡 Learning: Concurrent execution = time of slowest task")
    print(f"🚀 Speedup: 3x faster than sequential!\n")
    
    return results


# =============================================================================
# EXAMPLE 3: MANUAL TASK CREATION - MORE CONTROL
# =============================================================================

async def example_3_create_task():
    """
    Manual task creation using asyncio.create_task().
    
    Demonstrates the difference between:
    - Creating a task (starts running immediately in background)
    - Awaiting a coroutine (blocks until completion)
    
    create_task() gives you more control over when to wait for results.
    """
    print("\n" + "="*70)
    print("EXAMPLE 3: Manual Task Creation with create_task()")
    print("="*70)
    print("Creating tasks that run in the background...\n")
    
    start = time.perf_counter()
    
    # Create tasks - they start running immediately
    print("  Creating tasks (they start running now)...")
    task1 = asyncio.create_task(fetch_data("WeatherAPI", 2.0))
    task2 = asyncio.create_task(fetch_data("UserDatabase", 1.5))
    task3 = asyncio.create_task(fetch_data("PaymentService", 2.5))
    
    print("  All tasks created! They're running in the background.\n")
    
    # You could do other work here while tasks run in background
    await asyncio.sleep(0.5)
    print("  (Did some other work while tasks were running...)\n")
    
    # Now wait for all tasks to complete
    print("  Now waiting for all tasks to complete...")
    results = await asyncio.gather(task1, task2, task3)
    
    elapsed = time.perf_counter() - start
    
    print(f"\n⏱️  Total time: {elapsed:.2f}s")
    print(f"📊 Expected: ~2.5s (max of 2.0, 1.5, 2.5)")
    print(f"💡 Learning: create_task() schedules tasks immediately")
    print(f"   You can await them later when you need the results\n")
    
    return results


# =============================================================================
# EXAMPLE 4: ASYNC CONTEXT MANAGERS
# =============================================================================

class AsyncResource:
    """
    Demonstrates async context manager pattern.
    
    Used for resources that require async setup/teardown:
    - Database connections
    - HTTP sessions (like aiohttp.ClientSession)
    - File handles with async I/O
    - Any resource requiring async acquire/release
    """
    
    def __init__(self, name: str):
        self.name = name
        self.setup_time = 0.5
        self.teardown_time = 0.3
    
    async def __aenter__(self):
        """Called when entering 'async with' block"""
        print(f"  [{time.strftime('%H:%M:%S')}] Setting up {self.name}...")
        await asyncio.sleep(self.setup_time)  # Simulate async setup
        print(f"  [{time.strftime('%H:%M:%S')}] ✓ {self.name} ready")
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Called when exiting 'async with' block"""
        print(f"  [{time.strftime('%H:%M:%S')}] Cleaning up {self.name}...")
        await asyncio.sleep(self.teardown_time)  # Simulate async cleanup
        print(f"  [{time.strftime('%H:%M:%S')}] ✓ {self.name} closed")
        return False  # Don't suppress exceptions
    
    async def query(self, data: str):
        """Simulate using the resource"""
        print(f"  [{time.strftime('%H:%M:%S')}] Querying {self.name} for: {data}")
        await asyncio.sleep(0.5)
        return f"Result from {self.name}: {data}"


async def example_4_async_context_manager():
    """
    Shows async with statement for resource management.
    
    Real-world examples:
    - async with aiohttp.ClientSession() as session:
    - async with asyncpg.create_pool() as pool:
    - async with aiofiles.open('file.txt') as f:
    """
    print("\n" + "="*70)
    print("EXAMPLE 4: Async Context Managers")
    print("="*70)
    print("Managing async resources with 'async with'...\n")
    
    start = time.perf_counter()
    
    # Using async context manager ensures proper setup and cleanup
    async with AsyncResource("DatabaseConnection") as db:
        result = await db.query("SELECT * FROM users")
        print(f"  Got result: {result}")
    
    # Cleanup happens automatically even if exception occurs
    
    elapsed = time.perf_counter() - start
    
    print(f"\n⏱️  Total time: {elapsed:.2f}s")
    print(f"💡 Learning: async with handles async setup and teardown")
    print(f"   Guarantees cleanup even if errors occur\n")


# =============================================================================
# EXAMPLE 5: ERROR HANDLING IN ASYNC CODE
# =============================================================================

async def fetch_data_with_error(source: str, delay: float, should_fail: bool = False) -> Dict[str, Any]:
    """Modified fetch that can simulate failures"""
    print(f"  [{time.strftime('%H:%M:%S')}] Starting fetch from {source}...")
    await asyncio.sleep(delay)
    
    if should_fail:
        print(f"  [{time.strftime('%H:%M:%S')}] ✗ {source} failed!")
        raise ConnectionError(f"Failed to connect to {source}")
    
    print(f"  [{time.strftime('%H:%M:%S')}] ✓ Completed fetch from {source}")
    return {
        "source": source,
        "timestamp": time.time(),
        "data": f"Data from {source}"
    }


async def example_5_error_handling():
    """
    Handling exceptions in concurrent async code.
    
    Important: One task failing doesn't crash the entire program.
    You can use return_exceptions=True with gather() to handle errors gracefully.
    """
    print("\n" + "="*70)
    print("EXAMPLE 5: Error Handling in Async Code")
    print("="*70)
    print("Running concurrent tasks where one will fail...\n")
    
    start = time.perf_counter()
    
    # return_exceptions=True: exceptions are returned as results instead of raised
    results = await asyncio.gather(
        fetch_data_with_error("WeatherAPI", 1.0, should_fail=False),
        fetch_data_with_error("BrokenService", 1.5, should_fail=True),
        fetch_data_with_error("PaymentService", 2.0, should_fail=False),
        return_exceptions=True  # Key parameter for graceful error handling
    )
    
    elapsed = time.perf_counter() - start
    
    # Check which tasks succeeded and which failed
    print("\n  Results:")
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"    Task {i + 1}: ✗ Failed - {type(result).__name__}: {result}")
        else:
            print(f"    Task {i + 1}: ✓ Success - {result['source']}")
    
    print(f"\n⏱️  Total time: {elapsed:.2f}s")
    print(f"💡 Learning: return_exceptions=True prevents one failure from breaking everything")
    print(f"   Other tasks continue running and return their results\n")


# =============================================================================
# MAIN RUNNER
# =============================================================================

async def main():
    """
    Run all examples in sequence.
    
    Observe:
    - Timing differences between sequential and concurrent
    - Execution order in print statements
    - How errors are handled
    """
    print("\n" + "🐍 "*35)
    print(" "*20 + "ASYNC FUNDAMENTALS LEARNING EXAMPLES")
    print("🐍 "*35)
    
    # Run each example
    await example_1_sequential()
    await example_2_concurrent_gather()
    await example_3_create_task()
    await example_4_async_context_manager()
    await example_5_error_handling()
    
    # Summary
    print("\n" + "="*70)
    print("🎓 KEY TAKEAWAYS")
    print("="*70)
    print("""
1. Sequential execution: Total time = sum of all delays
2. Concurrent execution: Total time = max delay (tasks run simultaneously)
3. Event loop switches between tasks during 'await' points
4. create_task() schedules tasks to run immediately in background
5. async with manages resources with async setup/teardown
6. return_exceptions=True handles failures gracefully in gather()

🚀 Async is powerful for I/O-bound operations!
⚠️  But it won't help with CPU-bound calculations.

Next: Apply this to FastAPI endpoints that fetch external data!
""")


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
