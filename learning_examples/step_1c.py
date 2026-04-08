import asyncio
import time

async def fetch_data_async(n, start_time):
    """Async fetch with timestamp to show when it starts"""
    elapsed = time.perf_counter() - start_time
    print(f"  [{elapsed:.2f}s] Fetch {n} starting...")
    await asyncio.sleep(1)
    elapsed = time.perf_counter() - start_time
    print(f"  [{elapsed:.2f}s] Fetch {n} complete")
    return f"Data {n}"

async def async_concurrent():
    """Version 3: CONCURRENT with gather() - runs all at once!"""
    print("\n=== ASYNC CONCURRENT WITH GATHER() ===")
    start = time.perf_counter()
    
    # gather() creates and runs all tasks CONCURRENTLY
    # All 3 fetches start almost immediately, not one after another
    results = await asyncio.gather(
        fetch_data_async(1, start),
        fetch_data_async(2, start),
        fetch_data_async(3, start),
    )
    
    elapsed = time.perf_counter() - start
    print(f"Results: {results}")
    print(f"Time: {elapsed:.2f}s (all run concurrently, so only 1 second!)\n")

if __name__ == "__main__":
    asyncio.run(async_concurrent())
    
    # Compare the timestamps:
    # - All 3 fetches start at ~0.00s
    # - All 3 complete at ~1.00s
    # Total: ~1 second vs 3 seconds from step_1b!
    #
    # Why? The event loop runs all 3 awaits in parallel within the same thread
