
from src.news.contexts.news import *
from src.profile.contexts.profile import *
from src.stock.contexts.stock import *
from src.project.contexts.project import *


from sqlmodel import SQLModel, Field, Relationship, Field
from typing import List, Optional
from datetime import datetime


class News(NewsBase, table=True):
    __tablename__ = "news"
    __table_args__ = {'extend_existing': True}
    id: Optional[int] = Field(default=None, primary_key=True)
    stock_id: Optional[int] = Field(default=None, foreign_key="stocks.id")
    stock: Optional["Stock"] = Relationship(
        back_populates="news")

    hash_value: Optional[int]
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)




class Stock(StockBase, table=True):
    __tablename__ = "stocks"
    __table_args__ = {'extend_existing': True}
    id: Optional[int] = Field(default=None, primary_key=True)
    news: Optional[List["News"]] = Relationship(back_populates="stock")

    profiles: List["StockToProfile"] = Relationship(back_populates="stock")
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)


class Profile(ProfileBase, table=True):
    __tablename__ = "profiles"
    __table_args__ = {'extend_existing': True}
    id: Optional[int] = Field(default=None, primary_key=True)

    stocks: List["StockToProfile"] = Relationship(back_populates="profile")
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)


class StockToProfile(SQLModel, table=True):
    __tablename__ = "stocktoprofile"
    __table_args__ = {'extend_existing': True}

    stock_id: Optional[int] = Field(
        default=None, foreign_key="stocks.id", primary_key=True
    )

    profile_id: Optional[int] = Field(
        default=None, foreign_key="profiles.id", primary_key=True
    )

    stock: "Stock" = Relationship(back_populates="profiles")
    profile: "Profile" = Relationship(back_populates="stocks")

    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

class Project(ProjectBase, table=True):
    __tablename__ = "project"
    __table_args__ = {'extend_existing': True}
    id: Optional[int] = Field(default=None, primary_key=True)
