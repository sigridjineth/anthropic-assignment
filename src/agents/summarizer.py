"""
Summarizer Agent - Maintains live conversation summary.

Uses Anthropic's tool use feature for reliable structured JSON responses.
See: https://docs.anthropic.com/en/docs/build-with-claude/tool-use
"""

import anthropic
from ..config import get_settings, PERSONA_SYSTEM_CONTEXT
from ..models import SummarizerState, KeyMoment, PredictedQuestion

SYSTEM_PROMPT = f"""{PERSONA_SYSTEM_CONTEXT}

---

You are a conversation summarizer helping Sigrid during a customer call. Analyze the transcript and provide a structured summary.

Guidelines:
- Keep the summary concise and focused on business implications
- Key moments should capture decision-making signals or important requirements
- Predicted questions should help Sigrid prepare for what the customer might ask next
- Customer profile should be inferred from the conversation

Use the update_summary tool to provide your summary."""

# Tool definition for structured output
SUMMARIZER_TOOL = {
    "name": "update_summary",
    "description": "Update the conversation summary with new information",
    "input_schema": {
        "type": "object",
        "properties": {
            "summary": {
                "type": "string",
                "description": "A 2-3 sentence summary of the conversation so far"
            },
            "key_moments": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "quote": {"type": "string", "description": "Important quote from the conversation"},
                        "why_important": {"type": "string", "description": "Why this matters for the sale"},
                        "timestamp": {"type": ["string", "null"], "description": "Optional timestamp"}
                    },
                    "required": ["quote", "why_important"]
                },
                "description": "Key moments from the conversation"
            },
            "predicted_questions": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "question": {"type": "string", "description": "What the customer might ask next"},
                        "probability": {"type": "number", "description": "Likelihood 0.0-1.0"},
                        "domain": {
                            "type": ["string", "null"],
                            "enum": ["cdp_context_editing", "cdp_memory", "cdp_skills", "fintech_patterns", "pricing_guidance", None],
                            "description": "Related skill domain"
                        }
                    },
                    "required": ["question", "probability"]
                },
                "description": "Predicted next questions"
            },
            "customer_profile": {
                "type": "object",
                "properties": {
                    "industry": {"type": "string"},
                    "needs": {"type": "array", "items": {"type": "string"}},
                    "constraints": {"type": "array", "items": {"type": "string"}},
                    "decision_stage": {
                        "type": "string",
                        "enum": ["early", "middle", "late"]
                    }
                },
                "description": "Inferred customer profile"
            }
        },
        "required": ["summary", "key_moments", "predicted_questions", "customer_profile"]
    }
}


class SummarizerAgent:
    """Agent that maintains conversation summary using tool use."""

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
            tools=[SUMMARIZER_TOOL],
            tool_choice={"type": "tool", "name": "update_summary"},
            messages=[{"role": "user", "content": user_message}],
        )

        return self._parse_response(response)

    def _format_input(
        self,
        previous_state: SummarizerState | None,
        recent_transcript: str,
    ) -> str:
        """Format input for Claude."""
        parts = []

        if previous_state and previous_state.summary:
            parts.append(f"Previous summary: {previous_state.summary}")

        parts.append(f"New transcript:\n{recent_transcript}")

        return "\n\n".join(parts)

    def _parse_response(self, response) -> SummarizerState:
        """Parse tool use response."""
        # Find the tool use block
        for block in response.content:
            if block.type == "tool_use" and block.name == "update_summary":
                data = block.input

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

        # Fallback if tool use not found
        return SummarizerState(summary="Unable to summarize conversation.")
