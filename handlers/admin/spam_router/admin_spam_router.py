from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from handlers.admin.state import AdminState
from keyboards.admin.reply_admin import start_kb_menu

admin_spam_router = Router()


@admin_spam_router.message(AdminState.start, F.text == start_kb_menu[1])
async def admin_spam_start(message: types.Message, state: FSMContext):
    await message.answer(message.text)