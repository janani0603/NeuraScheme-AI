from datetime import datetime, UTC
from typing import Optional
from bson import ObjectId


def new_user_document(
    name: str,
    email: str,
    hashed_password: str,
    phone: Optional[str] = None,
    date_of_birth: Optional[str] = None,
    gender: Optional[str] = None,
    state: Optional[str] = None,
    district: Optional[str] = None,
    occupation: Optional[str] = None,
    education: Optional[str] = None,
    annual_income: Optional[float] = None,
    category: Optional[str] = None,
    is_student: bool = False,
    is_farmer: bool = False,
    is_business_owner: bool = False,
    has_disability: bool = False,
    age: Optional[int] = None,
    role: str = "user",
) -> dict:
    now = datetime.now(UTC)
    return {
        "name": name,
        "email": email,
        "hashed_password": hashed_password,
        "phone": phone,
        "date_of_birth": date_of_birth,
        "gender": gender,
        "state": state,
        "district": district,
        "occupation": occupation,
        "education": education,
        "annual_income": annual_income,
        "category": category,
        "is_student": is_student,
        "is_farmer": is_farmer,
        "is_business_owner": is_business_owner,
        "has_disability": has_disability,
        "age": age,
        "saved_schemes": [],
        "role": role,
        "is_active": True,
        "createdAt": now,
        "updatedAt": now,
    }
