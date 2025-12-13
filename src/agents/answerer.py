"""
Answerer Agent - Generates answers using skills.

Production pattern:
1. If official Skills API available: use container.skills + code_execution
2. If not: use prompt injection with skill content

Both patterns use Tool Use for reliable structured JSON output.

See: https://platform.claude.com/docs/en/build-with-claude/skills-guide
"""

import anthropic
from ..config import get_settings, PERSONA_SYSTEM_CONTEXT
from ..models import AnswerDraft, Source, SkillDomain
from ..services.skills import skill_manager, BETAS

# Base system prompt with persona
BASE_SYSTEM_PROMPT = f"""{PERSONA_SYSTEM_CONTEXT}

---

You are helping Sigrid answer customer questions during a discovery call.

Instructions:
1. Use the knowledge from your Skills to provide accurate answers
2. Cite sources when available (mention which skill/file the info comes from)
3. Include appropriate caveats (e.g., "actual savings vary")
4. Suggest follow-up questions Sigrid could ask the customer
5. Be specific - use numbers, percentages, and concrete examples
6. If unsure, say so clearly

Use the generate_answer tool to provide your response."""

# System prompt with injected skills
SYSTEM_PROMPT_WITH_SKILLS = f"""{PERSONA_SYSTEM_CONTEXT}

---

You are helping Sigrid answer customer questions during a discovery call.

You have access to the following specialized knowledge:

{{skills_content}}

Instructions:
1. Use the knowledge above to provide accurate answers
2. Cite sources when available (mention which skill/file the info comes from)
3. Include appropriate caveats (e.g., "actual savings vary")
4. Suggest follow-up questions Sigrid could ask the customer
5. Be specific - use numbers, percentages, and concrete examples
6. If unsure, say so clearly

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
    """Agent that generates answers using skills (official API or prompt injection)."""

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
        """Generate an answer using the specified skills."""
        # Ensure skill manager is initialized
        if not skill_manager.is_initialized:
            await skill_manager.initialize()

        # Choose approach based on API availability
        if skill_manager.using_official_api:
            return await self._answer_with_official_api(question, context, skill_domains)
        else:
            return await self._answer_with_prompt_injection(question, context, skill_domains)

    async def _answer_with_official_api(
        self,
        question: str,
        context: str,
        skill_domains: list[SkillDomain],
    ) -> AnswerDraft:
        """Generate answer using official Skills API with container.skills."""
        skills_config = skill_manager.get_skills_config(skill_domains[:4])

        tools = [ANSWER_TOOL]
        if skills_config:
            tools.append({"type": "code_execution_20250825", "name": "code_execution"})

        response = self.client.beta.messages.create(
            model=self.model,
            max_tokens=4096,
            betas=BETAS,
            system=BASE_SYSTEM_PROMPT,
            container={"skills": skills_config} if skills_config else None,
            tools=tools,
            tool_choice={"type": "tool", "name": "generate_answer"},
            messages=[
                {
                    "role": "user",
                    "content": f"Context from the conversation:\n{context}\n\nQuestion to answer:\n{question}",
                }
            ],
        )

        return self._parse_response(response, [d.value for d in skill_domains])

    async def _answer_with_prompt_injection(
        self,
        question: str,
        context: str,
        skill_domains: list[SkillDomain],
    ) -> AnswerDraft:
        """Generate answer using prompt injection fallback."""
        # Get skill content for injection
        skills_content = skill_manager.get_skills_content(skill_domains[:4])

        # Build system prompt with injected skills
        if skills_content:
            system_prompt = SYSTEM_PROMPT_WITH_SKILLS.format(skills_content=skills_content)
        else:
            system_prompt = BASE_SYSTEM_PROMPT

        response = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            system=system_prompt,
            tools=[ANSWER_TOOL],
            tool_choice={"type": "tool", "name": "generate_answer"},
            messages=[
                {
                    "role": "user",
                    "content": f"Context from the conversation:\n{context}\n\nQuestion to answer:\n{question}",
                }
            ],
        )

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
