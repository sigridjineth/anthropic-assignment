from pydantic import BaseModel, Field


class PrepInput(BaseModel):
    """Input for session preparation."""

    company: str = Field(..., min_length=1)
    industry: str = Field(..., min_length=1)
    roles: list[str] = Field(default_factory=list)
    purpose: str = Field(default="discovery")  # discovery | technical | pricing
    sensitive_topics: list[str] = Field(default_factory=list)
    competitors: str | None = None


class LikelyTopic(BaseModel):
    """A likely topic for the call."""

    topic: str
    reason: str


class PrepResult(BaseModel):
    """Output from session preparation."""

    session_brief: str
    likely_topics: list[LikelyTopic]
    discovery_questions: list[str]
    recommended_skills: list[str]
