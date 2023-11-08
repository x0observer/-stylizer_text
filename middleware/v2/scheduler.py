from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.exc import IntegrityError
from engine import AsyncSessionLocal
from src.stock.service import StockRepository
from middleware.v2.provider import NewsDataProvider

from src.utils.templates import *
from logger import *


class SchedulerRepository:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()

    async def scraping_scheduler(self):
        async with AsyncSessionLocal() as session:
            stock_repository = StockRepository(session)
            stocks = await stock_repository.get_stocks()
            logger.info("__profile_stocks__")
            logger.info(stocks)

            for stock in stocks:
                logger.info(f"__stock_iter__: {stock}")
                news_provider = NewsDataProvider(
                    stock.symbol, stock.id, stock.activate_at)

                try:
                    extracted_news = await news_provider.run()
                    if extracted_news:
                        unique_news = await insert_unique_objects(db=session, objects=extracted_news)
                        stock.activate_at = datetime.utcnow()  # Consider using UTC for consistency
                        await session.commit()
                        await session.refresh(stock)
                    else:
                        logger.info(
                            f"No news extracted for stock {stock.symbol}")

                except IntegrityError as e:
                    await session.rollback()
                    logger.error(f"IntegrityError for stock {stock.id}: {e}")
                except Exception as e:
                    await session.rollback()
                    logger.error(f"Error for stock {stock.id}: {e}")

            logger.info("Scraping task completed.")

    def add_job(self, func, trigger, **trigger_args):
        self.scheduler.add_job(func, trigger, **trigger_args)

    def start(self):
        self.scheduler.start()

    def run_now(self, func):
        self.scheduler.add_job(func, 'date')

    def reschedule_job(self, job_id, trigger, **trigger_args):
        self.scheduler.reschedule_job(job_id, trigger=trigger, **trigger_args)


# Использование SchedulerManager
# scheduler_manager = SchedulerRepository()

# # Добавление задачи с интервалом в 6 часов
# scheduler_manager.add_job(scheduler_manager.scraping_scheduler, 'interval', hours=6)

# # Принудительный запуск задачи
# scheduler_manager.run_now(scheduler_manager.scraping_scheduler)
