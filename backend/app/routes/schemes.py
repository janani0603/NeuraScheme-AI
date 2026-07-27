from fastapi import APIRouter, HTTPException, Query, Depends, status
from typing import Optional
from datetime import datetime, timezone
from bson import ObjectId

from app.schemas.scheme import SchemeResponse, SchemeListResponse
from app.services.scheme_service import (
    get_schemes,
    get_scheme_by_slug,
    get_categories,
    get_tags,
    get_levels,
)
from app.auth.dependencies import get_current_user
from app.database.connection import db

router = APIRouter(prefix="/schemes", tags=["Schemes"])


@router.get("", response_model=SchemeListResponse)
async def list_schemes(
    keyword: Optional[str] = Query(None),
    level: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    tag: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    sort_by: str = Query("scheme_name"),
    sort_order: str = Query("asc"),
):
    return await get_schemes(
        keyword=keyword, level=level, category=category, tag=tag,
        page=page, page_size=page_size, sort_by=sort_by, sort_order=sort_order,
    )


@router.get("/filters/categories")
async def list_categories():
    return await get_categories()


@router.get("/filters/tags")
async def list_tags():
    return await get_tags()


@router.get("/filters/levels")
async def list_levels():
    return await get_levels()


@router.post("/{slug}/save", status_code=status.HTTP_200_OK)
async def save_scheme(slug: str, current_user: dict = Depends(get_current_user)):
    scheme = await db.schemes.find_one({"slug": slug})
    if not scheme:
        raise HTTPException(status_code=404, detail="Scheme not found")
    await db.users.update_one(
        {"_id": current_user["_id"]},
        {
            "$addToSet": {"saved_schemes": slug},
            "$set": {"updatedAt": datetime.now(timezone.utc)},
        },
    )
    return {"message": "Scheme saved"}


@router.delete("/{slug}/save", status_code=status.HTTP_200_OK)
async def unsave_scheme(slug: str, current_user: dict = Depends(get_current_user)):
    await db.users.update_one(
        {"_id": current_user["_id"]},
        {
            "$pull": {"saved_schemes": slug},
            "$set": {"updatedAt": datetime.now(timezone.utc)},
        },
    )
    return {"message": "Scheme removed from saved"}


@router.get("/{slug}", response_model=SchemeResponse)
async def get_scheme(slug: str):
    scheme = await get_scheme_by_slug(slug)
    if not scheme:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Scheme '{slug}' not found")
    return scheme
