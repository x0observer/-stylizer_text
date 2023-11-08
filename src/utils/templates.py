from sqlmodel import SQLModel
from typing import Optional
from datetime import datetime
from sqlmodel import Session
from engine import *
from typing import List
from sqlalchemy.exc import IntegrityError
from enum import Enum
from fastapi import HTTPException, Security, Depends, APIRouter

import re
import pytz

import hashlib


class Readable(SQLModel):
    id: Optional[int]
    created_at: Optional[datetime]


class Paginatable(SQLModel):
    page: Optional[int] = 1
    items_per_page: Optional[int] = 10


moscow_tz = pytz.timezone('Europe/Moscow')

desired_datetime = datetime(2023, 10, 1, 0, 0, 0)

desired_datetime_moscow = moscow_tz.localize(desired_datetime)


class DateTrim:
    MONTH_PLACEHOLDERS = [
        ("января", 1),
        ("февраля", 2),
        ("марта", 3),
        ("апреля", 4),
        ("мая", 5),
        ("июня", 6),
        ("июля", 7),
        ("августа", 8),
        ("сентября", 9),
        ("октября", 10),
        ("ноября", 11),
        ("декабря", 12)
    ]

    def __init__(self, original_text: str, WHITESPACE_TRIM=" ", PHASE_TRIM=":") -> None:
        uniform_text = original_text.lower()
        print("uniform_text:", uniform_text)
        uniform_subjects = original_text.split(WHITESPACE_TRIM)
        uniform_subtime = uniform_subjects[-1].split(PHASE_TRIM)
        for uniform_date_placeholder in DateTrim.MONTH_PLACEHOLDERS:
            month_placeholder, month_numerator = uniform_date_placeholder
            if month_placeholder in uniform_text:
                date_args = {
                    "year": datetime.now().year,
                    "day": int(uniform_subjects[0]),
                    "month": month_numerator,
                    "hour": int(uniform_subtime[0]),
                    "minute": int(uniform_subtime[-1])
                }
                print("date_args:", date_args)
                self.datetime = datetime(**date_args)
                break

    def __call__(self, ):
        return self.datetime


def sign(string_to_hash, length=16):
    hash_object = hashlib.sha256(string_to_hash.encode())
    hex_dig = hash_object.hexdigest()
    truncated_hex_dig = hex_dig[:length]
    return truncated_hex_dig


async def insert_unique_objects(db: AsyncSession, objects: List[SQLModel]):
    unique_objects = []
    for obj in objects:
        try:
            db.add(obj)
            await db.flush()
            unique_objects.append(obj)
        except IntegrityError:
            await db.rollback()
        else:
            await db.commit()
    return unique_objects
