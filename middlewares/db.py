import os

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject
from typing import Callable, Dict, Awaitable, Any
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())
admin = int(os.getenv('ADMIN_ID'))


class DataBaseSession(BaseMiddleware):
    def __init__(self, session_pool: async_sessionmaker):
        self.session_pool = session_pool

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]):
        async with self.session_pool() as session:
            data['session'] = session
            return await handler(event, data)


class CounterMiddleware(BaseMiddleware):
    def __init__(self):
        self.counter = 0

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]):
        self.counter += 1
        if event.chat.id == admin:
            data['counter'] = self.counter
            return await handler(event, data)
