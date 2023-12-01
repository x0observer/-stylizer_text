from fastapi import APIRouter, Depends, HTTPException
from engine import get_async_session
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.auth.v2.auth import AuthRepository, get_auth_repository


from src.register import *
from src.auth.v2.auth import api_key_header


class PaymentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_payment(self, payment: PaymentCreate) -> Optional[PaymentReadable]:
        print("__new_payment__")
        new_payment = Payment(**payment.dict())
        self.db.add(new_payment)
        await self.db.commit()
        await self.db.refresh(new_payment)
        print("__out_payment__")
        return new_payment

    async def update_payment(self, payment_id: int, updated_payment: PaymentUpdate) -> Optional[PaymentReadable]:
        query = select(Payment).where(Payment.id == payment_id)
        execute = await self.db.execute(query)
        payment = execute.scalars().one_or_none()

        if payment:
            for attr, value in updated_payment.dict().items():
                if value is not None:
                    setattr(payment, attr, value)
            await self.db.commit()
            await self.db.refresh(payment)
        return payment

    async def patch_payment(self, payment_id: int, patch_payment: dict) -> Optional[PaymentReadable]:
        query = select(Payment).where(Payment.id == payment_id)
        execute = await self.db.execute(query)
        payment = execute.scalars().one_or_none()

        if payment:
            for attr, value in patch_payment.items():
                if value is not None:
                    setattr(payment, attr, value)

            await self.db.commit()
            await self.db.refresh(payment)

        return payment

    async def delete_payment(self, payment_id: int) -> Optional[PaymentReadable]:
        query = select(Payment).where(Payment.id == payment_id)
        execute = await self.db.execute(query)
        payment = execute.scalars().one_or_none()

        if payment:
            self.db.delete(payment)
            await self.db.commit()

        return payment

    async def get_payment(self, payment_id: int) -> Optional[PaymentReadable]:
        query = select(Payment).where(Payment.id == payment_id)
        execute = await self.db.execute(query)
        payment = execute.scalars().one_or_none()
        return payment
    
    async def get_payments(self,  queries: PaymentQueryable = None, paginate: Paginatable = None) -> Optional[List[PaymentReadable]]:
        queries = queries.dict()
        
        query = select(Payment)
        if queries:
            query = query.where(
                *(getattr(Payment, attr) == value for attr, value in queries.items() if attr and value )
            )

        offset = (paginate.page - 1) * paginate.items_per_page
        query = query.offset(offset).limit(paginate.items_per_page)

        execute = await self.db.execute(query)    
        payments = execute.scalars().all()
        return payments


async def get_payment_repository(db: AsyncSession = Depends(get_async_session), api_key: str = Security(api_key_header),  auth_repository: AuthRepository = Depends(get_auth_repository)) -> PaymentRepository:
    await auth_repository.get_active_user()
    return PaymentRepository(db)

