import logging

from aiogram import types
from aiogram.enums import ParseMode

from database.models import UserRepository, TheoryRepository
from database.utils.construct_schemas import ConstructUser, ConstructTheory
from keyboards.admin.reply_admin import start_kb
from utils.common.static_url import image_chat_id


async def set_theory_multi(message: types.Message, admin_add_state):
    try:
        for post in admin_add_state.posts_list:
            photo_id, text = post
            message_id = None
            if photo_id:
                res = await message.bot.send_photo(chat_id=image_chat_id, photo=photo_id)
                message_id = res.message_id
            new_theory = ConstructTheory(under_chapter=admin_add_state.under_chapter,
                                         photo_id=photo_id,
                                         text=text,
                                         message_id=message_id).model_dump()
            await TheoryRepository().add_object(data=new_theory)

        admin_add_state.text = None
        admin_add_state.photo = None
        admin_add_state.chapter = None
        admin_add_state.under_chapter = None
        admin_add_state.posts_list = []
        await message.answer("Теория добавлена", reply_markup=start_kb())
    except Exception as e:
        logging.info(f"Ошибка создания теории {e}")
        await message.answer("Ошибка создания теории", reply_markup=start_kb())


async def send_demo_add_post(message: types.Message, admin_spam_state):
    if admin_spam_state.photo:
        await message.answer_photo(photo=admin_spam_state.photo)
    await message.answer(text=admin_spam_state.text, parse_mode=ParseMode.HTML)
