"""
Answerer Agent - Generates answers using the official Claude Skills API.

This implementation uses:
- Official Skills API with container.skills parameter
- Code execution tool for skill execution
- Tool use for structured JSON output

See: https://platform.claude.com/docs/en/build-with-claude/skills-guide
"""

import anthropic
from ..config import get_settings
from ..models import AnswerDraft, Source, SkillDomain
from ..services.skills import skill_manager, BETAS

# System prompt for the answerer
SYSTEM_PROMPT = """You are a Technical Sales assistant helping answer customer questions during a sales call.

You have access to specialized knowledge through Skills that have been loaded into your environment.
Use this knowledge to provide accurate, helpful answers.

Instructions:
1. Use the knowledge from your Skills to provide accurate answers
2. Cite sources when available (mention which skill/file the info comes from)
3. Include appropriate caveats (e.g., "timelines subject to change")
4. Suggest follow-up questions the sales rep could ask
5. If unsure, say so clearly

Use the generate_answer tool to provide your response."""

# Tool definition for structured output
ANSWER_TOOL = {
    "name": "generate_answer",
    "description": "Generate an answer to the customer's question using available skills",
    "input_schema": {
        "type": "object",
        "properties": {
            "answer": {
                "type": "string",
                "description": "Your response (conversational tone, suitable for reading aloud)"
            },
            "sources": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string", "description": "Source name"},
                        "file": {"type": "string", "description": "skill/file.md path"},
                        "excerpt": {"type": ["string", "null"], "description": "Relevant quote"}
                    },
                    "required": ["title", "file"]
                },
                "description": "Sources used for the answer"
            },
            "confidence": {
                "type": "number",
                "minimum": 0,
                "maximum": 1,
                "description": "Confidence score 0.0-1.0"
            },
            "caveats": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Important disclaimers or caveats"
            },
            "followups": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Suggested follow-up questions"
            }
        },
        "required": ["answer", "sources", "confidence", "caveats", "followups"]
    }
}


class AnswererAgent:
    """Agent that generates answers using official Skills API and tool use."""

    def __init__(self):
        settings = get_settings()
        self.client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
        self.model = settings.model_name

    async def answer(
        self,
        question: str,
        context: str,
        skill_domains: list[SkillDomain],
    ) -> AnswerDraft:
        """Generate an answer using the specified skills via official API."""
        # Ensure skill manager is initialized
        if not skill_manager.is_initialized:
            await skill_manager.initialize()

        # Get container.skills config
        skills_config = skill_manager.get_skills_config(skill_domains[:4])  # Max 4 skills

        # Build tools list - always include our answer tool
        tools = [ANSWER_TOOL]

        # Build the request
        request_params = {
            "model": self.model,
            "max_tokens": 4096,
            "system": SYSTEM_PROMPT,
            "tools": tools,
            "tool_choice": {"type": "tool", "name": "generate_answer"},
            "messages": [
                {
                    "role": "user",
                    "content": f"Context from the conversation:\n{context}\n\nQuestion to answer:\n{question}",
                }
            ],
        }

        # Add skills via container if available
        if skills_config:
            # Add code execution tool for skills
            tools.append({"type": "code_execution_20250825", "name": "code_execution"})
            request_params["betas"] = BETAS
            request_params["container"] = {"skills": skills_config}

            # Use beta endpoint
            response = self.client.beta.messages.create(**request_params)
        else:
            # Fallback to standard API without skills
            response = self.client.messages.create(**request_params)

        return self._parse_response(response, [d.value for d in skill_domains])

    def _parse_response(self, response, skills_used: list[str]) -> AnswerDraft:
        """Parse tool use response."""
        # Find the tool use block
        for block in response.content:
            if hasattr(block, "type") and block.type == "tool_use" and block.name == "generate_answer":
                data = block.input
                return AnswerDraft(
                    answer=data.get("answer", ""),
                    sources=[
                        Source(
                            title=s.get("title", ""),
                            file=s.get("file", ""),
                            excerpt=s.get("excerpt"),
                        )
                        for s in data.get("sources", [])
                    ],
                    confidence=data.get("confidence", 0.5),
                    caveats=data.get("caveats", []),
                    followups=data.get("followups", []),
                    skills_used=skills_used,
                )

        # Fallback: try to extract text content
        text_content = ""
        for block in response.content:
            if hasattr(block, "text"):
                text_content += block.text

        if text_content:
            return AnswerDraft(
                answer=text_content,
                confidence=0.5,
                skills_used=skills_used,
            )

        # Final fallback
        return AnswerDraft(
            answer="I couldn't generate an answer. Please try again.",
            confidence=0.0,
            skills_used=skills_used,
        )
