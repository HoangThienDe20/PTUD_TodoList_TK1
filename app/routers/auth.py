from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.core.security import create_access_token, get_current_user, hash_password, verify_password
from app.db.session import get_session
from app.models.user import UserModel
from app.repositories.user_repository import user_repo
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse, UserOut

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, session: Session = Depends(get_session)) -> UserOut:
    existing = user_repo.get_by_email(session, payload.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = user_repo.create(
        session,
        email=payload.email,
        hashed_password=hash_password(payload.password),
    )
    return user


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, session: Session = Depends(get_session)) -> TokenResponse:
    user = user_repo.get_by_email(session, payload.email)
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="User is inactive")

    token = create_access_token(str(user.id))
    return TokenResponse(access_token=token)


@router.get("/me", response_model=UserOut)
def me(current_user: UserModel = Depends(get_current_user)) -> UserOut:
    return current_user
