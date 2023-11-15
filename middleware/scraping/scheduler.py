from fastapi import FastAPI, BackgroundTasks, Depends
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from sqlalchemy.exc import IntegrityError

from fastapi import APIRouter, Depends, HTTPException
from engine import get_async_session
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.register import *
from src.utils.templates import *
from middleware.scraping.core import Mediator
from engine import *


from src.stock.service import StockRepository

# Initialize the APScheduler
# scheduler = AsyncIOScheduler()
router = APIRouter()

# Dependency to get the async database session

# Define a background task function to be scheduled


# async def scraping_scheduler():
#     async with AsyncSessionLocal() as session:
#         try:
#             # Perform database operations here
#             stock_repository = StockRepository(db=session)
#             stocks = await stock_repository.get_stocks()
#             print("__profile_stocks__")
#             print(stocks)

#             for stock in stocks:
#                 print("__stock_iter__")
#                 print("__stock_obj__", stock)
#                 service = Mediator(stock.symbol, stock.id, stock.activate_at)

#                 try:
#                     extracted_news = await service()
#                     unique_news = await insert_unique_objects(db=session, objects=extracted_news)

#                     stock.activate_at = datetime.now()
#                     await session.commit()
#                     await session.refresh(stock)

#                 except IntegrityError as e:
#                     await session.rollback()  # Rollback the transaction if there's an IntegrityError
#                     print(f"IntegrityError for stock {stock.id}: {str(e)}")
#                 except Exception as e:
#                     await session.rollback()  # Rollback for other exceptions
#                     print(f"Error for stock {stock.id}: {str(e)}")

#         except Exception as e:
#             print(f"Database error: {str(e)}")


# # Schedule the background task to run every 1 minute
# scheduler.add_job(scraping_scheduler, "interval", minutes=360)


# @router.post("/scraping_scheduler_task/")
# async def scraping_scheduler_task(background_tasks: BackgroundTasks):
#     # You can trigger the background task immediately by adding it to background_tasks
#     background_tasks.add_task(scraping_scheduler)
#     return {"message": "Background task triggered"}
