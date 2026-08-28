# app/schemas/service.py
from pydantic import BaseModel
from decimal import Decimal
from typing import Optional


class ServiceBase(BaseModel):
    name: str
    photo_url: Optional[str] = None
    duration_minutes: int
    price: Decimal
    is_specialty: bool = False


class ServiceCreate(ServiceBase):
    pass


class ServiceRead(ServiceBase):
    id: int
    barber_id: int

    class Config:
        from_attributes = True