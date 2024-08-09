from aiogram.filters import BaseFilter
from aiogram.types import Message

from env_config import load_config

admin_ids = load_config().tg_bot.admin_ids


class AdminFilter(BaseFilter):
    is_admin: bool = True

    async def __call__(self, obj: Message) -> bool:
        return obj.from_user.id in admin_ids
