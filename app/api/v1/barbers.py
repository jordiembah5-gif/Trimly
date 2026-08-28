# app/api/v1/barbers.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# Import our database dependency
from app.api.deps import get_db

# Import models and schemas
from app.models.user import User
from app.schemas.barber import BarberUpdate

router = APIRouter()


@router.patch("/{salon_id}/update-capacity")
def update_salon_capacity(salon_id: int, update_data: BarberUpdate, db: Session = Depends(get_db)):
    """
    Allows a salon to update how many active barbers/chairs they currently have.
    """
    # 1. Find the salon in the database — salons are User rows with role="salon"
    salon = db.query(User).filter(User.id == salon_id, User.role == "salon").first()

    if not salon:
        raise HTTPException(status_code=404, detail="Salon not found.")

    # 2. Update the chairs if a new number was provided
    if update_data.capacity is not None:
        if update_data.capacity < 1:
            raise HTTPException(status_code=400, detail="A salon must have at least 1 chair.")

        salon.capacity = update_data.capacity

    # 3. Save the changes to the database
    db.commit()
    db.refresh(salon)

    return {
        "message": "Salon capacity updated successfully.",
        "new_capacity": salon.capacity
    }