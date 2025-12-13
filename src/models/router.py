from enum import Enum
from pydantic import BaseModel, Field


class SkillDomain(str, Enum):
    ROADMAP = "roadmap"
    ARCHITECTURE = "architecture"
    SECURITY = "security"
    PRICING = "pricing"
    CASE_STUDIES = "case_studies"
    COMPETITIVE = "competitive"
    INTEGRATION = "integration"
    DEPLOYMENT = "deployment"


class Urgency(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class SkillSuggestion(BaseModel):
    domain: SkillDomain
    skill_id: str | None = Field(default=None, description="Actual skill_01... ID")
    priority: int = Field(ge=1, le=5, default=3)
    confidence: float = Field(ge=0.0, le=1.0)


class RouterDecision(BaseModel):
    needs_skill: bool
    suggested_skills: list[SkillSuggestion] = Field(default_factory=list)
    trigger_reason: str = ""
    urgency: Urgency = Urgency.LOW
    detected_question: str | None = None
