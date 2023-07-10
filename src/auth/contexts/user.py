from sqlmodel import SQLModel, Field, Column, Integer
from typing import Optional
from src.utils.templates import Readable
from typing import List



class UserBase(SQLModel):
    username: str = Field(max_length=255, unique=True)
    email: str = Field(max_length=255, unique=True)
    password_hash: str = Field(max_length=255)


class UserCreate(SQLModel):
    username: str = Field(max_length=255, unique=True)
    email: str = Field(max_length=255, unique=True)
    password: str = Field(max_length=255)
    

class UserPublic(Readable, UserBase):
    pass
