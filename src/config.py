from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    anthropic_api_key: str = ""  # Required for production, optional for testing
    model_name: str = "claude-sonnet-4-5-20250929"
    router_model: str = "claude-haiku-4-5-20250929"  # Fast model for routing
    max_skills_per_request: int = 8

    # Beta flags for Skills API
    skills_beta: str = "skills-2025-10-02"
    code_execution_beta: str = "code-execution-2025-08-25"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()
