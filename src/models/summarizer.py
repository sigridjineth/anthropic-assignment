from pydantic import BaseModel, Field


class KeyMoment(BaseModel):
    """An important moment in the conversation."""

    quote: str
    why_important: str
    timestamp: str | None = None


class PredictedQuestion(BaseModel):
    """A predicted upcoming question."""

    question: str
    probability: float = Field(ge=0.0, le=1.0)
    domain: str | None = None


class SummarizerState(BaseModel):
    """Current state from the summarizer agent."""

    summary: str = ""
    key_moments: list[KeyMoment] = Field(default_factory=list)
    predicted_questions: list[PredictedQuestion] = Field(default_factory=list)
    customer_profile: dict = Field(default_factory=dict)
