import os

from aiogram.filters import BaseFilter
from aiogram.types import Message
from dotenv import find_dotenv, load_dotenv

from config import load_config

admin_ids = []


class AdminFilter(BaseFilter):
    is_admin: bool = True

    async def __call__(self, obj: Message) -> bool:
        return obj.from_user.id in admin_ids
