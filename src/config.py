"""
Application settings loaded from environment variables via pydantic-settings.

pydantic-settings does two things:
1. Reads .env file automatically
2. Validates all settings at startup (fail fast, not at first use)

If OPENWEATHER_API_KEY is missing, the app refuses to start.
This is better than a 500 error on the first weather request.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    All application settings in one place.
    
    Missing required fields raise an error at app startup.
    This follows the "fail fast" principle — you know immediately if config is wrong.
    
    Compare to Rails:
    - Rails: ENV['KEY'] returns string or nil (no validation, errors at runtime)
    - Pydantic: Validates types at startup, raises clear errors immediately
    """
    
    # OpenWeather API configuration (required)
    openweather_api_key: str  # Will fail to start if not in .env
    openweather_base_url: str = "https://api.openweathermap.org/data/2.5"
    
    # Ollama (local LLM) configuration — ready for Session 3
    ollama_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.1:8b"
    
    # App metadata
    app_version: str = "0.1.0"
    
    # HTTP client configuration
    verify_ssl: bool = True  # Disable in dev (True in production)
    
    model_config = {
        "env_file": ".env",
        "case_sensitive": False,  # Allow both OPENWEATHER_API_KEY and openweather_api_key
    }


# Create a singleton instance
# Import this in other modules: from src.config import settings
settings = Settings()
