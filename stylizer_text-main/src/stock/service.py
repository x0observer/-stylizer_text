from fastapi import APIRouter, Depends, HTTPException
from engine import get_async_session
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession


from src.register import *


class StockRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_stock(self, stock: StockCreate) -> Stock:
        print("__new_stock__")
        new_stock = Stock(**stock.dict())
        self.db.add(new_stock)
        await self.db.commit()
        await self.db.refresh(new_stock)
        print("__out_stock__")
        return new_stock

    async def update_stock(self, stock_id: int, updated_stock: StockBase) -> Optional[Stock]:
        query = select(Stock).where(Stock.id == stock_id)
        execute = await self.db.execute(query)
        stock = execute.scalars().one_or_none()

        if stock:
            for attr, value in updated_stock.dict().items():
                if value is not None:
                    setattr(stock, attr, value)
            await self.db.commit()
            await self.db.refresh(stock)
        return stock

    async def patch_stock(self, stock_id: int, patch_data: dict) -> Optional[Stock]:
        query = select(Stock).where(Stock.id == stock_id)
        execute = await self.db.execute(query)
        stock = execute.scalars().one_or_none()

        if stock:
            for attr, value in patch_data.items():
                if value is not None:
                    setattr(stock, attr, value)

            await self.db.commit()
            await self.db.refresh(stock)

        return stock

    async def delete_stock(self, stock_id: int) -> Optional[Stock]:
        query = select(Stock).where(Stock.id == stock_id)
        execute = await self.db.execute(query)
        stock = execute.scalars().one_or_none()

        if stock:
            self.db.delete(stock)
            await self.db.commit()

        return stock

    async def get_stock(self, stock_id: int):
        query = select(Stock).where(Stock.id == stock_id)
        execute = await self.db.execute(query)
        stock = execute.scalars().one_or_none()
        return stock

    async def get_stocks(self, filters: dict = None) -> List[Stock]:
        query = select(Stock)
        if filters:
            query = query.where(
                *(getattr(Stock, attr) == value for attr, value in filters.items())
            )
        execute = await self.db.execute(query)
        stocks = execute.scalars().all()
        return stocks
    
    async def get_stocks_by_titles(self, titles: List[str]) -> List[Stock]:
        query = select(Stock).where(Stock.title.in_(titles))
        result = await self.db.execute(query)
        stonks = result.scalars().all()
        return stonks


def get_stock_repository(db: AsyncSession = Depends(get_async_session)) -> StockRepository:
    return StockRepository(db)


router = APIRouter()


@router.post("/test")
async def execute(
    # stock: StockBase,
    # db: AsyncSession = Depends(get_async_session),
    # repository: StockRepository = Depends(get_stock_repository)
):
    print("__stock_endpoint__")
    # service = Mediator()
    # extracted_news = await service()
    return {"status": "success"}


@router.post("/create/", response_model=Stock)
async def create_stock(stock: StockCreate, repository: StockRepository = Depends(get_stock_repository)):
    created_stock = await repository.create_stock(stock)
    return created_stock


@router.get("/get/{stock_id}", response_model=StockFull)
async def get_stock(
    stock_id: int,
    repository: StockRepository = Depends(get_stock_repository)
):
    stock = await repository.get_stock(stock_id)
    if stock is None:
        raise HTTPException(status_code=404, detail="Stock not found")
    return stock


@router.post("/get_all/", response_model=List[Stock])
async def get_stocks(
    filters: dict = None,
    repository: StockRepository = Depends(get_stock_repository)
):
    stocks = await repository.get_stocks(filters)
    return stocks


@router.put("/update/{stock_id}", response_model=StockBase)
async def update_stock(
    stock_id: int,
    updated_stock: StockBase,
    repository: StockRepository = Depends(get_stock_repository)
):
    updated_stock_data = await repository.update_stock(stock_id, updated_stock)
    if updated_stock_data is None:
        raise HTTPException(status_code=404, detail="Stock not found")
    return updated_stock_data


@router.patch("/patch/{stock_id}", response_model=StockBase)
async def patch_stock(
    stock_id: int,
    patch_data: dict,
    repository: StockRepository = Depends(get_stock_repository)
):
    updated_stock_data = await repository.patch_stock(stock_id, patch_data)
    if updated_stock_data is None:
        raise HTTPException(status_code=404, detail="Stock not found")
    return updated_stock_data


@router.delete("/delete/{stock_id}", response_model=StockBase)
async def delete_stock(
    stock_id: int,
    repository: StockRepository = Depends(get_stock_repository)
):
    deleted_stock_data = await repository.delete_stock(stock_id)
    if deleted_stock_data is None:
        raise HTTPException(status_code=404, detail="Stock not found")
    return deleted_stock_data
