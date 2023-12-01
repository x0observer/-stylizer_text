from sqlalchemy.sql import ColumnElement

from .types import ModelAttribute


def icontains(field: ModelAttribute, value: str) -> ColumnElement:
    return field.ilike(f"%{value}%")