from fastapi import APIRouter, HTTPException, Query, status
from typing import Optional

from app.schemas.scheme import SchemeResponse, SchemeListResponse
from app.services.scheme_service import (
    get_schemes,
    get_scheme_by_slug,
    get_categories,
    get_tags,
    get_levels,
)

router = APIRouter(prefix="/schemes", tags=["Schemes"])


@router.get("", response_model=SchemeListResponse)
async def list_schemes(
    keyword: Optional[str] = Query(None, description="Full-text search keyword"),
    level: Optional[str] = Query(None, description="Central or State"),
    category: Optional[str] = Query(None, description="Scheme category"),
    tag: Optional[str] = Query(None, description="Tag filter"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Results per page"),
    sort_by: str = Query("scheme_name", description="Field to sort by"),
    sort_order: str = Query("asc", description="asc or desc"),
):
    result = await get_schemes(
        keyword=keyword,
        level=level,
        category=category,
        tag=tag,
        page=page,
        page_size=page_size,
        sort_by=sort_by,
        sort_order=sort_order,
    )
    return result


@router.get("/filters/categories")
async def list_categories():
    return {"categories": await get_categories()}


@router.get("/filters/tags")
async def list_tags():
    return {"tags": await get_tags()}


@router.get("/filters/levels")
async def list_levels():
    return {"levels": await get_levels()}


@router.get("/{slug}", response_model=SchemeResponse)
async def get_scheme(slug: str):
    scheme = await get_scheme_by_slug(slug)
    if not scheme:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Scheme '{slug}' not found",
        )
    return scheme
