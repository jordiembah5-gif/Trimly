from typing import Generator
from app.db.session import SessionLocal

def get_db() -> Generator:
    # Opens a database connection for a single API request
    db = SessionLocal()
    try:
        yield db
    finally:
        # Closes the connection when the request is done
        db.close()