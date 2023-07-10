from fastapi import FastAPI, Depends, HTTPException, APIRouter
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime, timedelta
from src.auth.contexts.auth import AuthUser
from src.auth.contexts.user import ActiveUser
from engine import get_db, get_session
from setup import settings
from src.auth.contexts.user import UserCreate, UserUniformPublic
from register import User
import json

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi_jwt_auth.exceptions import AuthJWTException
from pydantic import BaseModel


ACCESS_TOKEN_EXPIRE_MINUTES = settings["auth"]["access_token_expire_minutes"]
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(tags=["Authorization"])


class Settings(BaseModel):
    authjwt_secret_key: str = settings["auth"]["secret_key"]

# callback to get your configuration


@AuthJWT.load_config
def get_config():
    return Settings()


async def authenticate_user(username: str, password: str, db: Session):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not pwd_context.verify(password, user.password_hash):
        return False
    return user


@router.post("/login")
async def login(auth_user: AuthUser, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    user = authenticate_user(auth_user.username, auth_user.password, db)
    if not user:
        raise HTTPException(
            status_code=401, detail="Invalid username or password")
    print("ACCESS_TOKEN_EXPIRE_MINUTES: ", ACCESS_TOKEN_EXPIRE_MINUTES)

    active_user = ActiveUser.from_orm(user)
    access_token_expires = timedelta(minutes=30)
    access_token = Authorize.create_access_token(
        subject=active_user.email, expires_time=False
    )
    return {"access_token": access_token}


@router.post("/register")
async def register(user: UserCreate, db: Session = Depends(get_session)):
    db_user = User(
        username=user.username,
        email=user.email,
        password_hash=pwd_context.hash(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


async def get_active_user(db: Session = Depends(get_session),  Authorize: AuthJWT = Depends()):
    jwt_subject = Authorize.get_jwt_subject()
    print("jwt_subject: ", jwt_subject)
    db_user = db.query(User).filter(User.email == jwt_subject).first()
    if not db_user:
        return False

    return ActiveUser.from_orm(db_user)


@router.post("/self")
async def get_self(db: Session = Depends(get_session),  Authorize: AuthJWT = Depends()):
    return get_active_user(db=db, Authorize=Authorize)
