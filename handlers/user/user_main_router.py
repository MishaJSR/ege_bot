from aiogram.filters import Command, or_f
from aiogram import types, Router, F

from handlers.user.user_task_router import user_task_router
from handlers.user.payment.user_payment import user_payment_router

user_private_router = Router()
user_private_router.include_routers(user_payment_router, user_task_router)


@user_private_router.message(Command('about'))
async def start_about(message: types.Message):
    await message.answer('Это бот для подготовки к ЕГЭ')



