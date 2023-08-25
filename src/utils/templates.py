from sqlmodel import SQLModel
from typing import Optional
from datetime import datetime
from sqlmodel import Session
from engine import *
from typing import List
from sqlalchemy.exc import IntegrityError
import hashlib


class Readable(SQLModel):
    id: Optional[int]
    created_at: Optional[datetime]


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
    for obj in objects:
        try:
            db.add(obj)
            await db.flush()
        except IntegrityError:
                # Handle the unique constraint violation (skip the duplicate)
            db.rollback()
            continue
        await db.commit()


test_cases = ["23 августа в 20:29", "19 июля в 13:59"]

for test_case in test_cases:
    date_trim = DateTrim(test_case)
    print(date_trim())