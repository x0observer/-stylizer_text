from sqlmodel import SQLModel, Field, DateTime
from typing import Optional
from datetime import datetime

class StockBase(SQLModel):
    title: Optional[str]
    symbol: Optional[str]
    activate_at: Optional[datetime]

