from src.register import *
from src.utils.templates import *
from src.client.service import *
from src.auth.v2.auth import *
from src.auth.v2.auth import api_key_header

router = APIRouter(tags=["Client(Repository)"])


@router.post("/create/", response_model=ClientReadable)
async def create_client(client: ClientBase, repository: ClientRepository = Depends(get_client_repository)):
    create_client = await repository.create_client(client)
    return create_client


@router.get("/get/{client_id}", response_model=Optional[ClientReadable])
async def get_client(
    client_id: int,
    repository: ClientRepository = Depends(get_client_repository)
):
    client = await repository.get_client(client_id)
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return client



@router.get("/get_all/", response_model=Optional[List[ClientReadable]])
async def get_clients(
    queries: ClientQueryable = Depends(),
    paginate: Paginatable = Depends(),
    repository: ClientRepository = Depends(get_client_repository)
):
    clients = await repository.get_clients(queries, paginate)
    return clients


@router.put("/update/{client_id}", response_model=Optional[ClientReadable])
async def update_client(
    client_id: int,
    updated_client: ClientUpdate,
    repository: ClientRepository = Depends(get_client_repository)
):
    updated_client_data = await repository.update_client(client_id, updated_client)
    if updated_client_data is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return updated_client_data


@router.patch("/patch/{client_id}", response_model=Optional[ClientReadable])
async def patch_client(
    client_id: int,
    patch_data: dict,
    repository: ClientRepository = Depends(get_client_repository)
):
    updated_client_data = await repository.patch_client(client_id, patch_data)
    if updated_client_data is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return updated_client_data


@router.delete("/delete/{client_id}", response_model=Optional[ClientReadable])
async def delete_client(
    client_id: int,
    repository: ClientRepository = Depends(get_client_repository)
):
    deleted_client_data = await repository.delete_client(client_id)
    if deleted_client_data is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return deleted_client_data
