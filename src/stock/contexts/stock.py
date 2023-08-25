from sqlmodel import SQLModel, Field, DateTime
from typing import Optional
from datetime import datetime
from src.utils.templates import *

class StockBase(SQLModel):
    title: Optional[str]
    symbol: Optional[str]
    finite_signal: Optional[str]
    activate_at: Optional[datetime] = Field(None)

class StockReadable(Readable, StockBase):
    pass