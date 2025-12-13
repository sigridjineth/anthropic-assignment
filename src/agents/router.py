import json
import re
import anthropic
from ..config import get_settings
from ..models import RouterDecision, SkillSuggestion, SkillDomain

SYSTEM_PROMPT = """You are a skill routing agent for a Technical Sales copilot. Analyze the transcript to determine if any skills should be activated.

Available skills:
- roadmap: For questions about timelines, feature availability, GA dates, product direction
- architecture: For questions about how things work, data flow, system design, technical implementation
- security: For questions about SOC2, compliance, encryption, data residency, on-prem, privacy
- pricing: For questions about costs, plans, enterprise pricing, discounts

Your output must be valid JSON:
{
    "needs_skill": true/false,
    "suggested_skills": [{"domain": "skill_name", "confidence": 0.0-1.0}],
    "trigger_reason": "Why this skill was selected",
    "detected_question": "The customer's question if one was detected, or null",
    "urgency": "high/medium/low"
}

Guidelines:
- Set needs_skill to true only if a clear question or topic requiring specialized knowledge is detected
- Confidence should reflect how certain you are that this skill is relevant
- High urgency means the customer asked a direct question that needs immediate answer
- Medium urgency means the topic came up but wasn't a direct question
- Low urgency means it might be relevant soon but isn't needed now"""


class RouterAgent:
    def __init__(self):
        settings = get_settings()
        self.client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
        self.model = settings.model_name

    async def route(
        self,
        transcript_text: str,
        current_skills: list[str] | None = None,
        customer_context: str | None = None,
    ) -> RouterDecision:
        """Analyze transcript and decide which skills to activate."""
        user_message = self._format_input(transcript_text, current_skills, customer_context)

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_message}],
        )

        return self._parse_response(response)

    def _format_input(
        self,
        transcript_text: str,
        current_skills: list[str] | None,
        customer_context: str | None,
    ) -> str:
        parts = [f"Recent transcript:\n{transcript_text}"]

        if current_skills:
            parts.append(f"\nCurrently active skills: {', '.join(current_skills)}")

        if customer_context:
            parts.append(f"\nCustomer context: {customer_context}")

        return "\n".join(parts)

    def _parse_response(self, response) -> RouterDecision:
        content = response.content[0].text

        json_match = re.search(r"\{.*\}", content, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group())

            suggested_skills = []
            for s in data.get("suggested_skills", []):
                try:
                    domain = SkillDomain(s.get("domain", "").lower())
                    suggested_skills.append(
                        SkillSuggestion(domain=domain, confidence=s.get("confidence", 0.5))
                    )
                except ValueError:
                    continue

            return RouterDecision(
                needs_skill=data.get("needs_skill", False),
                suggested_skills=suggested_skills,
                trigger_reason=data.get("trigger_reason", ""),
                detected_question=data.get("detected_question"),
                urgency=data.get("urgency", "low"),
            )

        return RouterDecision(needs_skill=False)
