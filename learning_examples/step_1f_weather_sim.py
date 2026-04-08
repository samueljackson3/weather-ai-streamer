import asyncio
import random
import time

async def fetch_weather(city, start_time):
    """Fetch weather for a city with random delay (0.5s - 3s)"""
    delay = random.uniform(0.5, 3.0)
    await asyncio.sleep(delay)
    
    # Vancouver fails 50% of the time
    if city == "Vancouver" and random.random() < 0.5:
        raise Exception(f"Failed to fetch weather for {city}")
    
    elapsed = time.perf_counter() - start_time
    return {
        "city": city,
        "delay": delay,
        "timestamp": elapsed,
        "temp": random.randint(50, 75)
    }

async def main():
    """Orchestrate fetching weather from 5 cities"""
    cities = ["Seattle", "Portland", "Vancouver", "San Francisco", "Los Angeles"]
    start = time.perf_counter()
    
    print("Starting weather fetch for 5 cities...\n")
    
    # Create tasks for all cities
    tasks = [asyncio.create_task(fetch_weather(city, start)) for city in cities]
    
    # Process results as they complete
    results = []
    all_delays = []  # Track actual delays to calculate theoretical time
    
    for future in asyncio.as_completed(tasks):
        try:
            result = await future
            elapsed = time.perf_counter() - start
            print(f"✓ {result['city']:15} | Arrived at: {result['timestamp']:6.2f}s | "
                  f"Temp: {result['temp']}°F | Delay: {result['delay']:.2f}s")
            results.append(result)
            all_delays.append(result['delay'])
        except Exception as e:
            elapsed = time.perf_counter() - start
            print(f"✗ {str(e):40} | Elapsed: {elapsed:6.2f}s")
    
    # Calculate theoretical sequential time from ACTUAL delays
    theoretical_time = sum(all_delays)
    
    # Summary
    total_time = time.perf_counter() - start
    print(f"\n{'='*70}")
    print(f"Total elapsed time (parallel):  {total_time:.2f}s")
    print(f"Theoretical time (sequential):  {theoretical_time:.2f}s")
    print(f"Speed improvement:              {theoretical_time/total_time:.1f}x faster")
    print(f"{'='*70}\n")
    print(f"Successfully fetched: {len(results)}/{len(cities)} cities")

if __name__ == "__main__":
    asyncio.run(main())