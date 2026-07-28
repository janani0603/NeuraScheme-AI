from bson import ObjectId
from datetime import datetime, UTC
from app.database.connection import db
from app.models.notification import new_notification_document


async def get_user_notifications(user_id: str, unread_only: bool = False) -> list:
    query = {"userId": user_id}
    if unread_only:
        query["is_read"] = False
    cursor = db["notifications"].find(query).sort("createdAt", -1).limit(50)
    docs = await cursor.to_list(length=50)
    return [_serialize(d) for d in docs]


async def get_unread_count(user_id: str) -> int:
    return await db["notifications"].count_documents({"userId": user_id, "is_read": False})


async def mark_as_read(notification_id: str, user_id: str) -> bool:
    result = await db["notifications"].update_one(
        {"_id": ObjectId(notification_id), "userId": user_id},
        {"$set": {"is_read": True}},
    )
    return result.modified_count > 0


async def mark_all_as_read(user_id: str) -> int:
    result = await db["notifications"].update_many(
        {"userId": user_id, "is_read": False},
        {"$set": {"is_read": True}},
    )
    return result.modified_count


async def delete_notification(notification_id: str, user_id: str) -> bool:
    result = await db["notifications"].delete_one(
        {"_id": ObjectId(notification_id), "userId": user_id}
    )
    return result.deleted_count > 0


async def fan_out_notification(
    title: str,
    message: str,
    notification_type: str,
    scheme_slug: str = None,
    scheme_name: str = None,
) -> int:
    """Create one notification document per user. Returns count inserted."""
    cursor = db["users"].find({}, {"_id": 1})
    users = await cursor.to_list(length=None)
    if not users:
        return 0
    docs = [
        new_notification_document(
            user_id=str(u["_id"]),
            title=title,
            message=message,
            notification_type=notification_type,
            scheme_slug=scheme_slug,
            scheme_name=scheme_name,
        )
        for u in users
    ]
    result = await db["notifications"].insert_many(docs)
    return len(result.inserted_ids)


def _serialize(doc: dict) -> dict:
    return {
        "id": str(doc["_id"]),
        "userId": doc.get("userId", ""),
        "title": doc.get("title", ""),
        "message": doc.get("message", ""),
        "type": doc.get("type", ""),
        "scheme_slug": doc.get("scheme_slug"),
        "scheme_name": doc.get("scheme_name"),
        "is_read": doc.get("is_read", False),
        "createdAt": doc["createdAt"].isoformat() if doc.get("createdAt") else "",
    }
