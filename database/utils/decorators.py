import logging

import sqlalchemy
from sqlalchemy import select

from database.engine import async_session_maker
from database.exeptions import CustomException


def async_session_maker_decorator(func):
    async def wrapper(self_object, **kwargs):
        try:
            async with async_session_maker() as session:
                field_filter = kwargs.get("field_filter")
                data = kwargs.get("data")
                if not kwargs.get("field_filter"):
                    field_filter = {}
                if not data:
                    raise CustomException(message="Expecting kwargs data")
                try:
                    query = select(*[getattr(self_object.model, field) for field in data])
                except AttributeError:
                    raise CustomException(message="Unknown fields in data")
                try:
                    for key, value in field_filter.items():
                        query = query.filter(getattr(self_object.model, key) == value)
                except AttributeError:
                    raise CustomException(message="Unknown fields in field_filter")
                res = await session.execute(query)
                return await func(self_object, data=data, result_query=res)
        except Exception as e:
            logging.info(f"{e}")

    return wrapper
