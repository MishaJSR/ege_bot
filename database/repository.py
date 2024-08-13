from abc import ABC, abstractmethod

from sqlalchemy import insert, update

from database.utils.AlchemyDataObject import AlchemyDataObject
from database.utils.decorators import async_session_maker_decorator_select
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

    @abstractmethod
    async def update_fields(self, **kwargs) -> list[AlchemyDataObject]:
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model: None

    async def add_object(self, **kwargs) -> int:
        async with async_session_maker() as session:
            stmt = insert(self.model).values(**kwargs.get("data")).returning(self.model.id)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()

    @async_session_maker_decorator_select
    async def get_one_by_fields(self, **kwargs) -> AlchemyDataObject:
        res_values = list(kwargs.get("result_query").fetchone()._data)
        return AlchemyDataObject(kwargs.get("data"), res_values)

    @async_session_maker_decorator_select
    async def get_all_by_fields(self, **kwargs) -> list[AlchemyDataObject]:
        res_values = [el._data for el in kwargs.get("result_query").fetchall()]
        return [AlchemyDataObject(kwargs.get("data"), value) for value in res_values]

    async def update_one_field(self, **kwargs) -> AlchemyDataObject:
        try:
            data = kwargs.get("data")
            values = kwargs.get("values")
            async with async_session_maker() as session:
                query = update(self.model).where(self.model.user_id == 548349299).values(user_id=1)
                await session.execute(query)
                await session.commit()
            return True
        except Exception as e:
            print(e)
            return False
