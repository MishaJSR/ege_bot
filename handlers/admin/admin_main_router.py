import os

from aiogram.filters import Command, StateFilter
from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from docx import Document
from dotenv import find_dotenv, load_dotenv

from database.models import UserRepository, TaskRepository
from database.utils.construct_shemas import ConstructUser, ConstructTask
from filters.admin_filter import AdminFilter
from keyboards.admin.reply_admin import start_kb
from handlers.admin.states import Admin_state
from utils.test import load_to_db, get_all_files_in_directory

admin_private_router = Router()
admin_private_router.message.filter(AdminFilter())
load_dotenv(find_dotenv())


# @admin_private_router.message(Command('admin'))
# async def fill_admin_state(message: types.Message, state: FSMContext):
#     await message.answer(text='Привет админ', reply_markup=start_kb())
#     dictionary = ConstructUser(user_id=message.from_user.id,
#                                username=message.from_user.full_name,
#                                is_subscribe=True).model_dump()
#     task = ConstructTask(exam="Bnddfd",
#                          chapter="Bnddfd",
#                          under_chapter="Bnddfd",
#                          description="Bnddfd",
#                          answer_mode="Bnddfd",
#                          answers="Bnddfd",
#                          answer="Bnddfd",
#                          ).model_dump()
#     pass
#     res1 = await UserRepository().add_object(data=dictionary)
#     res2 = await TaskRepository().add_object(data=task)
#     pass
#     # res2 = await UserRepository().get_all_by_fields(data=user_fields, field_filter=field_filter2)


@admin_private_router.message(Command('admin'))
async def fill_admin_state(message: types.Message, state: FSMContext):
    await message.answer(text='Привет админ', reply_markup=start_kb())
    dictionary = ConstructUser(user_id=message.from_user.id,
                               username=message.from_user.full_name,
                               is_subscribe=True).model_dump()
    task_fields = ["answer"]
    task_filter = {
        "id": 270
    }
    res2 = await TaskRepository().get_one_by_fields(data=task_fields, field_filter=task_filter)
    print(res2)


@admin_private_router.message(Command('load'))
async def fill_admin_state(message: types.Message, state: FSMContext):
    directory_path = os.getcwd() + '\\utils\\loader\\human'
    all_files = get_all_files_in_directory(directory_path)
    for file in all_files:
        await load_to_db(file, chapter="Человек и общество")


