import logging
import random

from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from database.models import UserRepository, TaskRepository
from database.utils.AlchemyDataObject import AlchemyDataObject
from database.utils.construct_shemas import ConstructUser
from handlers.user.states import UserState
from keyboards.user.reply_user import answer_mode_kb


async def send_question(message: types.Message, user_state, state: FSMContext) -> object:
    if user_state.questions:
        user_state.now_question = random.choice(user_state.questions)
        user_state.questions.remove(user_state.now_question)
        res_message = f"*{user_state.now_question.description}*\n\n" \
                      f"{user_state.now_question.answers}\n"
        await message.answer(res_message, parse_mode="Markdown", reply_markup=ReplyKeyboardRemove())
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


async def add_new_user(user_id: int, username: str, is_subscribe: bool = False):
    try:
        new_user = ConstructUser(user_id=user_id,
                                 username=username,
                                 is_subscribe=is_subscribe).model_dump()
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


def split_array(arr, chunk_size):
    return [arr[i:i + chunk_size] for i in range(0, len(arr), chunk_size)]
