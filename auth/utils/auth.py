import datetime
from sqlalchemy.orm import Session
from sqlalchemy.orm import Session
from utils.hashing import Hash
from models import User
from schemas.token import Token
from utils.jwt_token import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token


def get_user(db: Session, email: str) -> User:
    return db.query(User).filter(User.email == email).first()


def authenticate_user(email: str, password: str, db: Session):
    user = get_user(db, email)
    if not user:
        return False
    if not Hash.verify_password(password, user.hashed_password):
        return False
    return user


def generate_token(email: str):
    access_token_expires = datetime.timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token)
