from datetime import datetime
from pydantic import BaseModel, Field


class TranscriptEntry(BaseModel):
    """A single entry in the call transcript."""

    speaker: str = Field(..., pattern="^(customer|sigrid)$")
    text: str = Field(..., min_length=1)
    timestamp: datetime = Field(default_factory=datetime.now)
