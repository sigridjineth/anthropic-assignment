"""
Answerer Agent - Generates answers using dynamically loaded skills.

## Skill Loading Approach

This implementation uses **prompt injection** to load skills:
1. Skills are stored locally in `skills/{domain}/SKILL.md`
2. When activated, skill content is loaded and injected into the system prompt
3. Claude uses this context to generate informed answers

This is a demo-friendly approach that works offline without API setup.

## Official Skills API (Production)

For production, Anthropic's official Skills API provides:
- `container.skills` parameter with `skill_id` and `version`
- Code execution environment for skill execution
- Versioning and skill management via `/v1/skills` endpoint

Example:
```python
response = client.beta.messages.create(
    model="claude-sonnet-4-5-20250929",
    betas=["code-execution-2025-08-25", "skills-2025-10-02"],
    container={
        "skills": [
            {"type": "custom", "skill_id": "skill_01xxx", "version": "latest"}
        ]
    },
    tools=[{"type": "code_execution_20250825", "name": "code_execution"}]
)
```

See: https://platform.claude.com/docs/en/build-with-claude/skills-guide
"""

import json
import re
from pathlib import Path
import anthropic
from ..config import get_settings
from ..models import AnswerDraft, Source, SkillDomain

SKILLS_DIR = Path(__file__).resolve().parent.parent.parent / "skills"

SYSTEM_PROMPT = """You are a Technical Sales assistant helping answer customer questions during a sales call.

You have access to specialized knowledge through the following Skills. Use this knowledge to provide accurate, helpful answers.

{skills_content}

Instructions:
1. Use the knowledge from the Skills above to provide accurate answers
2. Cite sources when available (mention which skill/file the info comes from)
3. Include appropriate caveats (e.g., "timelines subject to change")
4. Suggest follow-up questions the sales rep could ask
5. If unsure, say so clearly

Your output must be valid JSON:
{{
    "answer": "Your response (conversational tone, suitable for reading aloud)",
    "sources": [{{"title": "Source name", "file": "skill/file.md", "excerpt": "Relevant quote"}}],
    "confidence": 0.0-1.0,
    "caveats": ["Important disclaimers"],
    "followups": ["Suggested follow-up questions"]
}}"""


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
    ) -> AnswerDraft:
        """Generate an answer using the specified skills."""
        # Load skill content
        skills_content_parts = []
        for domain in skill_domains[:4]:  # Max 4 skills
            content = load_skill_content(domain)
            if content:
                skills_content_parts.append(content)

        skills_content = (
            "\n\n".join(skills_content_parts)
            if skills_content_parts
            else "No specific skills loaded. Answer based on general knowledge."
        )

        response = self.client.messages.create(
            model=self.model,
            max_tokens=2048,
            system=SYSTEM_PROMPT.format(skills_content=skills_content),
            messages=[
                {
                    "role": "user",
                    "content": f"Context from the conversation:\n{context}\n\nQuestion to answer:\n{question}",
                }
            ],
        )

        return self._parse_response(response, [d.value for d in skill_domains])

    def _parse_response(self, response, skills_used: list[str]) -> AnswerDraft:
        content = response.content[0].text

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

        # Fallback: return raw text
        return AnswerDraft(
            answer=content,
            confidence=0.5,
            skills_used=skills_used,
        )
