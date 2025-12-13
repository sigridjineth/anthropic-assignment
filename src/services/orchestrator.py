import time
from ..models import (
    TranscriptEntry,
    RouterDecision,
    AnswerDraft,
    SummarizerState,
    SkillDomain,
    SkillFiredEvent,
)
from .transcript import TranscriptStore
from ..agents.router import RouterAgent
from ..agents.answerer import AnswererAgent

# Cooldown settings
SKILL_COOLDOWN_SEC = 20.0
SUMMARIZER_INTERVAL_SEC = 45.0


class Orchestrator:
    def __init__(self):
        self.router_agent = RouterAgent()
        self.answerer_agent = AnswererAgent()
        self.summarizer_agent = None  # Will be initialized lazily
        self.last_router_decision: RouterDecision | None = None
        self.last_answer: AnswerDraft | None = None
        self.summarizer_state: SummarizerState = SummarizerState()
        self.active_skills: list[str] = []

        # Cooldown tracking: domain -> last fire timestamp
        self.last_skill_fire: dict[str, float] = {}
        # Event log
        self.skill_fired_log: list[SkillFiredEvent] = []
        # Summarizer timing
        self.last_summarizer_run: float = 0.0

    def _should_fire_skill(self, domain: str) -> bool:
        """Check if a skill can fire (respecting cooldown)."""
        now = time.time()
        if domain in self.last_skill_fire:
            if now - self.last_skill_fire[domain] < SKILL_COOLDOWN_SEC:
                return False
        return True

    def _record_skill_fire(self, domains: list[str], decision: RouterDecision) -> None:
        """Record skill activation and update cooldown."""
        now = time.time()
        for domain in domains:
            self.last_skill_fire[domain] = now

        # Add to event log
        if domains:
            avg_confidence = sum(
                s.confidence for s in decision.suggested_skills
                if s.domain.value in domains
            ) / len(domains) if domains else 0.0

            event = SkillFiredEvent(
                timestamp=now,
                domains=domains,
                trigger_reason=decision.trigger_reason,
                confidence=avg_confidence,
                detected_question=decision.detected_question,
                urgency=decision.urgency.value,
            )
            self.skill_fired_log.append(event)
            # Keep last 50 events
            if len(self.skill_fired_log) > 50:
                self.skill_fired_log = self.skill_fired_log[-50:]

    async def _maybe_run_summarizer(self, store: TranscriptStore) -> None:
        """Run summarizer if enough time has passed."""
        now = time.time()
        if now - self.last_summarizer_run < SUMMARIZER_INTERVAL_SEC:
            return

        # Lazy import to avoid circular dependency
        if self.summarizer_agent is None:
            from ..agents.summarizer import SummarizerAgent
            self.summarizer_agent = SummarizerAgent()

        try:
            recent_text = store.get_recent_text(seconds=60.0)
            full_text = store.get_full_text()
            self.summarizer_state = await self.summarizer_agent.summarize(
                previous_state=self.summarizer_state,
                recent_transcript=recent_text,
                full_transcript=full_text,
            )
            self.last_summarizer_run = now
        except Exception:
            pass  # Summarizer failure is non-critical

    async def on_transcript_added(
        self,
        entry: TranscriptEntry,
        store: TranscriptStore,
    ) -> None:
        # Run router on new entry
        recent_text = store.get_recent_text(seconds=60.0)
        decision = await self.router_agent.route(recent_text)
        self.last_router_decision = decision

        # Filter skills by cooldown
        if decision.needs_skill:
            eligible_skills = [
                s for s in decision.suggested_skills[:3]
                if self._should_fire_skill(s.domain.value)
            ]
            if eligible_skills:
                domains = [s.domain.value for s in eligible_skills]
                self.active_skills = domains
                self._record_skill_fire(domains, decision)
            # If no eligible skills (all on cooldown), keep previous active_skills

        # Auto-answer if urgency is high
        if decision.urgency.value == "high" and decision.detected_question:
            skill_domains = [
                s.domain for s in decision.suggested_skills
                if self._should_fire_skill(s.domain.value)
            ]
            if skill_domains:
                self.last_answer = await self.answerer_agent.answer(
                    question=decision.detected_question,
                    context=recent_text,
                    skill_domains=skill_domains,
                    with_skills=True,
                )

        # Maybe run summarizer
        await self._maybe_run_summarizer(store)

    async def ask(
        self,
        question: str,
        transcript_store: TranscriptStore,
        with_skills: bool = True,
    ) -> AnswerDraft:
        # First route to get relevant skills
        recent_text = transcript_store.get_recent_text(seconds=60.0)
        decision = await self.router_agent.route(recent_text + f"\n[user question]: {question}")
        self.last_router_decision = decision

        # Get skill domains (no cooldown for explicit asks)
        skill_domains = [s.domain for s in decision.suggested_skills] if with_skills else []

        # Record skill fire for asks too
        if with_skills and decision.needs_skill:
            domains = [s.domain.value for s in decision.suggested_skills[:3]]
            self._record_skill_fire(domains, decision)
            self.active_skills = domains

        # Answer with skills
        answer = await self.answerer_agent.answer(
            question=question,
            context=recent_text,
            skill_domains=skill_domains,
            with_skills=with_skills,
        )
        self.last_answer = answer
        return answer
