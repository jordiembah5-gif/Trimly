from pydantic import BaseModel
from typing import Optional

# 1. Base properties shared across all Barber schemas
class BarberBase(BaseModel):
    bio: Optional[str] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    # Here are your new fields!
    is_salon: bool = False
    capacity: int = 1

# 2. Properties required to create a new Barber profile
class BarberCreate(BarberBase):
    user_id: int

# 3. Properties allowed to be updated (like changing capacity later)
class BarberUpdate(BaseModel):
    bio: Optional[str] = None
    is_salon: Optional[bool] = None
    capacity: Optional[int] = None

# 4. What gets returned when viewing a barber's profile
class BarberRead(BarberBase):
    id: int
    user_id: int
    rating: float
    is_verified: bool

    class Config:
        from_attributes = True