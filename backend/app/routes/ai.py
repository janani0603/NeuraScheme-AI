import asyncio
import logging
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app.auth.dependencies import get_current_user
from app.schemas.ai import (
    AIRecommendationRequest,
    AssistantRequest,
    AssistantResponse,
    ConversationResponse,
    ConversationMessage,
    DeadlineRequest,
    DeadlineResponse,
    DocumentCheckRequest,
    DocumentCheckResponse,
    ComparisonRequest,
    ComparisonResponse,
)
from app.schemas.recommendation import RecommendationListResponse
from app.agents.workflow import run_recommendation_pipeline
from app.agents.application_agent import application_agent
from app.agents.deadline_agent import deadline_agent
from app.agents.document_checker_agent import document_checker_agent
from app.agents.comparison_agent import comparison_agent
from app.database.connection import db

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ai", tags=["AI"])


@router.post("/recommendations", response_model=RecommendationListResponse)
async def ai_recommendations(
    body: AIRecommendationRequest,
    current_user: dict = Depends(get_current_user),
):
    """
    Run the full LangGraph AI pipeline:
    Profile → Retrieval → Eligibility → Recommendation → Explanation
    """
    profile = body.model_dump()
    user_id = str(current_user["_id"])

    try:
        result = await asyncio.wait_for(
            run_recommendation_pipeline(profile, user_id),
            timeout=80.0
        )
    except asyncio.TimeoutError:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="AI pipeline timed out. Please try again.",
        )
    except Exception as e:
        logger.error(f"AI recommendation pipeline error for user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI recommendation service is temporarily unavailable. Please try again.",
        )

    if result.get("error") and not result.get("recommendations"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["error"],
        )

    return {
        "total": result["total"],
        "profile_completeness": result["profile_completeness"],
        "recommendations": result["recommendations"],
    }


@router.post("/recommendations/from-profile", response_model=RecommendationListResponse)
async def ai_recommendations_from_profile(
    current_user: dict = Depends(get_current_user),
):
    """
    Run AI recommendations using the authenticated user's saved profile.
    """
    profile = {
        "state": current_user.get("state"),
        "gender": current_user.get("gender"),
        "occupation": current_user.get("occupation"),
        "education": current_user.get("education"),
        "annual_income": current_user.get("annual_income"),
        "category": current_user.get("category"),
        "is_student": current_user.get("is_student", False),
        "is_farmer": current_user.get("is_farmer", False),
        "is_business_owner": current_user.get("is_business_owner", False),
        "has_disability": current_user.get("has_disability", False),
        "age": current_user.get("age"),
    }
    user_id = str(current_user["_id"])

    try:
        result = await run_recommendation_pipeline(profile, user_id)
    except Exception as e:
        logger.error(f"AI pipeline error for user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI recommendation service is temporarily unavailable.",
        )

    return {
        "total": result["total"],
        "profile_completeness": result["profile_completeness"],
        "recommendations": result["recommendations"],
    }


@router.post("/assistant", response_model=AssistantResponse)
async def ask_assistant(
    body: AssistantRequest,
    current_user: dict = Depends(get_current_user),
):
    """
    Ask the AI assistant a question about government schemes.
    Maintains conversation history. Answers grounded in stored scheme data only.
    """
    user_id = str(current_user["_id"])

    if not body.question.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Question cannot be empty",
        )

    try:
        result = await application_agent(
            user_id=user_id,
            question=body.question,
            conversation_id=body.conversation_id,
            scheme_slugs=body.scheme_slugs,
        )
    except Exception as e:
        logger.error(f"Assistant error for user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI assistant is temporarily unavailable. Please try again.",
        )

    return AssistantResponse(**result)


@router.get("/conversations", response_model=List[ConversationResponse])
async def get_conversations(current_user: dict = Depends(get_current_user)):
    """Return all conversations for the authenticated user."""
    user_id = str(current_user["_id"])
    cursor = db["conversations"].find(
        {"userId": user_id}
    ).sort("updatedAt", -1).limit(20)

    docs = await cursor.to_list(length=20)
    result = []
    for doc in docs:
        messages = [
            ConversationMessage(
                question=m.get("question", ""),
                response=m.get("response", ""),
                scheme_slugs=m.get("scheme_slugs", []),
                timestamp=m["timestamp"].isoformat() if m.get("timestamp") else "",
            )
            for m in doc.get("messages", [])
        ]
        result.append(ConversationResponse(
            conversation_id=str(doc["_id"]),
            messages=messages,
            createdAt=doc["createdAt"].isoformat() if doc.get("createdAt") else "",
            updatedAt=doc["updatedAt"].isoformat() if doc.get("updatedAt") else "",
        ))
    return result


@router.delete("/conversations/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_conversation(
    conversation_id: str,
    current_user: dict = Depends(get_current_user),
):
    """Delete a specific conversation."""
    user_id = str(current_user["_id"])
    result = await db["conversations"].delete_one(
        {"_id": conversation_id, "userId": user_id}
    )
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")


# ── Deadline Agent ────────────────────────────────────────────────────────────

@router.post("/deadlines", response_model=DeadlineResponse)
async def check_deadlines(
    body: DeadlineRequest,
    current_user: dict = Depends(get_current_user),
):
    """
    Extract and track deadlines for a list of schemes.
    Returns schemes sorted by urgency.
    """
    user_id = str(current_user["_id"])
    try:
        result = await deadline_agent(user_id=user_id, scheme_slugs=body.scheme_slugs)
    except Exception as e:
        logger.error(f"Deadline agent error: {e}")
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Deadline service unavailable")
    return result


@router.get("/deadlines", response_model=DeadlineResponse)
async def get_saved_deadlines(current_user: dict = Depends(get_current_user)):
    """Get previously saved deadline alerts for the current user."""
    user_id = str(current_user["_id"])
    doc = await db["deadline_alerts"].find_one({"userId": user_id})
    if not doc:
        return {"deadlines": [], "urgent_count": 0}
    deadlines = doc.get("deadlines", [])
    urgent_count = sum(1 for d in deadlines if d.get("urgency") == "high" and d.get("has_deadline"))
    return {"deadlines": deadlines, "urgent_count": urgent_count}


# ── Document Checker Agent ────────────────────────────────────────────────────

@router.post("/check-documents", response_model=DocumentCheckResponse)
async def check_documents(
    body: DocumentCheckRequest,
    current_user: dict = Depends(get_current_user),
):
    """
    Check if the user has all required documents for a specific scheme.
    """
    try:
        result = await document_checker_agent(
            scheme_slug=body.scheme_slug,
            user_documents=body.user_documents,
        )
    except Exception as e:
        logger.error(f"Document checker error: {e}")
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Document checker unavailable")
    if "error" in result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=result["error"])
    return result


# ── Comparison Agent ──────────────────────────────────────────────────────────

@router.post("/compare", response_model=ComparisonResponse)
async def compare_schemes(
    body: ComparisonRequest,
    current_user: dict = Depends(get_current_user),
):
    """
    Compare 2-4 schemes side by side with AI analysis.
    Optionally pass a profile for personalized best-match recommendation.
    """
    if len(body.scheme_slugs) < 2:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="At least 2 schemes required")

    profile = body.profile or {}
    # Fall back to user's own profile if none provided
    if not profile:
        profile = {
            "state": current_user.get("state"),
            "occupation": current_user.get("occupation"),
            "annual_income": current_user.get("annual_income"),
            "category": current_user.get("category"),
        }

    try:
        result = await comparison_agent(scheme_slugs=body.scheme_slugs, profile=profile)
    except Exception as e:
        logger.error(f"Comparison agent error: {e}")
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Comparison service unavailable")
    if "error" in result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result["error"])
    return result
