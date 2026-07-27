from fastapi import APIRouter, HTTPException, Request, status

from app.schemas.user import RegisterRequest, LoginRequest, TokenResponse
from app.services.user_service import get_user_by_email, create_user
from app.auth.password import verify_password
from app.auth.jwt import create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])


def _user_dict(user: dict) -> dict:
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "phone": user.get("phone"),
        "date_of_birth": user.get("date_of_birth"),
        "gender": user.get("gender"),
        "state": user.get("state"),
        "district": user.get("district"),
        "occupation": user.get("occupation"),
        "education": user.get("education"),
        "annual_income": user.get("annual_income"),
        "category": user.get("category"),
        "is_student": user.get("is_student", False),
        "is_farmer": user.get("is_farmer", False),
        "is_business_owner": user.get("is_business_owner", False),
        "has_disability": user.get("has_disability", False),
        "saved_schemes": [str(s) for s in user.get("saved_schemes", [])],
        "role": user.get("role", "user"),
        "is_active": user.get("is_active", True),
    }


@router.post("/register/debug")
async def register_debug(request: Request):
    body = await request.json()
    return {"received": body}


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(body: RegisterRequest):
    existing = await get_user_by_email(body.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists",
        )

    user = await create_user(body.model_dump())
    token = create_access_token(str(user["_id"]))
    return {"access_token": token, "token_type": "bearer", "user": _user_dict(user)}


@router.post("/login")
async def login(body: LoginRequest):
    user = await get_user_by_email(body.email)
    if not user or not verify_password(body.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    if not user.get("is_active", True):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive",
        )
    token = create_access_token(str(user["_id"]))
    return {"access_token": token, "token_type": "bearer", "user": _user_dict(user)}
