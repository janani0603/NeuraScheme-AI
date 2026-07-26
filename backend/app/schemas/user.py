from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, List


# ── Register ──────────────────────────────────────────────────────────────────

class RegisterRequest(BaseModel):
    # Step 1 – Account
    name: str
    email: EmailStr
    phone: Optional[str] = None
    password: str
    confirm_password: str

    # Step 2 – Personal
    date_of_birth: Optional[str] = None
    gender: Optional[str] = None
    state: Optional[str] = None
    district: Optional[str] = None

    # Step 3 – Professional
    occupation: Optional[str] = None
    education: Optional[str] = None
    annual_income: Optional[float] = None
    category: Optional[str] = None
    is_student: bool = False
    is_farmer: bool = False
    is_business_owner: bool = False
    has_disability: bool = False

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v

    @field_validator("confirm_password")
    @classmethod
    def passwords_match(cls, v: str, info) -> str:
        if "password" in info.data and v != info.data["password"]:
            raise ValueError("Passwords do not match")
        return v


# ── Login ─────────────────────────────────────────────────────────────────────

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# ── Token ─────────────────────────────────────────────────────────────────────

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ── User Profile ──────────────────────────────────────────────────────────────

class UserProfileResponse(BaseModel):
    id: str
    name: str
    email: str
    phone: Optional[str] = None
    date_of_birth: Optional[str] = None
    gender: Optional[str] = None
    state: Optional[str] = None
    district: Optional[str] = None
    occupation: Optional[str] = None
    education: Optional[str] = None
    annual_income: Optional[float] = None
    category: Optional[str] = None
    is_student: bool = False
    is_farmer: bool = False
    is_business_owner: bool = False
    has_disability: bool = False
    saved_schemes: List[str] = []
    role: str
    is_active: bool
    createdAt: str
    updatedAt: str


# ── Update Profile ────────────────────────────────────────────────────────────

class UpdateProfileRequest(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    date_of_birth: Optional[str] = None
    gender: Optional[str] = None
    state: Optional[str] = None
    district: Optional[str] = None
    occupation: Optional[str] = None
    education: Optional[str] = None
    annual_income: Optional[float] = None
    category: Optional[str] = None
    is_student: Optional[bool] = None
    is_farmer: Optional[bool] = None
    is_business_owner: Optional[bool] = None
    has_disability: Optional[bool] = None
