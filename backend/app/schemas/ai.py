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
