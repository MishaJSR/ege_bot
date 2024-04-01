import os

from aiogram.filters import BaseFilter
from aiogram.types import Message
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())
admin = int(os.getenv('ADMIN_ID'))


class AdminFilter(BaseFilter):
    is_admin: bool = True

    async def __call__(self, obj: Message) -> bool:
        return obj.from_user.id == admin
