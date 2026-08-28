from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.db.base import Base  # Make sure this matches your base import (e.g., app.db.base or app.db.base_class)

# This table acts as a bridge, linking Barbers/Salons to the specific services they offer
barber_services = Table(
    "barber_services",
    Base.metadata,
    Column("barber_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("service_id", Integer, ForeignKey("services.id"), primary_key=True)
)

class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    
    # Category is crucial! It tells the app if this is a "haircut" or "skincare"
    category = Column(String, nullable=False, index=True) 
    
    duration_minutes = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)

    # Links back to the users (barbers) who offer this service
    barbers = relationship("User", secondary=barber_services, back_populates="services")