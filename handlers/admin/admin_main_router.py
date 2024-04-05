from aiogram.filters import Command, StateFilter
from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from dotenv import find_dotenv, load_dotenv

from filters.admin_filter import AdminFilter
from keyboards.user.reply_user import start_kb
from keyboards.admin.reply_admin import start_kb
from handlers.admin.states import Admin_state
from handlers.admin.admin_spammer_router import admin_spammer_router
from handlers.admin.add_task_router import admin_add_task_router
from handlers.admin.delete_task_router import admin_delete_task_router

admin_private_router = Router()
admin_private_router.include_routers(admin_spammer_router, admin_add_task_router, admin_delete_task_router)
admin_private_router.message.filter(AdminFilter())
load_dotenv(find_dotenv())


@admin_private_router.message(Command('admin'))
async def fill_admin_state(message: types.Message, state: FSMContext):
    await message.answer(text='Привет админ', reply_markup=start_kb())
    await state.set_state(Admin_state.start)


@admin_private_router.message(StateFilter('*'), Command("назад"))
@admin_private_router.message(StateFilter('*'), F.text.casefold() == "назад")
async def back_step_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()

    if current_state == Admin_state.start:
        await message.answer('Предыдущего шага нет')
        return

    previous = None
    for step in Admin_state.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(f"Вы вернулись к прошлому шагу \n{Admin_state.texts[previous.state][0]}",
                                 reply_markup=Admin_state.texts[previous.state][1]())
            return
        previous = step


@admin_private_router.message(F.text == 'Отмена')
async def fill_admin_state(message: types.Message, state: FSMContext):
    await message.answer(text='Вы вернулись в основное меню', reply_markup=start_kb())
    await state.set_state(Admin_state.start)





