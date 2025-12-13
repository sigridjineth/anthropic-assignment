"""Mock fallback data for API failures during demo."""

from .models import (
    RouterDecision,
    SkillSuggestion,
    SkillDomain,
    Urgency,
    AnswerDraft,
    Source,
    SummarizerState,
    CustomerProfile,
    PredictedQuestion,
)

# Mock router decisions by detected topic
MOCK_ROUTER_DECISIONS = {
    "roadmap": RouterDecision(
        needs_skill=True,
        suggested_skills=[
            SkillSuggestion(domain=SkillDomain.ROADMAP, confidence=0.85, priority=1)
        ],
        trigger_reason="Timeline/availability question detected",
        urgency=Urgency.HIGH,
        detected_question="When will this feature be available?",
    ),
    "architecture": RouterDecision(
        needs_skill=True,
        suggested_skills=[
            SkillSuggestion(domain=SkillDomain.ARCHITECTURE, confidence=0.85, priority=1)
        ],
        trigger_reason="Technical architecture question detected",
        urgency=Urgency.HIGH,
        detected_question="How does this work under the hood?",
    ),
    "security": RouterDecision(
        needs_skill=True,
        suggested_skills=[
            SkillSuggestion(domain=SkillDomain.SECURITY, confidence=0.90, priority=1)
        ],
        trigger_reason="Security/compliance question detected",
        urgency=Urgency.HIGH,
        detected_question="What compliance certifications do you have?",
    ),
    "pricing": RouterDecision(
        needs_skill=True,
        suggested_skills=[
            SkillSuggestion(domain=SkillDomain.PRICING, confidence=0.85, priority=1)
        ],
        trigger_reason="Pricing question detected",
        urgency=Urgency.MEDIUM,
        detected_question="What are your pricing options?",
    ),
    "case_studies": RouterDecision(
        needs_skill=True,
        suggested_skills=[
            SkillSuggestion(domain=SkillDomain.CASE_STUDIES, confidence=0.80, priority=1)
        ],
        trigger_reason="Customer reference requested",
        urgency=Urgency.MEDIUM,
        detected_question="Do you have any customer examples?",
    ),
}

# Mock answers by skill domain
MOCK_ANSWERS = {
    "roadmap": AnswerDraft(
        answer="Based on our current roadmap, this feature is targeted for Q2 2025. "
        "It's currently in private beta with select customers, and we expect "
        "general availability by mid-year. Note that timelines are subject to change "
        "based on customer feedback and development priorities.",
        sources=[
            Source(
                title="Product Roadmap",
                file="roadmap/references/roadmap.md",
                excerpt="Q2 2025 target for GA",
            )
        ],
        confidence=0.85,
        caveats=["Timelines subject to change", "Depends on beta feedback"],
        followups=["Would you like to join the private beta?", "What's your timeline for implementation?"],
        skills_used=["roadmap"],
    ),
    "architecture": AnswerDraft(
        answer="Our system uses a modern microservices architecture with three main components: "
        "1) An API gateway for request handling, 2) A processing layer for core logic, "
        "and 3) A scalable data layer. We can handle thousands of requests per second "
        "with sub-100ms latency for most operations. The exact performance depends on "
        "your specific use case and configuration.",
        sources=[
            Source(
                title="System Overview",
                file="architecture/references/system_overview.md",
                excerpt="Microservices architecture with horizontal scaling",
            )
        ],
        confidence=0.80,
        caveats=["Performance varies by use case", "Specific benchmarks available upon request"],
        followups=["What's your expected request volume?", "Do you have specific latency requirements?"],
        skills_used=["architecture"],
    ),
    "security": AnswerDraft(
        answer="We maintain SOC 2 Type II certification and are GDPR compliant. "
        "All data is encrypted at rest (AES-256) and in transit (TLS 1.3). "
        "We offer data residency options in US, EU, and APAC regions. "
        "For enterprise customers, we also provide detailed security questionnaire responses "
        "and can arrange calls with our security team.",
        sources=[
            Source(
                title="Compliance Matrix",
                file="security/references/compliance_matrix.md",
                excerpt="SOC 2 Type II, GDPR, HIPAA available",
            )
        ],
        confidence=0.90,
        caveats=["HIPAA BAA available for healthcare customers"],
        followups=["Do you have specific compliance requirements?", "Would you like our security whitepaper?"],
        skills_used=["security"],
    ),
    "pricing": AnswerDraft(
        answer="We offer three pricing tiers: Starter (free tier with basic features), "
        "Professional ($X/month with full API access), and Enterprise (custom pricing "
        "with dedicated support and SLAs). For enterprise customers, we typically work "
        "on annual contracts with volume discounts. I can connect you with our sales team "
        "for a detailed quote based on your expected usage.",
        sources=[
            Source(
                title="Pricing FAQ",
                file="pricing/references/pricing_faq.md",
                excerpt="Three tiers: Starter, Professional, Enterprise",
            )
        ],
        confidence=0.75,
        caveats=["Pricing subject to negotiation for enterprise", "Volume discounts available"],
        followups=["What's your expected monthly usage?", "Do you have a budget range in mind?"],
        skills_used=["pricing"],
    ),
    "case_studies": AnswerDraft(
        answer="We have several customers in similar industries seeing great results. "
        "For example, a fintech company reduced their processing time by 60% and improved "
        "accuracy significantly. I can share anonymized case studies or arrange a call "
        "with a reference customer if that would be helpful.",
        sources=[
            Source(
                title="Fintech Success Story",
                file="case_studies/references/fintech_beta_bank.md",
                excerpt="60% reduction in processing time",
            )
        ],
        confidence=0.70,
        caveats=["Results vary by implementation", "Reference calls subject to customer availability"],
        followups=["Would you like to speak with a reference customer?", "What metrics are most important to you?"],
        skills_used=["case_studies"],
    ),
}

# Default fallback for unknown domains
DEFAULT_ROUTER_DECISION = RouterDecision(
    needs_skill=False,
    trigger_reason="No specific skill match",
    urgency=Urgency.LOW,
)

DEFAULT_ANSWER = AnswerDraft(
    answer="I'd be happy to help with that question. Let me get the right information "
    "for you. Could you provide a bit more context about your specific needs?",
    confidence=0.5,
    caveats=["General response - specific details may vary"],
    followups=["Could you tell me more about your use case?"],
    skills_used=[],
)

# Mock summarizer state for fintech scenario
MOCK_SUMMARIZER_STATE = SummarizerState(
    customer_profile=CustomerProfile(
        company="FinTech Startup",
        industry="Financial Services",
        geo="US",
        size="mid",
        technical_maturity="high",
    ),
    goals=[
        "Automate document processing",
        "Improve accuracy",
        "Reduce processing time",
    ],
    constraints=[
        "SOC 2 compliance required",
        "Data residency in US",
        "Integration with existing systems",
    ],
    predicted_questions=[
        PredictedQuestion(
            question="What about on-premise deployment?",
            probability=0.7,
            domain=SkillDomain.DEPLOYMENT,
        ),
        PredictedQuestion(
            question="How long does implementation take?",
            probability=0.6,
            domain=SkillDomain.ROADMAP,
        ),
    ],
    suggested_asks=[
        "What's your current processing volume?",
        "Who are the key stakeholders in this decision?",
        "What's your timeline for implementation?",
    ],
    summary_text="Fintech startup exploring AI-powered document processing. "
    "High technical maturity, requires SOC 2 compliance. "
    "Interested in architecture and security details.",
)


def get_mock_router_decision(text: str) -> RouterDecision:
    """Get a mock router decision based on text content."""
    text_lower = text.lower()

    # Check for domain keywords
    if any(kw in text_lower for kw in ["when", "timeline", "roadmap", "eta", "available"]):
        return MOCK_ROUTER_DECISIONS.get("roadmap", DEFAULT_ROUTER_DECISION)
    if any(kw in text_lower for kw in ["how does it work", "architecture", "technical"]):
        return MOCK_ROUTER_DECISIONS.get("architecture", DEFAULT_ROUTER_DECISION)
    if any(kw in text_lower for kw in ["security", "soc", "compliance", "encryption"]):
        return MOCK_ROUTER_DECISIONS.get("security", DEFAULT_ROUTER_DECISION)
    if any(kw in text_lower for kw in ["pricing", "cost", "price", "plan"]):
        return MOCK_ROUTER_DECISIONS.get("pricing", DEFAULT_ROUTER_DECISION)
    if any(kw in text_lower for kw in ["customer", "case study", "reference", "example"]):
        return MOCK_ROUTER_DECISIONS.get("case_studies", DEFAULT_ROUTER_DECISION)

    return DEFAULT_ROUTER_DECISION


def get_mock_answer(domain: str) -> AnswerDraft:
    """Get a mock answer for a skill domain."""
    return MOCK_ANSWERS.get(domain, DEFAULT_ANSWER)
