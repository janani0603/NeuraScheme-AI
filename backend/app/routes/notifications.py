from fastapi import APIRouter, Depends, HTTPException, status
from app.auth.dependencies import get_current_user
from app.services.notification_service import (
    get_user_notifications,
    get_unread_count,
    mark_as_read,
    mark_all_as_read,
    delete_notification,
)

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get("")
async def list_notifications(
    unread_only: bool = False,
    current_user: dict = Depends(get_current_user),
):
    user_id = str(current_user["_id"])
    notifications = await get_user_notifications(user_id, unread_only=unread_only)
    unread = await get_unread_count(user_id)
    return {"notifications": notifications, "unread_count": unread}


@router.get("/unread-count")
async def unread_count(current_user: dict = Depends(get_current_user)):
    count = await get_unread_count(str(current_user["_id"]))
    return {"unread_count": count}


@router.patch("/{notification_id}/read", status_code=status.HTTP_200_OK)
async def read_notification(
    notification_id: str,
    current_user: dict = Depends(get_current_user),
):
    ok = await mark_as_read(notification_id, str(current_user["_id"]))
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")
    return {"message": "Marked as read"}


@router.patch("/read-all", status_code=status.HTTP_200_OK)
async def read_all_notifications(current_user: dict = Depends(get_current_user)):
    count = await mark_all_as_read(str(current_user["_id"]))
    return {"message": f"{count} notifications marked as read"}


@router.delete("/{notification_id}", status_code=status.HTTP_200_OK)
async def remove_notification(
    notification_id: str,
    current_user: dict = Depends(get_current_user),
):
    ok = await delete_notification(notification_id, str(current_user["_id"]))
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")
    return {"message": "Notification deleted"}
