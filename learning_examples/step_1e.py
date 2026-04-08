import asyncio
import random

async def fetch_data_async(n):
    """Async fetch that may fail randomly (50% chance)"""
    print(f"  Fetch {n} starting...")
    await asyncio.sleep(1)
    
    # 50% chance this fetch raises an exception
    if random.random() < 0.5:
        raise ValueError(f"Fetch {n} failed!")
    
    print(f"  Fetch {n} complete")
    return f"Data {n}"

async def approach_1_try_except():
    """Approach 1: try/except around gather()"""
    print("\n=== APPROACH 1: try/except ===")
    try:
        # If ANY task raises, gather() raises immediately
        results = await asyncio.gather(
            fetch_data_async(1),
            fetch_data_async(2),
            fetch_data_async(3),
        )
        print(f"Results: {results}")
    except ValueError as e:
        # If a task fails, we catch the FIRST exception
        # Other tasks might still be running in background!
        print(f"ERROR: {e}")
        print("(Other tasks might still be running...)\n")

async def approach_2_return_exceptions():
    """Approach 2: gather() with return_exceptions=True"""
    print("=== APPROACH 2: return_exceptions=True ===")
    # return_exceptions=True means errors are returned as VALUES, not raised
    results = await asyncio.gather(
        fetch_data_async(1),
        fetch_data_async(2),
        fetch_data_async(3),
        return_exceptions=True
    )
    
    # results now contains both success VALUES and exception OBJECTS
    print(f"Results: {results}")
    for i, result in enumerate(results, 1):
        if isinstance(result, Exception):
            print(f"  Fetch {i}: ERROR - {result}")
        else:
            print(f"  Fetch {i}: {result}\n")

async def main():
    print("Run this multiple times - output will differ due to randomness!\n")
    await approach_1_try_except()
    await approach_2_return_exceptions()

if __name__ == "__main__":
    asyncio.run(main())
    
    # When to use each:
    # Approach 1: When you need to FAIL FAST (stop on first error)
    # Approach 2: When you need ALL results even if some fail (resilience)
