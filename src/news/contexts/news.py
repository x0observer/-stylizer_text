from sqlmodel import SQLModel, Field, DateTime
from typing import Optional
from datetime import datetime
from src.utils.templates import *
class NewsBase(SQLModel):
    link_href: Optional[str]
    date_text: Optional[str]
    title_text: Optional[str]
    summary_text: Optional[str]
    content_text: Optional[str]
    sign: Optional[str] = Field(unique=True)
    is_fresh: Optional[bool] = Field(True)
    publication_in: Optional[datetime]

class NewsReadable(Readable, NewsBase):
    pass

    