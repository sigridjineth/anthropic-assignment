import json
import re
import anthropic
from ..config import get_settings
from ..models import PrepInput, PrepResult, LikelyTopic

SYSTEM_PROMPT = """You are a Technical Sales preparation assistant. Given information about an upcoming sales call, generate a comprehensive session brief.

Your output must be valid JSON with this exact structure:
{
    "session_brief": "A 2-3 sentence summary of the meeting context and key focus areas",
    "likely_topics": [
        {"topic": "Topic name", "reason": "Why this topic is likely based on the input"}
    ],
    "discovery_questions": ["Question 1", "Question 2", ...],
    "recommended_skills": ["skill_domain_1", "skill_domain_2"]
}

Available skill domains: roadmap, architecture, security, pricing

Guidelines:
- Session brief should mention the company, industry, attendees, and call purpose
- Provide exactly 3 likely topics with clear reasoning
- Provide exactly 5 discovery questions that a sales rep should ask
- Recommend 2-4 relevant skills based on the context
- Be specific and actionable"""


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
                    LikelyTopic(topic=t.get("topic", ""), reason=t.get("reason", ""))
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
