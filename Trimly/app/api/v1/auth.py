# app/api/v1/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import timedelta
from jose import JWTError, jwt

# Import dependencies, security, and settings
from app.api.deps import get_db
from app.core.security import hash_password, verify_password, create_access_token
from app.core.config import settings

# Import models and schemas (adjust if your exact class names differ)
from app.models.user import User
from app.schemas.user import UserCreate, UserRead

router = APIRouter()

# Tells FastAPI where clients get their token from (this file's /login endpoint)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@router.post("/signup", response_model=UserRead)
def signup(user_in: UserCreate, db: Session = Depends(get_db)):
    # 1. Check if email already exists
    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
        raise HTTPException(status_code=400, detail="Email already registered.")

    # 2. Hash password and save new user
    hashed_pw = hash_password(user_in.password)
    new_user = User(
        email=user_in.email,
        hashed_password=hashed_pw,
        name=user_in.name,
        phone=user_in.phone,
        role=user_in.role,
        latitude=user_in.latitude,
        longitude=user_in.longitude,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login")
def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    # 1. Find user by email (OAuth2 uses 'username' for the email field)
    user = db.query(User).filter(User.email == form_data.username).first()

    # 2. Verify user exists and password is correct
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password.")

    # 3. Generate JWT access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:
    """
    Runs on every protected request. Decodes the JWT token sent by the client,
    verifies it, and returns the matching User row — or rejects the request
    if the token is missing, invalid, or expired.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception
    return user


@router.get("/me", response_model=UserRead)
def read_current_user(current_user: User = Depends(get_current_user)):
    """Lets the frontend silently check if a saved token is still valid on app launch."""
    return current_user