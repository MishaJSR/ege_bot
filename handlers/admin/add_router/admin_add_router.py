from aiogram import types, Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from handlers.admin.add_router.state import AdminAddState
from handlers.admin.add_router.utils import send_demo_add_post, set_theory_multi
from handlers.admin.state import AdminState
from handlers.user.utils import get_all_chapters, get_all_under_chapters
from keyboards.admin.reply_admin import start_kb_menu, back_kb, skip_kb, confirm_kb, start_kb, next_post_kb
from keyboards.user.reply_user import chapter_kb, under_chapter_kb
from utils.common.static_admin import *
from utils.common.static_user import TEXT_CHAPTER, TEXT_UNDER_CHAPTER, BACK_BUTTON

admin_add_router = Router()


@admin_add_router.message(StateFilter(AdminAddState), F.text == BACK_BUTTON)
async def back_step_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()

    if current_state == AdminAddState.send_photo:
        AdminAddState.text = None
        AdminAddState.photo = None
        AdminAddState.chapter = None
        AdminAddState.under_chapter = None
        AdminAddState.posts_list = []
        await message.answer("Вы вернулись в главное меню", reply_markup=start_kb())

    if current_state == AdminAddState.send_text:
        AdminAddState.photo = None
        await message.answer(SEND_PHOTO, reply_markup=skip_kb())
        await state.set_state(AdminAddState.send_photo)

    if current_state == AdminAddState.confirm_post:
        AdminAddState.text = None
        await message.answer(SEND_TEXT, reply_markup=back_kb())
        await state.set_state(AdminAddState.send_text)

    if current_state == AdminAddState.select_chapter:
        await message.answer(CONFIRM_TEXT, reply_markup=confirm_kb())
        await state.set_state(AdminAddState.confirm_post)

    if current_state == AdminAddState.select_under_chapter:
        AdminAddState.list_of_chapters = await get_all_chapters()
        await message.answer(TEXT_CHAPTER, reply_markup=chapter_kb(data=AdminAddState.list_of_chapters))
        await state.set_state(AdminAddState.select_chapter)

    if current_state == AdminAddState.confirm_under_chapter:
        AdminAddState.list_of_under_chapters = await get_all_under_chapters(chapter=AdminAddState.chapter)
        await message.answer(TEXT_UNDER_CHAPTER,
                             reply_markup=under_chapter_kb(data=AdminAddState.list_of_under_chapters))
        await state.set_state(AdminAddState.select_under_chapter)


@admin_add_router.message(AdminState.start, F.text == start_kb_menu[0])
async def admin_add_start(message: types.Message, state: FSMContext):
    await message.answer(SEND_PHOTO, reply_markup=skip_kb())
    await state.set_state(AdminAddState.send_photo)


@admin_add_router.message(AdminAddState.send_photo)
async def admin_spam_set_text(message: types.Message, state: FSMContext):
    if not message.text == SKIP_TEXT and not message.photo:
        await message.answer(DONT_UNDERSTAND_TRY_AGAIN)
        return
    if message.photo:
        AdminAddState.photo = message.photo[-1].file_id
    else:
        AdminAddState.photo = None
    await message.answer(SEND_TEXT, reply_markup=back_kb())
    await state.set_state(AdminAddState.send_text)


@admin_add_router.message(AdminAddState.send_text, F.text)
async def admin_spam_set_text(message: types.Message, state: FSMContext):
    AdminAddState.text = message.text
    await send_demo_add_post(message=message, admin_spam_state=AdminAddState)
    await message.answer(CONFIRM_TEXT, reply_markup=confirm_kb())
    await state.set_state(AdminAddState.confirm_post)


@admin_add_router.message(AdminAddState.confirm_post, F.text == BUTTON_CONFIRM)
async def admin_spam_set_text(message: types.Message, state: FSMContext):
    await message.answer(ADD_POST, reply_markup=next_post_kb())
    await state.set_state(AdminAddState.select_post_action)


@admin_add_router.message(AdminAddState.confirm_post, F.text == BUTTON_NOT_CONFIRM)
async def admin_spam_set_text(message: types.Message, state: FSMContext):
    await message.answer(RETURN_IN_MAIN_ADMIN, reply_markup=start_kb())
    await state.set_state(AdminState.start)


@admin_add_router.message(AdminAddState.select_post_action, F.text == BUTTON_END_POST)
async def admin_spam_set_text(message: types.Message, state: FSMContext):
    AdminAddState.list_of_chapters = await get_all_chapters()
    await message.answer(TEXT_CHAPTER, reply_markup=chapter_kb(data=AdminAddState.list_of_chapters))
    await state.set_state(AdminAddState.select_chapter)


@admin_add_router.message(AdminAddState.select_chapter, F.text)
async def admin_spam_set_text(message: types.Message, state: FSMContext):
    AdminAddState.chapter = message.text
    AdminAddState.list_of_under_chapters = await get_all_under_chapters(chapter=AdminAddState.chapter)
    await message.answer(TEXT_UNDER_CHAPTER, reply_markup=under_chapter_kb(data=AdminAddState.list_of_under_chapters))
    await state.set_state(AdminAddState.select_under_chapter)


@admin_add_router.message(AdminAddState.select_under_chapter, F.text)
async def admin_spam_set_text(message: types.Message, state: FSMContext):
    AdminAddState.under_chapter = message.text
    await message.answer(CONFIRM_TEXT, reply_markup=confirm_kb())
    await state.set_state(AdminAddState.confirm_under_chapter)


@admin_add_router.message(AdminAddState.confirm_under_chapter, F.text == BUTTON_CONFIRM)
async def admin_spam_set_text(message: types.Message):
    AdminAddState.posts_list.append([AdminAddState.photo, AdminAddState.text])
    await set_theory_multi(message, AdminAddState)


@admin_add_router.message(AdminAddState.select_post_action, F.text == BUTTON_NEXT_POST)
async def admin_spam_set_text(message: types.Message, state: FSMContext):
    AdminAddState.posts_list.append([AdminAddState.photo, AdminAddState.text])
    await message.answer(SEND_PHOTO, reply_markup=skip_kb())
    await state.set_state(AdminAddState.send_photo)
