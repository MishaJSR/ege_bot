from abc import ABC, abstractmethod

from sqlalchemy import insert

from database.utils.AlchemyDataObject import AlchemyDataObject
from database.utils.decorators import async_session_maker_decorator
from database.engine import async_session_maker


class AbstractRepository(ABC):
    @abstractmethod
    async def add_object(self, **kwargs) -> int:
        raise NotImplementedError
    @abstractmethod
    async def get_one_by_fields(self, **kwargs) -> AlchemyDataObject:
        raise NotImplementedError

    @abstractmethod
    async def get_all_by_fields(self, **kwargs) -> list[AlchemyDataObject]:
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model: None

    async def add_object(self, **kwargs) -> int:
        async with async_session_maker() as session:
            stmt = insert(self.model).values(**kwargs.get("data")).returning(self.model.id)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()

    @async_session_maker_decorator
    async def get_one_by_fields(self, **kwargs) -> AlchemyDataObject:
        res_values = list(kwargs.get("result_query").fetchone()._data)
        return AlchemyDataObject(kwargs.get("data"), res_values)

    @async_session_maker_decorator
    async def get_all_by_fields(self, **kwargs) -> list[AlchemyDataObject]:
        res_values = [el._data for el in kwargs.get("result_query").fetchall()]
        return [AlchemyDataObject(kwargs.get("data"), value) for value in res_values]
