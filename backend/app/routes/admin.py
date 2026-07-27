from fastapi import APIRouter, Depends, HTTPException, status
from app.auth.dependencies import get_current_user, get_current_admin
from app.database.connection import db
from datetime import datetime, timezone

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/analytics")
async def get_analytics(current_user: dict = Depends(get_current_admin)):
    total_schemes = await db.schemes.count_documents({})
    total_users = await db.users.count_documents({})
    total_recommendations = await db.recommendations.count_documents({})
    total_conversations = await db.conversations.count_documents({})
    return {
        "total_schemes": total_schemes,
        "total_users": total_users,
        "total_recommendations": total_recommendations,
        "total_conversations": total_conversations,
    }


@router.delete("/schemes/{slug}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_scheme(slug: str, current_user: dict = Depends(get_current_admin)):
    result = await db.schemes.delete_one({"slug": slug})
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scheme not found")
