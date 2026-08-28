# app/models/__init__.py

# Importing every model here means one single import (of this file)
# gives Alembic and the rest of the app access to all your tables at once.

from app.models.user import User
from app.models.barber import Barber, PortfolioItem, Review
from app.models.service import Service, barber_services
from app.models.availability import Availability
from app.models.booking import Booking
from app.models.notification import Notification