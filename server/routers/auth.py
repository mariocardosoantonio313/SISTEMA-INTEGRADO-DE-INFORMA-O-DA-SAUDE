from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from server.database import get_db
from server.models import User
from server.schemas import LoginRequest, LoginResponse
from server.security import verify_password

router = APIRouter(prefix="/api", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == payload.username).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Utilizador ou palavra-passe incorretos.")

    return LoginResponse(
        access_token="demo-token",
        token_type="bearer",
        username=user.username,
        profile=user.profile,
    )
