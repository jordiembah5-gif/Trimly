from sqlalchemy import Column, Integer, String, Float, Text
from sqlalchemy.orm import relationship
from app.db.base import Base  # Adjust if your import is different

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False)  # 'client', 'barber', 'salon'
    
    # --- NEW: Profile Upgrades ---
    logo_url = Column(String, nullable=True)
    about_us = Column(Text, nullable=True) 
    
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    capacity = Column(Integer, default=1, nullable=True)

    # --- NEW: Relationship to the Service model we just built ---
    # We use strings ("Service", "Booking", etc.) to prevent import errors
    services = relationship("Service", secondary="barber_services", back_populates="barbers")
    
    # Existing relationships (Keep these exactly as you had them!)
    portfolio_items = relationship("PortfolioItem", back_populates="barber", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="barber", cascade="all, delete-orphan")
    bookings = relationship("Booking", back_populates="barber", foreign_keys="[Booking.barber_id]")