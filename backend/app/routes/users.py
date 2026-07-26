from fastapi import APIRouter, Depends, HTTPException, status

from app.auth.dependencies import get_current_user
from app.schemas.user import UserProfileResponse, UpdateProfileRequest
from app.services.user_service import update_user_profile


router = APIRouter(prefix="/users", tags=["Users"])


def _serialize(user: dict) -> UserProfileResponse:
    return UserProfileResponse(
        id=str(user["_id"]),
        name=user["name"],
        email=user["email"],
        phone=user.get("phone"),
        date_of_birth=user.get("date_of_birth"),
        gender=user.get("gender"),
        state=user.get("state"),
        district=user.get("district"),
        occupation=user.get("occupation"),
        education=user.get("education"),
        annual_income=user.get("annual_income"),
        category=user.get("category"),
        is_student=user.get("is_student", False),
        is_farmer=user.get("is_farmer", False),
        is_business_owner=user.get("is_business_owner", False),
        has_disability=user.get("has_disability", False),
        saved_schemes=[str(s) for s in user.get("saved_schemes", [])],
        role=user.get("role", "user"),
        is_active=user.get("is_active", True),
        createdAt=user["createdAt"].isoformat(),
        updatedAt=user["updatedAt"].isoformat(),
    )


@router.get("/me", response_model=UserProfileResponse)
async def get_profile(current_user: dict = Depends(get_current_user)):
    return _serialize(current_user)


@router.put("/me", response_model=UserProfileResponse)
async def update_profile(
    body: UpdateProfileRequest,
    current_user: dict = Depends(get_current_user),
):
    updated = await update_user_profile(
        str(current_user["_id"]),
        body.model_dump(exclude_unset=True),
    )
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return _serialize(updated)
