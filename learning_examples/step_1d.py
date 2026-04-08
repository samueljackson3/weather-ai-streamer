import asyncio
import time

async def fetch_data_async(n, start_time):
    """Async fetch with timestamp"""
    elapsed = time.perf_counter() - start_time
    print(f"  [{elapsed:.2f}s] Fetch {n} starting...")
    await asyncio.sleep(1)
    elapsed = time.perf_counter() - start_time
    print(f"  [{elapsed:.2f}s] Fetch {n} complete")
    return f"Data {n}"

async def async_with_create_task():
    """Manual task creation - tasks start BEFORE we await them"""
    print("\n=== ASYNC WITH CREATE_TASK() ===")
    start = time.perf_counter()
    
    # create_task() STARTS the task immediately and returns a Task object
    # It doesn't wait for it to complete - it returns right away!
    task1 = asyncio.create_task(fetch_data_async(1, start))
    task2 = asyncio.create_task(fetch_data_async(2, start))
    task3 = asyncio.create_task(fetch_data_async(3, start))
    
    # Between task creation and awaiting, we can do other work
    # But notice: tasks are ALREADY RUNNING in the background!
    print(f"  [All tasks created - they're running now!]")
    
    # Now gather all results by awaiting all tasks
    # This is similar to gather(), but we created tasks manually
    results = await asyncio.gather(task1, task2, task3)
    
    elapsed = time.perf_counter() - start
    print(f"Results: {results}")
    print(f"Time: {elapsed:.2f}s\n")

if __name__ == "__main__":
    asyncio.run(async_with_create_task())
    
    # Key difference from gather():
    # - gather() creates AND awaits tasks in one call
    # - create_task() creates tasks that START IMMEDIATELY
    #   even if you haven't awaited them yet!
