# Import SQLAlchemy tools for defining columns and linking tables
from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.base import Base

# Defines the blueprint for portfolio pictures/videos uploaded by barbers
class PortfolioItem(Base):
    __tablename__ = "portfolio_items"

    # Unique identifier for each uploaded media item
    id = Column(Integer, primary_key=True, index=True)
    
    # Links the media to the specific barber or salon who uploaded it
    barber_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # The URL link to where the image/video is stored
    media_url = Column(String, nullable=False)
    
    # Specifies if the uploaded file is an 'image' or a 'video'
    media_type = Column(String, nullable=False)  
    
    # The name or title of the hairstyle shown in the picture/video
    hairstyle_name = Column(String, nullable=False, index=True)
    
    # Optional link so clients can book a service directly from tapping the picture
    linked_service_id = Column(Integer, ForeignKey("services.id"), nullable=True)

    # Relationships to easily fetch the barber who owns the portfolio and the bookable service
    barber = relationship("User", back_populates="portfolio_items")
    linked_service = relationship("Service")


# Defines the blueprint for client reviews and 5-star ratings
class Review(Base):
    __tablename__ = "reviews"

    # Unique identifier for each review
    id = Column(Integer, primary_key=True, index=True)
    
    # Links the review to the client who wrote it
    client_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Links the review to the barber who performed the service
    barber_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # The specific haircut or style that the client is rating
    hairstyle_name = Column(String, nullable=False, index=True)
    
    # The star rating given by the client (1 to 5)
    rating = Column(Integer, nullable=False)  
    
    # The written feedback/paragraph left by the client
    comment = Column(Text, nullable=True)

    # Relationship allowing the app to easily fetch the reviews belonging to a barber
    barber = relationship("User", foreign_keys=[barber_id], back_populates="reviews")