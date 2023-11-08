import re
from src.utils.templates import *  # Предполагается, что у вас есть такой модуль
from playwright.async_api import async_playwright
from src.register import *
from logger import *

import asyncio
from random import randint


class NewsFactory:
    @staticmethod
    def create_news(sign, link_href, date_text, title_text, summary_text, publication_in, stock_id):
        cleared_content = re.sub('<[^<]+?>', "", sign)
        news = News(**NewsBase(
            sign=cleared_content,
            link_href=link_href,
            date_text=date_text,
            title_text=title_text,
            summary_text=summary_text,
            publication_in=publication_in,
            content_text=cleared_content
        ).dict(), stock_id=stock_id)
        logger.info(f"News created for stock_id {stock_id}: {title_text}")
        return news


class NewsDataProvider:
    BASE_TIMESPAN = 1
    LOGOUT_TIMESPAN = 4

    def __init__(self, stock_symbol: str = None, stock_id: int = None, activate_at: datetime = None):
        self.stock_symbol = stock_symbol
        self.stock_id = stock_id
        self.activate_at = activate_at

    async def fetch_news(self, page, browser, element):
        try:
            text = await element.inner_html()
            subject = "feed-item"
            link_element = await element.query_selector('a.%s__head' % subject)

            if not link_element:
                subject = "feed-item-big"
                link_element = await element.query_selector('a.%s__head' % subject)

            link_href = await link_element.get_attribute('href')
            date_text = await (await element.query_selector('.%s__date' % subject)).inner_text()

            date_trim = DateTrim(date_text)
            parsed_date = date_trim()
            if parsed_date <= self.activate_at:
                logger.info(
                    f"Time limit reached for collecting news for stock symbol {self.stock_symbol}. No more news will be collected after {self.activate_at}.")
                return None

            title_text = await (await element.query_selector('.%s__title' % subject)).inner_text()
            summary_text = await (await element.query_selector('.%s__summary' % subject)).inner_text()

            child_page = await browser.new_page()
            await asyncio.sleep(randint(self.BASE_TIMESPAN, self.LOGOUT_TIMESPAN))
            await child_page.goto(link_href)
            await child_page.wait_for_selector('div[data-id="publication-content"]')
            targeted_div_content = await child_page.inner_html('div[data-id="publication-content"]')

            await child_page.close()
            news = NewsFactory.create_news(
                sign=targeted_div_content,
                link_href=link_href,
                date_text=date_text,
                title_text=title_text,
                summary_text=summary_text,
                publication_in=parsed_date,
                stock_id=self.stock_id
            )
            return news
        except Exception as e:
            logger.exception(
                f"Error fetching news for stock symbol {self.stock_symbol}: {e}")
            return None

    async def run(self):
        try:
            async with async_playwright() as playwright:
                chromium = playwright.firefox
                browser = await chromium.launch()  # Use await here
                page = await browser.new_page()
                base_url = f"https://bcs-express.ru/category?tag={self.stock_symbol}"
                await page.goto(base_url)
                await page.wait_for_selector('.feed__list')
                child_elements = await page.query_selector_all('.feed__list > *')

                extracted_news = []
                for element in child_elements:
                    news = await self.fetch_news(page, browser, element)
                    if news:
                        extracted_news.append(news)
                    else:
                        break

                logger.info(
                    f"Extracted {len(extracted_news)} news items for stock symbol {self.stock_symbol}")
                return extracted_news
        except Exception as e:
            logger.exception(
                f"Error running news data provider for stock symbol {self.stock_symbol}: {e}")
            return []
