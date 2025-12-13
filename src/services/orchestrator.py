from ..models import (
    TranscriptEntry,
    RouterDecision,
    AnswerDraft,
    SummarizerState,
    SkillDomain,
)
from .transcript import TranscriptStore
from ..agents.router import RouterAgent
from ..agents.answerer import AnswererAgent


class Orchestrator:
    def __init__(self):
        self.router_agent = RouterAgent()
        self.answerer_agent = AnswererAgent()
        self.last_router_decision: RouterDecision | None = None
        self.last_answer: AnswerDraft | None = None
        self.summarizer_state: SummarizerState = SummarizerState()
        self.active_skills: list[str] = []

    async def on_transcript_added(
        self,
        entry: TranscriptEntry,
        store: TranscriptStore,
    ) -> None:
        # Run router on new entry
        recent_text = store.get_recent_text(seconds=60.0)
        decision = await self.router_agent.route(recent_text)
        self.last_router_decision = decision

        # Update active skills
        if decision.needs_skill:
            self.active_skills = [s.domain.value for s in decision.suggested_skills[:3]]

        # Auto-answer if urgency is high
        if decision.urgency.value == "high" and decision.detected_question:
            self.last_answer = await self.answerer_agent.answer(
                question=decision.detected_question,
                context=recent_text,
                skill_domains=[s.domain for s in decision.suggested_skills],
                with_skills=True,
            )

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

        # Get skill domains
        skill_domains = [s.domain for s in decision.suggested_skills] if with_skills else []

        # Answer with skills
        answer = await self.answerer_agent.answer(
            question=question,
            context=recent_text,
            skill_domains=skill_domains,
            with_skills=with_skills,
        )
        self.last_answer = answer
        return answer
