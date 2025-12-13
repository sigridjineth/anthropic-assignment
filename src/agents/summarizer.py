import json
import re
import anthropic
from ..config import get_settings
from ..models import (
    SummarizerState,
    CustomerProfile,
    KeyMoment,
    PredictedQuestion,
    SkillDomain,
)

SUMMARIZER_PROMPT = """You are a sales call analyst. Analyze the conversation and extract key insights.

Previous summary state:
{previous_state}

Full conversation transcript:
{full_transcript}

Recent segment (last 60s):
{recent_transcript}

Extract and update:
1. Customer profile (company, industry, size, technical maturity)
2. Their goals and constraints
3. Key moments (important quotes with reasons)
4. Predicted upcoming questions (with probability and relevant skill domain)
5. Suggested discovery questions the sales rep should ask

Skill domains available:
- roadmap: Product timelines, feature availability
- architecture: System design, performance
- security: Compliance, encryption, data handling
- pricing: Plans, costs
- case_studies: Customer success stories
- competitive: Comparison with alternatives
- integration: SDKs, APIs
- deployment: Cloud/on-prem options

Respond in JSON format:
{{
    "customer_profile": {{
        "company": "name or null",
        "industry": "...",
        "geo": "...",
        "size": "startup/mid/enterprise",
        "technical_maturity": "low/medium/high"
    }},
    "goals": ["goal1", "goal2"],
    "constraints": ["constraint1"],
    "key_moments": [
        {{
            "offset_sec": 0,
            "quote": "exact quote",
            "why_important": "reason",
            "importance": "high/medium/low"
        }}
    ],
    "predicted_questions": [
        {{
            "question": "likely question",
            "probability": 0.0-1.0,
            "domain": "skill_domain"
        }}
    ],
    "suggested_asks": ["discovery question to ask"],
    "summary_text": "1-3 sentence summary of call so far"
}}
"""


class SummarizerAgent:
    def __init__(self):
        settings = get_settings()
        self.client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
        self.model = settings.router_model  # Use faster model for summarization

    async def summarize(
        self,
        previous_state: SummarizerState | None,
        recent_transcript: str,
        full_transcript: str,
    ) -> SummarizerState:
        # Format previous state for prompt
        prev_state_str = "None (start of call)"
        if previous_state and previous_state.summary_text:
            prev_state_str = previous_state.summary_text

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1500,
                messages=[
                    {
                        "role": "user",
                        "content": SUMMARIZER_PROMPT.format(
                            previous_state=prev_state_str,
                            full_transcript=full_transcript[:3000],  # Limit context
                            recent_transcript=recent_transcript,
                        ),
                    }
                ],
            )

            return self._parse_response(response, previous_state)

        except Exception:
            # Return previous state on error
            return previous_state or SummarizerState()

    def _parse_response(
        self, response, previous_state: SummarizerState | None
    ) -> SummarizerState:
        try:
            content = response.content[0].text
            # Extract JSON from response
            json_match = re.search(r"\{.*\}", content, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())

                # Parse customer profile
                profile_data = data.get("customer_profile", {})
                profile = CustomerProfile(
                    company=profile_data.get("company"),
                    industry=profile_data.get("industry"),
                    geo=profile_data.get("geo"),
                    size=profile_data.get("size"),
                    technical_maturity=profile_data.get("technical_maturity"),
                )

                # Parse key moments
                key_moments = []
                for km in data.get("key_moments", []):
                    try:
                        key_moments.append(
                            KeyMoment(
                                offset_sec=km.get("offset_sec", 0),
                                quote=km.get("quote", ""),
                                why_important=km.get("why_important", ""),
                                importance=km.get("importance", "medium"),
                            )
                        )
                    except Exception:
                        continue

                # Parse predicted questions
                predicted_questions = []
                for pq in data.get("predicted_questions", []):
                    try:
                        domain_str = pq.get("domain", "roadmap")
                        predicted_questions.append(
                            PredictedQuestion(
                                question=pq.get("question", ""),
                                probability=pq.get("probability", 0.5),
                                domain=SkillDomain(domain_str),
                            )
                        )
                    except Exception:
                        continue

                return SummarizerState(
                    customer_profile=profile,
                    goals=data.get("goals", []),
                    constraints=data.get("constraints", []),
                    key_moments=key_moments,
                    predicted_questions=predicted_questions,
                    suggested_asks=data.get("suggested_asks", []),
                    summary_text=data.get("summary_text", ""),
                )

        except (json.JSONDecodeError, IndexError, KeyError):
            pass

        # Return previous state on parse error
        return previous_state or SummarizerState()
