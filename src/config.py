from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    anthropic_api_key: str = ""
    model_name: str = "claude-sonnet-4-20250514"

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache
def get_settings() -> Settings:
    return Settings()


# Persona configuration
PERSONA = {
    "name": "Sigrid",
    "role": "Developer Relations IC",
    "company": "Anthropic",
    "mission": "Help developers build better with Claude",
    "context": """Today's call:
- Technical discovery with potential enterprise customer
- They're evaluating Claude for their AI product
- Need to understand their use case, recommend CDP features""",
    "tools": """Your tools:
- Skills: CDP feature docs, pricing, case studies, best practices
- Goal: Match their problem to the right platform feature"""
}


# Persona context to inject into Claude calls
PERSONA_SYSTEM_CONTEXT = f"""You are helping {PERSONA['name']}, an {PERSONA['company']} {PERSONA['role']}.

{PERSONA['name']}'s role:
- {PERSONA['mission']}
- Technical discovery with enterprise customers
- Match customer problems to Claude Developer Platform (CDP) features

{PERSONA['name']}'s tools:
- CDP feature docs (Context Editing, Memory, Skills)
- Pricing guidance and ROI calculations
- Industry patterns and case studies (especially fintech)

Respond in a way that helps {PERSONA['name']} during the customer call. Be specific, use numbers, and cite sources from the attached skills."""
