from pydantic import BaseModel, Field


class Source(BaseModel):
    """A source reference for an answer."""

    title: str
    file: str
    excerpt: str | None = None


class AnswerDraft(BaseModel):
    """A draft answer from the answerer agent."""

    answer: str
    sources: list[Source] = Field(default_factory=list)
    confidence: float = Field(ge=0.0, le=1.0, default=0.5)
    caveats: list[str] = Field(default_factory=list)
    followups: list[str] = Field(default_factory=list)
    skills_used: list[str] = Field(default_factory=list)
