import json
import re
import anthropic
from ..config import get_settings
from ..models import AnswerDraft, Source, SkillDomain
from ..skills.registry import SkillRegistry

ANSWERER_PROMPT_WITH_SKILLS = """You are a Technical Sales assistant helping answer customer questions during a sales call.

You have access to specialized knowledge through Skills that contain accurate, up-to-date information.

Context from the conversation:
{context}

Question to answer:
{question}

Instructions:
1. Use the knowledge from your Skills to provide accurate answers
2. Cite sources when available (file names from Skills)
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

ANSWERER_PROMPT_WITHOUT_SKILLS = """You are a Technical Sales assistant helping answer customer questions during a sales call.

Context from the conversation:
{context}

Question to answer:
{question}

Instructions:
1. Answer based on your general knowledge
2. Be honest about uncertainty
3. Suggest follow-up actions if unsure

Respond in JSON format:
{{
    "answer": "Your response",
    "sources": [],
    "confidence": 0.0-1.0,
    "caveats": ["..."],
    "followups": ["..."]
}}
"""


class AnswererAgent:
    def __init__(self):
        settings = get_settings()
        self.client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
        self.model = settings.model_name
        self.skills_beta = settings.skills_beta
        self.code_execution_beta = settings.code_execution_beta
        self.registry = SkillRegistry()

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
        # Get skill IDs from registry
        skills_config = []
        for domain in skill_domains[:8]:  # Max 8 skills
            skill_id = self.registry.get_skill_id(domain)
            if skill_id:
                skills_config.append({
                    "type": "custom",
                    "skill_id": skill_id,
                    "version": "latest",
                })

        try:
            response = self.client.beta.messages.create(
                model=self.model,
                max_tokens=2048,
                betas=[self.code_execution_beta, self.skills_beta],
                container={"skills": skills_config} if skills_config else None,
                tools=[{"type": "code_execution_20250825", "name": "code_execution"}] if skills_config else None,
                messages=[
                    {
                        "role": "user",
                        "content": ANSWERER_PROMPT_WITH_SKILLS.format(
                            context=context,
                            question=question,
                        ),
                    }
                ],
            )

            return self._parse_response(response, [d.value for d in skill_domains])

        except Exception as e:
            # Fallback if skills fail
            return AnswerDraft(
                answer=f"I encountered an issue accessing specialized knowledge: {str(e)}. Let me try to help with general knowledge.",
                confidence=0.3,
                caveats=["Could not access specialized skills"],
                skills_used=[],
            )

    async def _answer_without_skills(
        self,
        question: str,
        context: str,
    ) -> AnswerDraft:
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2048,
                messages=[
                    {
                        "role": "user",
                        "content": ANSWERER_PROMPT_WITHOUT_SKILLS.format(
                            context=context,
                            question=question,
                        ),
                    }
                ],
            )

            return self._parse_response(response, [])

        except Exception as e:
            return AnswerDraft(
                answer=f"I encountered an error: {str(e)}",
                confidence=0.0,
                caveats=["Error occurred"],
                skills_used=[],
            )

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
