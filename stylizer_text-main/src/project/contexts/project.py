from sqlmodel import SQLModel, Field, DateTime
from typing import Optional
from datetime import datetime

class ProjectBase(SQLModel):
    title: Optional[str]
    default_prompt: Optional[str] 
    activate_at: Optional[datetime]
    