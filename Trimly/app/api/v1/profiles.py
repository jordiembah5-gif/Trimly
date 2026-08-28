from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from app.db.session import get_db

# Import the exact database models we just created
from app.models.user import User
from app.models.service import Service
from app.models.barber import PortfolioItem
from app.api.v1.auth import get_current_user

# Create the router so FastAPI knows these endpoints exist
router = APIRouter(prefix="/profiles", tags=["Barber & Salon Profiles"])

# --- SCHEMAS (Data validation for what the user sends) ---

# Validates data when a salon updates their profile
class ProfileUpdate(BaseModel):
    logo_url: Optional[str] = None
    about_us: Optional[str] = None

# Validates data when adding a haircut or skincare to the menu
class ServiceCreate(BaseModel):
    name: str
    category: str  # e.g., 'haircut' or 'skincare'
    duration_minutes: int
    price: float

# Validates data when uploading a picture or video to the portfolio
class PortfolioUpload(BaseModel):
    media_url: str
    media_type: str # e.g., 'image' or 'video'
    hairstyle_or_service_name: str 
    linked_service_id: Optional[int] = None


# --- ENDPOINTS (The actual actions the app performs) ---

@router.put("/update-details", status_code=200)
def update_shop_details(payload: ProfileUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Allows a logged-in salon or barber to update their bio and logo."""
    
    # Check if the user is a client (clients can't have a salon profile)
    if current_user.role not in ["barber", "salon"]:
        raise HTTPException(status_code=403, detail="Only salons or barbers can update profile details.")
    
    # Update the database if the user provided a new logo or bio
    if payload.logo_url is not None: 
        current_user.logo_url = payload.logo_url
    if payload.about_us is not None: 
        current_user.about_us = payload.about_us
        
    db.commit()
    return {"message": "Profile updated", "about_us": current_user.about_us}

@router.post("/services", status_code=201)
def add_specific_service(payload: ServiceCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Adds a new service (like a fade or facial) to the barber's menu."""
    
    if current_user.role not in ["barber", "salon"]:
        raise HTTPException(status_code=403, detail="Only salons or barbers can add services.")

    # Convert the category to lowercase so the database stays organized
    standardized_category = payload.category.strip().lower()
    
    # Create the new service in the database
    new_service = Service(
        name=payload.name, 
        category=standardized_category, 
        duration_minutes=payload.duration_minutes, 
        price=payload.price
    )
    
    db.add(new_service)
    # Link this new service to the current logged-in barber
    current_user.services.append(new_service)
    db.commit()
    
    return {"message": f"Added {standardized_category}: {payload.name}"}

@router.post("/portfolio", status_code=201)
def upload_portfolio_media(payload: PortfolioUpload, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Uploads a picture or video to the barber's portfolio grid."""
    
    if current_user.role not in ["barber", "salon"]:
        raise HTTPException(status_code=403, detail="Only salons or barbers can upload media.")

    # Create the new portfolio picture/video in the database
    new_item = PortfolioItem(
        barber_id=current_user.id, 
        media_url=payload.media_url, 
        media_type=payload.media_type,
        hairstyle_name=payload.hairstyle_or_service_name, 
        linked_service_id=payload.linked_service_id
    )
    
    db.add(new_item)
    db.commit()
    
    return {"message": f"Successfully uploaded {payload.media_type}."}