from fastapi import APIRouter, Depends
from engine import get_async_session
from middleware.scraping.core import Mediator
from playwright.async_api import async_playwright

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession


router = APIRouter()


@router.post("/scraping")
async def execute(
    db: AsyncSession = Depends(get_async_session),
):
    service = Mediator()
    extracted_news = await service()
    return {"status": "success", "data": extracted_news}


@router.post("/scraping/test")
async def test(
    db: AsyncSession = Depends(get_async_session),
):

    return {"status": "success"}
    
