from pydantic import BaseModel, Field


class PrepInput(BaseModel):
    """Input for session preparation."""

    company: str = Field(default="Unknown Company")
    industry: str = Field(default="enterprise")
    roles: list[str] = Field(default_factory=list)
    purpose: str = Field(default="discovery")  # discovery | technical | pricing
    sensitive_topics: list[str] = Field(default_factory=list)
    competitors: str | None = None
    raw_context: str | None = None  # Raw user input for AI to parse


class LikelyTopic(BaseModel):
    """A likely topic for the call."""

    topic: str
    reason: str
    confidence: float | None = None  # 0.0 - 1.0


class PrepResult(BaseModel):
    """Output from session preparation."""

    session_brief: str
    likely_topics: list[LikelyTopic]
    discovery_questions: list[str]
    recommended_skills: list[str]
