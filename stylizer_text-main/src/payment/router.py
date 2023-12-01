from src.utils.templates import *
from src.payment.service import *

router = APIRouter(tags=["Payment(Repository)"])


@router.post("/create/", response_model=Optional[PaymentReadable])
async def create_payment(payment: PaymentCreate, repository: PaymentRepository = Depends(get_payment_repository)):
    created_payment = await repository.create_payment(payment)
    return created_payment


@router.get("/get/{payment_id}", response_model=Optional[PaymentReadable])
async def get_payment(
    payment_id: int,
    repository: PaymentRepository = Depends(get_payment_repository)
):
    payment = await repository.get_payment(payment_id)
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment


@router.get("/get_all/", response_model=Optional[List[PaymentReadable]])
async def get_payments(
    queries: PaymentQueryable = Depends(),
    paginate: Paginatable = Depends(),
    repository: PaymentRepository = Depends(get_payment_repository)
):
    payment = await repository.get_payments(queries, paginate)
    return payment


@router.put("/update/{payment_id}", response_model=Optional[PaymentReadable])
async def update_payment(
    payment_id: int,
    updated_payment: PaymentUpdate,
    repository: PaymentRepository = Depends(get_payment_repository)
):
    updated_payment_data = await repository.update_payment(payment_id, updated_payment)
    if updated_payment_data is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return updated_payment_data


@router.patch("/patch/{payment_id}", response_model=Optional[PaymentReadable])
async def patch_payment(
    payment_id: int,
    patch_data: dict,
    repository: PaymentRepository = Depends(get_payment_repository)
):
    updated_payment_data = await repository.patch_payment(payment_id, patch_data)
    if updated_payment_data is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return updated_payment_data


@router.delete("/delete/{payment_id}", response_model=Optional[PaymentReadable])
async def delete_payment(
    payment_id: int,
    repository: PaymentRepository = Depends(get_payment_repository)
):
    deleted_payment_data = await repository.delete_payment(payment_id)
    if deleted_payment_data is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return deleted_payment_data
