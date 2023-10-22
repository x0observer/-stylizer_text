from sqlmodel import SQLModel, Field, Column, Integer
from typing import Optional
from src.utils.templates import Readable
from typing import List

class MetaLoggerBase(SQLModel):
    message : Optional[str] 

