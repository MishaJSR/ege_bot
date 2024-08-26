from aiogram import types, Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
import validators

from handlers.admin.spam_router.state import AdminSpamState
from handlers.admin.spam_router.utils import send_demo, send_spam
from handlers.admin.state import AdminState
from keyboards.admin.inline_admin import make_markup_kb
from keyboards.admin.reply_admin import *
from keyboards.user.reply_user import back_kb
from utils.common.static_user import BACK_BUTTON

admin_spam_router = Router()


@admin_spam_router.message(StateFilter(AdminSpamState), F.text == BACK_BUTTON)
async def back_step_handler(message: types.Message, state: FSMContext) -> None:
    AdminSpamState.photo = None
    AdminSpamState.text = None
    AdminSpamState.button_text = None
    AdminSpamState.button_link = None
    AdminSpamState.markup = None
    await message.answer(RETURN_IN_MAIN_ADMIN, reply_markup=start_kb())
    await state.set_state(AdminState.start)


@admin_spam_router.message(AdminState.start, F.text == start_kb_menu[2])
async def admin_spam_photo_send(message: types.Message, state: FSMContext):
    await message.answer(SEND_PHOTO, reply_markup=skip_kb())
    await state.set_state(AdminSpamState.send_photo)


@admin_spam_router.message(AdminSpamState.send_photo)
async def admin_spam_set_text(message: types.Message, state: FSMContext):
    if not message.text == SKIP_TEXT and not message.photo:
        await message.answer(DONT_UNDERSTAND_TRY_AGAIN)
        return
    if message.photo:
        AdminSpamState.photo = message.photo[-1].file_id
    await message.answer(SEND_TEXT, reply_markup=back_kb())
    await state.set_state(AdminSpamState.send_text)


@admin_spam_router.message(AdminSpamState.send_text, F.text)
async def admin_spam_set_text(message: types.Message, state: FSMContext):
    AdminSpamState.text = message.md_text
    await message.answer(SEND_BUTTON_TEXT, reply_markup=skip_kb())
    await state.set_state(AdminSpamState.send_button_text)


@admin_spam_router.message(AdminSpamState.send_button_text, F.text)
async def admin_spam_set_text(message: types.Message, state: FSMContext):
    if message.text == BUTTON_SKIP:
        await send_demo(message=message, admin_spam_state=AdminSpamState)
        await message.answer(CONFIRM_TEXT, reply_markup=confirm_kb())
        await state.set_state(AdminSpamState.show_post)
        return
    AdminSpamState.button_text = message.text
    await message.answer(SEND_BUTTON_LINK, reply_markup=back_kb())
    await state.set_state(AdminSpamState.send_button_link)


@admin_spam_router.message(AdminSpamState.send_button_link, F.text)
async def admin_spam_set_text(message: types.Message, state: FSMContext):
    if not validators.url(message.text):
        await message.answer(DONT_UNDERSTAND_TRY_AGAIN)
        return
    AdminSpamState.button_link = message.md_text
    AdminSpamState.markup = make_markup_kb(text=AdminSpamState.text, url=AdminSpamState.button_link)
    await send_demo(message=message, admin_spam_state=AdminSpamState)
    await message.answer(CONFIRM_TEXT, reply_markup=confirm_kb())
    await state.set_state(AdminSpamState.show_post)


@admin_spam_router.message(AdminSpamState.show_post, F.text == BUTTON_CONFIRM)
async def admin_spam_set_text(message: types.Message, state: FSMContext):
    await send_spam(message, AdminSpamState)
    await state.set_state(AdminState.start)


@admin_spam_router.message(AdminSpamState.show_post, F.text == BUTTON_NOT_CONFIRM)
async def admin_spam_set_text(message: types.Message, state: FSMContext):
    AdminSpamState.photo = None
    AdminSpamState.text = None
    AdminSpamState.button_text = None
    AdminSpamState.button_link = None
    AdminSpamState.markup = None
    await message.answer(RETURN_IN_MAIN_ADMIN, reply_markup=start_kb())
    await state.set_state(AdminState.start)
