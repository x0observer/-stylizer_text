from fastapi import APIRouter, Depends
from engine import get_async_session
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


# @router.post("/execute/{project_id}")
# async def execute(
#     stock_id: int,
#     datetime: datetime,
#     prompt: str = "\n\nTranslate the above financial news into a simple JSON format: ",
#     db: AsyncSession = Depends(get_async_session),
# ):

#     query = select(News).join(Stock, News.stock_id == stock_id).where(
#         News.publication_in > datetime)
#     execute = await db.execute(query)
#     news = execute.scalars().all()
#     if not news:
#         return {"status": "failed", "data": []}
#     # print("news:", news)
#     print("__news__")
#     # random.shuffle(news)
#     selected_news = [news.content_text for news in news]
#     print("selected_news:", selected_news)
#     incoming_content = prompt + \
#         ' '.join(selected_news)[:(1024+512)-len(prompt)]
#     print("selected_news:", incoming_content)
#     return {"status": "success", "data": OpenAIService.generate_response_by_prompt(prompt=incoming_content, openai_key="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")}


@router.post("/prompt/{stock_id}")
async def execute(
    stock_id: int,
    datetime: datetime,
    prompt: str = " дан список новостей по акции. Ты финасовый аналитик, сделай умозаключение по каждой новости. Добавь шутки и смайлики, донести информацию в легком формате, оставь важные показатели: ",
    db: AsyncSession = Depends(get_async_session),
):
    query = select(Stock).where(Stock.id == stock_id)
    execute = await db.execute(query)
    stock = execute.scalars().one_or_none()
    if not stock:
        return {"status": "failed", "data": []}

    finite_prompt = stock.title + " " + prompt

    query = select(News).join(Stock, News.stock_id == stock_id).where(
        News.publication_in > datetime)
    execute = await db.execute(query)
    news = execute.scalars().all()
    if not news:
        return {"status": "failed", "data": []}

    max_tokens_limit = 2049
    total_length = len(finite_prompt)
    summarized_news = ""

    if total_length < max_tokens_limit:
        current_length = len(finite_prompt)
        for obj in news:
            local_prompt_by_news = " - " + obj.date_original_text + \
                " - " + obj.summary_text + " - " + obj.processed_news + ";"

            print("__local_prompt_by_news__", len(local_prompt_by_news))
            print("__condition_local_prompt_by_news__", current_length +
                  len(local_prompt_by_news) + 1 <= max_tokens_limit)
            if current_length + len(local_prompt_by_news) + 1 <= max_tokens_limit:
                summarized_news += local_prompt_by_news
                current_length += len(local_prompt_by_news) + 1
            else:
                break

    finite_prompt += summarized_news

    return {"status": "success", "finite_prompt": finite_prompt, "length": len(finite_prompt), "updated_content": OpenAIService.generate_response_by_prompt(prompt=finite_prompt, )}
