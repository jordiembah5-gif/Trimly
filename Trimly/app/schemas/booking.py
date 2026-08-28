from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class ServiceResponse(BaseModel):
    id: int
    name: str
    duration_minutes: int
    price: float

    class Config:
        orm_mode = True

class PortfolioImageResponse(BaseModel):
    id: int
    image_url: str
    hairstyle_name: str

    class Config:
        orm_mode = True

class BarberProfileResponse(BaseModel):
    id: int
    email: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    services: List[ServiceResponse] = []
    portfolio_images: List[PortfolioImageResponse] = []
    average_rating: Optional[float] = None

    class Config:
        orm_mode = True

class BookingCreate(BaseModel):
    barber_id: int
    service_ids: List[int]
    start_time: datetime

class PortfolioUploadCreate(BaseModel):
    image_url: str
    hairstyle_name: str

class ReviewCreate(BaseModel):
    barber_id: int
    hairstyle_name: Optional[str] = None
    rating: int  # 1 to 5
    comment: Optional[str] = None