from pydantic import BaseModel
from typing import Optional, List


# ── Single Scheme Response ────────────────────────────────────────────────────

class SchemeResponse(BaseModel):
    id: str
    scheme_name: str
    slug: str
    details: str
    benefits: str
    eligibility: str
    application: str
    documents: str
    level: str
    schemeCategory: List[str]
    tags: List[str]
    createdAt: str


# ── Paginated List Response ───────────────────────────────────────────────────

class SchemeListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    total_pages: int
    schemes: List[SchemeResponse]


# ── Search / Filter Query Params ──────────────────────────────────────────────

class SchemeFilterParams(BaseModel):
    keyword: Optional[str] = None
    level: Optional[str] = None          # "Central" | "State"
    category: Optional[str] = None
    tag: Optional[str] = None
    page: int = 1
    page_size: int = 20
    sort_by: str = "scheme_name"         # "scheme_name" | "createdAt"
    sort_order: str = "asc"              # "asc" | "desc"
