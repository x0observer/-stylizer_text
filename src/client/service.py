from fastapi import APIRouter, Depends, HTTPException
from engine import get_async_session
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.auth.v2.auth import get_auth_repository, AuthRepository

from fastapi_jwt_auth import AuthJWT
from src.utils.templates import *
from src.register import *
from src.auth.v2.auth import api_key_header

class ClientRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_client(self, client: ClientCreate) -> Optional[ClientReadable]:
        print("__new_client__")
        new_client = Client(**client.dict())
        self.db.add(new_client)
        await self.db.commit()
        await self.db.refresh(new_client)
        print("__out_client__")
        return new_client

    async def update_client(self, client_id: int, updated_client: ClientUpdate) -> Optional[ClientReadable]:
        query = select(Client).where(Client.id == client_id)
        execute = await self.db.execute(query)
        client = execute.scalars().one_or_none()

        if client:
            for attr, value in updated_client.dict().items():
                if value is not None:
                    setattr(client, attr, value)
            await self.db.commit()
            await self.db.refresh(client)
        return client

    async def patch_client(self, client_id: int, patch_client: dict) -> Optional[ClientReadable]:
        query = select(Client).where(Client.id == client_id)
        execute = await self.db.execute(query)
        client = execute.scalars().one_or_none()

        if client:
            for attr, value in patch_client.items():
                if value is not None:
                    setattr(client, attr, value)

            await self.db.commit()
            await self.db.refresh(client)

        return client

    async def delete_client(self, client_id: int) -> Optional[ClientReadable]:
        query = select(Client).where(Client.id == client_id)
        execute = await self.db.execute(query)
        client = execute.scalars().one_or_none()

        if client:
            self.db.delete(client)
            await self.db.commit()

        return client

    async def get_client(self, client_id: int) -> Optional[ClientReadable]:
        query = select(Client).where(Client.id == client_id)
        execute = await self.db.execute(query)
        client = execute.scalars().one_or_none()
        return client

    async def get_clients(self, queries: ClientQueryable = None, paginate: Paginatable = None) -> Optional[List[ClientReadable]]:
        queries = queries.dict()

        query = select(Client)
        if queries:
            query = query.where(
                *(getattr(Client, attr) == value for attr, value in queries.items() if attr and value)
            )

        offset = (paginate.page - 1) * paginate.items_per_page
        query = query.offset(offset).limit(paginate.items_per_page)

        execute = await self.db.execute(query)
        clients = execute.scalars().all()
        return clients


async def get_client_repository(db: AsyncSession = Depends(get_async_session), api_key: str = Security(api_key_header), auth_repository: AuthRepository = Depends(get_auth_repository)) -> ClientRepository:
    await auth_repository.get_active_user()
    return ClientRepository(db)
