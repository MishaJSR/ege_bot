import os
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommandScopeAllPrivateChats
from dotenv import find_dotenv, load_dotenv

from handlers.user_private import user_private_router
from handlers.admin_private import admin_private_router
from common.bot_cmd_list import private

load_dotenv(find_dotenv())

ALLOWED_UPDATES = ['message, edited_message']
bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()
dp.include_router(user_private_router)
dp.include_router(admin_private_router)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=private, scope=BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)


asyncio.run(main())
