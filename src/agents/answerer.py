import json
import re
from pathlib import Path
import anthropic
from ..config import get_settings
from ..models import AnswerDraft, Source, SkillDomain

# Skills directory
SKILLS_DIR = Path(__file__).resolve().parent.parent.parent / "skills"

SYSTEM_PROMPT_WITH_SKILLS = """You are a Technical Sales assistant helping answer customer questions during a sales call.

You have access to specialized knowledge through the following Skills. Use this knowledge to provide accurate, helpful answers.

{skills_content}

Instructions:
1. Use the knowledge from the Skills above to provide accurate answers
2. Cite sources when available (mention which skill/file the info comes from)
3. Include appropriate caveats (e.g., "timelines subject to change")
4. Suggest follow-up questions the sales rep could ask
5. If unsure, say so and suggest escalation

Respond in JSON format:
{{
    "answer": "Your response (conversational tone, suitable for reading aloud)",
    "sources": [{{"title": "...", "file": "...", "excerpt": "..."}}],
    "confidence": 0.0-1.0,
    "caveats": ["..."],
    "followups": ["suggested follow-up questions"]
}}
"""

SYSTEM_PROMPT_WITHOUT_SKILLS = """You are a Technical Sales assistant helping answer customer questions during a sales call.

You do NOT have access to any specialized company knowledge or skills. Answer based only on your general knowledge.

Instructions:
1. Answer based on your general knowledge only
2. Be honest about uncertainty - you don't have access to specific company information
3. Suggest follow-up actions if unsure
4. Do not make up specific details about products, pricing, or timelines

Respond in JSON format:
{{
    "answer": "Your response",
    "sources": [],
    "confidence": 0.0-1.0,
    "caveats": ["..."],
    "followups": ["..."]
}}
"""


def load_skill_content(domain: SkillDomain) -> str | None:
    """Load skill content from local files."""
    skill_dir = SKILLS_DIR / domain.value
    if not skill_dir.exists():
        return None

    content_parts = []

    # Load SKILL.md
    skill_md = skill_dir / "SKILL.md"
    if skill_md.exists():
        content_parts.append(f"=== SKILL: {domain.value.upper()} ===\n")
        content_parts.append(skill_md.read_text())

    # Load reference files
    refs_dir = skill_dir / "references"
    if refs_dir.exists():
        for ref_file in refs_dir.glob("*.md"):
            content_parts.append(f"\n--- Reference: {ref_file.name} ---\n")
            content_parts.append(ref_file.read_text())

    return "\n".join(content_parts) if content_parts else None


class AnswererAgent:
    def __init__(self):
        settings = get_settings()
        self.client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
        self.model = settings.model_name

    async def answer(
        self,
        question: str,
        context: str,
        skill_domains: list[SkillDomain],
        with_skills: bool = True,
    ) -> AnswerDraft:
        if with_skills and skill_domains:
            return await self._answer_with_skills(question, context, skill_domains)
        else:
            return await self._answer_without_skills(question, context)

    async def _answer_with_skills(
        self,
        question: str,
        context: str,
        skill_domains: list[SkillDomain],
    ) -> AnswerDraft:
        # Load skill content from local files
        skills_content_parts = []
        for domain in skill_domains[:8]:  # Max 8 skills
            content = load_skill_content(domain)
            if content:
                skills_content_parts.append(content)

        skills_content = "\n\n".join(skills_content_parts) if skills_content_parts else "No skills loaded."

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2048,
                system=SYSTEM_PROMPT_WITH_SKILLS.format(skills_content=skills_content),
                messages=[
                    {
                        "role": "user",
                        "content": f"Context from the conversation:\n{context}\n\nQuestion to answer:\n{question}",
                    }
                ],
            )

            return self._parse_response(response, [d.value for d in skill_domains])

        except Exception:
            # Use mock fallback on API failure
            from ..fallback import get_mock_answer
            if skill_domains:
                return get_mock_answer(skill_domains[0].value)
            return get_mock_answer("default")

    async def _answer_without_skills(
        self,
        question: str,
        context: str,
    ) -> AnswerDraft:
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2048,
                system=SYSTEM_PROMPT_WITHOUT_SKILLS,
                messages=[
                    {
                        "role": "user",
                        "content": f"Context from the conversation:\n{context}\n\nQuestion to answer:\n{question}",
                    }
                ],
            )

            return self._parse_response(response, [])

        except Exception:
            # Use default fallback on API failure
            from ..fallback import DEFAULT_ANSWER
            return DEFAULT_ANSWER

    def _parse_response(self, response, skills_used: list[str]) -> AnswerDraft:
        try:
            content = response.content[0].text
            # Extract JSON from response
            json_match = re.search(r"\{.*\}", content, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                return AnswerDraft(
                    answer=data.get("answer", content),
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
        except (json.JSONDecodeError, IndexError, KeyError):
            pass

        # Fallback: return raw text
        content = response.content[0].text if response.content else "No response"
        return AnswerDraft(
            answer=content,
            confidence=0.5,
            skills_used=skills_used,
        )
