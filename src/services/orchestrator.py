import time
from datetime import datetime
from ..agents import RouterAgent, SummarizerAgent, AnswererAgent
from ..models import TranscriptEntry, SkillDomain, AnswerDraft
from .session import Session, SkillFiredEvent

SKILL_COOLDOWN_SEC = 20.0


class Orchestrator:
    """Coordinates the 3-agent system."""

    def __init__(self):
        self.router = RouterAgent()
        self.summarizer = SummarizerAgent()
        self.answerer = AnswererAgent()

    async def process_transcript(self, session: Session, entry: TranscriptEntry) -> None:
        """Process a new transcript entry through the agent pipeline."""
        # Build context from recent transcript
        recent_text = self._get_recent_text(session)

        # 1. Router: Decide which skills to activate
        router_decision = await self.router.route(
            transcript_text=recent_text,
            current_skills=session.active_skills,
            customer_context=session.summarizer_state.summary if session.summarizer_state else None,
        )
        session.router_decision = router_decision

        # 2. Check if we should activate skills (respecting cooldown)
        if router_decision.needs_skill and router_decision.suggested_skills:
            skills_to_activate = []
            for skill in router_decision.suggested_skills:
                if self._should_fire_skill(session, skill.domain.value):
                    skills_to_activate.append(skill.domain.value)
                    self._record_skill_fire(session, skill.domain.value)

            if skills_to_activate:
                session.active_skills = skills_to_activate
                session.skill_fired_log.append(
                    SkillFiredEvent(
                        timestamp=datetime.now(),
                        domains=skills_to_activate,
                        trigger_reason=router_decision.trigger_reason,
                        confidence=router_decision.suggested_skills[0].confidence,
                        detected_question=router_decision.detected_question,
                    )
                )

        # 3. Summarizer: Update conversation summary
        summarizer_state = await self.summarizer.summarize(
            previous_state=session.summarizer_state,
            recent_transcript=recent_text,
        )
        session.summarizer_state = summarizer_state

        # 4. Answerer: Generate answer if there's a detected question
        if router_decision.detected_question and router_decision.urgency in ["high", "medium"]:
            skill_domains = [SkillDomain(s) for s in session.active_skills if s in [d.value for d in SkillDomain]]
            if skill_domains:
                answer = await self.answerer.answer(
                    question=router_decision.detected_question,
                    context=recent_text,
                    skill_domains=skill_domains,
                )
                session.current_answer = answer

    async def ask_question(self, session: Session, question: str) -> AnswerDraft:
        """Direct question to the answerer."""
        recent_text = self._get_recent_text(session)

        # First route to find relevant skills
        router_decision = await self.router.route(
            transcript_text=f"{recent_text}\n\n[Sales Rep Question]: {question}",
            current_skills=session.active_skills,
        )

        # Determine which skills to use
        skill_domains = []
        if router_decision.suggested_skills:
            skill_domains = [s.domain for s in router_decision.suggested_skills[:3]]
        elif session.active_skills:
            skill_domains = [SkillDomain(s) for s in session.active_skills if s in [d.value for d in SkillDomain]]

        # Generate answer
        answer = await self.answerer.answer(
            question=question,
            context=recent_text,
            skill_domains=skill_domains,
        )

        session.current_answer = answer
        return answer

    def _get_recent_text(self, session: Session, count: int = 10) -> str:
        """Get recent transcript as text."""
        entries = session.transcript[-count:]
        lines = []
        for entry in entries:
            speaker = entry.speaker.capitalize()
            lines.append(f"[{speaker}] {entry.text}")
        return "\n".join(lines)

    def _should_fire_skill(self, session: Session, domain: str) -> bool:
        """Check if a skill can fire (respecting cooldown)."""
        if domain not in session.last_skill_fire:
            return True

        last_fire = session.last_skill_fire[domain]
        elapsed = (datetime.now() - last_fire).total_seconds()
        return elapsed >= SKILL_COOLDOWN_SEC

    def _record_skill_fire(self, session: Session, domain: str) -> None:
        """Record that a skill was fired."""
        session.last_skill_fire[domain] = datetime.now()
