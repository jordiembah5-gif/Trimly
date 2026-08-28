# app/schemas/notification.py
from pydantic import BaseModel
from datetime import datetime

from app.models.notification import NotificationRecipient, NotificationType


# Notifications are created internally by the app, not by client requests,
# so there's no NotificationCreate schema — only Read, for viewing/debugging
class NotificationRead(BaseModel):
    id: int
    booking_id: int
    recipient: NotificationRecipient
    type: NotificationType
    send_at: datetime
    sent: bool

    class Config:
        from_attributes = True