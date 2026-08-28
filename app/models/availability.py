# app/models/availability.py
from sqlalchemy import Column, Integer, ForeignKey, Time, Date, Boolean
from sqlalchemy.orm import relationship

from app.db.base import Base


class Availability(Base):
    __tablename__ = "availabilities"

    # Primary key — unique ID for each free/working window a barber sets
    id = Column(Integer, primary_key=True, index=True)

    # Which barber this availability window belongs to
    barber_id = Column(Integer, ForeignKey("barbers.id"), nullable=False)

    # Day of week this window repeats on: 0 = Monday ... 6 = Sunday
    # Used for a barber's regular weekly schedule (e.g. "every Tuesday, 9am-5pm")
    day_of_week = Column(Integer, nullable=True)

    # OR a specific one-off date, for barbers overriding their schedule
    # for a single day (e.g. extra hours on a holiday, or a day off)
    specific_date = Column(Date, nullable=True)

    # Start and end of this free window — raw working hours,
    # NOT individual bookable slots. Slots get carved out of this
    # later by subtracting existing bookings and matching service duration.
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)

    # Lets a barber mark a specific_date as fully blocked/unavailable
    # (e.g. sick day, holiday) instead of deleting and recreating rows
    is_blocked = Column(Boolean, default=False)

    # Creates an easy Python-side link: availability.barber gives you the full Barber row
    barber = relationship("Barber", backref="availabilities")