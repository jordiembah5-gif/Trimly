# app/api/v1/bookings.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, timedelta

from app.db.session import get_db

# Import the specific, separated models for the booking logic
from app.models.user import User
from app.models.service import Service
from app.models.barber import PortfolioItem
from app.models.booking import Booking
from app.api.v1.auth import get_current_user

# Create the router so FastAPI knows these booking endpoints exist
router = APIRouter(prefix="/bookings", tags=["Advanced Bookings & History"])

# --- SCHEMAS ---

# Validates the data sent when a client books an appointment
class AdvancedBookingCreate(BaseModel):
    barber_id: int
    start_time: datetime
    service_ids: Optional[List[int]] = []
    portfolio_item_id: Optional[int] = None
    custom_hairstyle_name: Optional[str] = None


# --- ENDPOINTS ---

@router.post("/", status_code=201)
def create_comprehensive_booking(
    payload: AdvancedBookingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Creates a booking, enforces the 1-haircut rule, and generates a receipt."""

    # Verify the barber actually exists
    barber = db.query(User).filter(User.id == payload.barber_id).first()
    if not barber:
        raise HTTPException(status_code=404, detail="Barber or salon not found.")

    # Tracking variables for the receipt and rules
    total_duration_minutes = 0
    total_price = 0.0
    receipt_breakdown = []
    haircut_count = 0

    # 1. Process standard menu selections
    if payload.service_ids:
        services = db.query(Service).filter(Service.id.in_(payload.service_ids)).all()
        for svc in services:
            if svc.category.lower() == "haircut":
                haircut_count += 1
            total_duration_minutes += svc.duration_minutes
            total_price += svc.price
            receipt_breakdown.append({
                "item": f"{svc.category.capitalize()}: {svc.name}",
                "price": svc.price,
                "duration": svc.duration_minutes,
            })

    # 2. Process booking from a portfolio picture
    if payload.portfolio_item_id:
        item = db.query(PortfolioItem).filter(PortfolioItem.id == payload.portfolio_item_id).first()
        if item and item.linked_service_id:
            linked_svc = db.query(Service).filter(Service.id == item.linked_service_id).first()
            if linked_svc:
                if linked_svc.category.lower() == "haircut":
                    haircut_count += 1
                total_duration_minutes += linked_svc.duration_minutes
                total_price += linked_svc.price
                receipt_breakdown.append({
                    "item": f"Portfolio Ref: {item.hairstyle_name}",
                    "price": linked_svc.price,
                    "duration": linked_svc.duration_minutes,
                })

    # 3. ENFORCE RULE: Block more than 1 haircut per appointment
    if haircut_count > 1:
        raise HTTPException(status_code=400, detail="Only one haircut per appointment.")

    # 4. Process custom text requests
    if payload.custom_hairstyle_name:
        if haircut_count >= 1:
            raise HTTPException(status_code=400, detail="Cannot add a custom haircut alongside an existing one.")
        total_duration_minutes += 60
        total_price += 25.0
        receipt_breakdown.append({
            "item": f"Custom: {payload.custom_hairstyle_name}",
            "price": 25.0,"duration": 60,
            })

        # Prevent empty bookings
        if total_duration_minutes == 0:
            raise HTTPException(status_code=400, detail="Select at least one service.")

        # Calculate exact schedule timeline
        end_time = payload.start_time + timedelta(minutes=total_duration_minutes)

        # Save the new booking to the database
        new_booking = Booking(
            client_id=current_user.id,
            barber_id=payload.barber_id,
            start_time=payload.start_time,
            end_time=end_time,
            total_price=total_price,
        )
        db.add(new_booking)
        db.commit()
        db.refresh(new_booking)

        # Return the detailed receipt to the app
        return {
            "status": "success",
            "booking_id": new_booking.id,
            "receipt": receipt_breakdown,
            "totals": {"price": total_price, "duration": total_duration_minutes},
        }


@router.get("/history", status_code=200)
def get_client_booking_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieves a client's past booking history and total amounts paid."""

    if current_user.role != "client":
        raise HTTPException(status_code=403, detail="Only clients can view history here.")

    # Query database for bookings where the end time has already passed
    past_bookings = (
        db.query(Booking)
        .filter(Booking.client_id == current_user.id, Booking.end_time < datetime.now())
        .order_by(Booking.start_time.desc())
        .all()
    )

    # Format the data cleanly for the app UI
    history_data = []
    for booking in past_bookings:
        barber = db.query(User).filter(User.id == booking.barber_id).first()
        history_data.append({
            "booking_id": booking.id,
            "date": booking.start_time.strftime("%B %d, %Y"),
            "total_paid": booking.total_price,
            "barber_shop_name": barber.email if barber else "Unknown Shop",
        })

    return {"status": "success", "history": history_data}