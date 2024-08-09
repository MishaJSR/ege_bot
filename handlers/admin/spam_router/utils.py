from aiogram import types
from aiogram.fsm.context import FSMContext


async def send_demo(message: types.Message, admin_spam_state):
    if admin_spam_state.photo:
        await message.answer_photo(photo=admin_spam_state.photo,
                                   caption=admin_spam_state.text,
                                   reply_markup=admin_spam_state.markup)
    else:
        await message.answer(text=admin_spam_state.text, reply_markup=admin_spam_state.markup)