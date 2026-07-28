from datetime import datetime, UTC
from typing import Optional
from bson import ObjectId
from pymongo import ReturnDocument

from app.database.connection import db
from app.models.user import new_user_document
from app.auth.password import hash_password


async def get_user_by_email(email: str) -> Optional[dict]:
    return await db["users"].find_one({"email": email})


async def get_user_by_id(user_id: str) -> Optional[dict]:
    return await db["users"].find_one({"_id": ObjectId(user_id)})


async def create_user(data: dict) -> dict:
    document = new_user_document(
        name=data["name"],
        email=data["email"],
        hashed_password=hash_password(data["password"]),
        phone=data.get("phone"),
        date_of_birth=data.get("date_of_birth"),
        gender=data.get("gender"),
        state=data.get("state"),
        district=data.get("district"),
        occupation=data.get("occupation"),
        education=data.get("education"),
        annual_income=data.get("annual_income"),
        category=data.get("category"),
        is_student=data.get("is_student", False),
        is_farmer=data.get("is_farmer", False),
        is_business_owner=data.get("is_business_owner", False),
        has_disability=data.get("has_disability", False),
    )
    result = await db["users"].insert_one(document)
    document["_id"] = result.inserted_id
    return document


async def update_user_profile(user_id: str, updates: dict) -> Optional[dict]:
    updates["updatedAt"] = datetime.now(UTC)
    clean = {k: v for k, v in updates.items() if v is not None and v != ""}
    bool_fields = ["is_student", "is_farmer", "is_business_owner", "has_disability"]
    for field in bool_fields:
        if field in updates and updates[field] is not None:
            clean[field] = bool(updates[field])
    return await db["users"].find_one_and_update(
        {"_id": ObjectId(user_id)},
        {"$set": clean},
        return_document=ReturnDocument.AFTER,
    )
