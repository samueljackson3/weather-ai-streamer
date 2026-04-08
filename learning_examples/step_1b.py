import asyncio
import time

def fetch_data_sync(n):
    """Synchronous version - BLOCKS the entire program"""
    print(f"  Fetch {n} starting...")
    time.sleep(1)  # Blocks everything - nothing else can run
    print(f"  Fetch {n} complete")
    return f"Data {n}"

async def fetch_data_async(n):
    """Async version - allows event loop to run other tasks"""
    print(f"  Fetch {n} starting...")
    await asyncio.sleep(1)  # Yields control - other tasks COULD run
    print(f"  Fetch {n} complete")
    return f"Data {n}"

def sync_version():
    """Version 1: Synchronous - each fetch blocks the next"""
    print("\n=== SYNCHRONOUS VERSION ===")
    start = time.perf_counter()
    
    results = [fetch_data_sync(i) for i in range(1, 4)]
    
    elapsed = time.perf_counter() - start
    print(f"Results: {results}")
    print(f"Time: {elapsed:.2f}s (each fetch blocks, so 1+1+1 = 3s)\n")

async def async_sequential():
    """Version 2: Async but still SEQUENTIAL - no concurrency yet"""
    print("=== ASYNC SEQUENTIAL VERSION ===")
    start = time.perf_counter()
    
    # Still calling one after another - no parallelism yet!
    results = [await fetch_data_async(i) for i in range(1, 4)]
    
    elapsed = time.perf_counter() - start
    print(f"Results: {results}")
    print(f"Time: {elapsed:.2f}s (still sequential, so 1+1+1 = 3s)\n")

if __name__ == "__main__":
    sync_version()
    asyncio.run(async_sequential())
    
    # Both take ~3 seconds because we're still waiting for each to finish!
    # Step 1C will use gather() to run them CONCURRENTLY (~1s total)
