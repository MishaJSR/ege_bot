import os

from aiogram.filters import Command
from aiogram import types, Router
from aiogram.fsm.context import FSMContext

from database.models import UserRepository, TaskRepository
from database.utils.construct_schemas import ConstructUser, ConstructTask
from filters.admin_filter import AdminFilter
from handlers.admin.add_router.admin_add_router import admin_add_router
from handlers.admin.spam_router.admin_spam_router import admin_spam_router
from handlers.admin.state import AdminState
from keyboards.admin.reply_admin import start_kb
from utils.common.static_admin import *

admin_private_router = Router()
admin_private_router.include_routers(admin_add_router, admin_spam_router)
admin_private_router.message.filter(AdminFilter())


@admin_private_router.message(Command('admin'))
async def admin_start(message: types.Message, state: FSMContext):
    await message.answer(text=HELLO_ADMIN, reply_markup=start_kb())
    await state.set_state(AdminState.start)




