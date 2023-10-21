from fastapi import APIRouter, Depends
from engine import get_async_session
from middleware.scraping.core import Mediator
from playwright.async_api import async_playwright

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.utils.templates import *
from src.profile.service import ProfileRepository

router = APIRouter()

import asyncio


@router.post("/scraping/{profile_id}")
async def execute(
    profile_id: int,
    db: AsyncSession = Depends(get_async_session),
):
    profile_repository = ProfileRepository(db=db)
    stocks = await profile_repository.get_profile_stocks(profile_id)
    print("__profile_stocks__")
    print(stocks)

    for stock in stocks:
        print("__stock_iter__")
        print("__stock_obj__", stock)
        service = Mediator(stock.symbol, stock.id, stock.activate_at)
        
        try:
            extracted_news = await service()
            unique_news = await insert_unique_objects(db=db, objects=extracted_news)

            stock.activate_at = datetime.now()
            await db.commit()
            await db.refresh(stock)

        except IntegrityError as e:
            await db.rollback()  # Rollback the transaction if there's an IntegrityError
            print(f"IntegrityError for stock {stock.id}: {str(e)}")
        except Exception as e:
            await db.rollback()  # Rollback for other exceptions
            print(f"Error for stock {stock.id}: {str(e)}")

    return {"status": "success", "extracted_news": extracted_news, "unique_news": unique_news}

@router.post("/scraping/test")
async def test(
    db: AsyncSession = Depends(get_async_session),
):

    return {"status": "success"}


import asyncio
from fastapi import FastAPI, BackgroundTasks



# Define a background task function
async def activate_scraping():

    profile_repository = ProfileRepository(db=get_async_session())
    profiles = await profile_repository.get_profiles()


    for profile in profiles:
        for profile_stock in profile.stocks:
            service = Mediator(stock=profile_stock.stock)
            extracted_news = await service()
            await insert_unique_objects(db=get_async_session(), objects=extracted_news)


    # Simulate sending an email (replace with your actual email sending code)
    await asyncio.sleep(1800)  # Sleep for 30 minutes (1800 seconds)
    print(f"Activate scraping")

# Define a route that uses BackgroundTasks
@router.post("/activate_scraping/")
async def send_activate_scraping(background_tasks: BackgroundTasks):
    # Add the task to the background queue
    background_tasks.add_task(activate_scraping)
    return {"message": "Scraping will be activate in 30 minutes."}
    
