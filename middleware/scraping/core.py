from middleware.scraping.core import *
import random
from playwright.sync_api import sync_playwright
from playwright.async_api import async_playwright
import time
from random import randint
from bs4 import BeautifulSoup

from src.register import *
from src.news.contexts.news import NewsBase
from src.utils.templates import *
import asyncio


import re


def sorting_by_publication_date(obj):
    return obj.publication_in


class Mediator:
    BASE_TIMESPAN = 1
    LOGOUT_TIMESPAN = 4

    def __init__(self, stock_symbol: str = None, stock_id: int = None, activate_at: datetime = None):
        # TODO: SETTING APPLY
        self.stock_symbol = stock_symbol
        self.stock_id = stock_id
        self.activate_at = activate_at

    async def run(self, playwright, base_timespan=BASE_TIMESPAN, logout_timespan=LOGOUT_TIMESPAN, source_url: str = "https://bcs-express.ru", subquery_span="/category", query_span: str = "/category?tag=/{/}", trim="/{/}", extracted_news: News = []):
        
        query_symbol = self.stock_symbol

        print("__chromium_launch__")
        chromium = playwright.firefox
        browser = await chromium.launch()  # Use await here
        page = await browser.new_page()
        base_url = source_url + \
            query_span.replace(
                trim, query_symbol) if query_symbol else source_url + subquery_span
        print("source:", base_url)
        await page.goto(base_url)  # Use await here
        print("__page_goto__")
        # await asyncio.sleep(randint(base_timespan, logout_timespan))  # Use asyncio.sleep for asynchronous sleeping

        # print("text:",await page.content())
        await asyncio.sleep(randint(base_timespan, logout_timespan))
        # Wait for the div element to be present
        await page.wait_for_selector('.feed__list')

        # Extract all child elements of the div
        child_elements = await page.query_selector_all('.feed__list > *')

        # Process and use the extracted data as needed
        random.shuffle(child_elements)
        print("__childs_elements__")
        for element in child_elements:
            try:
                text = await element.inner_html()

                print("text: ", text)
                subject = "feed-item"
                link_element = await element.query_selector('a.%s__head' % subject)

                if not link_element:
                    subject = "feed-item-big"
                    link_element = await element.query_selector('a.%s__head' % subject)

                link_href = await link_element.get_attribute('href')

                date_text = await (await element.query_selector('.%s__date' % subject)).inner_text()

                try:

                    date_trim = DateTrim(date_text)

                except ValueError:
                    break

                print("{%s}//{%s} " % (date_trim(), self.activate_at))
                   
                if date_trim() <= self.activate_at:
                    print("The limit of the last news collector activation has been reached: %s//%s " % (date_trim(), self.activate_at))
                    break


                title_text = await (await element.query_selector('.%s__title' % subject)).inner_text()
                summary_text = await (await element.query_selector('.%s__summary' % subject)).inner_text()

                child_page = await browser.new_page()
                print("link_href:", link_href)
                await asyncio.sleep(randint(base_timespan, logout_timespan))

                try: 
                    await child_page.goto(link_href)
                    print("__child_page_goto__")
                    # await asyncio.sleep(randint(base_timespan, logout_timespan))  # Use asyncio.sleep for asynchronous sleeping

                    await child_page.wait_for_selector('div[data-id="publication-content"]')

                    targeted_div_content = await child_page.inner_html('div[data-id="publication-content"]')

                    await child_page.close()

                    # print(targeted_div_content)
                    print("-----")

                    HTML_TAGS_PATTERN = '<[^<]+?>'
                    EMPTY_PLACEHOLDER = ""

                    cleared_content = re.sub(
                        HTML_TAGS_PATTERN, EMPTY_PLACEHOLDER, str(targeted_div_content))
                    extracted_news.append(News(**NewsBase(sign=sign(cleared_content), link_href=link_href, date_text=date_text,
                                                      title_text=title_text, summary_text=summary_text, publication_in=date_trim(), content_text=cleared_content).dict(), stock_id=self.stock_id))
                except:
                    print("unprocessable page: s%" % (link_href))
                finally:
                    continue




            except AttributeError or ValueError:
                continue

        await browser.close()  # Use await here
        print("__extracted_news__")
        extracted_news = sorted(
            extracted_news, key=sorting_by_publication_date)
        print(extracted_news)
        return extracted_news

    async def __call__(self, ):
        print("__call__")
        async with async_playwright() as playwright:
            return await self.run(playwright=playwright, extracted_news=[])
