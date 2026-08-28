# app/schemas/availability.py
from pydantic import BaseModel
from datetime import time, date
from typing import Optional


class AvailabilityBase(BaseModel):
    day_of_week: Optional[int] = None  # 0=Monday ... 6=Sunday
    specific_date: Optional[date] = None
    start_time: time
    end_time: time
    is_blocked: bool = False


class AvailabilityCreate(AvailabilityBase):
    pass


class AvailabilityRead(AvailabilityBase):
    id: int
    barber_id: int

    class Config:
        from_attributes = True