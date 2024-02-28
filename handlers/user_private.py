from aiogram.filters import CommandStart, Command, or_f
from aiogram import types, Router, F

from keyboards.reply import start_kb

user_private_router = Router()


@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer('Вы запустили бота', reply_markup=start_kb)


@user_private_router.message(Command('history'))
async def start_theme(message: types.Message):
    await message.answer('Выберите экзамен')

@user_private_router.message(Command('society'))
async def start_theme(message: types.Message):
    await message.answer('Выберите экзамен')


@user_private_router.message(Command('about'))
async def start_about(message: types.Message):
    await message.answer('Это бот для подготовки к ЕГЭ')


@user_private_router.message(or_f(Command('payment'), F.text.lower().contains('оплата')))
async def payment(message: types.Message):
    await message.answer('Этот сервис ожидает подключения')


@user_private_router.message(F.text, F.text.lower().contains('привет'))
async def start_filter(message: types.Message):
    await message.answer('Привет)')


@user_private_router.message(F.text)
async def start_filter(message: types.Message):
    await message.answer('Привет выберите предмет который вы будете изучать')
