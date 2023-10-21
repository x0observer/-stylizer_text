from fastapi import APIRouter, Depends, HTTPException
from engine import get_async_session
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession


from src.register import *
from src.profile.contexts.profile import ProfileFull
from src.stock.service import StockRepository

class ProfileRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_profile(self, profile: ProfileBase) -> Profile:
        print("__new_stock__")
        new_profile = Profile(**profile.dict())
        self.db.add(new_profile)
        await self.db.commit()
        await self.db.refresh(new_profile)
        print("__out_stock__")
        return new_profile

    async def update_profile(self, profile_id: int, updated_profile: ProfileBase) -> Optional[Profile]:
        query = select(Profile).where(Profile.id == profile_id)
        execute = await self.db.execute(query)
        profile = execute.scalars().one_or_none()

        if profile:
            for attr, value in updated_profile.dict().items():
                if value is not None:
                    setattr(profile, attr, value)
            await self.db.commit()
            await self.db.refresh(profile)
        return profile

    async def patch_profile(self, profile_id: int, patch_data: dict) -> Optional[Profile]:
        query = select(Profile).where(Profile.id == profile_id)
        execute = await self.db.execute(query)
        profile = execute.scalars().one_or_none()

        if profile:
            for attr, value in patch_data.items():
                if value is not None:
                    setattr(profile, attr, value)

            await self.db.commit()
            await self.db.refresh(profile)

        return profile

    async def delete_profile(self, profile_id: int) -> Optional[Profile]:
        query = select(Profile).where(Profile.id == profile_id)
        execute = await self.db.execute(query)
        profile = execute.scalars().one_or_none()

        if profile:
            self.db.delete(profile)
            await self.db.commit()

        return profile

    async def get_profile(self, profile_id: int) -> Optional[ProfileFull]:
        query = select(Profile).where(Profile.id == profile_id)
        execute = await self.db.execute(query)
        profile = execute.scalars().one_or_none()
        return profile
    
    async def get_profile_stocks(self, profile_id: int) -> Optional[StockBase]:
        query = select(Stock).join(StockToProfile).where(StockToProfile.profile_id == profile_id)
        execute = await self.db.execute(query)
        stocks = execute.scalars().all()
        print("__profile_stocks__")
        print(stocks)
        return stocks

    async def get_profiles(self, filters: dict = None) -> List[Profile]:
        query = select(Profile)
        if filters:
            query = query.where(
                *(getattr(Profile, attr) == value for attr, value in filters.items())
            )
        profile = await self.db.execute(query).all()
        return profile

    async def add_stonks_to_profile(self, profile_id: int, stonks: List[Stock]) -> List[Profile]:
        query = select(Profile).where(Profile.id == profile_id)
        execute = await self.db.execute(query)
        profile = execute.scalars().one_or_none()

        if profile is None:
            return None  # Profile not found

        for stonk in stonks:
            # Create an entry in the association table
            stock_to_profile = StockToProfile(
                stock_id=stonk.id,
                profile_id=profile.id
            )
            self.db.add(stock_to_profile)

        await self.db.commit()
        await self.db.refresh(profile)
        
        return profile
    


def get_profile_repository(db: AsyncSession = Depends(get_async_session)) -> ProfileRepository:
    return ProfileRepository(db)


router = APIRouter()



@router.post("/create/", response_model=Profile)
async def create_profile(profile: ProfileBase, repository: ProfileRepository = Depends(get_profile_repository)):
    created_profile = await repository.create_profile(profile)
    return created_profile


@router.post("/{profile_id}/add_stocks/", response_model=ProfileFull)
async def add_stocks_to_profile(
    profile_id: int,
    titles: List[str],  # List of Stock objects from the request body
    db: AsyncSession = Depends(get_async_session),
):
    
    stock_repository = StockRepository(db=db)
    stocks = await stock_repository.get_stocks_by_titles(titles)

    print("stocks: ",stocks)
    profile_repository = ProfileRepository(db=db)
    profile = await profile_repository.add_stonks_to_profile(profile_id, stocks)
    
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    return profile

@router.get("/get/{profile_id}", response_model=Optional[ProfileFull])
async def get_profile(
    profile_id: int,
    repository: ProfileRepository = Depends(get_profile_repository)
):
    profile = await repository.get_profile(profile_id)
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


@router.get("/get_all/", response_model=List[Profile])
async def get_stocks(
    filters: dict = None,
    repository: ProfileRepository = Depends(get_profile_repository)
):
    profiles = await repository.get_profile(filters)
    return profiles


@router.put("/update/{profile_id}", response_model=Profile)
async def update_profile(
    profile_id: int,
    updated_profile: ProfileBase,
    repository: ProfileRepository = Depends(get_profile_repository)
):
    updated_profile_data = await repository.update_profile(profile_id, updated_profile)
    if updated_profile_data is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return updated_profile_data


@router.patch("/patch/{profile_id}", response_model=Profile)
async def patch_profile(
    profile_id: int,
    patch_data: dict,
    repository: ProfileRepository = Depends(get_profile_repository)
):
    updated_profile_data = await repository.patch_profile(profile_id, patch_data)
    if updated_profile_data is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return updated_profile_data


@router.delete("/delete/{profile_id}", response_model=Profile)
async def delete_profile(
    profile_id: int,
    repository: ProfileRepository = Depends(get_profile_repository)
):
    deleted_profile_data = await repository.delete_profile(profile_id)
    if deleted_profile_data is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return deleted_profile_data
