from sqlmodel import SQLModel, Field, DateTime
from typing import Optional
from datetime import datetime
from src.utils.templates import *
from src.referral.contexts.referral_subscription import ReferralSubscriptionReadable

class ClientBase(SQLModel):
    first_name: Optional[str]
    second_name: Optional[str]
    alias: Optional[str]
    uid: Optional[str]
    is_activated: Optional[bool] = Field(False)


class ClientQueryable(ClientBase):
    pass


class ClientReadable(Readable, ClientBase):
    own_referral_subscription: Optional["ReferralSubscriptionReadable"] 


class ClientCreate(ClientBase):
    pass


class ClientUpdate(ClientBase):
    pass
