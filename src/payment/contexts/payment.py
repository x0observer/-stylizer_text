from sqlmodel import SQLModel, Field, DateTime
from typing import Optional
from datetime import datetime
from src.utils.templates import *


class PaymentStep(str, Enum):
    PENDING = "PENDING"
    FAILED = "FAILED"
    COMPLETED = "COMPLETED"
    REFUNDED = "REFUNDED"


class PaymentCurrency(str, Enum):
    RUB = "RUB"


class PaymentBase(SQLModel):
    step: Optional[PaymentStep] = PaymentStep.PENDING
    amount: Optional[float] = 0.0
    currency: Optional[PaymentCurrency] = PaymentCurrency.RUB
    link: Optional[str] = None


class PaymentCreate(PaymentBase):
    pass


class PaymentQueryable(PaymentBase):
    pass


class PaymentUpdate(PaymentBase):
    pass


class PaymentReadable(Readable, PaymentBase):
    pass
