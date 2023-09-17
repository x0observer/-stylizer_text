from fastapi import APIRouter, Depends
from engine import get_async_session
from middleware.scraping.core import Mediator
from playwright.async_api import async_playwright

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.utils.templates import *
from src.profile.service import ProfileRepository
from src.register import *
from datetime import datetime

from src.utils.extensions.openai import *
import random
router = APIRouter()


@router.post("/execute/{project_id}")
async def execute(
    project_id: int,
    datetime: datetime,
    limit: int,
    prompt: str = "\n\nTranslate the above financial news into a simple JSON format: ",
    db: AsyncSession = Depends(get_async_session),
):
    
    query = select(News).join(Stock, News.stock_id == Stock.id).join(StockToProfile, Stock.id == StockToProfile.stock_id).where(StockToProfile.profile_id == project_id).where(News.publication_in > datetime)
    execute = await db.execute(query)
    news = execute.scalars().all()
    
    print("news:", news)
    print("__news__")
    random.shuffle(news)
    selected_news = [news.content_text for news in news][:-limit]
    
    incoming_content = prompt + ' '.join(selected_news)[:1024]
    return {"status": "success", "data" : OpenAIService.generate_response_by_prompt(prompt=incoming_content, openai_key="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")}