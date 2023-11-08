from sqlmodel import SQLModel, Field, DateTime
from typing import Optional
from datetime import datetime
from src.utils.templates import *


class ReferralSubscriptionBase(SQLModel):
    code: Optional[str] = None


class ReferralSubscriptionCreate(ReferralSubscriptionBase):
    pass

class ReferralSubscriptionQueryable(ReferralSubscriptionBase):
    pass

class ReferralSubscriptionUpdate(ReferralSubscriptionBase):
    pass

class ReferralSubscriptionReadable(Readable, ReferralSubscriptionBase):
    pass