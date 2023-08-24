# # engine = create_async_engine(DATABASE_URL, echo=True, future=True)



# # async def get_session() -> AsyncSession:
# #     async_session = sessionmaker(
# #         engine, class_=AsyncSession, expire_on_commit=False
# #     )
# #     async with async_session() as session:
# #         yield sessionfrom sqlalchemy import create_engine

from setup import settings
# from fastapi import FastAPI, Depends
# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
# from datetime import datetime
# from typing import List, Optional
# from sqlalchemy import Column, Integer, String, DateTime
# from sqlalchemy.orm import declarative_base, sessionmaker
# from sqlalchemy.future import select
# from sqlmodel import SQLModel


# SQLALCHEMY_DATABASE_URL = settings["db"]["uri"]
# engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True)

# # Create an AsyncSession
# async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


# async def init_db():
#     async with engine.begin() as connection:
#         # await conn.run_sync(SQLModel.metadata.drop_all)
#         await connection.run_sync(SQLModel.metadata.create_all)



# async def get_async_session() -> AsyncSession:
#     async with async_session() as session:
#         yield session


from sqlmodel import SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession, AsyncEngine

from sqlalchemy.orm import sessionmaker


POSTGRESQL_ASYNC_DATABASE_URL = settings["db"]["uri"]

engine = AsyncEngine(create_engine(POSTGRESQL_ASYNC_DATABASE_URL, echo=True, future=True))

async def init_db():
    async with engine.begin() as connection:
        # await connection.run_sync(SQLModel.metadata.drop_all)
        await connection.run_sync(SQLModel.metadata.create_all)


async def get_async_session() -> AsyncSession:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session