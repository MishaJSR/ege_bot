import logging
import random

from aiogram import types
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from database.models import UserRepository, TaskRepository, TheoryRepository
from database.utils.AlchemyDataObject import AlchemyDataObject
from database.utils.construct_schemas import ConstructUser
from keyboards.user.reply_user import answer_mode_kb, under_chapter_kb
from utils.common.static_user import *


async def send_question(message: types.Message, user_state, state: FSMContext) -> object:
    if user_state.questions:
        user_state.now_question = random.choice(user_state.questions)
        user_state.questions.remove(user_state.now_question)
        res_message = f"<b>{user_state.now_question.description}</b>\n\n" \
                      f"{user_state.now_question.answers}\n"
        await message.answer(res_message, parse_mode=ParseMode.HTML, reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer("Задания закончились", reply_markup=answer_mode_kb())
        await state.set_state(user_state.answer_mode)


async def check_user(user_id: int) -> str | bool:
    user_field = ["username"]
    user_filter = {
        "user_id": user_id
    }
    res = await UserRepository().get_one_by_fields(data=user_field, field_filter=user_filter)
    if res:
        return res.username
    return False


async def add_new_user(user_id: int, username: str):
    try:
        new_user = ConstructUser(user_id=user_id,
                                 username=username,
                                 is_subscribe=True).model_dump()
        await UserRepository().add_object(data=new_user)
    except Exception as e:
        logging.info(f"Ошибка регистрации пользователя {e}")


async def get_all_chapters() -> list[str]:
    task_fields = ["chapter"]
    rows = await TaskRepository().get_all_by_fields(data=task_fields, distinct=True)
    return [el.chapter for el in rows]


async def get_all_under_chapters(chapter) -> list[str]:
    task_fields = ["under_chapter"]
    task_filter = {
        "chapter": chapter
    }
    rows = await TaskRepository().get_all_by_fields(data=task_fields, field_filter=task_filter, distinct=True)
    return [el.under_chapter for el in rows]


async def get_questions(under_chapter) -> AlchemyDataObject:
    task_fields = ["description", "answers", "answer", "about"]
    task_filter = {"under_chapter": under_chapter}
    rows = await TaskRepository().get_all_by_fields(data=task_fields, field_filter=task_filter)
    return rows


async def go_to_under_chapters(message: types.Message, user_state):
    if len(user_state.list_of_under_chapters) == 1:
        await message.answer(TEXT_UNDER_CHAPTER,
                             reply_markup=under_chapter_kb(data=user_state.list_of_under_chapters))
    else:
        user_state.index_now_under_chapter = 0
        await message.answer(TEXT_UNDER_CHAPTER,
                             reply_markup=under_chapter_kb(data=user_state.list_of_under_chapters[0], is_more=True))


async def update_under_chapters(message: types.Message, user_state):
    cur_ind = user_state.index_now_under_chapter
    has_more_button = len(user_state.list_of_under_chapters) - 1 == cur_ind
    is_return = False
    if cur_ind != 0:
        is_return = True
    if user_state.index_now_under_chapter < len(user_state.list_of_under_chapters):
        if has_more_button:
            await message.answer(TEXT_UNDER_CHAPTER,
                                 reply_markup=under_chapter_kb(data=user_state.list_of_under_chapters[cur_ind],
                                                               is_return=True))
        else:
            await message.answer(TEXT_UNDER_CHAPTER,
                                 reply_markup=under_chapter_kb(data=user_state.list_of_under_chapters[cur_ind],
                                                               is_more=True,
                                                               is_return=is_return))
    else:
        await message.answer(EMPTY_UNDER_CHAPTERS)


def split_array(arr, chunk_size):
    return [arr[i:i + chunk_size] for i in range(0, len(arr), chunk_size)]


async def send_theory(message: types.Message, user_state):
    theory_field = ["text", "photo_id"]
    theory_filter = {
        "under_chapter": user_state.select_under_chapter
    }
    posts = await TheoryRepository().get_all_by_fields(data=theory_field, field_filter=theory_filter)
    for post in posts:
        if post.photo_id:
            await message.answer_photo(photo=post.photo_id)
        await message.answer(post.text, parse_mode=ParseMode.HTML)
