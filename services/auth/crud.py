# services/auth/crud.py
from sqlalchemy.orm import Session
from .models import User
from . import schemas
from .utils.password import get_password_hash, verify_password
from .utils.jwt import create_access_token

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user_in: schemas.UserCreate):
    hashed = get_password_hash(user_in.password)
    user = User(email=user_in.email, hashed_password=hashed, is_active=True)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user