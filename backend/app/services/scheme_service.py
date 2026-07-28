from typing import Optional
from bson import ObjectId

from app.database.connection import db


def _serialize(doc: dict) -> dict:
    return {
        "id": str(doc["_id"]),
        "scheme_name": doc.get("scheme_name", ""),
        "slug": doc.get("slug", ""),
        "details": doc.get("details", ""),
        "benefits": doc.get("benefits", ""),
        "eligibility": doc.get("eligibility", ""),
        "application": doc.get("application", ""),
        "documents": doc.get("documents", ""),
        "level": doc.get("level", ""),
        "schemeCategory": doc.get("schemeCategory", []),
        "tags": doc.get("tags", []),
        "createdAt": doc["createdAt"].isoformat() if doc.get("createdAt") else "",
    }


async def get_schemes(
    keyword: Optional[str],
    level: Optional[str],
    category: Optional[str],
    tag: Optional[str],
    state: Optional[str],
    page: int,
    page_size: int,
    sort_by: str,
    sort_order: str,
) -> dict:
    conditions = []

    if keyword:
        conditions.append({"$or": [
            {"scheme_name": {"$regex": keyword, "$options": "i"}},
            {"details": {"$regex": keyword, "$options": "i"}},
            {"eligibility": {"$regex": keyword, "$options": "i"}},
            {"benefits": {"$regex": keyword, "$options": "i"}},
            {"tags": {"$regex": keyword, "$options": "i"}},
        ]})

    if level:
        conditions.append({"level": {"$regex": f"^{level}$", "$options": "i"}})

    if category:
        conditions.append({"schemeCategory": {"$regex": category, "$options": "i"}})

    if tag:
        conditions.append({"tags": {"$regex": tag, "$options": "i"}})

    if state:
        conditions.append({"$or": [
            {"level": {"$regex": "^central$", "$options": "i"}},
            {"eligibility": {"$regex": state, "$options": "i"}},
            {"details": {"$regex": state, "$options": "i"}},
            {"tags": {"$regex": state, "$options": "i"}},
        ]})

    query = {"$and": conditions} if conditions else {}

    sort_direction = 1 if sort_order == "asc" else -1
    sort_spec = [(sort_by, sort_direction)]
    projection = {"embedding": 0}

    total = await db["schemes"].count_documents(query)
    total_pages = max(1, -(-total // page_size))  # ceiling division
    skip = (page - 1) * page_size

    cursor = db["schemes"].find(query, projection)
    cursor = cursor.sort(sort_spec).skip(skip).limit(page_size)

    docs = await cursor.to_list(length=page_size)

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "schemes": [_serialize(d) for d in docs],
    }


async def get_scheme_by_slug(slug: str) -> Optional[dict]:
    doc = await db["schemes"].find_one({"slug": slug})
    if doc is None:
        return None
    return _serialize(doc)


async def get_scheme_by_id(scheme_id: str) -> Optional[dict]:
    doc = await db["schemes"].find_one({"_id": ObjectId(scheme_id)})
    if doc is None:
        return None
    return _serialize(doc)


async def get_categories() -> list:
    pipeline = [
        {"$unwind": "$schemeCategory"},
        {"$group": {"_id": "$schemeCategory"}},
        {"$sort": {"_id": 1}},
    ]
    results = await db["schemes"].aggregate(pipeline).to_list(length=None)
    return [r["_id"] for r in results if r["_id"]]


async def get_tags() -> list:
    pipeline = [
        {"$unwind": "$tags"},
        {"$group": {"_id": "$tags"}},
        {"$sort": {"_id": 1}},
    ]
    results = await db["schemes"].aggregate(pipeline).to_list(length=None)
    return [r["_id"] for r in results if r["_id"]]


async def get_levels() -> list:
    results = await db["schemes"].distinct("level")
    return sorted([r for r in results if r])


async def get_states() -> list:
    results = await db["schemes"].distinct("state")
    return sorted([r for r in results if r])
