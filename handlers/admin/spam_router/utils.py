import logging

from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode

from database.models import UserRepository
from keyboards.admin.reply_admin import start_kb


async def send_demo(message: types.Message, admin_spam_state):
    admin_spam_state.text = admin_spam_state.text
    if admin_spam_state.photo:
        await message.answer_photo(photo=admin_spam_state.photo, parse_mode=ParseMode.HTML)
    await message.answer(text=admin_spam_state.text,
                         reply_markup=admin_spam_state.markup,
                         parse_mode=ParseMode.HTML)


async def send_spam(message: types.Message, admin_spam_state):
    user_field = ["user_id"]
    users = await UserRepository().get_all_by_fields(data=user_field)
    counter = 0
    for user in users:
        if admin_spam_state.photo:
            try:
                await message.bot.send_photo(chat_id=user.user_id,
                                             photo=admin_spam_state.photo)
                counter += 1

            except Exception as e:
                logging.info("Cant send user spam")

        try:
            await message.bot.send_message(chat_id=user.user_id,
                                           text=admin_spam_state.text,
                                           reply_markup=admin_spam_state.markup,
                                           parse_mode=ParseMode.HTML)
            counter += 1
        except Exception as e:
            logging.info("Cant send user spam")
    await message.answer(f"Отправлено {counter} пользователям", reply_markup=start_kb())

