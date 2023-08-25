from fastapi import APIRouter, Depends
from engine import get_async_session
from middleware.scraping.core import Mediator
from playwright.async_api import async_playwright

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.utils.templates import *
from src.profile.service import ProfileRepository

router = APIRouter()


@router.post("/scraping/{profile_id}")
async def execute(
    profile_id: int,
    db: AsyncSession = Depends(get_async_session),
):
    profile_repository = ProfileRepository(db=db)
    profile = await profile_repository.get_profile(profile_id)


    for profile_stock in profile.stocks:
        service = Mediator(stock=profile_stock.stock)
        extracted_news = await service()
        await insert_unique_objects(db=db, objects=extracted_news)



    return {"status": "success", "data": extracted_news}


@router.post("/scraping/test")
async def test(
    db: AsyncSession = Depends(get_async_session),
):

    return {"status": "success"}
    
