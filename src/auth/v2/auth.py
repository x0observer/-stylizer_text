from fastapi import HTTPException, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from pydantic import BaseModel

from fastapi.security.api_key import APIKeyHeader
from fastapi_jwt_auth import AuthJWT
from passlib.context import CryptContext
from datetime import timedelta
from src.register import User
from src.auth.contexts.auth import AuthUser
from src.auth.contexts.user import UserCreate, UserUniformPublic

from src.utils.templates import *
from engine import get_async_session

# Set the access token expiration time (in minutes) here
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
api_key_header = APIKeyHeader(
    name='Authorization', description="Bearer <<access_token>>")






class Settings(BaseModel):
    authjwt_secret_key: str = "SECRET_KEY"

# callback to get your configuration


@AuthJWT.load_config
def get_config():
    return Settings()


class AuthRepository:
    def __init__(self, db: AsyncSession, auth: AuthJWT):
        self.db = db
        self.auth = auth

    async def authenticate_user(self, username: str, password: str):
        query = select(User).where(User.username == username)
        execute = await self.db.execute(query)
        user = execute.scalars().one_or_none()

        if not user or not pwd_context.verify(password, user.password_hash):
            return None
        return user

    async def create_access_token(self, user_email: str):
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        return self.auth.create_access_token(subject=user_email, expires_time=access_token_expires)

    async def register_user(self, user: UserCreate):
        db_user = User(
            username=user.username,
            email=user.email,
            password_hash=pwd_context.hash(user.password)
        )
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user

    async def get_user_by_email(self, email: str):
        query = select(User).where(User.email == email)
        execute = await self.db.execute(query)
        user = execute.scalars().one_or_none()
        return user

    async def get_active_user(self, ):
        jwt_subject = self.auth.get_jwt_subject()
        db_user = await self.get_user_by_email(jwt_subject)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        return db_user


def get_auth_repository(db: AsyncSession = Depends(get_async_session), auth: AuthJWT = Depends()) -> AuthRepository:
    return AuthRepository(db, auth)
