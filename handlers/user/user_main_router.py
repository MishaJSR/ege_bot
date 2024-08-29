from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from handlers.user.profile_router.state import UserProfileState
from handlers.user.profile_router.user_profile_router import user_profile_router
from handlers.user.state import UserState
from handlers.user.study_router.state import UserStudyState
from handlers.user.study_router.user_study_router import user_study_router
from handlers.user.utils import check_user, add_new_user, print_statistic, count_statistic, send_status
from keyboards.user.reply_user import *
from utils.common.static_user import *

user_main_router = Router()
user_main_router.include_routers(user_study_router, user_profile_router)


@user_main_router.message(CommandStart())
async def user_start(message: types.Message, state: FSMContext):
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


@user_main_router.message(UserState.start, F.text == BUTTON_START_PREPARE_1)
async def user_press_start_train(message: types.Message, state: FSMContext):
    await message.answer(TEXT_MAIN_CHAPTER, reply_markup=main_chapter_kb())
    await state.set_state(UserStudyState.main_chapter)


@user_main_router.message(Command("profile"))
async def user_press_start_train(message: types.Message, state: FSMContext):
    percent, all_user_tasks, all_tasks, percent_ready, status = await count_statistic(message)
    points = int(percent * percent_ready)
    await send_status(message, status, points)
    await print_statistic(message, percent, all_user_tasks, all_tasks, percent_ready)
    await state.set_state(UserProfileState.start)


@user_main_router.message(UserState.start, F.text == BUTTON_START_PREPARE_2)
async def user_press_start_train(message: types.Message, state: FSMContext):
    percent, all_user_tasks, all_tasks, percent_ready, status = await count_statistic(message)
    points = int(percent * percent_ready)
    await send_status(message, status, points)
    await print_statistic(message, percent, all_user_tasks, all_tasks, percent_ready)
    await state.set_state(UserProfileState.start)
