"""
Prep Agent - Generates session preparation using structured tool output.

Uses Anthropic's tool use feature for reliable structured JSON responses.
See: https://docs.anthropic.com/en/docs/build-with-claude/tool-use
"""

import anthropic
from ..config import get_settings
from ..models import PrepInput, PrepResult, LikelyTopic

SYSTEM_PROMPT = """You are a Technical Sales preparation assistant. The user will describe an upcoming sales call in natural language.

Your job is to:
1. Understand the context from whatever they provide (company, industry, roles, concerns, etc.)
2. Generate a session brief to help them prepare

Available skill domains (recommend what's relevant):
- roadmap: Product timelines, feature availability, release dates
- architecture: System design, data flow, technical implementation
- security: SOC2, compliance, encryption, data handling
- pricing: Plans, costs, enterprise options

Guidelines:
- Infer company type, industry, and concerns from the user's description
- Predict 3 likely topics they'll discuss (with confidence 0.0-1.0)
- Generate 3-5 discovery questions the sales rep should ask
- Recommend 2-4 skills to pre-attach based on inferred topics
- Be concise and actionable

Use the generate_session_prep tool to provide your response."""

# Tool definition for structured output
PREP_TOOL = {
    "name": "generate_session_prep",
    "description": "Generate session preparation materials for the sales call",
    "input_schema": {
        "type": "object",
        "properties": {
            "session_brief": {
                "type": "string",
                "description": "Concise 1-2 sentence summary: company context + key focus areas"
            },
            "likely_topics": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "topic": {"type": "string", "description": "Topic name"},
                        "reason": {"type": "string", "description": "Brief reason why this topic is likely"},
                        "confidence": {"type": "number", "description": "Confidence score 0.0-1.0"}
                    },
                    "required": ["topic", "reason", "confidence"]
                },
                "description": "3 likely topics for discussion"
            },
            "discovery_questions": {
                "type": "array",
                "items": {"type": "string"},
                "description": "3-5 discovery questions the sales rep should ask"
            },
            "recommended_skills": {
                "type": "array",
                "items": {
                    "type": "string",
                    "enum": ["roadmap", "architecture", "security", "pricing"]
                },
                "description": "2-4 skill domains to pre-attach"
            }
        },
        "required": ["session_brief", "likely_topics", "discovery_questions", "recommended_skills"]
    }
}


class PrepAgent:
    """Agent that generates session prep using tool use for structured output."""

    def __init__(self):
        settings = get_settings()
        self.client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
        self.model = settings.model_name

    async def prepare(self, input_data: PrepInput) -> PrepResult:
        """Generate session preparation materials using tool use."""
        user_message = self._format_input(input_data)

        response = self.client.messages.create(
            model=self.model,
            max_tokens=2048,
            system=SYSTEM_PROMPT,
            tools=[PREP_TOOL],
            tool_choice={"type": "tool", "name": "generate_session_prep"},
            messages=[{"role": "user", "content": user_message}],
        )

        return self._parse_response(response)

    def _format_input(self, input_data: PrepInput) -> str:
        """Format input for Claude."""
        # If raw context is provided, use it directly - let Claude infer
        if input_data.raw_context:
            return input_data.raw_context

        # Fallback to structured input
        parts = [
            f"Company: {input_data.company}",
            f"Industry: {input_data.industry}",
            f"Attendee Roles: {', '.join(input_data.roles) if input_data.roles else 'Not specified'}",
            f"Call Purpose: {input_data.purpose}",
            f"Sensitive Topics: {', '.join(input_data.sensitive_topics) if input_data.sensitive_topics else 'None specified'}",
        ]
        if input_data.competitors:
            parts.append(f"Known Competitors: {input_data.competitors}")

        return "\n".join(parts)

    def _parse_response(self, response) -> PrepResult:
        """Parse tool use response."""
        # Find the tool use block
        for block in response.content:
            if block.type == "tool_use" and block.name == "generate_session_prep":
                data = block.input
                return PrepResult(
                    session_brief=data.get("session_brief", ""),
                    likely_topics=[
                        LikelyTopic(
                            topic=t.get("topic", ""),
                            reason=t.get("reason", ""),
                            confidence=t.get("confidence"),
                        )
                        for t in data.get("likely_topics", [])
                    ],
                    discovery_questions=data.get("discovery_questions", []),
                    recommended_skills=data.get("recommended_skills", []),
                )

        # Fallback if tool use not found
        return PrepResult(
            session_brief="Unable to parse session context. Please provide more details.",
            likely_topics=[],
            discovery_questions=[],
            recommended_skills=["architecture", "security"],
        )
