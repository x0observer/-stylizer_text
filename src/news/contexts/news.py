from sqlmodel import SQLModel, Field, DateTime
from typing import Optional
from datetime import datetime

class NewsBase(SQLModel):
    link_href: Optional[str]
    date_text: Optional[str]
    title_text: Optional[str]
    summary_text: Optional[str]
    publication_in: Optional[datetime]



    