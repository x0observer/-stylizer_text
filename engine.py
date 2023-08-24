# engine = create_async_engine(DATABASE_URL, echo=True, future=True)


# async def init_db():
#     async with engine.begin() as conn:
#         # await conn.run_sync(SQLModel.metadata.drop_all)
#         await conn.run_sync(SQLModel.metadata.create_all)


# async def get_session() -> AsyncSession:
#     async_session = sessionmaker(
#         engine, class_=AsyncSession, expire_on_commit=False
#     )
#     async with async_session() as session:
#         yield sessionfrom sqlalchemy import create_engine

from setup import settings
from sqlmodel import Session, create_engine, SQLModel


SQLALCHEMY_DATABASE_URL = settings["db"]["uri"]
engine = create_engine(SQLALCHEMY_DATABASE_URL)


def get_session():
    with Session(engine) as session:
        yield session
