import json
import re
import anthropic
from ..config import get_settings
from ..models import PrepInput, PrepResult, LikelyTopic

SYSTEM_PROMPT = """You are a Technical Sales preparation assistant. The user will describe an upcoming sales call in natural language. Your job is to:

1. **Understand** the context from whatever they provide (company, industry, roles, concerns, etc.)
2. **Generate** a session brief to help them prepare

Your output must be valid JSON:
{
    "session_brief": "Concise 1-2 sentence summary: company context + key focus areas",
    "likely_topics": [
        {"topic": "Topic name", "reason": "Brief reason", "confidence": 0.9}
    ],
    "discovery_questions": ["Question 1", "Question 2", ...],
    "recommended_skills": ["skill_domain_1", "skill_domain_2"]
}

Available skill domains (choose what's relevant):
- **roadmap**: Product timelines, feature availability, release dates
- **architecture**: System design, data flow, technical implementation
- **security**: SOC2, compliance, encryption, data handling
- **pricing**: Plans, costs, enterprise options

Guidelines:
- Infer company type, industry, and concerns from the user's description
- Predict 3 likely topics they'll discuss (with confidence 0.0-1.0)
- Generate 3-5 discovery questions the sales rep should ask
- Recommend 2-4 skills to pre-attach based on inferred topics
- Be concise and actionable"""


class PrepAgent:
    def __init__(self):
        settings = get_settings()
        self.client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
        self.model = settings.model_name

    async def prepare(self, input_data: PrepInput) -> PrepResult:
        """Generate session preparation materials."""
        user_message = self._format_input(input_data)

        response = self.client.messages.create(
            model=self.model,
            max_tokens=2048,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_message}],
        )

        return self._parse_response(response)

    def _format_input(self, input_data: PrepInput) -> str:
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
        content = response.content[0].text

        # Extract JSON from response
        json_match = re.search(r"\{.*\}", content, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group())
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

        # Fallback if JSON parsing fails
        return PrepResult(
            session_brief=content[:500],
            likely_topics=[],
            discovery_questions=[],
            recommended_skills=["architecture", "security"],
        )
