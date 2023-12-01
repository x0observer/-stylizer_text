from sqlmodel import SQLModel, Field, DateTime
from typing import Optional
from datetime import datetime
from src.utils.templates import Readable
from typing import List

from src.stock.contexts.stock import *
class ProfileStock(SQLModel):
    stock_id: Optional[int]
    profile_id: Optional[int]
    stock: Optional["StockReadable"]

class ProfileBase(SQLModel):
    title: Optional[str]
    description: Optional[str]
    activate_at: Optional[datetime] = Field(None)

class ProfileReadable(Readable, ProfileBase):
    pass

class ProfileFull(ProfileReadable):
    stocks: Optional[List["ProfileStock"]]
    pass