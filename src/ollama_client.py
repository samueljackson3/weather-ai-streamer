"""
Ollama integration: prompt building, HTTP calls, and streaming.

Single responsibility: everything LLM-related lives here.
main.py imports from here; doesn't know about Ollama's HTTP API details.
"""

import json
import httpx
from src.models import WeatherResponse
from src.config import settings
from typing import AsyncGenerator


def build_weather_prompt(weather: WeatherResponse) -> str:
    """
    Turn a WeatherResponse into a natural language prompt for the LLM.
    
    Key learning: Prompt engineering is domain-specific string formatting.
    The quality of this string directly impacts summary quality.
    Try different versions and compare outputs.
    """
    unit_label = {"metric": "°C", "imperial": "°F", "standard": "K"}[weather.units.value]
    return (
        f"The current weather in {weather.city}, {weather.country} is "
        f"{weather.temperature}{unit_label} (feels like {weather.feels_like}{unit_label}), "
        f"{weather.description}, humidity {weather.humidity}%, "
        f"wind speed {weather.wind_speed} m/s. "
        f"Write a 2-3 sentence friendly weather summary for someone deciding what to wear today. "
        f"Be specific and practical. Do not mention the city name in the first sentence."
    )


async def call_ollama(prompt: str, client: httpx.AsyncClient) -> str:
    """
    Call Ollama API and wait for the complete response (non-streaming).
    
    Use this first — validate the full pipeline before adding streaming.
    
    Raises:
        httpx.ConnectError: Ollama is not running
        httpx.TimeoutException: Model is taking too long
        ValueError: Unexpected response shape from Ollama
    """
    response = await client.post(
        f"{settings.ollama_url}/api/generate",
        json={"model": "llama3.2:3b", "prompt": prompt, "stream": False},
        timeout=30.0,
    )
    response.raise_for_status()
    data = response.json()
    return data["response"]


async def stream_ollama_summary(
    prompt: str,
    client: httpx.AsyncClient,
) -> AsyncGenerator[str, None]:
    """
    Stream Ollama response tokens as Server-Sent Events.
    
    Key learning: Ollama's streaming API sends newline-delimited JSON.
    Each line is: {"model":"...","response":"token","done":false}
    The last line has "done":true and an empty "response".
    
    We transform each token into SSE format: "data: {token}\\n\\n"
    
    Why AsyncGenerator? It lets FastAPI's StreamingResponse pull tokens
    one at a time without buffering the entire response in memory.
    """
    async with client.stream(
        "POST",
        f"{settings.ollama_url}/api/generate",
        json={"model": "llama3.2:3b", "prompt": prompt, "stream": True},
        timeout=60.0,
    ) as response:
        async for line in response.aiter_lines():
            if not line.strip():
                continue
            try:
                chunk = json.loads(line)
                token = chunk.get("response", "")
                if token:
                    yield f"data: {token}\n\n"
                if chunk.get("done"):
                    yield "data: [DONE]\n\n"
                    return
            except json.JSONDecodeError:
                continue
