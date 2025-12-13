from pydantic import BaseModel, Field
import time


class SkillFiredEvent(BaseModel):
    """Record of a skill activation event."""
    timestamp: float = Field(default_factory=time.time)
    domains: list[str] = Field(default_factory=list)
    trigger_reason: str = ""
    confidence: float = Field(ge=0.0, le=1.0, default=0.0)
    detected_question: str | None = None
    urgency: str = "low"

    @property
    def relative_time_str(self) -> str:
        """Human-readable relative time."""
        elapsed = time.time() - self.timestamp
        if elapsed < 60:
            return f"{int(elapsed)}s ago"
        elif elapsed < 3600:
            return f"{int(elapsed / 60)}m ago"
        else:
            return f"{int(elapsed / 3600)}h ago"
