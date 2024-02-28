from aiogram.filters import CommandStart, Command
from aiogram import types, Router, F

user_private_router = Router()


@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer(text='Вы запустили бота')


@user_private_router.message(Command('theme'))
async def start_theme(message: types.Message):
    await message.answer('Выберите темы')


@user_private_router.message(Command('about'))
async def start_about(message: types.Message):
    await message.answer('Это бот для подготовки к ЕГЭ')

@user_private_router.message(Command('payment'))
async def start_about(message: types.Message):
    await message.answer('Этот сервис ожидает подключения')


@user_private_router.message(F.text)
async def start_filter(message: types.Message):
    await message.answer('Этот сервис ожидает подключения...')
