from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import create_access_token, decode_token, hash_password, verify_password
from app.models.entities import User

router = APIRouter(tags=["auth"])
_bearer = HTTPBearer(auto_error=False)


class RegisterIn(BaseModel):
    name: str
    email: EmailStr
    password: str


class LoginIn(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: str
    name: str
    email: str


def get_current_user(
    creds: HTTPAuthorizationCredentials | None = Depends(_bearer),
    db: Session = Depends(get_db),
) -> User:
    if not creds:
        raise HTTPException(status_code=401, detail="Not authenticated.")
    user_id = decode_token(creds.credentials)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid or expired token.")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found.")
    return user


def get_optional_user(
    creds: HTTPAuthorizationCredentials | None = Depends(_bearer),
    db: Session = Depends(get_db),
) -> User | None:
    if not creds:
        return None
    user_id = decode_token(creds.credentials)
    if not user_id:
        return None
    return db.query(User).filter(User.id == user_id).first()


@router.post("/auth/register", response_model=dict)
def register(data: RegisterIn, db: Session = Depends(get_db)):
    if len(data.password) < 8:
        raise HTTPException(status_code=422, detail="Password must be at least 8 characters.")
    if db.query(User).filter(User.email == data.email.lower()).first():
        raise HTTPException(status_code=400, detail="An account with this email already exists.")
    user = User(name=data.name.strip(), email=data.email.lower(), password_hash=hash_password(data.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"access_token": create_access_token(user.id), "token_type": "bearer",
            "user": {"id": user.id, "name": user.name, "email": user.email}}


@router.post("/auth/login", response_model=dict)
def login(data: LoginIn, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email.lower()).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password.")
    return {"access_token": create_access_token(user.id), "token_type": "bearer",
            "user": {"id": user.id, "name": user.name, "email": user.email}}


@router.get("/auth/me", response_model=UserOut)
def me(user: User = Depends(get_current_user)):
    return user
