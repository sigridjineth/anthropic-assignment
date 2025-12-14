"""Post-call models for call notes and skill update proposals."""

from pydantic import BaseModel, Field


class SkillUpdateProposal(BaseModel):
    """A proposed update to a skill based on call learnings."""

    skill_id: str = Field(description="The skill to update (e.g., 'fintech_patterns')")
    file_path: str = Field(description="The file to update (e.g., 'compliance_handling.md')")
    update_type: str = Field(description="Type: 'add_pattern' | 'add_example' | 'update_guidance'")
    content: str = Field(description="The content to add or update")
    rationale: str = Field(description="Why this update is valuable")


class PostCallResult(BaseModel):
    """Result from post-call analysis."""

    # Call summary
    call_summary: str = Field(description="2-3 sentence summary of the call")
    topics_covered: list[str] = Field(description="Topics discussed during the call")
    outcome: str = Field(description="Call outcome (e.g., 'follow-up scheduled', 'demo requested')")

    # Customer insights
    customer_pain_points: list[str] = Field(description="Pain points identified")
    customer_requirements: list[str] = Field(description="Key requirements mentioned")

    # Skill usage
    skills_used: list[str] = Field(description="Skills that were activated during the call")
    skills_helpful: list[str] = Field(description="Skills that provided useful answers")

    # Proposed updates
    skill_update_proposals: list[SkillUpdateProposal] = Field(
        default_factory=list,
        description="Suggested updates to skills based on learnings"
    )

    # Follow-up
    follow_up_actions: list[str] = Field(
        default_factory=list,
        description="Recommended follow-up actions"
    )
