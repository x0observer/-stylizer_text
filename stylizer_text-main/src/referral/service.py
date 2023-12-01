from fastapi import Depends, HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.auth.v2.auth import AuthRepository, get_auth_repository
from engine import get_async_session
from typing import Optional, List
from src.register import *
from src.utils.templates import *
from src.auth.v2.auth import api_key_header


import uuid

class ReferralSubscriptionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_referral_subscription(self, referral_subscription: ReferralSubscriptionCreate) -> Optional[ReferralSubscriptionReadable]:
        new_referral_subscription = ReferralSubscription(
            **referral_subscription.dict())
        self.db.add(new_referral_subscription)
        await self.db.commit()
        await self.db.refresh(new_referral_subscription)
        return new_referral_subscription

    async def update_referral_subscription(self, referral_subscription_id: int, updated_referral_subscription: ReferralSubscriptionUpdate) -> Optional[ReferralSubscriptionReadable]:
        query = select(ReferralSubscription).where(
            ReferralSubscription.id == referral_subscription_id)
        execute = await self.db.execute(query)
        referral_subscription = execute.scalars().one_or_none()

        if referral_subscription:
            for attr, value in updated_referral_subscription.dict().items():
                if value is not None:
                    setattr(referral_subscription, attr, value)
            await self.db.commit()
            await self.db.refresh(referral_subscription)
        return referral_subscription

    async def delete_referral_subscription(self, referral_subscription_id: int) -> Optional[ReferralSubscriptionReadable]:
        query = select(ReferralSubscription).where(
            ReferralSubscription.id == referral_subscription_id)
        execute = await self.db.execute(query)
        referral_subscription = execute.scalars().one_or_none()

        if referral_subscription:
            self.db.delete(referral_subscription)
            await self.db.commit()

        return referral_subscription

    async def get_referral_subscription(self, referral_subscription_id: int) -> Optional[ReferralSubscriptionReadable]:
        query = select(ReferralSubscription).where(
            ReferralSubscription.id == referral_subscription_id)
        execute = await self.db.execute(query)
        referral_subscription = execute.scalars().one_or_none()
        return referral_subscription
    
    async def get_client(self, referral_subscription_code: str) -> Optional[ReferralSubscriptionReadable]:
        query = select(ReferralSubscription).where(
            ReferralSubscription.code == referral_subscription_code)
        execute = await self.db.execute(query)
        referral_subscription = execute.scalars().one_or_none()
        return referral_subscription
    

    async def attach_clinet(self, referral_subscription_code: str, client_id: int):
        referral_subscription = await self.get_client(referral_subscription_code)
        new_referral_bundle = Referral(
                subscription_id=referral_subscription.id,
                referrer_id=client_id,
                # Другие необходимые поля можно добавить здесь
            )
        self.db.add(new_referral_bundle)
        await self.db.commit()
        await self.db.refresh(new_referral_bundle)
        return new_referral_bundle

    async def get_referral_subscriptions(self, queries: ReferralSubscriptionQueryable = None, paginate: Paginatable = None) -> Optional[List[ReferralSubscriptionReadable]]:
        queries = queries.dict() if queries else {}

        query = select(ReferralSubscription)
        if queries:
            query = query.where(
                *(getattr(ReferralSubscription, attr) == value for attr, value in queries.items() if attr and value)
            )

        offset = (paginate.page - 1) * paginate.items_per_page
        query = query.offset(offset).limit(paginate.items_per_page)

        execute = await self.db.execute(query)
        referral_subscriptions = execute.scalars().all()
        return referral_subscriptions

    async def generate_referral_subscription(self, client_id: int) -> Optional[ReferralSubscriptionReadable]:
            # Генерация уникального идентификатора для реферальной подписки
            unique_id = uuid.uuid4()
            print("__unique_code__", unique_id)

            # Создание объекта реферальной подписки
            referral_subscription_data = ReferralSubscriptionCreate(
                owner_id=client_id,
                code=str(unique_id),
                # Другие необходимые поля можно добавить здесь
            )

            # Сохранение реферальной подписки в базе данных
            new_referral_subscription = await self.create_referral_subscription(referral_subscription_data)

            return new_referral_subscription
    



async def get_referral_subscription_repository(db: AsyncSession = Depends(get_async_session), api_key: str = Security(api_key_header), auth_repository: AuthRepository = Depends(get_auth_repository)) -> ReferralSubscriptionRepository:
    await auth_repository.get_active_user()
    return ReferralSubscriptionRepository(db)


