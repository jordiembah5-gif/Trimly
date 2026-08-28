from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User

router = APIRouter(prefix="/location", tags=["Location & Mapping"])

@router.get("/nearby-barbers")
def get_nearby_barbers(
    lat: float = Query(..., description="Customer latitude"),
    lon: float = Query(..., description="Customer longitude"),
    radius_km: float = Query(10.0, description="Search radius in kilometers"),
    db: Session = Depends(get_db)
):
    """
    Finds barbers within a specified radius using latitude and longitude.
    """
    # Fetch all users whose role is 'barber' (adjust model filter based on your role field setup)
    barbers = db.query(User).filter(User.role == "barber").all()
    
    nearby = []
    for barber in barbers:
        # Simple placeholder for distance calculation or direct return of coordinates for mapping apps
        if barber.latitude is not None and barber.longitude is not None:
            # You can feed these coordinates directly into Google Maps or any routing tool
            nearby.append({
                "id": barber.id,
                "name": barber.name,
                "phone": barber.phone,
                "latitude": barber.latitude,
                "longitude": barber.longitude
            })
            
    return {
        "search_center": {"latitude": lat, "longitude": lon},
        "radius_km": radius_km,
        "barbers_found": nearby
    }