from pydantic import BaseModel
from typing import Optional, List


class AIRecommendationRequest(BaseModel):
    state: Optional[str] = None
    gender: Optional[str] = None
    occupation: Optional[str] = None
    education: Optional[str] = None
    annual_income: Optional[float] = None
    category: Optional[str] = None
    is_student: bool = False
    is_farmer: bool = False
    is_business_owner: bool = False
    has_disability: bool = False
    age: Optional[int] = None


class AssistantRequest(BaseModel):
    question: str
    conversation_id: Optional[str] = None
    scheme_slugs: Optional[List[str]] = None


class AssistantResponse(BaseModel):
    conversation_id: str
    question: str
    response: str
    agents_used: List[str] = []


class ConversationMessage(BaseModel):
    question: str
    response: str
    scheme_slugs: List[str]
    timestamp: str


class ConversationResponse(BaseModel):
    conversation_id: str
    messages: List[ConversationMessage]
    createdAt: str
    updatedAt: str


# ── Deadline Agent ────────────────────────────────────────────────────────────

class DeadlineRequest(BaseModel):
    scheme_slugs: List[str]


class DeadlineItem(BaseModel):
    slug: str
    scheme_name: str
    has_deadline: bool
    deadline_text: Optional[str] = None
    deadline_date: Optional[str] = None
    is_ongoing: bool
    urgency: str


class DeadlineResponse(BaseModel):
    deadlines: List[DeadlineItem]
    urgent_count: int


# ── Document Checker Agent ────────────────────────────────────────────────────

class DocumentCheckRequest(BaseModel):
    scheme_slug: str
    user_documents: List[str] = []


class DocumentCheckResponse(BaseModel):
    scheme_slug: str
    scheme_name: str
    required_documents: List[str]
    have: List[str]
    missing: List[str]
    optional: List[str]
    ready_to_apply: bool
    readiness_score: int
    advice: str


# ── Comparison Agent ──────────────────────────────────────────────────────────

class ComparisonRequest(BaseModel):
    scheme_slugs: List[str]
    profile: Optional[dict] = {}


class ComparisonItem(BaseModel):
    slug: str
    scheme_name: str
    key_benefit: str
    target_audience: str
    ease_of_apply: str
    benefit_amount: str
    pros: List[str]
    cons: List[str]
    level: str
    schemeCategory: List[str]


class ComparisonResponse(BaseModel):
    summary: str
    best_for_user: str
    reason: str
    comparison: List[ComparisonItem]
    schemes_compared: int
