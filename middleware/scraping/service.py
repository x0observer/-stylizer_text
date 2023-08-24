from fastapi import APIRouter, Depends
from engine import get_session, Session
from middleware.scraping.core import Mediator
from playwright.async_api import async_playwright

router = APIRouter()


@router.post("/scraping")
async def execute(
    db: Session = Depends(get_session),
):
    service = Mediator()
    extracted_news = await service()
    return {"status": "success", "data": extracted_news}


@router.post("/scraping/hello")
async def test(
    db: Session = Depends(get_session),
):
    async with async_playwright() as playwright:
        print("__async_playwright__")
        browser = await playwright.chromium.launch()
        page = await browser.new_page()
        await page.goto("http://playwright.dev")
        print(await page.title())
        await browser.close()
        return {"status": 200}
    
