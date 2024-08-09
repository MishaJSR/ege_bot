from aiogram.filters import Command
from aiogram import types, Router
from aiogram.fsm.context import FSMContext

from filters.admin_filter import AdminFilter
from handlers.admin.add_router.admin_add_router import admin_add_router
from handlers.admin.spam_router.admin_spam_router import admin_spam_router
from handlers.admin.state import AdminState
from keyboards.admin.reply_admin import start_kb
from utils.common.static_admin import *

admin_private_router = Router()
admin_private_router.include_routers(admin_add_router, admin_spam_router)
admin_private_router.message.filter(AdminFilter())


@admin_private_router.message(Command('admin'))
async def admin_start(message: types.Message, state: FSMContext):
    await message.answer(text=HELLO_ADMIN, reply_markup=start_kb())
    await state.set_state(AdminState.start)




# @admin_private_router.message(Command('load'))
# async def fill_admin_state(message: types.Message, state: FSMContext):
#     directory_path = os.getcwd() + '\\utils\\loader\\pravo'
#     all_files = get_all_files_in_directory(directory_path)
#     for file in all_files:
#         await load_to_db(file, chapter="Право 🕊")

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
