from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import get_all_users
from keyboards.user.reply_user import start_kb
from keyboards.admin.reply_admin import start_kb, answers_kb_end, reset_kb, send_img_kb
from handlers.admin.states import Admin_state, AdminStateSender

admin_spammer_router = Router()


@admin_spammer_router.message(F.text == 'Отправить рассылку')
async def fill_admin_state(message: types.Message, state: FSMContext):
    await message.answer(text='Напишите текст рассылки', reply_markup=reset_kb())
    await state.set_state(AdminStateSender.text_state)


@admin_spammer_router.message(AdminStateSender.text_state)
async def fill_admin_state(message: types.Message, state: FSMContext):
    AdminStateSender.text = message.text
    await message.answer(text='Отправьте изображение', reply_markup=send_img_kb())
    await state.set_state(AdminStateSender.image_state)


@admin_spammer_router.message(AdminStateSender.image_state)
async def process_photo(message: types.Message, state: FSMContext):
    if message.text == 'Оставить пустым':
        await message.answer(text=AdminStateSender.text, reply_markup=answers_kb_end())
    else:
        await message.answer_photo(caption=AdminStateSender.text, photo=message.photo[-1].file_id,
                                   reply_markup=answers_kb_end())
        AdminStateSender.photo = message.photo[-1].file_id
    await message.answer(text='Все верно?')
    await state.set_state(AdminStateSender.confirm_state)


@admin_spammer_router.message(AdminStateSender.confirm_state)
async def process_photo(message: types.Message, session: AsyncSession, state: FSMContext):
    if message.text == 'Подтвердить':
        res = await get_all_users(session)
        await message.answer(text="Начало рассылки")
        for user in res:
            await spammer(message, user, AdminStateSender)
            # await message.bot.send_photo(chat_id=user._mapping['user_id'], photo=AdminStateSender.photo,
            #                              caption=AdminStateSender.text)
        await message.answer(text="Рассылка завершена", reply_markup=start_kb())
    else:
        await message.answer(text="Ошибка рассылки", reply_markup=start_kb())
    await state.set_state(Admin_state.start)


async def spammer(message, user, state):
    if state.photo is None:
        await message.bot.send_message(chat_id=user._mapping['user_id'], text=state.text)
    else:
        await message.bot.send_photo(chat_id=user._mapping['user_id'], photo=state.photo, caption=state.text)