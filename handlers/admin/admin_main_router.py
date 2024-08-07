from aiogram.filters import Command, StateFilter
from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from dotenv import find_dotenv, load_dotenv

from database.models import UserRepository, TaskRepository
from database.utils.construct_shemas import ConstructUser, ConstructTask
from filters.admin_filter import AdminFilter
from keyboards.user.reply_user import start_kb
from keyboards.admin.reply_admin import start_kb
from handlers.admin.states import Admin_state

admin_private_router = Router()
admin_private_router.message.filter(AdminFilter())
load_dotenv(find_dotenv())


@admin_private_router.message(Command('admin'))
async def fill_admin_state(message: types.Message, state: FSMContext):
    await message.answer(text='Привет админ', reply_markup=start_kb())
    dictionary = ConstructUser(user_id=message.from_user.id,
                               username=message.from_user.full_name,
                               is_subscribe=True).model_dump()
    task = ConstructTask(exam="Bnddfd",
                         chapter="Bnddfd",
                         under_chapter="Bnddfd",
                         description="Bnddfd",
                         answer_mode="Bnddfd",
                         answers="Bnddfd",
                         answer="Bnddfd",
                         ).model_dump()
    pass
    res1 = await UserRepository().add_object(data=dictionary)
    res2 = await TaskRepository().add_object(data=task)
    pass
    # res2 = await UserRepository().get_all_by_fields(data=user_fields, field_filter=field_filter2)






