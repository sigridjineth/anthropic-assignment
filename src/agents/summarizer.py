import json
import re
import anthropic
from ..config import get_settings
from ..models import SummarizerState, KeyMoment, PredictedQuestion

SYSTEM_PROMPT = """You are a conversation summarizer for a Technical Sales copilot. Analyze the transcript and provide a structured summary.

Your output must be valid JSON:
{
    "summary": "A 2-3 sentence summary of the conversation so far",
    "key_moments": [
        {"quote": "Important quote", "why_important": "Why this matters", "timestamp": "optional"}
    ],
    "predicted_questions": [
        {"question": "What the customer might ask next", "probability": 0.0-1.0, "domain": "skill_domain or null"}
    ],
    "customer_profile": {
        "industry": "Their industry",
        "needs": ["List of needs"],
        "constraints": ["List of constraints"],
        "decision_stage": "early/middle/late"
    }
}

Guidelines:
- Keep the summary concise and focused on business implications
- Key moments should capture decision-making signals or important requirements
- Predicted questions should help the sales rep prepare
- Customer profile should be inferred from the conversation"""


class SummarizerAgent:
    def __init__(self):
        settings = get_settings()
        self.client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
        self.model = settings.model_name

    async def summarize(
        self,
        previous_state: SummarizerState | None,
        recent_transcript: str,
    ) -> SummarizerState:
        """Update the conversation summary."""
        user_message = self._format_input(previous_state, recent_transcript)

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_message}],
        )

        return self._parse_response(response)

    def _format_input(
        self,
        previous_state: SummarizerState | None,
        recent_transcript: str,
    ) -> str:
        parts = []

        if previous_state and previous_state.summary:
            parts.append(f"Previous summary: {previous_state.summary}")

        parts.append(f"New transcript:\n{recent_transcript}")

        return "\n\n".join(parts)

    def _parse_response(self, response) -> SummarizerState:
        content = response.content[0].text

        json_match = re.search(r"\{.*\}", content, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group())

            key_moments = [
                KeyMoment(
                    quote=m.get("quote", ""),
                    why_important=m.get("why_important", ""),
                    timestamp=m.get("timestamp"),
                )
                for m in data.get("key_moments", [])
            ]

            predicted_questions = [
                PredictedQuestion(
                    question=q.get("question", ""),
                    probability=q.get("probability", 0.5),
                    domain=q.get("domain"),
                )
                for q in data.get("predicted_questions", [])
            ]

            return SummarizerState(
                summary=data.get("summary", ""),
                key_moments=key_moments,
                predicted_questions=predicted_questions,
                customer_profile=data.get("customer_profile", {}),
            )

        return SummarizerState(summary=content[:500])
