"""
Post-call Agent - Generates call notes and skill update proposals.

Uses Anthropic's tool use feature for reliable structured JSON responses.
"""

import anthropic
from ..config import get_settings, PERSONA_SYSTEM_CONTEXT
from ..models import PostCallResult, SkillUpdateProposal
from ..services.session import Session

SYSTEM_PROMPT = f"""{PERSONA_SYSTEM_CONTEXT}

---

You are helping Sigrid generate post-call notes and identify learnings.

Your job is to:
1. Summarize what happened in the call
2. Extract customer pain points and requirements
3. Note which skills were helpful
4. Propose skill updates based on patterns detected

Guidelines for skill update proposals:
- Only propose updates when you detect NEW patterns not already in the skill
- Be specific about what to add (exact wording)
- Focus on patterns that would help in future similar calls
- Examples: new objection handling, common questions, success stories

Use the generate_post_call_analysis tool to provide your response."""

# Tool definition for structured output
POSTCALL_TOOL = {
    "name": "generate_post_call_analysis",
    "description": "Generate post-call analysis including notes and skill update proposals",
    "input_schema": {
        "type": "object",
        "properties": {
            "call_summary": {
                "type": "string",
                "description": "2-3 sentence summary of the call"
            },
            "topics_covered": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Topics discussed during the call"
            },
            "outcome": {
                "type": "string",
                "description": "Call outcome (e.g., 'follow-up scheduled', 'demo requested', 'needs internal discussion')"
            },
            "customer_pain_points": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Pain points identified from the conversation"
            },
            "customer_requirements": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Key requirements mentioned by the customer"
            },
            "skills_used": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Skills that were activated during the call"
            },
            "skills_helpful": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Skills that provided useful answers"
            },
            "skill_update_proposals": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "skill_id": {
                            "type": "string",
                            "description": "Skill to update (e.g., 'fintech_patterns')"
                        },
                        "file_path": {
                            "type": "string",
                            "description": "File to update (e.g., 'compliance_handling.md')"
                        },
                        "update_type": {
                            "type": "string",
                            "enum": ["add_pattern", "add_example", "update_guidance"],
                            "description": "Type of update"
                        },
                        "content": {
                            "type": "string",
                            "description": "The content to add"
                        },
                        "rationale": {
                            "type": "string",
                            "description": "Why this update is valuable"
                        }
                    },
                    "required": ["skill_id", "file_path", "update_type", "content", "rationale"]
                },
                "description": "Proposed updates to skills based on call learnings"
            },
            "follow_up_actions": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Recommended follow-up actions"
            }
        },
        "required": [
            "call_summary", "topics_covered", "outcome",
            "customer_pain_points", "customer_requirements",
            "skills_used", "skills_helpful", "skill_update_proposals", "follow_up_actions"
        ]
    }
}


class PostCallAgent:
    """Agent that generates post-call analysis using tool use."""

    def __init__(self):
        settings = get_settings()
        self.client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
        self.model = settings.model_name

    async def analyze(self, session: Session) -> PostCallResult:
        """Generate post-call analysis."""
        user_message = self._format_session(session)

        response = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            system=SYSTEM_PROMPT,
            tools=[POSTCALL_TOOL],
            tool_choice={"type": "tool", "name": "generate_post_call_analysis"},
            messages=[{"role": "user", "content": user_message}],
        )

        return self._parse_response(response)

    def _format_session(self, session: Session) -> str:
        """Format session data for Claude."""
        parts = [
            f"# Call: {session.company}",
            f"Duration: {len(session.transcript)} transcript entries",
            "",
            "## Prep Brief",
            session.prep_result.session_brief if session.prep_result else "No prep available",
            "",
            "## Full Transcript",
        ]

        for entry in session.transcript:
            speaker = entry.speaker.capitalize()
            parts.append(f"[{speaker}] {entry.text}")

        parts.extend([
            "",
            "## Skills Activated During Call",
            ", ".join(session.active_skills) if session.active_skills else "None",
            "",
            "## Skill Fire Events",
        ])

        for event in session.skill_fired_log:
            parts.append(f"- {', '.join(event.domains)}: {event.trigger_reason}")

        if session.summarizer_state:
            parts.extend([
                "",
                "## Live Summary (at end of call)",
                session.summarizer_state.summary or "No summary",
            ])

        return "\n".join(parts)

    def _parse_response(self, response) -> PostCallResult:
        """Parse tool use response."""
        for block in response.content:
            if block.type == "tool_use" and block.name == "generate_post_call_analysis":
                data = block.input
                return PostCallResult(
                    call_summary=data.get("call_summary", ""),
                    topics_covered=data.get("topics_covered", []),
                    outcome=data.get("outcome", ""),
                    customer_pain_points=data.get("customer_pain_points", []),
                    customer_requirements=data.get("customer_requirements", []),
                    skills_used=data.get("skills_used", []),
                    skills_helpful=data.get("skills_helpful", []),
                    skill_update_proposals=[
                        SkillUpdateProposal(
                            skill_id=p.get("skill_id", ""),
                            file_path=p.get("file_path", ""),
                            update_type=p.get("update_type", "add_pattern"),
                            content=p.get("content", ""),
                            rationale=p.get("rationale", ""),
                        )
                        for p in data.get("skill_update_proposals", [])
                    ],
                    follow_up_actions=data.get("follow_up_actions", []),
                )

        # Fallback
        return PostCallResult(
            call_summary="Unable to generate call summary.",
            topics_covered=[],
            outcome="Unknown",
            customer_pain_points=[],
            customer_requirements=[],
            skills_used=[],
            skills_helpful=[],
            skill_update_proposals=[],
            follow_up_actions=[],
        )
