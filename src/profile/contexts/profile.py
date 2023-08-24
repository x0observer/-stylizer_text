from sqlmodel import SQLModel, Field, DateTime
from typing import Optional
from datetime import datetime

class ProfileBase(SQLModel):
    title: Optional[str]
    description: Optional[str]
    activate_at: Optional[datetime]