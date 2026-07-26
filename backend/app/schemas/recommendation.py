from pydantic import BaseModel
from typing import Optional, List


# ── Eligibility Check Request ─────────────────────────────────────────────────

class EligibilityRequest(BaseModel):
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


# ── Single Recommendation Result ──────────────────────────────────────────────

class RecommendationResult(BaseModel):
    id: str
    scheme_name: str
    slug: str
    level: str
    schemeCategory: List[str]
    tags: List[str]
    benefits: str
    documents: str
    eligibility_score: float
    confidence_score: float
    matched_conditions: List[str]
    missing_conditions: List[str]
    explanation: str
    generatedAt: str


# ── Recommendation List Response ──────────────────────────────────────────────

class RecommendationListResponse(BaseModel):
    total: int
    profile_completeness: float
    recommendations: List[RecommendationResult]
