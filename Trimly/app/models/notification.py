# app/models/notification.py
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum, Boolean
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base


# Who this specific notification is meant for
class NotificationRecipient(str, enum.Enum):
    customer = "customer"
    barber = "barber"


# How far before the appointment this notification should fire
class NotificationType(str, enum.Enum):
    two_hours = "2h"
    one_hour = "1h"
    thirty_minutes = "30m"


class Notification(Base):
    __tablename__ = "notifications"

    # Primary key — unique ID for every scheduled notification
    id = Column(Integer, primary_key=True, index=True)

    # Which booking this notification is attached to-
    booking_id = Column(Integer, ForeignKey("bookings.id"), nullable=False)

    # Whether this notification goes to the customer or the barber
    # (each booking generates separate notification rows for each side)
    recipient = Column(Enum(NotificationRecipient), nullable=False)

    # Which reminder this is — 2h, 1h, or 30m before the appointment
    type = Column(Enum(NotificationType), nullable=False)

    # The exact calculated time this notification should be sent
    # (booking.start_time minus 2h/1h/30m, calculated when the booking is confirmed)
    send_at = Column(DateTime(timezone=True), nullable=False)

    # Flips to True once a background job has actually sent it —
    # prevents the same notification from being sent twice
    sent = Column(Boolean, default=False)

    # Easy Python-side link: notification.booking gives you the full Booking row
    booking = relationship("Booking", backref="notifications")