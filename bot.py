import os
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommandScopeAllPrivateChats
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from dotenv import find_dotenv, load_dotenv

from database.config import load_config

load_dotenv(find_dotenv())

from handlers.user.user_main_router import user_private_router
from handlers.admin.admin_main_router import admin_private_router
from common.bot_cmd_list import private
from middlewares.db import DataBaseSession
from database.engine import create_engine, create_session_pool


def get_storage(config):
    return RedisStorage.from_url(
        config.redis.dsn(),
        key_builder=DefaultKeyBuilder(with_bot_id=True, with_destiny=True),
    )



ALLOWED_UPDATES = ['message, edited_message']



async def on_startup(bot):
    print('Bot start')


async def on_shutdown(bot):
    print('Bot end')


async def main():
    config = load_config()
    storage = get_storage(config)

    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher(storage=storage)
    dp.include_routers(admin_private_router, user_private_router)

    engine = create_engine(config.db)
    session_pool = create_session_pool(engine)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    dp.update.middleware(DataBaseSession(session_pool=session_pool))
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=private, scope=BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)


asyncio.run(main())
