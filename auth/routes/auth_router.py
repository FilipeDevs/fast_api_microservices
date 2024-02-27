from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from db.config import get_db
from utils.auth import authenticate_user, generate_token
from sqlalchemy.orm import Session
from schemas.token import Token

auth_router = APIRouter()


@auth_router.post("/login", response_model=Token)
async def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db())):
    user = authenticate_user(request.username, request.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = generate_token(user.email)
    return token
