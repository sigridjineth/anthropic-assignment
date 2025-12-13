from enum import Enum
from pydantic import BaseModel, Field


class EscalationType(str, Enum):
    ASK_ENG_SLACK = "ask_eng_slack"
    SCHEDULE_FOLLOWUP = "schedule_followup"


class Source(BaseModel):
    title: str
    file: str
    excerpt: str | None = Field(default=None, description="1-2 line summary")


class EscalationAction(BaseModel):
    type: EscalationType
    draft_message: str


class AnswerDraft(BaseModel):
    answer: str
    sources: list[Source] = Field(default_factory=list)
    confidence: float = Field(ge=0.0, le=1.0, default=0.5)
    caveats: list[str] = Field(default_factory=list)
    followups: list[str] = Field(default_factory=list)
    escalation_action: EscalationAction | None = None
    skills_used: list[str] = Field(default_factory=list, description="Domains used")
