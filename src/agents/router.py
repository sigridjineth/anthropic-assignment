import json
import re
import anthropic
from ..config import get_settings
from ..models import RouterDecision, SkillSuggestion, SkillDomain, Urgency

# Rule-based keyword patterns for fast routing
KEYWORD_PATTERNS: dict[SkillDomain, list[str]] = {
    SkillDomain.ROADMAP: [
        r"\bwhen\b.*\b(available|ready|launch|release|ship)\b",
        r"\beta\b",
        r"\broadmap\b",
        r"\bbeta\b",
        r"\bga\b",
        r"\bgeneral availability\b",
        r"\btimeline\b",
        r"\bcoming soon\b",
        r"\bplanned\b",
    ],
    SkillDomain.ARCHITECTURE: [
        r"\bhow does it work\b",
        r"\barchitecture\b",
        r"\balgorithm\b",
        r"\bunder the hood\b",
        r"\btechnical.*detail\b",
        r"\binfrastructure\b",
        r"\bscalability\b",
        r"\bperformance\b",
        r"\blatency\b",
    ],
    SkillDomain.SECURITY: [
        r"\bsoc\s*2\b",
        r"\bhipaa\b",
        r"\bgdpr\b",
        r"\bencryption\b",
        r"\bdata\s*residency\b",
        r"\bcompliance\b",
        r"\bsecurity\b",
        r"\baudit\b",
        r"\bprivacy\b",
        r"\bcertification\b",
    ],
    SkillDomain.PRICING: [
        r"\bpricing\b",
        r"\bcost\b",
        r"\blicense\b",
        r"\bsubscription\b",
        r"\bplan\b",
        r"\btier\b",
        r"\bfree\s*trial\b",
        r"\benterprise\b.*\b(pricing|plan)\b",
    ],
    SkillDomain.CASE_STUDIES: [
        r"\bcustomer\s*(story|stories)\b",
        r"\bcase\s*stud(y|ies)\b",
        r"\breference\b",
        r"\bsuccess\s*stor(y|ies)\b",
        r"\bwho\s*(else)?\s*uses\b",
        r"\bexample\s*customer\b",
    ],
    SkillDomain.COMPETITIVE: [
        r"\bvs\b",
        r"\bcompare\b",
        r"\bcompetitor\b",
        r"\balternative\b",
        r"\bdifferent\s*from\b",
        r"\bbetter\s*than\b",
    ],
    SkillDomain.INTEGRATION: [
        r"\bintegrat(e|ion)\b",
        r"\bsdk\b",
        r"\bapi\b",
        r"\bwebhook\b",
        r"\bconnect\b",
        r"\bplugin\b",
    ],
    SkillDomain.DEPLOYMENT: [
        r"\bdeploy\b",
        r"\bon-prem\b",
        r"\bself-host\b",
        r"\bcloud\b",
        r"\bregion\b",
        r"\bsaas\b",
        r"\bhybrid\b",
    ],
}

ROUTER_PROMPT = """You are a skill router for a Technical Sales Interview Copilot.

Analyze the recent conversation transcript and determine if any specialized knowledge skills are needed to answer questions.

Available skill domains:
- roadmap: Product timelines, feature availability, beta/GA status
- architecture: System design, algorithms, performance characteristics
- security: Compliance (SOC2, HIPAA), encryption, data handling
- pricing: Plans, costs, enterprise options
- case_studies: Customer success stories, references
- competitive: Comparison with alternatives
- integration: SDKs, APIs, webhooks
- deployment: Cloud/on-prem options, regions

Recent transcript:
{transcript}

Respond in JSON format:
{{
    "needs_skill": true/false,
    "suggested_skills": [
        {{"domain": "...", "confidence": 0.0-1.0}}
    ],
    "trigger_reason": "brief explanation",
    "urgency": "high/medium/low",
    "detected_question": "the question from transcript if any"
}}

Only include skills with confidence > 0.5. Max 3 skills.
Set urgency=high if there's a direct question needing immediate answer.
"""


class RouterAgent:
    def __init__(self):
        settings = get_settings()
        self.client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
        self.model = settings.router_model

    def _rule_based_route(self, text: str) -> list[SkillSuggestion]:
        text_lower = text.lower()
        suggestions = []

        for domain, patterns in KEYWORD_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, text_lower, re.IGNORECASE):
                    suggestions.append(
                        SkillSuggestion(domain=domain, confidence=0.85, priority=1)
                    )
                    break  # One match per domain is enough

        return suggestions

    async def route(self, transcript_text: str) -> RouterDecision:
        # First try rule-based routing
        rule_suggestions = self._rule_based_route(transcript_text)

        # If we have high-confidence matches, use them
        if rule_suggestions:
            has_question = "?" in transcript_text
            return RouterDecision(
                needs_skill=True,
                suggested_skills=rule_suggestions[:3],
                trigger_reason="Keyword match",
                urgency=Urgency.HIGH if has_question else Urgency.MEDIUM,
                detected_question=self._extract_question(transcript_text) if has_question else None,
            )

        # Fall back to LLM routing for ambiguous cases
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=500,
                messages=[
                    {
                        "role": "user",
                        "content": ROUTER_PROMPT.format(transcript=transcript_text),
                    }
                ],
            )

            # Parse JSON response
            content = response.content[0].text
            # Extract JSON from response
            json_match = re.search(r"\{.*\}", content, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                return RouterDecision(
                    needs_skill=data.get("needs_skill", False),
                    suggested_skills=[
                        SkillSuggestion(
                            domain=SkillDomain(s["domain"]),
                            confidence=s.get("confidence", 0.7),
                        )
                        for s in data.get("suggested_skills", [])
                    ],
                    trigger_reason=data.get("trigger_reason", ""),
                    urgency=Urgency(data.get("urgency", "low")),
                    detected_question=data.get("detected_question"),
                )
        except Exception:
            pass

        # Default: no skill needed
        return RouterDecision(needs_skill=False)

    def _extract_question(self, text: str) -> str | None:
        lines = text.split("\n")
        for line in reversed(lines):
            if "?" in line:
                # Extract just the question part
                parts = line.split(":")
                if len(parts) > 1:
                    return parts[-1].strip()
                return line.strip()
        return None
