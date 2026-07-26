from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional

from app.schemas.recommendation import EligibilityRequest, RecommendationListResponse
from app.services.recommendation_service import generate_recommendations, get_user_recommendations
from app.auth.dependencies import get_current_user
from app.auth.jwt import decode_token
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])

# Optional bearer — does not raise if token is missing
_optional_bearer = OAuth2PasswordBearer(tokenUrl="/auth/login", auto_error=False)


async def _optional_user(token: Optional[str] = Depends(_optional_bearer)) -> Optional[str]:
    """Returns user_id string if token is valid, else None."""
    if not token:
        return None
    try:
        return decode_token(token)
    except JWTError:
        return None


@router.post("/check", response_model=RecommendationListResponse)
async def check_eligibility(
    body: EligibilityRequest,
    user_id: Optional[str] = Depends(_optional_user),
):
    """
    Run the eligibility engine against the submitted profile.
    Works for both guests and authenticated users.
    If authenticated, results are saved to the recommendations collection.
    """
    profile = body.model_dump()
    result = await generate_recommendations(profile, user_id=user_id)
    return result


@router.get("/me", response_model=RecommendationListResponse)
async def my_recommendations(current_user: dict = Depends(get_current_user)):
    """
    Return the last saved recommendations for the logged-in user.
    """
    result = await get_user_recommendations(str(current_user["_id"]))
    return result


@router.post("/me/refresh", response_model=RecommendationListResponse)
async def refresh_recommendations(current_user: dict = Depends(get_current_user)):
    """
    Re-run the eligibility engine using the user's saved profile.
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
        "age": None,
    }
    result = await generate_recommendations(profile, user_id=str(current_user["_id"]))
    return result
