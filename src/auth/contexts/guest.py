from sqlmodel import SQLModel, Field, Column, Integer
from typing import Optional
from src.utils.templates import Readable
from typing import List



class GuestBase(SQLModel):
    username: str = Field(max_length=255, unique=True, index=True)
    email: str = Field(max_length=255, unique=True)
    password_hash: str = Field(max_length=255)


class GuestCreate(SQLModel):
    external_id: int = Field(max_length=255, unique=True, index=True)
    username: str = Field(max_length=255, unique=True)
    

class GuestPublic(Readable, GuestBase):
    pass
