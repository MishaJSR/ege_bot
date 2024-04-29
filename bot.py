import logging
import os
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommandScopeAllPrivateChats
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from dotenv import find_dotenv, load_dotenv
import betterlogging as bl

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

def setup_logging():
    log_level = logging.INFO
    bl.basic_colorized_config(level=log_level)

    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
    )
    logger = logging.getLogger(__name__)
    logger.info("Starting bot")






async def on_startup(bot):
    print('Bot start')


async def on_shutdown(bot):
    print('Bot end')


async def main():
    setup_logging()
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


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error("Бот был выключен!")
