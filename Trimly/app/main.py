from fastapi import FastAPI
from app.api.v1 import auth, barbers, bookings
from app.api.v1 import auth, barbers, bookings, location

# Initialize the FastAPI application
app = FastAPI(title="Trimly API", version="1.0.0", description="Barber & Salon Booking System")

# Connect all the routes we built in the api/v1 folder
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(barbers.router, prefix="/api/v1/barbers", tags=["Barbers & Salons"])
app.include_router(bookings.router, prefix="/api/v1/bookings", tags=["Bookings"])
app.include_router(location.router, prefix="/api/v1")

# A simple test route to ensure the server is running
@app.get("/")
def read_root():
    return {"status": "success", "message": "Welcome to the Trimly API"}