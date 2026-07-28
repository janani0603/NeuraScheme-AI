from datetime import datetime, UTC


def new_notification_document(
    user_id: str,
    title: str,
    message: str,
    notification_type: str,
    scheme_slug: str = None,
    scheme_name: str = None,
) -> dict:
    return {
        "userId": user_id,
        "title": title,
        "message": message,
        "type": notification_type,   # "new_scheme" | "deadline" | "update" | "system"
        "scheme_slug": scheme_slug,
        "scheme_name": scheme_name,
        "is_read": False,
        "createdAt": datetime.now(UTC),
    }
