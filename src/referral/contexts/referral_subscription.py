from sqlmodel import SQLModel, Field, DateTime
from typing import Optional
from datetime import datetime
from src.utils.templates import *


class ReferralSubscriptionBase(SQLModel):
    code: Optional[str] = None


class ReferralSubscriptionCreate(ReferralSubscriptionBase):
    owner_id: Optional[int] = None


class ReferralSubscriptionQueryable(ReferralSubscriptionBase):
    pass


class ReferralSubscriptionUpdate(ReferralSubscriptionBase):
    pass


class OwnerReferralBase(Readable):
    first_name: Optional[str]
    second_name: Optional[str]
    alias: Optional[str]
    uid: Optional[str]
    is_activated: Optional[bool] = Field(False)


class SelfReferralBase(Readable):
    first_name: Optional[str]
    second_name: Optional[str]
    alias: Optional[str]
    uid: Optional[str]
    is_activated: Optional[bool] = Field(False)


class ReferralBundle(Readable):
    referrer_id: Optional[int]
    referrer: Optional["SelfReferralBase"]


class ReferralSubscriptionReadable(Readable, ReferralSubscriptionCreate):
    owner: Optional["OwnerReferralBase"]
    referrals: Optional[List["ReferralBundle"]]
