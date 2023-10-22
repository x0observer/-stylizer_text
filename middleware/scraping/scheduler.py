from fastapi import FastAPI, BackgroundTasks, Depends
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from sqlalchemy.exc import IntegrityError

from fastapi import APIRouter, Depends, HTTPException
from engine import get_async_session
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.register import *
from engine import *
# Initialize the APScheduler
scheduler = AsyncIOScheduler()

router = APIRouter()

# Dependency to get the async database session

# Define a background task function to be scheduled


# async def background_task():
#     async with SessionLocal() as session:
#         try:
#             # Perform database operations here
#             new_metalogger = MetaLogger(message="__background_task__")
#             session.add(new_metalogger)
#             session.commit()
#             session.refresh(new_metalogger)
#             print("Database operation successful")
#         except Exception as e:
#             print(f"Database error: {str(e)}")

# Endpoint to schedule the background task


async def background_task():
    async with AsyncSessionLocal() as session:
        try:
            # Perform database operations here
            new_metalogger = MetaLogger(message="__background_task__")
            session.add(new_metalogger)
            await session.commit()
            await session.refresh(new_metalogger)
            print("Database operation successful")
        except Exception as e:
            print(f"Database error: {str(e)}")


# Schedule the background task to run every 1 minute
scheduler.add_job(background_task, "interval", minutes=1)


@router.post("/trigger_task/")
async def trigger_background_task(background_tasks: BackgroundTasks):
    # You can trigger the background task immediately by adding it to background_tasks
    background_tasks.add_task(background_task)
    return {"message": "Background task triggered"}
