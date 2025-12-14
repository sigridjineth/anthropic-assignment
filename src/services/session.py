import uuid
from dataclasses import dataclass, field
from datetime import datetime
from ..models import (
    PrepResult,
    TranscriptEntry,
    RouterDecision,
    AnswerDraft,
    SummarizerState,
    PostCallResult,
)


@dataclass
class SkillFiredEvent:
    """Record of a skill activation."""

    timestamp: datetime
    domains: list[str]
    trigger_reason: str
    confidence: float
    detected_question: str | None


@dataclass
class Session:
    """A sales copilot session."""

    id: str
    company: str
    created_at: datetime = field(default_factory=datetime.now)

    # Prep data
    prep_result: PrepResult | None = None

    # Transcript
    transcript: list[TranscriptEntry] = field(default_factory=list)

    # Agent states
    router_decision: RouterDecision | None = None
    summarizer_state: SummarizerState | None = None
    current_answer: AnswerDraft | None = None

    # Skill tracking
    active_skills: list[str] = field(default_factory=list)
    recommended_skills: list[str] = field(default_factory=list)
    skill_fired_log: list[SkillFiredEvent] = field(default_factory=list)

    # Cooldown tracking
    last_skill_fire: dict[str, datetime] = field(default_factory=dict)

    # Post-call
    ended_at: datetime | None = None
    post_call_result: PostCallResult | None = None
    archive_path: str | None = None  # Path to interview_records archive


class SessionStore:
    """In-memory session storage."""

    def __init__(self):
        self._sessions: dict[str, Session] = {}

    def create(self, company: str, prep_result: PrepResult | None = None) -> Session:
        """Create a new session."""
        session_id = str(uuid.uuid4())[:8]

        # Pre-attach top 2 skills, rest stay as recommended
        all_recommended = prep_result.recommended_skills if prep_result else []
        pre_attached = all_recommended[:2]  # First 2 are pre-attached
        remaining = all_recommended  # All stay in recommended for reference

        session = Session(
            id=session_id,
            company=company,
            prep_result=prep_result,
            active_skills=pre_attached,
            recommended_skills=remaining,
        )
        self._sessions[session_id] = session
        return session

    def get(self, session_id: str) -> Session | None:
        """Get a session by ID."""
        return self._sessions.get(session_id)

    def add_transcript(self, session_id: str, entry: TranscriptEntry) -> bool:
        """Add a transcript entry to a session."""
        session = self.get(session_id)
        if not session:
            return False
        session.transcript.append(entry)
        return True

    def get_recent_transcript(self, session_id: str, count: int = 10) -> str:
        """Get recent transcript as text."""
        session = self.get(session_id)
        if not session:
            return ""

        entries = session.transcript[-count:]
        lines = []
        for entry in entries:
            speaker = entry.speaker.capitalize()
            lines.append(f"[{speaker}] {entry.text}")

        return "\n".join(lines)


# Global session store
session_store = SessionStore()
