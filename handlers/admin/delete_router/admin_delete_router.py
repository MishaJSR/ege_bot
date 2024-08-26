from aiogram import types, Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from handlers.admin.add_router.state import AdminAddState
from handlers.admin.add_router.utils import send_demo_add_post, set_theory_multi
from handlers.admin.delete_router.state import AdminDeleteState
from handlers.admin.delete_router.utils import check_theory, delete_theory
from handlers.admin.state import AdminState
from handlers.user.utils import get_all_chapters, get_all_under_chapters
from keyboards.admin.reply_admin import start_kb_menu, back_kb, skip_kb, confirm_kb, start_kb, next_post_kb
from keyboards.user.reply_user import chapter_kb, under_chapter_kb
from utils.common.static_admin import *
from utils.common.static_user import TEXT_CHAPTER, TEXT_UNDER_CHAPTER, BACK_BUTTON, DONT_UNDERSTAND

admin_delete_router = Router()


@admin_delete_router.message(StateFilter(AdminDeleteState), F.text == BACK_BUTTON)
async def back_step_handler(message: types.Message, state: FSMContext) -> None:
    AdminDeleteState.list_of_chapters = []
    AdminDeleteState.choose_under_chapter = None
    await message.answer(RETURN_IN_MAIN_ADMIN, reply_markup=start_kb())
    await state.set_state(AdminState.start)


@admin_delete_router.message(F.text == start_kb_menu[1])
async def admin_spam_photo_send(message: types.Message, state: FSMContext):
    AdminDeleteState.list_of_chapters = await get_all_chapters()
    await message.answer(TEXT_CHAPTER, reply_markup=chapter_kb(data=AdminDeleteState.list_of_chapters))
    await state.set_state(AdminDeleteState.select_chapter)


@admin_delete_router.message(AdminDeleteState.select_chapter, F.text)
async def admin_spam_photo_send(message: types.Message, state: FSMContext):
    if message.text not in AdminDeleteState.list_of_chapters:
        await message.answer(DONT_UNDERSTAND)
        return
    AdminDeleteState.list_of_under_chapters = await get_all_under_chapters(chapter=message.text)
    await message.answer(TEXT_UNDER_CHAPTER,
                         reply_markup=under_chapter_kb(data=AdminDeleteState.list_of_under_chapters))
    await state.set_state(AdminDeleteState.select_under_chapter)


@admin_delete_router.message(AdminDeleteState.select_under_chapter, F.text)
async def admin_spam_photo_send(message: types.Message, state: FSMContext):
    AdminDeleteState.choose_under_chapter = message.text
    theory_ids = await check_theory(AdminDeleteState.choose_under_chapter)
    if not theory_ids:
        await message.answer(TEXT_NOT_UNDER_CHAPTER)
        return
    await message.answer(CONFIRM_TEXT, reply_markup=confirm_kb())
    await state.set_state(AdminDeleteState.confirm_under_chapter)


@admin_delete_router.message(AdminDeleteState.confirm_under_chapter, F.text == BUTTON_CONFIRM)
async def admin_spam_photo_send(message: types.Message, state: FSMContext):
    await delete_theory(AdminDeleteState.choose_under_chapter)
    await message.answer(DELETE_THEORY, reply_markup=start_kb())
    await state.set_state(AdminState.start)
