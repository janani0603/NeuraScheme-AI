import re
from datetime import datetime, timezone
from typing import Optional

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr

from app.auth.dependencies import get_current_admin
from app.auth.password import hash_password
from app.database.connection import db
from app.models.scheme import new_scheme_document
from app.services.notification_service import fan_out_notification

router = APIRouter(prefix="/admin", tags=["Admin"])


# ── Schemas ───────────────────────────────────────────────────────────────────

class AddSchemeRequest(BaseModel):
    scheme_name: str
    slug: Optional[str] = None
    details: str
    benefits: str
    eligibility: str
    application: str
    documents: str
    level: str
    schemeCategory: list[str] = []
    tags: list[str] = []


class UpdateSchemeRequest(BaseModel):
    scheme_name: Optional[str] = None
    details: Optional[str] = None
    benefits: Optional[str] = None
    eligibility: Optional[str] = None
    application: Optional[str] = None
    documents: Optional[str] = None
    level: Optional[str] = None
    schemeCategory: Optional[list[str]] = None
    tags: Optional[list[str]] = None


class AddUserRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str = "user"


class UpdateRoleRequest(BaseModel):
    role: str   # "user" | "admin"


# ── Analytics ─────────────────────────────────────────────────────────────────

@router.get("/analytics")
async def get_analytics(current_user: dict = Depends(get_current_admin)):
    total_schemes = await db.schemes.count_documents({})
    total_users = await db.users.count_documents({})
    total_recommendations = await db.recommendations.count_documents({})
    total_conversations = await db.conversations.count_documents({})
    total_notifications = await db.notifications.count_documents({})
    return {
        "total_schemes": total_schemes,
        "total_users": total_users,
        "total_recommendations": total_recommendations,
        "total_conversations": total_conversations,
        "total_notifications": total_notifications,
    }


# ── User Management ───────────────────────────────────────────────────────────

@router.get("/users")
async def list_users(
    page: int = 1,
    page_size: int = 20,
    search: Optional[str] = None,
    current_user: dict = Depends(get_current_admin),
):
    query = {}
    if search:
        query = {"$or": [
            {"name": {"$regex": search, "$options": "i"}},
            {"email": {"$regex": search, "$options": "i"}},
        ]}
    total = await db.users.count_documents(query)
    skip = (page - 1) * page_size
    cursor = db.users.find(query, {"hashed_password": 0}).skip(skip).limit(page_size).sort("createdAt", -1)
    docs = await cursor.to_list(length=page_size)
    users = [_serialize_user(u) for u in docs]
    return {"total": total, "page": page, "page_size": page_size, "users": users}


@router.post("/users", status_code=status.HTTP_201_CREATED)
async def create_user(
    body: AddUserRequest,
    current_user: dict = Depends(get_current_admin),
):
    existing = await db.users.find_one({"email": body.email})
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")
    now = datetime.now(timezone.utc)
    doc = {
        "name": body.name,
        "email": body.email,
        "hashed_password": hash_password(body.password),
        "role": body.role,
        "is_active": True,
        "saved_schemes": [],
        "createdAt": now,
        "updatedAt": now,
    }
    result = await db.users.insert_one(doc)
    doc["_id"] = result.inserted_id
    return _serialize_user(doc)


@router.patch("/users/{user_id}/role", status_code=status.HTTP_200_OK)
async def update_user_role(
    user_id: str,
    body: UpdateRoleRequest,
    current_user: dict = Depends(get_current_admin),
):
    if body.role not in ("user", "admin"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Role must be 'user' or 'admin'")
    result = await db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"role": body.role, "updatedAt": datetime.now(timezone.utc)}},
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"message": f"Role updated to {body.role}"}


@router.delete("/users/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(
    user_id: str,
    current_user: dict = Depends(get_current_admin),
):
    if str(current_user["_id"]) == user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot delete your own account")
    result = await db.users.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"message": "User deleted"}


# ── Scheme Management ─────────────────────────────────────────────────────────

@router.post("/schemes", status_code=status.HTTP_201_CREATED)
async def add_scheme(
    body: AddSchemeRequest,
    current_user: dict = Depends(get_current_admin),
):
    slug = body.slug or _slugify(body.scheme_name)
    existing = await db.schemes.find_one({"slug": slug})
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Scheme with this slug already exists")

    search_text = " ".join(filter(None, [
        body.scheme_name, body.details, body.benefits,
        body.eligibility, " ".join(body.schemeCategory), " ".join(body.tags),
    ])).lower()

    doc = new_scheme_document(
        scheme_name=body.scheme_name,
        slug=slug,
        details=body.details,
        benefits=body.benefits,
        eligibility=body.eligibility,
        application=body.application,
        documents=body.documents,
        level=body.level,
        scheme_category=body.schemeCategory,
        tags=body.tags,
        search_text=search_text,
    )
    result = await db.schemes.insert_one(doc)

    # Fan-out notification to all users
    await fan_out_notification(
        title="New Scheme Available",
        message=f"A new government scheme has been added: {body.scheme_name}. Check if you're eligible!",
        notification_type="new_scheme",
        scheme_slug=slug,
        scheme_name=body.scheme_name,
    )

    doc["_id"] = result.inserted_id
    return {"message": "Scheme added and users notified", "slug": slug, "id": str(result.inserted_id)}


@router.put("/schemes/{slug}", status_code=status.HTTP_200_OK)
async def update_scheme(
    slug: str,
    body: UpdateSchemeRequest,
    current_user: dict = Depends(get_current_admin),
):
    updates = {k: v for k, v in body.model_dump(exclude_unset=True).items() if v is not None}
    if not updates:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields to update")
    updates["updatedAt"] = datetime.now(timezone.utc)
    result = await db.schemes.update_one({"slug": slug}, {"$set": updates})
    if result.matched_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scheme not found")
    return {"message": "Scheme updated"}


@router.delete("/schemes/{slug}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_scheme(
    slug: str,
    current_user: dict = Depends(get_current_admin),
):
    result = await db.schemes.delete_one({"slug": slug})
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scheme not found")


# ── Helpers ───────────────────────────────────────────────────────────────────

def _slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    return re.sub(r"-+", "-", text)


def _serialize_user(u: dict) -> dict:
    return {
        "id": str(u["_id"]),
        "name": u.get("name", ""),
        "email": u.get("email", ""),
        "role": u.get("role", "user"),
        "is_active": u.get("is_active", True),
        "state": u.get("state"),
        "occupation": u.get("occupation"),
        "createdAt": u["createdAt"].isoformat() if u.get("createdAt") else "",
    }
