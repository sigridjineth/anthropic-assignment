"""
Router Agent - Determines which skills to activate based on transcript.

Uses Anthropic's tool use feature for reliable structured JSON responses.
See: https://docs.anthropic.com/en/docs/build-with-claude/tool-use
"""

import anthropic
from ..config import get_settings
from ..models import RouterDecision, SkillSuggestion, SkillDomain

SYSTEM_PROMPT = """You are a skill routing agent for a Technical Sales copilot. Analyze the transcript to determine if any skills should be activated.

Available skills:
- roadmap: For questions about timelines, feature availability, GA dates, product direction
- architecture: For questions about how things work, data flow, system design, technical implementation
- security: For questions about SOC2, compliance, encryption, data residency, on-prem, privacy
- pricing: For questions about costs, plans, enterprise pricing, discounts

Guidelines:
- Set needs_skill to true only if a clear question or topic requiring specialized knowledge is detected
- Confidence should reflect how certain you are that this skill is relevant
- High urgency means the customer asked a direct question that needs immediate answer
- Medium urgency means the topic came up but wasn't a direct question
- Low urgency means it might be relevant soon but isn't needed now

Use the route_skills tool to provide your routing decision."""

# Tool definition for structured output
ROUTER_TOOL = {
    "name": "route_skills",
    "description": "Determine which skills should be activated based on the transcript",
    "input_schema": {
        "type": "object",
        "properties": {
            "needs_skill": {
                "type": "boolean",
                "description": "Whether any skill needs to be activated"
            },
            "suggested_skills": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "domain": {
                            "type": "string",
                            "enum": ["roadmap", "architecture", "security", "pricing"],
                            "description": "Skill domain to activate"
                        },
                        "confidence": {
                            "type": "number",
                            "minimum": 0,
                            "maximum": 1,
                            "description": "Confidence score 0.0-1.0"
                        }
                    },
                    "required": ["domain", "confidence"]
                },
                "description": "Skills to activate with confidence scores"
            },
            "trigger_reason": {
                "type": "string",
                "description": "Why this skill was selected"
            },
            "detected_question": {
                "type": ["string", "null"],
                "description": "The customer's question if one was detected"
            },
            "urgency": {
                "type": "string",
                "enum": ["high", "medium", "low"],
                "description": "Urgency level of the response needed"
            }
        },
        "required": ["needs_skill", "suggested_skills", "trigger_reason", "urgency"]
    }
}


class RouterAgent:
    """Agent that routes to appropriate skills using tool use."""

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
            tools=[ROUTER_TOOL],
            tool_choice={"type": "tool", "name": "route_skills"},
            messages=[{"role": "user", "content": user_message}],
        )

        return self._parse_response(response)

    def _format_input(
        self,
        transcript_text: str,
        current_skills: list[str] | None,
        customer_context: str | None,
    ) -> str:
        """Format input for Claude."""
        parts = [f"Recent transcript:\n{transcript_text}"]

        if current_skills:
            parts.append(f"\nCurrently active skills: {', '.join(current_skills)}")

        if customer_context:
            parts.append(f"\nCustomer context: {customer_context}")

        return "\n".join(parts)

    def _parse_response(self, response) -> RouterDecision:
        """Parse tool use response."""
        # Find the tool use block
        for block in response.content:
            if block.type == "tool_use" and block.name == "route_skills":
                data = block.input

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

        # Fallback if tool use not found
        return RouterDecision(needs_skill=False)
