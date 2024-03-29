import emoji
from aiogram.filters import CommandStart, StateFilter, or_f, Command
from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from database.orm_query import orm_get_modules_task, orm_get_prepare_module, add_user, check_new_user
from keyboards.user.reply_user import start_kb, prepare_kb, subj_kb, module_kb, train_kb, under_prepare_kb, main_but, \
    start_but, modules, teor
from sqlalchemy.ext.asyncio import AsyncSession

user_payment_router = Router()

@user_payment_router.message(or_f(Command('payment'), F.text.lower().contains('Оплата подписки')))
async def payment(message: types.Message):
    await message.answer('Этот сервис ожидает подключения')
