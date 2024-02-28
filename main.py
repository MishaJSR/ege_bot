from aiogram import Bot, Dispatcher, types
import asyncio
from aiogram.filters import CommandStart

bot = Bot(token=token)
dp = Dispatcher()


@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer(text='Вы запустили бота')


@dp.message()
async def start_cmd(message: types.Message):
    await message.answer(text=message.text)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


asyncio.run(main())
