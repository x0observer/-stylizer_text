from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from src.auth.contexts.auth import AuthUser
from src.auth.contexts.user import UserCreate, UserUniformPublic
from src.auth.v2.auth import AuthRepository, get_auth_repository  # Import the AuthRepository class
from src.auth.v2.auth import api_key_header

router = APIRouter(tags=["Authentication(Repository)"])


@router.post("/login")
async def login(auth_user: AuthUser, repository: AuthRepository = Depends(get_auth_repository)):
    """
    Authenticate a user and generate an access token.

    Args:
        auth_user (AuthUser): User authentication data.
        repository (AuthRepository): Repository for handling authentication.

    Returns:
        dict: A dictionary containing an access token.
    """
    db_user = await repository.authenticate_user(auth_user.username, auth_user.password)
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    access_token = await repository.create_access_token(db_user.email)
    return {"access_token": access_token}

@router.post("/register")
async def register(user: UserCreate, repository: AuthRepository = Depends(get_auth_repository)):
    """
    Register a new user.

    Args:
        user (UserCreate): User registration data.
        repository (AuthRepository): Repository for user registration.

    Returns:
        UserUniformPublic: Information about the registered user.
    """
    return await repository.register_user(user)

@router.post("/self")
async def get_self(repository: AuthRepository = Depends(get_auth_repository), api_key: str = Security(api_key_header)):
    """
    Get information about the authenticated user.

    Args:
        repository (AuthRepository): Repository for retrieving user information.

    Returns:
        UserUniformPublic: Information about the authenticated user.
    """
    return await repository.get_active_user()