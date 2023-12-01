


from sqlmodel import SQLModel, Field, DateTime
from typing import Optional
from datetime import datetime

class PublicationBase(SQLModel):
    title: Optional[str]
    description: Optional[str]

    prompt: Optional[str]
    incoming_content: Optional[str]
    outgoing_content: Optional[str]

    activate_at: Optional[datetime] = Field(None)