import asyncio
import time

async def simple_task():
    """async = declares this function as asynchronous (can use await inside)"""
    print("Starting task")
    
    # await = pauses this function until asyncio.sleep(1) completes
    # During the pause, other async tasks could run
    await asyncio.sleep(1)
    
    print("Task complete")
    return "Task complete"

if __name__ == "__main__":
    start = time.perf_counter()
    
    # asyncio.run() = starts event loop and runs the async function
    result = asyncio.run(simple_task())
    
    elapsed = time.perf_counter() - start
    print(f"Result: {result}")
    print(f"Time elapsed: {elapsed:.2f}s")
