from sqlmodel import SQLModel, Field, DateTime
from typing import Optional
from datetime import datetime
from src.utils.templates import *
from src.news.contexts.news import NewsReadable
from src.utils.templates import desired_datetime
class StockBase(SQLModel):
    title: Optional[str]
    symbol: Optional[str]
    finite_signal: Optional[str]
    activate_at: Optional[datetime] = desired_datetime

class StockCreate(SQLModel):
    title: Optional[str]
    symbol: Optional[str]
    finite_signal: Optional[str]

class StockReadable(Readable, StockBase):
    pass

class StockFull(StockReadable):
    news: Optional[List["NewsReadable"]]