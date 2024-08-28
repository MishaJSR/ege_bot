import re

from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter

from handlers.user.profile_router.state import UserProfileState
from handlers.user.state import UserState
from handlers.user.utils import *
from keyboards.user.inline_user import get_inline_channel, get_inline_about
from keyboards.user.reply_user import *
from utils.common.static_url import channel
from utils.common.static_user import *

user_profile_router = Router()


@user_profile_router.message(StateFilter(UserProfileState), F.text == BACK_BUTTON)
async def back_step_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()

    if current_state == UserProfileState.start:
        username = await check_user(user_id=message.from_user.id)
        if username:
            await message.answer(f"Привет {username}")
        else:
            await add_new_user(
                user_id=message.from_user.id,
                username=message.from_user.full_name,
            )
            await message.answer(f"Привет {message.from_user.full_name}")
        await message.answer(GREETING, reply_markup=start_user_kb())
        await state.set_state(UserState.start)
        return

    if current_state == UserProfileState.chapter:
        percent, all_user_tasks, all_tasks, percent_ready, status = await count_statistic(message)
        await send_status(message, status)
        await print_statistic(message, percent, all_user_tasks, all_tasks, percent_ready)
        await state.set_state(UserProfileState.start)
        return

    if current_state == UserProfileState.under_chapter:
        res = await message.bot.get_chat_member(chat_id=channel, user_id=message.from_user.id)
        if res.status.value not in ['member', 'creator']:
            await message.answer(TEXT_NOT_SUBSCRIBE_CHANNEL, reply_markup=get_inline_channel())
            return
        await message.answer("Вы вернулись к прошлому шагу")
        await message.answer(TEXT_CHAPTER, reply_markup=chapter_kb(data=UserProfileState.list_of_chapters))
        await state.set_state(UserProfileState.chapter)
        return


@user_profile_router.message(UserProfileState.start, F.text == BUTTON_MORE_STATISTIC)
async def back_step_handler(message: types.Message, state: FSMContext) -> None:
    UserProfileState.list_of_chapters = await get_all_chapters()
    await message.answer(TEXT_CHAPTER, reply_markup=chapter_kb(data=UserProfileState.list_of_chapters))
    await state.set_state(UserProfileState.chapter)


@user_profile_router.message(UserProfileState.chapter, F.text)
async def back_step_handler(message: types.Message, state: FSMContext) -> None:
    res = await message.bot.get_chat_member(chat_id=channel, user_id=message.from_user.id)
    if res.status.value not in ['member', 'creator']:
        await message.answer(TEXT_NOT_SUBSCRIBE_CHANNEL, reply_markup=get_inline_channel())
        return
    if message.text not in UserProfileState.list_of_chapters:
        await message.answer(DONT_UNDERSTAND)
        return
    UserProfileState.list_of_under_chapters = await get_all_under_chapters(chapter=message.text)
    UserProfileState.list_of_under_chapters = split_array(UserProfileState.list_of_under_chapters, 6)
    percent, all_user_tasks, all_tasks, percent_ready, status = await count_statistic(message,
                                                                                      flag="chapter",
                                                                                      chapter=message.text)
    await print_statistic(message, percent, all_user_tasks, all_tasks, percent_ready,
                          addition=f"Статистика по блоку: <b>{message.text}</b>\n\n")
    await go_to_under_chapters(message=message, user_state=UserProfileState)
    await state.set_state(UserProfileState.under_chapter)


@user_profile_router.message(UserProfileState.under_chapter, F.text == RETURN_BUTTON)
async def user_press_under_chapter_return(message: types.Message):
    UserProfileState.index_now_under_chapter -= 1
    await update_under_chapters(message=message, user_state=UserProfileState)


@user_profile_router.message(UserProfileState.under_chapter, F.text == MORE_BUTTON)
async def user_press_under_chapter_more(message: types.Message):
    UserProfileState.index_now_under_chapter += 1
    await update_under_chapters(message=message, user_state=UserProfileState)


@user_profile_router.message(UserProfileState.under_chapter, F.text)
async def back_step_handler(message: types.Message, state: FSMContext) -> None:
    if message.text not in UserProfileState.list_of_under_chapters[UserProfileState.index_now_under_chapter]:
        await message.answer(DONT_UNDERSTAND)
        return
    UserProfileState.select_under_chapter = message.text
    percent, all_user_tasks, all_tasks, percent_ready, status = await count_statistic(message,
                                                                                      flag="under_chapter",
                                                                                      under_chapter=UserProfileState.select_under_chapter)
    await print_statistic(message, percent, all_user_tasks, all_tasks, percent_ready,
                          addition=f"Статистика по теме: <b>{UserProfileState.select_under_chapter}</b>\n\n")


@user_profile_router.message(UserProfileState.start, F.text == BUTTON_ABOUT_LEVEL)
async def back_step_handler(message: types.Message, state: FSMContext) -> None:
    await message.answer(TEXT_LEVEL)
