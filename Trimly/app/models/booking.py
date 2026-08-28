# Import SQLAlchemy tools for database columns and linking tables
from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db.base import Base

# Define the blueprint for the 'bookings' table in the database
class Booking(Base):
    __tablename__ = "bookings"

    # Unique identifier for each appointment
    id = Column(Integer, primary_key=True, index=True)
    
    # Links to the User table to identify the client booking the service
    client_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Links to the User table to identify the barber/salon being booked
    barber_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Exact start and calculated end times for the appointment
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)  
    
    # Summed total cost of all services requested (used for the receipt)
    total_price = Column(Float, nullable=False)  

    # Relationships that allow the app to easily fetch client and barber details
    client = relationship("User", foreign_keys=[client_id])
    barber = relationship("User", foreign_keys=[barber_id], back_populates="bookings")