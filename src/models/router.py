from enum import Enum
from pydantic import BaseModel, Field


class SkillDomain(str, Enum):
    """Available skill domains for CDP DevRel."""

    CDP_CONTEXT_EDITING = "cdp_context_editing"
    CDP_MEMORY = "cdp_memory"
    CDP_SKILLS = "cdp_skills"
    FINTECH_PATTERNS = "fintech_patterns"
    PRICING_GUIDANCE = "pricing_guidance"


class SkillSuggestion(BaseModel):
    """A suggested skill with confidence."""

    domain: SkillDomain
    confidence: float = Field(ge=0.0, le=1.0)


class RouterDecision(BaseModel):
    """Decision from the router agent."""

    needs_skill: bool = False
    suggested_skills: list[SkillSuggestion] = Field(default_factory=list)
    trigger_reason: str = ""
    detected_question: str | None = None
    urgency: str = Field(default="low", pattern="^(high|medium|low)$")
