from pydantic import BaseModel, Field


class Source(BaseModel):
    """A source reference for an answer."""

    title: str
    file: str
    excerpt: str | None = None


class Solution(BaseModel):
    """A concrete, actionable solution."""

    action: str  # e.g., "Use context.summarize()"
    benefit: str  # e.g., "Reduces token usage by 60%"
    source: str  # e.g., "cdp_context_editing"


class AnswerDraft(BaseModel):
    """A draft answer from the answerer agent."""

    headline: str = ""  # One-line direct answer
    solutions: list[Solution] = Field(default_factory=list)  # Actionable solutions
    answer: str = ""  # Full conversational answer
    sources: list[Source] = Field(default_factory=list)
    confidence: float = Field(ge=0.0, le=1.0, default=0.5)
    caveats: list[str] = Field(default_factory=list)
    followups: list[str] = Field(default_factory=list)
    skills_used: list[str] = Field(default_factory=list)
