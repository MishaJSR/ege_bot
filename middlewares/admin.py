import os

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from typing import Callable, Dict, Awaitable, Any

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())
admin = int(os.getenv('ADMIN_ID'))


class AdminMiddleware(BaseMiddleware):
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
