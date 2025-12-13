from enum import Enum
from pydantic import BaseModel, Field
import uuid
import time


class Speaker(str, Enum):
    PROSPECT = "prospect"
    SALES = "sales"
    SE = "se"  # Sales Engineer


class TranscriptEntry(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    ts_ms: int = Field(default_factory=lambda: int(time.time() * 1000))
    offset_sec: float = Field(description="Seconds from call start")
    speaker: Speaker
    text: str
    confidence: float | None = Field(default=None, description="STT confidence 0-1")

    def is_question(self) -> bool:
        return "?" in self.text
