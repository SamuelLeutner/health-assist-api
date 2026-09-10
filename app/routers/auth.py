from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from app.database import get_db
from app.models.user import User
from app.schemas.auth import Token
from app.security.jwt import create_access_token, verify_password
from app.security.rate_limit import limiter

router = APIRouter(prefix="/auth", tags=["auth"])

AUTH_RATE_LIMIT = "5/minute"


@router.post("/token", response_model=Token)
@limiter.limit(AUTH_RATE_LIMIT)
def login_for_access_token(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.exec(select(User).where(User.username == form_data.username)).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.username})
    return Token(access_token=access_token, token_type="bearer")
