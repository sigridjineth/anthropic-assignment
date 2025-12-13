from pydantic import BaseModel, Field
from .router import SkillDomain


class CustomerProfile(BaseModel):
    company: str | None = None
    industry: str | None = None
    geo: str | None = None
    size: str | None = None
    technical_maturity: str | None = None


class KeyMoment(BaseModel):
    offset_sec: float
    quote: str
    why_important: str
    importance: str = Field(default="medium", pattern="^(high|medium|low)$")


class PredictedQuestion(BaseModel):
    question: str
    probability: float = Field(ge=0.0, le=1.0)
    domain: SkillDomain


class SimilarCase(BaseModel):
    case_name: str
    match_score: int = Field(ge=0, le=100)
    takeaway: str
    source: str | None = None


class SummarizerState(BaseModel):
    customer_profile: CustomerProfile = Field(default_factory=CustomerProfile)
    goals: list[str] = Field(default_factory=list)
    constraints: list[str] = Field(default_factory=list)
    key_moments: list[KeyMoment] = Field(default_factory=list)
    predicted_questions: list[PredictedQuestion] = Field(default_factory=list)
    open_questions: list[str] = Field(default_factory=list)
    suggested_asks: list[str] = Field(default_factory=list)
    similar_cases: list[SimilarCase] = Field(default_factory=list)
    summary_text: str = ""
